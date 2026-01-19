"""JSON receipt parsing service.

Parses Biedronka e-receipt JSON files into structured Python objects.
"""

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from backend.models.receipt import (
    DiscountLineInput,
    DiscountVatInput,
    FiscalFooterInput,
    HeaderDataInput,
    PackInput,
    PaymentInput,
    ReceiptInput,
    SellLineInput,
    SumInCurrencyInput,
    clean_product_name,
    grosze_to_pln,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Output Dataclasses
# =============================================================================


@dataclass
class ReceiptItem:
    """Przetworzony produkt z paragonu."""

    name_raw: str  # oryginalna nazwa
    name_clean: str  # oczyszczona nazwa
    vat_id: str
    quantity: float
    unit_price_pln: float  # cena jednostkowa w PLN
    total_pln: float  # suma przed rabatem w PLN
    discount_pln: float  # rabat w PLN
    final_price_pln: float  # suma po rabacie w PLN
    is_storno: bool = False


@dataclass
class Pack:
    """Opakowanie zwrotne."""

    name: str
    quantity: int
    unit_price_pln: float
    total_pln: float


@dataclass
class Receipt:
    """Przetworzony paragon."""

    receipt_number: str  # uniqueNumber z fiscalFooter
    date: datetime
    tin: str  # NIP sklepu
    store_number: str | None
    pos_number: str | None
    transaction_number: str | None
    items: list[ReceiptItem]
    packs: list[Pack]
    payment_method: str
    total_before_discount_pln: float
    total_discount_pln: float
    total_after_discount_pln: float
    total_with_packs_pln: float
    cashier: str | None
    loyalty_card: str | None
    file_hash: str = ""


@dataclass
class ParseResult:
    """Result of parsing multiple files."""

    receipts: list[Receipt] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    files_processed: int = 0
    files_skipped: int = 0


# =============================================================================
# Helper Functions
# =============================================================================


def normalize_product_name(name: str) -> str:
    """Normalize product name by splitting concatenated words.

    "KaszaPęczak4X100g" -> "Kasza Pęczak 4X100g"

    Args:
        name: Cleaned product name (without VAT letter)

    Returns:
        Name with spaces inserted between words
    """
    # Insert space before uppercase letter if preceded by lowercase
    # e.g., "KaszaPęczak" -> "Kasza Pęczak"
    result = re.sub(r"([a-ząćęłńóśźż])([A-ZĄĆĘŁŃÓŚŹŻ])", r"\1 \2", name)

    # Insert space before digit if preceded by letter (but not if it's like "4X")
    # e.g., "Pęczak4X" -> "Pęczak 4X"
    result = re.sub(r"([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ])(\d)", r"\1 \2", result)

    return result


def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA256 hash of file content."""
    return hashlib.sha256(content).hexdigest()


# =============================================================================
# Parsing Functions
# =============================================================================


def extract_header_data(header: list[dict[str, Any]]) -> HeaderDataInput | None:
    """Extract headerData from header array.

    Args:
        header: List of header items from JSON

    Returns:
        HeaderDataInput if found, None otherwise
    """
    for item in header:
        if "headerData" in item:
            return HeaderDataInput.model_validate(item["headerData"])
    return None


def parse_body_items(
    body: list[dict[str, Any]],
) -> tuple[
    list[ReceiptItem],
    list[Pack],
    PaymentInput | None,
    FiscalFooterInput | None,
    SumInCurrencyInput | None,
    float,  # total_discount_from_vouchers
]:
    """Parse body items into structured objects.

    Handles the linkage between sellLine and discountLine where
    discountLine ALWAYS follows the sellLine it applies to.

    Args:
        body: List of body items from JSON

    Returns:
        Tuple of (items, packs, payment, fiscal_footer, sum_in_currency, voucher_discount)
    """
    items: list[ReceiptItem] = []
    packs: list[Pack] = []
    payment: PaymentInput | None = None
    fiscal_footer: FiscalFooterInput | None = None
    sum_in_currency: SumInCurrencyInput | None = None
    voucher_discount_grosze: int = 0

    current_item: ReceiptItem | None = None

    for body_item in body:
        # Parse sellLine - creates new item
        if "sellLine" in body_item:
            # Save previous item if exists
            if current_item is not None:
                items.append(current_item)

            sell = SellLineInput.model_validate(body_item["sellLine"])

            # Skip storno items
            if sell.is_storno:
                current_item = None
                continue

            current_item = ReceiptItem(
                name_raw=sell.name,
                name_clean=normalize_product_name(clean_product_name(sell.name)),
                vat_id=sell.vat_id,
                quantity=sell.quantity_numeric,
                unit_price_pln=grosze_to_pln(sell.price),
                total_pln=grosze_to_pln(sell.total),
                discount_pln=0.0,
                final_price_pln=grosze_to_pln(sell.total),
                is_storno=sell.is_storno,
            )

        # Parse discountLine - applies to previous sellLine
        elif "discountLine" in body_item and current_item is not None:
            discount = DiscountLineInput.model_validate(body_item["discountLine"])
            discount_pln = grosze_to_pln(discount.value)
            current_item.discount_pln = discount_pln
            current_item.final_price_pln = current_item.total_pln - discount_pln

        # Parse discountVat (voucher) - category-level discount
        elif "discountVat" in body_item:
            voucher = DiscountVatInput.model_validate(body_item["discountVat"])
            voucher_discount_grosze += voucher.value

        # Parse pack - deposit items
        elif "pack" in body_item:
            pack = PackInput.model_validate(body_item["pack"])
            packs.append(
                Pack(
                    name=pack.name,
                    quantity=pack.quantity_numeric,
                    unit_price_pln=grosze_to_pln(pack.price),
                    total_pln=grosze_to_pln(pack.total),
                )
            )

        # Parse payment
        elif "payment" in body_item:
            payment = PaymentInput.model_validate(body_item["payment"])

        # Parse fiscalFooter
        elif "fiscalFooter" in body_item:
            fiscal_footer = FiscalFooterInput.model_validate(body_item["fiscalFooter"])

        # Parse sumInCurrency
        elif "sumInCurrency" in body_item:
            sum_in_currency = SumInCurrencyInput.model_validate(
                body_item["sumInCurrency"]
            )

    # Don't forget the last item
    if current_item is not None:
        items.append(current_item)

    return (
        items,
        packs,
        payment,
        fiscal_footer,
        sum_in_currency,
        grosze_to_pln(voucher_discount_grosze),
    )


def parse_receipt_json(json_data: dict[str, Any], file_hash: str = "") -> Receipt:
    """Parse receipt JSON into Receipt object.

    Args:
        json_data: Raw JSON dict from e-paragon file
        file_hash: SHA256 hash of source file (optional)

    Returns:
        Parsed Receipt object

    Raises:
        ValueError: If required fields are missing
    """
    # Validate with Pydantic model
    receipt_input = ReceiptInput.model_validate(json_data)

    # Extract header data
    header_data = receipt_input.header_data
    if header_data is None:
        raise ValueError("Missing headerData in receipt")

    # Parse body items - use original JSON body to preserve structure
    items, packs, payment, fiscal_footer, sum_in_currency, voucher_discount = (
        parse_body_items(json_data.get("body", []))
    )

    # Validate required fields
    if fiscal_footer is None:
        raise ValueError("Missing fiscalFooter in receipt")

    # Calculate totals
    items_total = sum(item.total_pln for item in items)
    items_discount = sum(item.discount_pln for item in items)
    total_discount = items_discount + voucher_discount

    # Use sumInCurrency if available, otherwise calculate
    if sum_in_currency:
        total_before_discount = grosze_to_pln(sum_in_currency.fiscal_total)
        total_with_packs = grosze_to_pln(sum_in_currency.total_with_packs)
    else:
        total_before_discount = items_total
        packs_total = sum(p.total_pln for p in packs)
        total_with_packs = items_total - total_discount + packs_total

    total_after_discount = total_before_discount - total_discount

    # Extract IDZ data
    idz_data = receipt_input.parsed_idz

    return Receipt(
        receipt_number=fiscal_footer.unique_number,
        date=header_data.parsed_datetime,
        tin=header_data.tin,
        store_number=idz_data.get("store_number"),
        pos_number=idz_data.get("pos_number") or (
            fiscal_footer.cash_number.replace("Kasa ", "")
            if fiscal_footer.cash_number else None
        ),
        transaction_number=idz_data.get("transaction_number"),
        items=items,
        packs=packs,
        payment_method=payment.name if payment else "Unknown",
        total_before_discount_pln=total_before_discount,
        total_discount_pln=total_discount,
        total_after_discount_pln=total_after_discount,
        total_with_packs_pln=total_with_packs,
        cashier=fiscal_footer.cashier,
        loyalty_card=receipt_input.loyalty_card,
        file_hash=file_hash,
    )


def parse_receipt_file(file_content: bytes) -> Receipt:
    """Parse receipt from file bytes.

    Args:
        file_content: Raw bytes of JSON file

    Returns:
        Parsed Receipt object

    Raises:
        json.JSONDecodeError: If file is not valid JSON
        ValueError: If required fields are missing
    """
    file_hash = calculate_file_hash(file_content)
    json_data = json.loads(file_content.decode("utf-8"))
    return parse_receipt_json(json_data, file_hash)


def parse_multiple_files(
    files: list[tuple[str, bytes]],
) -> ParseResult:
    """Parse multiple receipt files.

    Args:
        files: List of (filename, content) tuples

    Returns:
        ParseResult with successful receipts and errors
    """
    result = ParseResult()

    for filename, content in files:
        result.files_processed += 1
        try:
            receipt = parse_receipt_file(content)
            result.receipts.append(receipt)
        except json.JSONDecodeError as e:
            error_msg = f"{filename}: Invalid JSON - {e}"
            result.errors.append(error_msg)
            result.files_skipped += 1
            logger.warning(error_msg)
        except ValueError as e:
            error_msg = f"{filename}: {e}"
            result.errors.append(error_msg)
            result.files_skipped += 1
            logger.warning(error_msg)
        except Exception as e:
            error_msg = f"{filename}: Unexpected error - {e}"
            result.errors.append(error_msg)
            result.files_skipped += 1
            logger.exception(error_msg)

    return result


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    # Test data based on real Biedronka receipt structure
    test_json = {
        "protoVersion": "000",
        "IDZ": "c=test|g=test|s=5160|p=11|t=1060",
        "deviceType": 1,
        "header": [
            {"image": {}},
            {"headerText": {"headerTextLines": "<p>Test Store</p>"}},
            {
                "headerData": {
                    "date": "2024-01-17T15:08:58.000Z",
                    "docNumber": 172202,
                    "tin": "7791011327",
                }
            },
        ],
        "body": [
            {
                "sellLine": {
                    "name": "Banan Luz                C",
                    "vatId": "C",
                    "price": 699,
                    "total": 517,
                    "quantity": "0,740",
                    "isStorno": False,
                }
            },
            {
                "discountLine": {
                    "base": 517,
                    "value": 148,
                    "isDiscount": True,
                    "isPercent": False,
                    "vatId": "C",
                }
            },
            {
                "sellLine": {
                    "name": "Mleko 2% 1L              B",
                    "vatId": "B",
                    "price": 349,
                    "total": 349,
                    "quantity": "1",
                    "isStorno": False,
                }
            },
            {
                "pack": {
                    "name": "But Plastik kaucja",
                    "price": 50,
                    "quantity": "2",
                    "total": 100,
                }
            },
            {
                "sumInCurrency": {
                    "fiscalTotal": 866,
                    "totalWithPacks": 966,
                }
            },
            {
                "payment": {
                    "type": 2,
                    "amount": 966,
                    "name": "DEBIT MASTERCARD",
                    "currency": "PLN",
                    "isStorno": False,
                }
            },
            {
                "fiscalFooter": {
                    "uniqueNumber": "TEST123",
                    "cashier": "Kasjer nr 33",
                    "cashNumber": "Kasa 11",
                }
            },
            {"addLine": {"id": 6, "value": "99529*****723"}},
        ],
    }

    # Test parsing
    receipt = parse_receipt_json(test_json, "test_hash")

    print(f"Paragon: {receipt.receipt_number}")
    print(f"Data: {receipt.date}")
    print(f"Sklep: {receipt.store_number}")
    print(f"Produktów: {len(receipt.items)}")
    print(f"Opakowań: {len(receipt.packs)}")
    print(f"Płatność: {receipt.payment_method}")
    print(f"Karta lojalnościowa: {receipt.loyalty_card}")
    print()

    for item in receipt.items:
        print(f"  - {item.name_clean}: {item.quantity} x {item.unit_price_pln:.2f} PLN")
        print(f"    Suma: {item.total_pln:.2f} PLN, Rabat: {item.discount_pln:.2f} PLN")
        print(f"    Finalna cena: {item.final_price_pln:.2f} PLN")

    print()
    print(f"Suma przed rabatem: {receipt.total_before_discount_pln:.2f} PLN")
    print(f"Suma rabatów: {receipt.total_discount_pln:.2f} PLN")
    print(f"Suma po rabacie: {receipt.total_after_discount_pln:.2f} PLN")
    print(f"Suma z kaucją: {receipt.total_with_packs_pln:.2f} PLN")
    print()
    print("Parser OK!")
