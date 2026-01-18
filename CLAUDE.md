# CLAUDE.md - Kontekst projektu dla Claude Code

## 🎯 O projekcie

**ParagonStats** - aplikacja webowa do analizy paragonów zakupowych ze sklepu Biedronka w stylu "Spotify Wrapped".

### Główne założenia
- Użytkownik uploaduje pliki JSON z e-paragonami
- System parsuje, agreguje i wizualizuje dane
- MVP bez autentykacji (dane w session)
- Gromadzenie surowych plików dla przyszłego AI
- Waitlista emailowa dla budowania bazy użytkowników
- Monetyzacja przez BuyCoffee.to (dobrowolne wsparcie)
- **NOWE:** Generowanie obrazków do udostępniania w social media

### Właściciel projektu
Sebastian - Data Analyst w Mastercard, doświadczenie z Python, Pandas, SQL, Spark. 
Projekt realizowany wieczorami i w weekendy.
**Uwaga:** Sebastian ma ADHD - preferuje krótkie, konkretne taski z natychmiastowym feedbackiem.

---

## 🛠️ Stack technologiczny

| Warstwa | Technologia | Wersja |
|---------|-------------|--------|
| Backend | FastAPI | 0.109+ |
| Frontend MVP | Streamlit | 1.30+ |
| Język | Python | 3.11+ |
| Baza danych | SQLite | 3 |
| Eksport | openpyxl, csv | latest |
| **Obrazki** | **Pillow** | latest |
| Walidacja | Pydantic | 2.0+ |
| Wykresy | Plotly | 5.x |
| Testy | pytest | 7.x+ |
| AI (post-MVP) | sentence-transformers | latest |

---

## 📁 Struktura projektu

```
paragonstats/
├── README.md
├── PRD.md
├── CLAUDE.md
├── ROADMAP_ADHD.md
├── PRIVACY_POLICY.md
├── TERMS_OF_SERVICE.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── receipt.py
│   │   ├── stats.py
│   │   └── waitlist.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── stats.py
│   │   ├── wrapped.py
│   │   ├── exporter.py
│   │   ├── storage.py
│   │   ├── deduplication.py
│   │   └── image_generator.py  # NOWE
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   ├── stats.py
│   │   ├── export.py
│   │   ├── waitlist.py
│   │   └── images.py           # NOWE
│   │
│   └── tests/
│       └── ...
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── 1_📤_Upload.py
│   │   ├── 2_📊_Dashboard.py
│   │   └── 3_🎉_Wrapped.py
│   └── components/
│       ├── __init__.py
│       ├── charts.py
│       ├── metrics.py
│       ├── email_form.py
│       ├── buycoffee.py
│       └── share_images.py     # NOWE
│
├── assets/                     # NOWE
│   ├── fonts/
│   ├── logo/
│   └── templates/
│
├── storage/
│   └── raw_receipts/
│
├── data/
│   └── .gitkeep
│
└── legal/
    ├── privacy_policy.md
    └── terms_of_service.md
```

---

## 📊 Struktura JSON e-paragonu Biedronka (ZWERYFIKOWANE)

### ⚠️ KRYTYCZNE: Wszystkie kwoty są w GROSZACH (int) - dzielić przez 100!

### Kluczowe ścieżki do danych

| Dane | Ścieżka JSON | Typ | Przykład |
|------|--------------|-----|----------|
| **Data/czas** | `header[2].headerData.date` | ISO8601 | `"2026-01-17T15:08:58.000Z"` |
| **Nr dokumentu** | `header[2].headerData.docNumber` | int | `172202` |
| **NIP** | `header[2].headerData.tin` | string | `"7791011327"` |
| **Adres sklepu** | `header[1].headerText.headerTextLines` | HTML | wymaga parsowania |
| **Nr sklepu** | `IDZ` parametr `s=` | string | `"5160"` |
| **Nr kasy** | `IDZ` parametr `p=` LUB `fiscalFooter.cashNumber` | string | `"11"` / `"Kasa 11"` |
| **Nr transakcji** | `IDZ` parametr `t=` LUB `addLine[id=0]` | string | `"1060"` |
| **Unikalny ID** | `body[].fiscalFooter.uniqueNumber` | string | `"EAZ2202168920"` |
| **Nr złożony** | `body[].addLine[id=30]` | string | `"5160260117106011"` |
| **Karta lojalnościowa** | `body[].addLine[id=6]` | string | `"99529*****723"` |
| **Kasjer** | `body[].fiscalFooter.cashier` | string | `"Kasjer nr 33"` |
| **Suma produktów** | `body[].sumInCurrency.fiscalTotal` | int | `15217` (grosze) |
| **Suma z kaucją** | `body[].sumInCurrency.totalWithPacks` | int | `15567` (grosze) |
| **Suma rabatów** | `body[].discountSummary.discounts` | int | `2940` (grosze) |
| **Płatność** | `body[].payment.name` | string | `"DEBIT MASTERCARD 07 1"` |
| **Kod kreskowy** | `body[].barcode.data` | base64 | `"MTAwMDA1MTYw..."` |

### Produkt (sellLine)

```json
{
  "sellLine": {
    "name": "KaszaPęczak4X100g        C",  // ~25 znaków + litera VAT
    "vatId": "C",                           // A=23%, B=8%, C=5%, D=0%
    "price": 189,                           // GROSZE! = 1.89 PLN
    "total": 567,                           // GROSZE! = 5.67 PLN
    "quantity": "3",                        // STRING! może być "0,740"
    "isStorno": false                       // WAŻNE: pomijać jeśli true!
  }
}
```

### Rabat produktowy (discountLine) - występuje PO sellLine

```json
{
  "discountLine": {
    "base": 567,        // kwota przed rabatem (grosze)
    "value": 189,       // wartość rabatu (grosze)
    "isDiscount": true,
    "isPercent": false,
    "vatId": "C"
  }
}
```

### Voucher (discountVat) - rabat na poziomie stawki VAT

```json
{
  "discountVat": {
    "name": "Voucher",
    "base": 8650,
    "value": 533,       // 5.33 PLN rabatu
    "vatId": "A"
  }
}
```

### Opakowania zwrotne (pack) - opcjonalne

```json
{
  "pack": {
    "name": "But Plastik kaucja",
    "price": 50,        // 0.50 PLN za sztukę
    "quantity": "7",
    "total": 350        // 3.50 PLN łącznie
  }
}
```

### Parsowanie quantity

```python
def parse_quantity(qty_str: str) -> float:
    """Parse quantity string to float. Handles Polish decimal comma."""
    return float(qty_str.replace(",", "."))

# "3" -> 3.0
# "0,740" -> 0.74
```

### Parsowanie IDZ

```python
import re

def parse_idz(idz: str) -> dict:
    """Extract store, pos, transaction from IDZ string."""
    pattern = r's=(\d+)\|p=(\d+)\|t=(\d+)'
    match = re.search(pattern, idz)
    if match:
        return {
            "store_number": match.group(1),
            "pos_number": match.group(2),
            "transaction_number": match.group(3)
        }
    return {}

# "c=...|g=...|s=5160|p=11|t=1060" -> {"store_number": "5160", "pos_number": "11", "transaction_number": "1060"}
```

---

## 📊 Model danych (SQLite)

### Główne tabele

| Tabela | Opis | Klucz unikalny |
|--------|------|----------------|
| `receipts` | Paragony | `unique_number` (EAZ...) |
| `items` | Pozycje zakupowe | `id` (auto) |
| `vouchers` | Vouchery/rabaty VAT | `id` (auto) |
| `packs` | Opakowania zwrotne | `id` (auto) |
| `vat_summary` | Podsumowanie VAT | `id` (auto) |
| `file_hashes` | Deduplikacja | `file_hash` |
| `raw_products` | Baza produktów (AI) | `name_clean` |
| `waitlist` | Emaile | `email` |

### Kluczowe pola receipts

```sql
unique_number TEXT UNIQUE NOT NULL,  -- główny identyfikator
store_number TEXT,                    -- "5160"
fiscal_total INTEGER,                 -- suma produktów (grosze)
total_with_packs INTEGER,             -- suma z kaucją (grosze)
total_discount INTEGER,               -- suma rabatów (grosze)
loyalty_card TEXT,                    -- "99529*****723"
```

### Kluczowe pola items

```sql
name_raw TEXT NOT NULL,              -- "KaszaPęczak4X100g        C"
name_clean TEXT,                     -- "KaszaPęczak4X100g"
quantity_numeric REAL,               -- 3.0 lub 0.74
price INTEGER,                       -- cena jednostkowa (grosze)
final_price INTEGER,                 -- po rabacie (grosze)
is_storno BOOLEAN DEFAULT FALSE,     -- WAŻNE!
```

---

## 🔌 API Endpoints

| Method | Endpoint | Opis |
|--------|----------|------|
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Upload + consent |
| GET | `/api/stats/basic` | Podstawowe statystyki |
| GET | `/api/stats/top-products` | Top produkty |
| GET | `/api/stats/time-distribution` | Rozkład czasowy |
| GET | `/api/wrapped` | Wrapped summary |
| GET | `/api/export/xlsx` | Eksport Excel |
| GET | `/api/export/csv` | Eksport CSV |
| POST | `/api/waitlist` | Zapis na waitlistę |
| GET | `/api/images/top-products` | **NOWE:** Obrazek top produkty |
| GET | `/api/images/calendar` | **NOWE:** Obrazek kalendarz |
| GET | `/api/images/savings` | **NOWE:** Obrazek oszczędności |
| GET | `/api/images/favorite-time` | **NOWE:** Obrazek ulubiony czas |

---

## 🖼️ Generowanie obrazków (NOWE)

### Specyfikacja MVP

| Parametr | Wartość |
|----------|---------|
| Format | PNG |
| Wymiary | 1080 × 1080 px |
| Biblioteka | Pillow |

### Typy obrazków

1. **Top 3 produkty** - najpopularniejsze produkty
2. **Kalendarz** - dni z zakupami / heatmapa
3. **Oszczędności** - suma i % oszczędności
4. **Ulubiony czas** - dzień tygodnia + godzina

### Przykład implementacji

```python
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def generate_image(width=1080, height=1080, bg_color='#FFFFFF'):
    """Create base image canvas."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    return img, draw

def save_to_bytes(img: Image) -> BytesIO:
    """Save image to BytesIO for HTTP response."""
    output = BytesIO()
    img.save(output, format='PNG', quality=95)
    output.seek(0)
    return output
```

---

## 🔐 Deduplikacja

### Algorytm

```python
import hashlib

def calculate_file_hash(content: bytes) -> str:
    """SHA256 hash pliku."""
    return hashlib.sha256(content).hexdigest()

def is_duplicate_file(file_hash: str, db) -> bool:
    """Sprawdź file_hashes."""
    return db.execute(
        "SELECT 1 FROM file_hashes WHERE file_hash = ?", 
        (file_hash,)
    ).fetchone() is not None

def is_duplicate_receipt(unique_number: str, db) -> bool:
    """Sprawdź receipts.unique_number."""
    return db.execute(
        "SELECT 1 FROM receipts WHERE unique_number = ?", 
        (unique_number,)
    ).fetchone() is not None
```

### Flow uploadu

1. Oblicz hash pliku → sprawdź `file_hashes`
2. Jeśli nowy → parsuj JSON
3. Wyciągnij `unique_number` → sprawdź `receipts`
4. Jeśli nowy → zapisz paragon + pozycje
5. Pomiń pozycje z `isStorno=true`

---

## 📐 Konwencje kodu

### Python
- **Type hints** - ZAWSZE
- **Docstrings** - Google style
- **Nazewnictwo** - snake_case dla funkcji, PascalCase dla klas
- **Formatowanie** - black, isort, ruff

### Przykład:

```python
def parse_receipt(
    json_data: dict,
    file_hash: str
) -> tuple[Receipt, list[Item]]:
    """
    Parse receipt JSON into database models.
    
    Args:
        json_data: Raw JSON from e-paragon file
        file_hash: SHA256 hash of source file
    
    Returns:
        Tuple of (Receipt, list of Items)
        
    Raises:
        ValueError: If required fields are missing
    """
    ...
```

### Git commits
```
feat(parser): add support for discountLine
fix(upload): handle isStorno items correctly
refactor(images): extract common drawing functions
docs: update PRD with verified JSON structure
```

---

## ⚠️ Ważne uwagi implementacyjne

### 1. Grosze → PLN
```python
def grosze_to_pln(grosze: int) -> float:
    """Convert grosze to PLN."""
    return grosze / 100

# 15217 -> 152.17
```

### 2. Obsługa isStorno
```python
for item in body:
    if 'sellLine' in item:
        if item['sellLine'].get('isStorno', False):
            continue  # POMIŃ stornowane pozycje!
        # ... process item
```

### 3. Łączenie sellLine + discountLine
```python
current_item = None
for item in body:
    if 'sellLine' in item:
        # Zapisz poprzedni item (jeśli był)
        if current_item:
            items.append(current_item)
        current_item = parse_sell_line(item['sellLine'])
    elif 'discountLine' in item and current_item:
        # Dodaj rabat do bieżącego itemu
        current_item.discount_value = item['discountLine']['value']
        current_item.final_price = current_item.total - current_item.discount_value
```

### 4. Czyszczenie nazwy produktu
```python
def clean_product_name(name_raw: str) -> str:
    """Remove VAT letter and extra spaces from product name."""
    # "KaszaPęczak4X100g        C" -> "KaszaPęczak4X100g"
    return name_raw.rstrip(' ABCDEFG').strip()
```

---

## 🚫 Czego NIE robić

- ❌ Autentykacja w MVP
- ❌ Płatności za eksport
- ❌ Inne sieci niż Biedronka
- ❌ Scraping paragonów
- ❌ Kategoryzacja AI (post-MVP)
- ❌ Ekstrakcja gramatur z nazw (post-MVP)

---

## 💡 Wskazówki dla Claude Code

### Dla ADHD-friendly development:
1. **Jeden task na raz** - nie mieszaj feature'ów
2. **Natychmiastowy feedback** - zawsze uruchom i przetestuj
3. **Małe commity** - łatwiej wrócić do działającego stanu
4. **Wizualne rezultaty** - priorytetyzuj UI nad perfekcyjny backend

### Przy implementacji:
1. Najpierw działający szkielet
2. Potem testy happy path
3. Na końcu edge cases

### Przy błędach:
1. Sprawdź logi
2. Dodaj print/logging
3. Izoluj problem do najmniejszego fragmentu

---

## 🧪 Testowanie parserów

### Przykładowe dane testowe

```python
SAMPLE_SELL_LINE = {
    "name": "Banan Luz                C",
    "vatId": "C",
    "price": 699,      # 6.99 PLN/kg
    "total": 517,      # 5.17 PLN
    "quantity": "0,740",  # 0.74 kg
    "isStorno": False
}

SAMPLE_DISCOUNT_LINE = {
    "base": 517,
    "value": 148,      # 1.48 PLN rabatu
    "isDiscount": True,
    "isPercent": False,
    "vatId": "C"
}

# Po rabacie: 517 - 148 = 369 groszy = 3.69 PLN
```

---

## 📞 Pomocne komendy

```bash
# Uruchom backend
uvicorn backend.main:app --reload --port 8000

# Uruchom frontend
streamlit run frontend/app.py

# Testy
pytest backend/tests/ -v

# Formatowanie
black . && isort .

# Sprawdź typy
mypy backend/

# Lint
ruff check .
```
