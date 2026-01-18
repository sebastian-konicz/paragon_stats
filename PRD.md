# PRD: ParagonStats MVP

## Metadata
- **Nazwa projektu:** ParagonStats (wcześniej: Biedronka Wrapped)
- **Autor:** Sebastian
- **Data utworzenia:** 2025-01-14
- **Ostatnia aktualizacja:** 2025-01-18
- **Status:** Draft
- **Wersja:** 0.3 (MVP)

---

## 1. Problem Statement

### Problem
Użytkownicy sklepu Biedronka z włączoną funkcją e-paragonów gromadzą dane o swoich zakupach, ale nie mają prostego sposobu na ich analizę i wyciągnięcie wniosków. Dane są rozproszone w wielu plikach JSON, trudne do interpretacji i nie dają żadnych insightów.

### Rozwiązanie
Aplikacja webowa "ParagonStats" pozwalająca na:
- Upload plików JSON z e-paragonami
- Automatyczne przetwarzanie i agregację danych
- Wizualizację statystyk zakupowych w stylu "Spotify Wrapped"
- Odkrywanie wzorców zakupowych (co, kiedy, za ile)
- Eksport przetworzonych danych do Excel/CSV
- **NOWE:** Generowanie obrazków do udostępniania w social media

### Dla kogo (MVP)
- Użytkownicy Biedronki z e-paragonami
- Osoby zainteresowane kontrolą wydatków
- Tech-savvy użytkownicy (MVP wymaga ręcznego eksportu JSON)

### Wartość dla właściciela
- Budowanie bazy produktów dla przyszłego algorytmu kategoryzacji AI
- Budowanie listy zainteresowanych użytkowników (waitlista)
- Potencjalne wsparcie finansowe przez buycoffee.to

---

## 2. Goals & Non-Goals

### ✅ Goals (MVP - must have)

#### Core Features
- [ ] Upload jednego lub wielu plików JSON z paragonami
- [ ] Walidacja i parsowanie struktury paragonów
- [ ] Przechowywanie danych w bazie (SQLite dla użytkownika, cloud storage dla surowych plików)
- [ ] Gromadzenie surowych plików JSON dla budowy bazy produktów
- [ ] Deduplikacja plików (hash-based)

#### Dashboard & Statystyki
- [ ] Suma wydatków (ogółem, per miesiąc)
- [ ] Liczba wizyt w sklepie
- [ ] Suma oszczędności na rabatach i voucherach
- [ ] Top 10 najczęściej kupowanych produktów
- [ ] Top 10 produktów na które wydano najwięcej
- [ ] Średnia wartość paragonu
- [ ] Rozkład zakupów wg dni tygodnia
- [ ] Rozkład zakupów wg godzin
- [ ] Filtrowanie po zakresie dat
- [ ] Podstawowy "Wrapped" - podsumowanie roczne/miesięczne

#### Eksport danych
- [ ] Eksport do pliku Excel (.xlsx)
- [ ] Eksport do pliku CSV (.csv)

#### Obrazki do Social Media (NOWE)
- [ ] Generowanie obrazków z statystykami do udostępniania
- [ ] Format: 1080x1080 px (kwadrat) - MVP
- [ ] Typy obrazków:
  - [ ] Top 3 produkty
  - [ ] Kalendarz roczny zakupów / suma dni z zakupami
  - [ ] Suma oszczędności / % oszczędności
  - [ ] Najpopularniejszy dzień i godzina zakupów
- [ ] Branding: logo + nazwa ParagonStats na obrazku
- [ ] Pobieranie obrazka jako PNG

#### Engagement & Monetyzacja
- [ ] Formularz email (waitlista) na stronie wyników - bez przeładowania
- [ ] Widget/przycisk BuyCoffee.to

#### Legal
- [ ] Polityka prywatności
- [ ] Regulamin serwisu
- [ ] Checkbox zgody przed uploadem

### ⏳ Goals (Post-MVP - nice to have)
- [ ] Dodatkowe formaty obrazków: Stories (1080x1920), Poziomy (1200x630)
- [ ] Ciemny/jasny motyw obrazków
- [ ] Więcej typów obrazków (ciekawostki, porównania)
- [ ] Matchowanie produktów z bazą kategorii (AI/embeddingi)
- [ ] Kategoryzacja wydatków (nabiał, pieczywo, słodycze, etc.)
- [ ] Porównanie okresów (miesiąc do miesiąca)
- [ ] Trendy i wykresy czasowe
- [ ] Udostępnianie Wrapped jako obrazek
- [ ] Autentykacja użytkowników
- [ ] Ekstrakcja gramatur z nazw produktów (g, kg, ml, l, szt.)

### ❌ Non-Goals (nie w MVP)
- Konta użytkowników / logowanie
- Automatyczne pobieranie paragonów (scraping)
- Obsługa innych sieci sklepów (Lidl, Żabka)
- Aplikacja mobilna
- Rekomendacje produktowe

---

## 3. User Stories

### US-1: Upload paragonów
```
JAKO użytkownik Biedronki
CHCĘ uploadować pliki JSON z moimi paragonami
ABY móc przeanalizować swoje zakupy

Kryteria akceptacji:
- Mogę wybrać jeden lub wiele plików JSON naraz
- Widzę checkbox ze zgodą na przetwarzanie danych
- Muszę zaakceptować regulamin przed uploadem
- System waliduje format plików przed przetworzeniem
- Widzę postęp przetwarzania
- Dostaję informację o liczbie przetworzonych paragonów
- Błędne pliki są raportowane (które i dlaczego)
- Duplikaty są wykrywane i pomijane
- Pozycje stornowane (isStorno=true) są prawidłowo obsługiwane
```

### US-2: Podstawowe statystyki
```
JAKO użytkownik
CHCĘ zobaczyć podsumowanie moich wydatków
ABY wiedzieć ile i na co wydaję pieniądze

Kryteria akceptacji:
- Widzę sumę wszystkich wydatków (fiscalTotal - produkty)
- Widzę sumę zapłaconą (totalWithPacks - z kaucjami)
- Widzę liczbę wizyt w sklepie
- Widzę średnią wartość paragonu
- Widzę sumę oszczędności z rabatów i voucherów
- Widzę % oszczędności względem cen wyjściowych
- Mogę filtrować po zakresie dat
```

### US-3: Top produkty
```
JAKO użytkownik
CHCĘ zobaczyć ranking moich najczęstszych zakupów
ABY zrozumieć swoje nawyki zakupowe

Kryteria akceptacji:
- Widzę top 10 produktów wg ilości
- Widzę top 10 produktów wg wydanej kwoty
- Dla każdego produktu widzę: nazwę, ilość, sumę wydatków
```

### US-4: Wzorce czasowe
```
JAKO użytkownik
CHCĘ zobaczyć kiedy najczęściej robię zakupy
ABY zoptymalizować swoje wizyty w sklepie

Kryteria akceptacji:
- Widzę rozkład zakupów wg dni tygodnia (wykres)
- Widzę rozkład zakupów wg godzin (wykres)
- Dane są pokazane jako liczba wizyt i/lub suma wydatków
- Widzę najpopularniejszy dzień i godzinę zakupów
```

### US-5: Wrapped view
```
JAKO użytkownik
CHCĘ zobaczyć atrakcyjne podsumowanie typu "Wrapped"
ABY mieć przyjemność z przeglądania swoich danych

Kryteria akceptacji:
- Widzę podsumowanie w atrakcyjnej formie wizualnej
- Zawiera kluczowe statystyki (suma, oszczędności, top produkty)
- Zawiera ciekawostki (np. "Kupiłeś 156 bananów!")
- Mogę wybrać okres (rok/miesiąc)
```

### US-6: Eksport danych
```
JAKO użytkownik
CHCĘ wyeksportować moje przetworzone dane
ABY móc je dalej analizować w Excelu

Kryteria akceptacji:
- Mogę pobrać plik Excel (.xlsx) ze wszystkimi paragonami
- Mogę pobrać plik CSV ze wszystkimi paragonami
- Pliki zawierają: datę, godzinę, produkty, ceny, rabaty
- Nazwy kolumn są czytelne (po polsku)
```

### US-7: Waitlista email
```
JAKO użytkownik zainteresowany pełną wersją
CHCĘ zostawić swój email
ABY otrzymać powiadomienie gdy serwis będzie gotowy

Kryteria akceptacji:
- Formularz email jest widoczny na górze strony wyników
- Wpisanie emaila nie powoduje przeładowania strony
- Widzę potwierdzenie zapisania
- Mój email jest zapisywany w bazie
```

### US-8: Wsparcie projektu
```
JAKO użytkownik zadowolony z serwisu
CHCĘ wesprzeć finansowo twórcę
ABY pomóc w rozwoju aplikacji

Kryteria akceptacji:
- Widzę wyraźny przycisk/widget BuyCoffee.to
- Kliknięcie otwiera stronę BuyCoffee w nowej karcie
- Widget nie jest nachalny ale jest widoczny
```

### US-9: Obrazki do Social Media (NOWE)
```
JAKO użytkownik
CHCĘ pobrać ładne obrazki z moimi statystykami
ABY podzielić się nimi na social media

Kryteria akceptacji:
- Mogę wygenerować obrazek z wybraną statystyką
- Obrazek ma format 1080x1080 px (kwadrat)
- Na obrazku jest logo/nazwa ParagonStats
- Mogę pobrać obrazek jako plik PNG
- Dostępne typy obrazków:
  - Top 3 produkty
  - Kalendarz zakupów / ilość dni z zakupami
  - Suma/procent oszczędności
  - Najpopularniejszy dzień i godzina
```

---

## 4. Technical Approach

### Stack technologiczny

| Warstwa | Technologia | Uzasadnienie |
|---------|-------------|--------------|
| Backend | FastAPI (Python 3.11+) | Szybki, async, type hints |
| Frontend | Streamlit | Rapid prototyping, Python |
| Baza danych | SQLite | Zero setup, wystarczy dla MVP |
| Storage plików | Local filesystem (MVP) → S3/R2 (później) | Prostota na start |
| Eksport | openpyxl (xlsx), csv module | Standardowe |
| **Obrazki** | **Pillow** | Generowanie PNG, tekst, kompozycje |
| Walidacja | Pydantic v2 | Integracja z FastAPI |
| Wykresy | Plotly / Altair | Interaktywne, ładne |
| Testy | pytest | Standard |

### Architektura MVP

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI                                │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│  │  Upload  │ │Dashboard │ │   Wrapped   │ │   Export/Email      │ │
│  │ +Consent │ │ +Email   │ │  +Obrazki   │ │   +BuyCoffee        │ │
│  └────┬─────┘ └────┬─────┘ └──────┬──────┘ └──────────┬──────────┘ │
└───────┼────────────┼──────────────┼───────────────────┼────────────┘
        │            │              │                   │
        ▼            ▼              ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                              │
│  POST /upload   GET /stats/*   GET /wrapped   GET /export/*         │
│  POST /waitlist               GET /images/*                         │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
┌───────────────────┐ ┌───────────┐ ┌───────────────────┐
│   SQLite DB       │ │  Raw JSON │ │   Waitlist DB     │
│   (parsed data)   │ │  Storage  │ │   (emails)        │
└───────────────────┘ └───────────┘ └───────────────────┘
```

### Struktura projektu

```
paragonstats/
├── README.md
├── PRD.md
├── CLAUDE.md
├── PRIVACY_POLICY.md
├── TERMS_OF_SERVICE.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── database.py          # SQLite connection
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── receipt.py       # Receipt models
│   │   ├── stats.py         # Stats models
│   │   └── waitlist.py      # Email waitlist model
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py        # JSON parsing
│   │   ├── stats.py         # Statistics
│   │   ├── wrapped.py       # Wrapped generation
│   │   ├── exporter.py      # Excel/CSV export
│   │   ├── storage.py       # Raw file storage
│   │   ├── deduplication.py # Hash-based dedup
│   │   └── image_generator.py  # NOWE: Generowanie obrazków
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py        # Upload endpoints
│   │   ├── stats.py         # Stats endpoints
│   │   ├── export.py        # Export endpoints
│   │   ├── waitlist.py      # Waitlist endpoint
│   │   └── images.py        # NOWE: Image endpoints
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
│       ├── charts.py
│       ├── metrics.py
│       ├── email_form.py
│       ├── buycoffee.py
│       └── share_images.py  # NOWE: Komponent obrazków
│
├── assets/                  # NOWE: Zasoby graficzne
│   ├── fonts/
│   │   └── .gitkeep
│   ├── logo/
│   │   └── .gitkeep        # Logo ParagonStats (do dodania)
│   └── templates/          # Szablony obrazków
│       └── .gitkeep
│
├── storage/
│   └── raw_receipts/        # Surowe pliki JSON (gitignored)
│
├── data/
│   └── .gitkeep
│
└── legal/
    ├── privacy_policy.md
    └── terms_of_service.md
```

---

## 5. Struktura JSON e-paragonu Biedronka (ZWERYFIKOWANE)

### ⚠️ UWAGA: Wszystkie kwoty są w GROSZACH (int) - dzielić przez 100!

### Główna struktura pliku

```json
{
  "protoVersion": "000",
  "IDZ": "c=...|g=...|s=5160|p=11|t=1060",
  "deviceType": 2,
  "printed": false,
  "data": "eyJ...(JWT - pomijamy)...",
  "header": [...],
  "body": [...],
  "sign": "07DAC7CFD..."
}
```

### Pole IDZ (identyfikator złożony)

Format: `c={client}|g={guid}|s={store}|p={pos}|t={transaction}`

| Parametr | Znaczenie | Przykład |
|----------|-----------|----------|
| `s` | Numer sklepu | `5160` |
| `p` | Numer kasy | `11` |
| `t` | Numer transakcji | `1060` |

### Sekcja header

```json
"header": [
  {
    "image": {
      "id": "EAZ2202168920-1-167870",
      "hash": "DmwwvSQRHLaIxnrFwFSH2ZMvlLZHRrslUP5n/gwzXpU=",
      "data": "Qk02FwAA...(bitmap logo - pomijamy)"
    }
  },
  {
    "headerText": {
      "headerTextLines": "<div class=\"align-center\">BIEDRONKA \"CODZIENNIE NISKIE CENY\" 5160</div><div class=\"align-center\">02-785 WARSZAWA UL. SUROWIECKIEGO/ROMERA 10</div>..."
    }
  },
  {
    "headerData": {
      "tin": "7791011327",
      "docNumber": 172202,
      "date": "2026-01-17T15:08:58.000Z",
      "CPS": 56
    }
  }
]
```

| Pole | Ścieżka | Typ | Opis |
|------|---------|-----|------|
| NIP sklepu | `header[2].headerData.tin` | string | NIP Jeronimo Martins |
| Nr dokumentu | `header[2].headerData.docNumber` | int | Numer paragonu |
| Data/czas | `header[2].headerData.date` | ISO8601 | Data i czas zakupu |
| Adres sklepu | `header[1].headerText.headerTextLines` | HTML | Wymaga parsowania |

### Sekcja body - Produkty (sellLine)

```json
{
  "sellLine": {
    "name": "KaszaPęczak4X100g        C",
    "vatId": "C",
    "price": 189,
    "total": 567,
    "quantity": "3",
    "isStorno": false
  }
}
```

| Pole | Typ | Opis | Uwagi |
|------|-----|------|-------|
| `name` | string | Nazwa produktu (~25 znaków) | Kończy się literą stawki VAT |
| `vatId` | string | Stawka VAT | A=23%, B=8%, C=5%, D=0% |
| `price` | int | Cena jednostkowa | **W GROSZACH!** |
| `total` | int | Wartość brutto | **W GROSZACH!** |
| `quantity` | string | Ilość | Może być "3" lub "0,740" |
| `isStorno` | bool | Czy stornowano | **WAŻNE: pomijać jeśli true!** |

### Sekcja body - Rabaty produktowe (discountLine)

Występuje bezpośrednio PO powiązanym `sellLine`:

```json
{
  "discountLine": {
    "base": 567,
    "value": 189,
    "isDiscount": true,
    "isPercent": false,
    "isStorno": false,
    "vatId": "C"
  }
}
```

| Pole | Typ | Opis |
|------|-----|------|
| `base` | int | Kwota przed rabatem (grosze) |
| `value` | int | Wartość rabatu (grosze) |
| `isPercent` | bool | Czy rabat procentowy |

### Sekcja body - Vouchery (discountVat)

Rabaty na poziomie stawki VAT (nie produktu):

```json
{
  "discountVat": {
    "base": 8650,
    "value": 533,
    "isDiscount": true,
    "isPercent": false,
    "name": "Voucher",
    "isStorno": false,
    "vatId": "A"
  }
}
```

### Sekcja body - Opakowania zwrotne (pack)

Opcjonalne - nie występuje w każdym paragonie:

```json
{
  "pack": {
    "name": "But Plastik kaucja",
    "price": 50,
    "quantity": "7",
    "total": 350,
    "isNegative": false
  }
}
```

### Sekcja body - Podsumowanie rabatów (discountSummary)

```json
{
  "discountSummary": {
    "discounts": 2940
  }
}
```

### Sekcja body - Podsumowanie VAT (vatSummary)

```json
{
  "vatSummary": {
    "currency": "PLN",
    "vatRatesSummary": [
      {
        "vatId": "A",
        "vatRate": 2300,
        "vatSale": 8117,
        "vatAmount": 1518
      },
      {
        "vatId": "C",
        "vatRate": 500,
        "vatSale": 7100,
        "vatAmount": 338
      }
    ]
  }
}
```

| Pole | Typ | Opis |
|------|-----|------|
| `vatRate` | int | Stawka VAT × 100 (2300 = 23%) |
| `vatSale` | int | Sprzedaż w tej stawce (grosze) |
| `vatAmount` | int | Kwota VAT (grosze) |

### Sekcja body - Suma (sumInCurrency)

```json
{
  "sumInCurrency": {
    "fiscalTotal": 15217,
    "totalWithPacks": 15567,
    "currency": "PLN",
    "printBig": true,
    "printable": true
  }
}
```

| Pole | Typ | Opis |
|------|-----|------|
| `fiscalTotal` | int | Suma produktów (bez kaucji) |
| `totalWithPacks` | int | Suma do zapłaty (z kaucją) |

### Sekcja body - Płatność (payment)

```json
{
  "payment": {
    "type": "2",
    "amount": 15567,
    "name": "DEBIT MASTERCARD 07 1",
    "currency": "PLN"
  }
}
```

### Sekcja body - Stopka fiskalna (fiscalFooter)

```json
{
  "fiscalFooter": {
    "billNumber": 137,
    "uniqueNumber": "EAZ2202168920",
    "cashNumber": "Kasa 11",
    "cashier": "Kasjer nr 33",
    "CPS": 56,
    "date": "2026-01-17T15:08:59.000Z"
  }
}
```

| Pole | Typ | Opis |
|------|-----|------|
| `billNumber` | int | Numer paragonu na kasie |
| `uniqueNumber` | string | **Unikalny identyfikator paragonu** |
| `cashNumber` | string | Numer kasy |
| `cashier` | string | Numer kasjera |

### Sekcja body - Dane dodatkowe (addLine)

```json
{
  "addLine": {
    "id": 0,
    "data": "<div class=\"align-left\">Nr&nbsp;transakcji:<span class=\"float-right\">1060</span></div>",
    "width": 80,
    "CPS": 56
  }
}
```

| ID | Zawartość |
|----|-----------|
| `0` | Numer transakcji |
| `6` | Numer karty Moja Biedronka (99529*****723) |
| `30` | Numer złożony (5160260117106011) |
| `41` | Podsumowanie rabatów (HTML) |

### Sekcja body - Kod kreskowy (barcode)

```json
{
  "barcode": {
    "id": 5,
    "data": "MTAwMDA1MTYwMTA2MDIyMDgxMTk4MA=="
  }
}
```

Pole `data` zawiera kod w Base64.

---

## 6. Data Model

### Schema bazy danych (SQLite)

```sql
-- Tabela paragonów
CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Identyfikatory
    unique_number TEXT UNIQUE NOT NULL,      -- EAZ2202168920 (główny klucz)
    doc_number INTEGER,                       -- 172202
    bill_number INTEGER,                      -- 137 (nr na kasie)
    composite_number TEXT,                    -- 5160260117106011
    
    -- Sklep
    store_number TEXT,                        -- 5160
    store_address TEXT,                       -- Parsowane z headerText
    tin TEXT,                                 -- 7791011327 (NIP)
    
    -- Czas
    date DATE NOT NULL,
    time TIME NOT NULL,
    datetime DATETIME NOT NULL,
    day_of_week INTEGER,                      -- 0=Monday
    hour INTEGER,
    
    -- Kasa
    cash_number TEXT,                         -- "Kasa 11"
    cashier TEXT,                             -- "Kasjer nr 33"
    transaction_number TEXT,                  -- 1060
    
    -- Kwoty (w GROSZACH - int)
    fiscal_total INTEGER,                     -- Suma produktów
    total_with_packs INTEGER,                 -- Suma z kaucjami
    total_discount INTEGER,                   -- Suma rabatów
    
    -- Płatność
    payment_method TEXT,                      -- "DEBIT MASTERCARD 07 1"
    payment_type TEXT,                        -- "2"
    
    -- Kaucje (opcjonalne)
    packs_total INTEGER DEFAULT 0,            -- Suma kaucji
    
    -- Karta lojalnościowa
    loyalty_card TEXT,                        -- "99529*****723"
    
    -- Metadane
    file_hash TEXT,                           -- SHA256 pliku źródłowego
    barcode TEXT,                             -- Kod kreskowy (base64)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_json TEXT                             -- Cały JSON (opcjonalnie)
);

-- Tabela pozycji
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    
    -- Produkt
    name_raw TEXT NOT NULL,                   -- "KaszaPęczak4X100g        C"
    name_clean TEXT,                          -- "KaszaPęczak4X100g" (bez VAT)
    vat_id TEXT,                              -- "C"
    
    -- Ilość i cena (GROSZE)
    quantity TEXT,                            -- "3" lub "0,740"
    quantity_numeric REAL,                    -- 3.0 lub 0.74
    price INTEGER,                            -- Cena jednostkowa
    total INTEGER,                            -- Wartość brutto
    
    -- Rabat (opcjonalny)
    discount_base INTEGER,
    discount_value INTEGER,
    discount_is_percent BOOLEAN DEFAULT FALSE,
    final_price INTEGER,                      -- total - discount_value
    
    -- Storno
    is_storno BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);

-- Tabela voucherów
CREATE TABLE vouchers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    
    name TEXT,                                -- "Voucher"
    vat_id TEXT,                              -- "A" lub "C"
    base INTEGER,                             -- Podstawa
    value INTEGER,                            -- Wartość rabatu
    
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);

-- Tabela opakowań zwrotnych
CREATE TABLE packs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    
    name TEXT,                                -- "But Plastik kaucja"
    price INTEGER,                            -- Cena jednostkowa (50 = 0.50 PLN)
    quantity INTEGER,
    total INTEGER,
    
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);

-- Tabela podsumowania VAT (per paragon)
CREATE TABLE vat_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    
    vat_id TEXT,                              -- "A", "C"
    vat_rate INTEGER,                         -- 2300 = 23%
    vat_sale INTEGER,                         -- Sprzedaż w tej stawce
    vat_amount INTEGER,                       -- Kwota VAT
    
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);

-- Deduplikacja plików
CREATE TABLE file_hashes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_hash TEXT UNIQUE NOT NULL,
    original_filename TEXT,
    file_size INTEGER,
    receipt_count INTEGER,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Waitlista
CREATE TABLE waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    source TEXT DEFAULT 'dashboard',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_hash TEXT
);

-- Baza produktów (dla AI)
CREATE TABLE raw_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_raw TEXT NOT NULL,
    name_clean TEXT UNIQUE,
    occurrence_count INTEGER DEFAULT 1,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indeksy
CREATE INDEX idx_receipts_date ON receipts(date);
CREATE INDEX idx_receipts_unique ON receipts(unique_number);
CREATE INDEX idx_receipts_hash ON receipts(file_hash);
CREATE INDEX idx_receipts_store ON receipts(store_number);
CREATE INDEX idx_items_receipt ON items(receipt_id);
CREATE INDEX idx_items_name ON items(name_clean);
CREATE INDEX idx_vouchers_receipt ON vouchers(receipt_id);
CREATE INDEX idx_packs_receipt ON packs(receipt_id);
CREATE INDEX idx_vat_receipt ON vat_summary(receipt_id);
CREATE INDEX idx_file_hashes_hash ON file_hashes(file_hash);
CREATE INDEX idx_raw_products_name ON raw_products(name_clean);
```

---

## 7. Deduplikacja plików

### Strategia

1. **Przy uploadzie pliku:**
   - Oblicz SHA256 hash całego pliku
   - Sprawdź czy hash istnieje w `file_hashes`
   - Jeśli TAK → pomiń plik, zwróć info "duplikat"
   - Jeśli NIE → przetwórz i zapisz hash

2. **Dodatkowa warstwa:**
   - Sprawdź `unique_number` w tabeli `receipts`
   - Jeśli istnieje → pomiń paragon

3. **Storage surowych plików:**
   - Zapisz plik jako `{hash}.json` w `storage/raw_receipts/`
   - Unikamy duplikatów na poziomie filesystem

### Implementacja

```python
import hashlib

def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA256 hash of file content."""
    return hashlib.sha256(content).hexdigest()

def is_duplicate_file(file_hash: str, db_conn) -> bool:
    """Check if file was already processed."""
    cursor = db_conn.execute(
        "SELECT 1 FROM file_hashes WHERE file_hash = ?",
        (file_hash,)
    )
    return cursor.fetchone() is not None

def is_duplicate_receipt(unique_number: str, db_conn) -> bool:
    """Check if receipt was already processed."""
    cursor = db_conn.execute(
        "SELECT 1 FROM receipts WHERE unique_number = ?",
        (unique_number,)
    )
    return cursor.fetchone() is not None
```

---

## 8. API Endpoints

### Upload

```
POST /api/upload
Content-Type: multipart/form-data

Request:
  - files: List[UploadFile]
  - consent: bool (wymagane: true)

Response 200:
{
  "success": true,
  "receipts_processed": 45,
  "receipts_skipped_duplicate": 3,
  "receipts_skipped_storno": 1,
  "files_skipped_duplicate": 1,
  "receipts_failed": 2,
  "errors": ["plik_3.json: Brak pola 'unique_number'"],
  "new_products_found": 23
}
```

### Statistics

```
GET /api/stats/basic?date_from=2024-01-01&date_to=2024-12-31

Response 200:
{
  "fiscal_total": 1521700,          // grosze
  "fiscal_total_pln": 15217.00,     // PLN
  "total_with_packs": 1556700,
  "total_with_packs_pln": 15567.00,
  "total_discount": 294000,
  "total_discount_pln": 2940.00,
  "discount_percent": 16.2,         // % oszczędności
  "receipts_count": 156,
  "avg_receipt_value_pln": 97.54,
  "items_count": 1234
}
```

### Export

```
GET /api/export/xlsx
GET /api/export/csv

Query params:
  - date_from, date_to (opcjonalne)

Response:
  - Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  - Content-Disposition: attachment; filename="paragonstats_export_2024.xlsx"
```

### Images (NOWE)

```
GET /api/images/top-products?limit=3&period=year

Response:
  - Content-Type: image/png
  - Content-Disposition: attachment; filename="paragonstats_top3.png"

GET /api/images/calendar?year=2024

GET /api/images/savings?period=year

GET /api/images/favorite-time?period=year
```

### Waitlist

```
POST /api/waitlist

Request:
{
  "email": "user@example.com",
  "source": "dashboard"
}

Response 200:
{
  "success": true,
  "message": "Email zapisany! Powiadomimy Cię o starcie."
}
```

---

## 9. Generowanie obrazków (NOWE)

### Specyfikacja techniczna

| Parametr | Wartość MVP |
|----------|-------------|
| Format | PNG |
| Wymiary | 1080 × 1080 px (kwadrat) |
| Tło | Do ustalenia (jasne/gradient) |
| Czcionka | Do ustalenia (czytelna, moderna) |
| Logo | Placeholder, docelowo logo ParagonStats |

### Typy obrazków MVP

#### 1. Top 3 produkty
```
┌─────────────────────────────┐
│      🏆 TWOJE TOP 3         │
│         w 2024              │
│                             │
│  1. Banan Luz        156x   │
│  2. Mleko UHT 2%     98x    │
│  3. Chleb tostowy    87x    │
│                             │
│     [logo ParagonStats]     │
└─────────────────────────────┘
```

#### 2. Kalendarz / Dni z zakupami
```
┌─────────────────────────────┐
│    📅 TWÓJ ROK ZAKUPÓW      │
│          2024               │
│                             │
│     156 dni z zakupami      │
│      w Biedronce            │
│                             │
│   [mini kalendarz/heatmap]  │
│                             │
│     [logo ParagonStats]     │
└─────────────────────────────┘
```

#### 3. Oszczędności
```
┌─────────────────────────────┐
│    💰 TWOJE OSZCZĘDNOŚCI    │
│          2024               │
│                             │
│      2 940,00 zł            │
│    zaoszczędzono na         │
│    rabatach i voucherach    │
│                             │
│      to 16,2% mniej!        │
│                             │
│     [logo ParagonStats]     │
└─────────────────────────────┘
```

#### 4. Ulubiony czas zakupów
```
┌─────────────────────────────┐
│   ⏰ KIEDY KUPUJESZ?        │
│          2024               │
│                             │
│   Ulubiony dzień:           │
│      SOBOTA                 │
│                             │
│   Ulubiona godzina:         │
│      17:00 - 18:00          │
│                             │
│     [logo ParagonStats]     │
└─────────────────────────────┘
```

### Implementacja (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def generate_top_products_image(
    products: list[tuple[str, int]],  # [(nazwa, ilość), ...]
    period: str = "2024"
) -> BytesIO:
    """Generate top products image."""
    
    # Utwórz canvas
    img = Image.new('RGB', (1080, 1080), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Załaduj czcionki
    font_title = ImageFont.truetype("assets/fonts/font.ttf", 64)
    font_item = ImageFont.truetype("assets/fonts/font.ttf", 48)
    
    # Rysuj tytuł
    draw.text((540, 100), "🏆 TWOJE TOP 3", font=font_title, anchor="mm", fill='#333')
    draw.text((540, 180), f"w {period}", font=font_item, anchor="mm", fill='#666')
    
    # Rysuj produkty
    y = 350
    for i, (name, count) in enumerate(products[:3], 1):
        draw.text((100, y), f"{i}. {name}", font=font_item, fill='#333')
        draw.text((900, y), f"{count}x", font=font_item, anchor="rm", fill='#E31837')
        y += 100
    
    # Dodaj logo (placeholder)
    # logo = Image.open("assets/logo/logo.png")
    # img.paste(logo, (440, 900))
    
    # Zapisz do BytesIO
    output = BytesIO()
    img.save(output, format='PNG', quality=95)
    output.seek(0)
    return output
```

---

## 10. UI/UX Updates

### Dashboard z Email + BuyCoffee + Obrazki

```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 PARAGONSTATS - Twój Dashboard                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 📧 Zostaw email - powiadomimy Cię o nowych funkcjach!       │   │
│  │ [          twoj@email.pl          ] [Zapisz się]            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │ 15 234 zł│ │ 1 876 zł │ │   156    │ │  97.65 zł│              │
│  │ Wydano   │ │Zaoszczędz│ │  Wizyt   │ │ Średnia  │              │
│  │          │ │  (16,2%) │ │          │ │          │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
│                                                                     │
│  ... (wykresy, top produkty) ...                                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  📱 UDOSTĘPNIJ NA SOCIAL MEDIA                              │   │
│  │                                                              │   │
│  │  [🏆 Top 3]  [📅 Kalendarz]  [💰 Oszczędności]  [⏰ Czas]   │   │
│  │                                                              │   │
│  │  Kliknij aby pobrać obrazek 1080x1080 px                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  📥 EKSPORTUJ DANE                                          │   │
│  │  [📗 Pobierz Excel]  [📄 Pobierz CSV]                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ☕ Podoba Ci się ParagonStats? Wesprzyj rozwój!            │   │
│  │            [☕ Postaw kawę na BuyCoffee.to]                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 11. Success Metrics (MVP)

### Techniczne
- [ ] Upload 100 paragonów < 10 sekund
- [ ] Deduplikacja działa (0 duplikatów w bazie)
- [ ] Poprawna obsługa pozycji stornowanych
- [ ] Eksport Excel/CSV generuje się < 5 sekund
- [ ] Generowanie obrazka < 2 sekundy
- [ ] Test coverage > 70%

### Produktowe
- [ ] 10+ emaili na waitliście (po pierwszych testach)
- [ ] 1+ kawa na BuyCoffee (walidacja modelu)
- [ ] 1000+ unikalnych produktów w bazie `raw_products`
- [ ] 10+ pobranych obrazków (walidacja funkcji share)

### Edukacyjne
- [ ] Działający fullstack (FastAPI + Streamlit)
- [ ] Obsługa plików binarnych (Excel, PNG)
- [ ] Asynchroniczne formularze

---

## 12. Legal Requirements

### Wymagane dokumenty
1. **Polityka Prywatności** - osobny plik `PRIVACY_POLICY.md`
2. **Regulamin** - osobny plik `TERMS_OF_SERVICE.md`

### Checkbox consent (wymagany przed uploadem)
```
☑️ Akceptuję Regulamin i Politykę Prywatności. Oświadczam, że:
   - Uploadowane pliki są moimi własnymi e-paragonami
   - Wyrażam zgodę na przetwarzanie danych z paragonów w celu analizy
   - Wyrażam zgodę na wykorzystanie zanonimizowanych nazw produktów 
     do budowy bazy kategoryzacji
   - Rozumiem, że mogę wycofać zgodę i zażądać usunięcia danych w każdej chwili
```

---

## 13. Open Questions

1. ~~**Format JSON** - Jaka jest rzeczywista struktura?~~ ✅ ROZWIĄZANE
2. **BuyCoffee URL** - Jaki jest Twój link do profilu?
3. **Storage** - Czy na MVP filesystem wystarczy, czy od razu S3/R2?
4. **RODO** - Czy potrzebujesz DPO? (przy >5000 użytkowników)
5. **Logo** - Kiedy będzie gotowe logo do obrazków?
6. **Czcionka** - Czy masz preferencje co do fontu na obrazkach?

---

## Changelog

| Data | Wersja | Zmiany |
|------|--------|--------|
| 2025-01-14 | 0.1 | Initial MVP PRD |
| 2025-01-17 | 0.2 | Dodano: deduplikację, waitlistę, eksport, BuyCoffee, legal |
| 2025-01-18 | 0.3 | Dodano: zweryfikowaną strukturę JSON, obrazki social media, isStorno, vatSummary, rozszerzone schema DB |
