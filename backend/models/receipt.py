"""Receipt and Item Pydantic models."""

from datetime import date, datetime, time
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


# =============================================================================
# Helper functions
# =============================================================================

def grosze_to_pln(grosze: int) -> float:
    """Konwertuj grosze na PLN."""
    return grosze / 100


def clean_product_name(raw_name: str) -> str:
    """Usuń trailing VAT letter i whitespace.

    "KaszaPęczak4X100g        C" -> "KaszaPęczak4X100g"
    """
    return raw_name.rstrip().rstrip("ABCD").rstrip()


VAT_RATES: dict[str, int] = {
    "A": 23,
    "B": 8,
    "C": 5,
    "D": 0,
}


# =============================================================================
# INPUT Models (from Biedronka JSON)
# =============================================================================

class SellLineInput(BaseModel):
    """Model for sellLine from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    vat_id: str = Field(alias="vatId")
    price: int  # grosze
    total: int  # grosze
    quantity: str  # "3" lub "0,740"
    is_storno: bool = Field(default=False, alias="isStorno")

    @computed_field
    @property
    def quantity_numeric(self) -> float:
        """Parse quantity string to float. Handles Polish decimal comma."""
        return float(self.quantity.replace(",", "."))

    @computed_field
    @property
    def name_clean(self) -> str:
        """Clean product name without VAT letter."""
        return clean_product_name(self.name)


class DiscountLineInput(BaseModel):
    """Model for discountLine from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    base: int  # grosze - kwota przed rabatem
    value: int  # grosze - wartość rabatu
    is_discount: bool = Field(alias="isDiscount")
    is_percent: bool = Field(alias="isPercent")
    vat_id: str = Field(alias="vatId")


class DiscountVatInput(BaseModel):
    """Model for discountVat (voucher) from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    base: int  # grosze
    value: int  # grosze
    vat_id: str = Field(alias="vatId")


class PackInput(BaseModel):
    """Model for pack (opakowania zwrotne) from receipt JSON."""

    name: str
    price: int  # grosze
    quantity: str  # może być string
    total: int  # grosze

    @computed_field
    @property
    def quantity_numeric(self) -> int:
        """Parse quantity to int."""
        return int(self.quantity.replace(",", ".").split(".")[0])


class PaymentInput(BaseModel):
    """Model for payment from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    type: str | int  # może być string "2" lub int 2
    amount: int  # grosze
    name: str
    currency: str
    is_storno: bool = Field(default=False, alias="isStorno")


class VatRateSummaryInput(BaseModel):
    """Model for vatRate summary from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    vat_id: str = Field(alias="vatId")
    vat_rate: int = Field(alias="vatRate")  # stawka VAT w procentach
    vat_sale: int = Field(alias="vatSale")  # grosze - wartość netto
    vat_amount: int = Field(alias="vatAmount")  # grosze - kwota VAT


class SumInCurrencyInput(BaseModel):
    """Model for sumInCurrency from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    fiscal_total: int = Field(alias="fiscalTotal")  # grosze - suma produktów
    total_with_packs: int = Field(alias="totalWithPacks")  # grosze - suma z kaucją


class DiscountSummaryInput(BaseModel):
    """Model for discountSummary from receipt JSON."""

    discounts: int  # grosze - suma rabatów


class FiscalFooterInput(BaseModel):
    """Model for fiscalFooter from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    unique_number: str = Field(alias="uniqueNumber")  # np. "EAZ2202168920"
    cashier: str | None = None  # np. "Kasjer nr 33"
    cash_number: str | None = Field(default=None, alias="cashNumber")  # np. "Kasa 11"


class HeaderDataInput(BaseModel):
    """Model for headerData from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    date: str  # ISO8601: "2026-01-17T15:08:58.000Z"
    doc_number: int = Field(alias="docNumber")
    tin: str  # NIP

    @computed_field
    @property
    def parsed_datetime(self) -> datetime:
        """Parse ISO8601 date string to datetime."""
        return datetime.fromisoformat(self.date.replace("Z", "+00:00"))

    @computed_field
    @property
    def parsed_date(self) -> date:
        """Extract date from datetime."""
        return self.parsed_datetime.date()

    @computed_field
    @property
    def parsed_time(self) -> time:
        """Extract time from datetime."""
        return self.parsed_datetime.time()


class HeaderTextInput(BaseModel):
    """Model for headerText from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    header_text_lines: str = Field(alias="headerTextLines")  # HTML z adresem


class AddLineInput(BaseModel):
    """Model for addLine from receipt JSON."""

    id: int
    value: str


class VatSummaryInput(BaseModel):
    """Model for vatSummary from receipt JSON."""

    model_config = ConfigDict(populate_by_name=True)

    currency: str
    vat_rates_summary: list[VatRateSummaryInput] = Field(alias="vatRatesSummary")


class ImageInput(BaseModel):
    """Model for image in header."""

    pass  # Ignorujemy obrazek - puste dla kompatybilności


class HeaderItemInput(BaseModel):
    """Wrapper for header array items - każdy element ma JEDEN klucz."""

    model_config = ConfigDict(populate_by_name=True)

    image: ImageInput | None = None
    header_text: HeaderTextInput | None = Field(default=None, alias="headerText")
    header_data: HeaderDataInput | None = Field(default=None, alias="headerData")


class BodyItemInput(BaseModel):
    """Wrapper for body array items - każdy element ma JEDEN klucz."""

    model_config = ConfigDict(populate_by_name=True)

    sell_line: SellLineInput | None = Field(default=None, alias="sellLine")
    discount_line: DiscountLineInput | None = Field(default=None, alias="discountLine")
    discount_vat: DiscountVatInput | None = Field(default=None, alias="discountVat")
    discount_summary: DiscountSummaryInput | None = Field(default=None, alias="discountSummary")
    vat_summary: VatSummaryInput | None = Field(default=None, alias="vatSummary")
    sum_in_currency: SumInCurrencyInput | None = Field(default=None, alias="sumInCurrency")
    pack: PackInput | None = None
    payment: PaymentInput | None = None
    fiscal_footer: FiscalFooterInput | None = Field(default=None, alias="fiscalFooter")
    add_line: AddLineInput | None = Field(default=None, alias="addLine")
    barcode: dict | None = None  # Ignorujemy barcode


def parse_idz(idz: str) -> dict[str, str]:
    """Parsuje string IDZ i wyciąga store, pos, transaction.

    Przykład: "c=...|g=...|s=5160|p=11|t=1060"
    Zwraca: {"store_number": "5160", "pos_number": "11", "transaction_number": "1060"}
    """
    import re
    result = {}

    # Szukamy s=, p=, t= w stringu
    store_match = re.search(r'\|s=(\d+)', idz)
    pos_match = re.search(r'\|p=(\d+)', idz)
    trans_match = re.search(r'\|t=(\d+)', idz)

    if store_match:
        result["store_number"] = store_match.group(1)
    if pos_match:
        result["pos_number"] = pos_match.group(1)
    if trans_match:
        result["transaction_number"] = trans_match.group(1)

    return result


class ReceiptInput(BaseModel):
    """Główny model całego paragonu z JSON Biedronka.

    Struktura JSON:
    {
        "protoVersion": "000",
        "IDZ": "c=...|s=5160|p=11|t=1060",
        "header": [...],
        "body": [...],
        ...
    }
    """

    model_config = ConfigDict(populate_by_name=True)

    proto_version: str = Field(alias="protoVersion")
    idz: str = Field(alias="IDZ")
    device_type: int = Field(alias="deviceType")
    printed: bool = False
    header: list[HeaderItemInput]
    body: list[BodyItemInput]
    # data i sign ignorujemy - niepotrzebne do analizy

    @computed_field
    @property
    def parsed_idz(self) -> dict[str, str]:
        """Rozparsowany IDZ z numerem sklepu, kasy i transakcji."""
        return parse_idz(self.idz)

    @computed_field
    @property
    def header_data(self) -> HeaderDataInput | None:
        """Wyciąga headerData z tablicy header."""
        for item in self.header:
            if item.header_data:
                return item.header_data
        return None

    @computed_field
    @property
    def fiscal_footer(self) -> FiscalFooterInput | None:
        """Wyciąga fiscalFooter z tablicy body."""
        for item in self.body:
            if item.fiscal_footer:
                return item.fiscal_footer
        return None

    @computed_field
    @property
    def sum_in_currency(self) -> SumInCurrencyInput | None:
        """Wyciąga sumInCurrency z tablicy body."""
        for item in self.body:
            if item.sum_in_currency:
                return item.sum_in_currency
        return None

    @computed_field
    @property
    def discount_summary(self) -> DiscountSummaryInput | None:
        """Wyciąga discountSummary z tablicy body."""
        for item in self.body:
            if item.discount_summary:
                return item.discount_summary
        return None

    @computed_field
    @property
    def payment(self) -> PaymentInput | None:
        """Wyciąga pierwszy payment z tablicy body."""
        for item in self.body:
            if item.payment:
                return item.payment
        return None

    @computed_field
    @property
    def sell_lines(self) -> list[SellLineInput]:
        """Zwraca wszystkie sellLine z body."""
        return [item.sell_line for item in self.body if item.sell_line]

    @computed_field
    @property
    def discount_lines(self) -> list[DiscountLineInput]:
        """Zwraca wszystkie discountLine z body."""
        return [item.discount_line for item in self.body if item.discount_line]

    @computed_field
    @property
    def packs(self) -> list[PackInput]:
        """Zwraca wszystkie pack z body."""
        return [item.pack for item in self.body if item.pack]

    @computed_field
    @property
    def vouchers(self) -> list[DiscountVatInput]:
        """Zwraca wszystkie discountVat (vouchery) z body."""
        return [item.discount_vat for item in self.body if item.discount_vat]

    def get_add_line(self, line_id: int) -> str | None:
        """Zwraca wartość addLine o podanym id (np. 6 dla karty lojalnościowej)."""
        for item in self.body:
            if item.add_line and item.add_line.id == line_id:
                return item.add_line.value
        return None

    @computed_field
    @property
    def loyalty_card(self) -> str | None:
        """Karta lojalnościowa (addLine id=6)."""
        return self.get_add_line(6)


# =============================================================================
# DB Models (for database storage)
# =============================================================================

class ReceiptDB(BaseModel):
    """Receipt model for database storage."""

    unique_number: str  # PRIMARY KEY z fiscalFooter (np. "EAZ2202168920")
    store_number: str | None = None  # z IDZ parametr s=
    pos_number: str | None = None  # z IDZ parametr p= lub fiscalFooter.cashNumber
    transaction_number: str | None = None  # z IDZ parametr t=
    fiscal_total: int  # grosze - suma produktów
    total_with_packs: int  # grosze - suma z kaucją
    total_discount: int = 0  # grosze - suma rabatów
    loyalty_card: str | None = None  # np. "99529*****723"
    receipt_date: date
    receipt_time: time
    payment_method: str
    cashier: str | None = None
    file_hash: str
    tin: str | None = None  # NIP sklepu

    @computed_field
    @property
    def fiscal_total_pln(self) -> float:
        """Fiscal total in PLN."""
        return grosze_to_pln(self.fiscal_total)

    @computed_field
    @property
    def total_with_packs_pln(self) -> float:
        """Total with packs in PLN."""
        return grosze_to_pln(self.total_with_packs)

    @computed_field
    @property
    def total_discount_pln(self) -> float:
        """Total discount in PLN."""
        return grosze_to_pln(self.total_discount)


class ItemDB(BaseModel):
    """Item model for database storage."""

    receipt_unique_number: str  # FK do receipts
    name_raw: str  # oryginalna nazwa z paragonu
    name_clean: str  # oczyszczona nazwa
    vat_id: str
    quantity_numeric: float  # 3.0 lub 0.74
    price: int  # grosze - cena jednostkowa
    total: int  # grosze - cena całkowita przed rabatem
    discount_value: int = 0  # grosze - wartość rabatu
    final_price: int  # grosze - cena po rabacie
    is_storno: bool = False

    @computed_field
    @property
    def price_pln(self) -> float:
        """Unit price in PLN."""
        return grosze_to_pln(self.price)

    @computed_field
    @property
    def total_pln(self) -> float:
        """Total in PLN (before discount)."""
        return grosze_to_pln(self.total)

    @computed_field
    @property
    def discount_value_pln(self) -> float:
        """Discount value in PLN."""
        return grosze_to_pln(self.discount_value)

    @computed_field
    @property
    def final_price_pln(self) -> float:
        """Final price in PLN (after discount)."""
        return grosze_to_pln(self.final_price)

    @computed_field
    @property
    def vat_rate(self) -> int:
        """VAT rate percentage."""
        return VAT_RATES.get(self.vat_id, 0)


class VoucherDB(BaseModel):
    """Voucher model for database storage."""

    receipt_unique_number: str  # FK do receipts
    name: str
    vat_id: str
    base: int  # grosze
    value: int  # grosze

    @computed_field
    @property
    def value_pln(self) -> float:
        """Voucher value in PLN."""
        return grosze_to_pln(self.value)


class PackDB(BaseModel):
    """Pack (opakowanie zwrotne) model for database storage."""

    receipt_unique_number: str  # FK do receipts
    name: str
    price: int  # grosze - cena jednostkowa
    quantity: int
    total: int  # grosze

    @computed_field
    @property
    def total_pln(self) -> float:
        """Total in PLN."""
        return grosze_to_pln(self.total)


class VatSummaryDB(BaseModel):
    """VAT summary model for database storage."""

    receipt_unique_number: str  # FK do receipts
    vat_id: str
    vat_rate: int  # stawka VAT w procentach
    vat_sale: int  # grosze - wartość netto
    vat_amount: int  # grosze - kwota VAT


class FileHashDB(BaseModel):
    """File hash model for deduplication."""

    file_hash: str  # SHA256 hash
    filename: str | None = None
    uploaded_at: datetime


# =============================================================================
# RESPONSE Models (for API responses)
# =============================================================================

class UploadResult(BaseModel):
    """Response model for upload endpoint."""

    receipts_processed: int
    receipts_skipped_duplicate: int
    items_processed: int
    items_skipped_storno: int
    errors: list[str] = Field(default_factory=list)
    new_products_found: int = 0


class ReceiptResponse(BaseModel):
    """Response model for single receipt."""

    unique_number: str
    store_number: str | None
    fiscal_total_pln: float
    total_with_packs_pln: float
    total_discount_pln: float
    receipt_date: date
    receipt_time: time
    payment_method: str
    items_count: int


class ItemResponse(BaseModel):
    """Response model for single item."""

    name: str
    quantity: float
    price_pln: float
    final_price_pln: float
    discount_pln: float
    vat_rate: int


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    # Test SellLineInput z polskim przecinkiem
    sell_line = SellLineInput(
        name="Banan Luz                C",
        vatId="C",
        price=699,
        total=517,
        quantity="0,740",
        isStorno=False
    )
    print(f"SellLineInput OK: {sell_line.name_clean} x {sell_line.quantity_numeric}")

    # Test parse_idz
    idz_result = parse_idz("c=123|g=456|s=5160|p=11|t=1060")
    print(f"parse_idz OK: {idz_result}")

    # Test grosze_to_pln
    assert grosze_to_pln(15217) == 152.17
    print(f"grosze_to_pln OK: {grosze_to_pln(15217)} PLN")

    # Test clean_product_name
    assert clean_product_name("KaszaPęczak4X100g        C") == "KaszaPęczak4X100g"
    print(f"clean_product_name OK")

    print("\nModels OK!")
