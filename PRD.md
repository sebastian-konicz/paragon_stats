# PRD: ParagonStats MVP

## Metadata
- **Nazwa projektu:** ParagonStats (wcześniej: Biedronka Wrapped)
- **Autor:** Sebastian
- **Data utworzenia:** 2025-01-14
- **Ostatnia aktualizacja:** 2025-01-17
- **Status:** Draft
- **Wersja:** 0.2 (MVP)

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
- [ ] **NOWE:** Gromadzenie surowych plików JSON dla budowy bazy produktów
- [ ] **NOWE:** Deduplikacja plików (hash-based)

#### Dashboard & Statystyki
- [ ] Suma wydatków (ogółem, per miesiąc)
- [ ] Liczba wizyt w sklepie
- [ ] Suma oszczędności na rabatach
- [ ] Top 10 najczęściej kupowanych produktów
- [ ] Top 10 produktów na które wydano najwięcej
- [ ] Średnia wartość paragonu
- [ ] Rozkład zakupów wg dni tygodnia
- [ ] Rozkład zakupów wg godzin
- [ ] Filtrowanie po zakresie dat
- [ ] Podstawowy "Wrapped" - podsumowanie roczne/miesięczne

#### Eksport danych
- [ ] **NOWE:** Eksport do pliku Excel (.xlsx)
- [ ] **NOWE:** Eksport do pliku CSV (.csv)

#### Engagement & Monetyzacja
- [ ] **NOWE:** Formularz email (waitlista) na stronie wyników - bez przeładowania
- [ ] **NOWE:** Widget/przycisk BuyCoffee.to

#### Legal
- [ ] **NOWE:** Polityka prywatności
- [ ] **NOWE:** Regulamin serwisu
- [ ] **NOWE:** Checkbox zgody przed uploadem

### ⏳ Goals (Post-MVP - nice to have)
- [ ] Matchowanie produktów z bazą kategorii (AI/embeddingi)
- [ ] Kategoryzacja wydatków (nabiał, pieczywo, słodycze, etc.)
- [ ] Porównanie okresów (miesiąc do miesiąca)
- [ ] Trendy i wykresy czasowe
- [ ] Udostępnianie Wrapped jako obrazek
- [ ] Autentykacja użytkowników

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
```

### US-2: Podstawowe statystyki
```
JAKO użytkownik
CHCĘ zobaczyć podsumowanie moich wydatków
ABY wiedzieć ile i na co wydaję pieniądze

Kryteria akceptacji:
- Widzę sumę wszystkich wydatków
- Widzę liczbę wizyt w sklepie
- Widzę średnią wartość paragonu
- Widzę sumę oszczędności z rabatów
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

### US-6: Eksport danych (NOWE)
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

### US-7: Waitlista email (NOWE)
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

### US-8: Wsparcie projektu (NOWE)
```
JAKO użytkownik zadowolony z serwisu
CHCĘ wesprzeć finansowo twórcę
ABY pomóc w rozwoju aplikacji

Kryteria akceptacji:
- Widzę wyraźny przycisk/widget BuyCoffee.to
- Kliknięcie otwiera stronę BuyCoffee w nowej karcie
- Widget nie jest nachalny ale jest widoczny
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
| Walidacja | Pydantic v2 | Integracja z FastAPI |
| Wykresy | Plotly / Altair | Interaktywne, ładne |
| Testy | pytest | Standard |

### Architektura MVP

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI                                │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│  │  Upload  │ │Dashboard │ │   Wrapped   │ │   Export/Email      │ │
│  │ +Consent │ │ +Email   │ │             │ │   +BuyCoffee        │ │
│  └────┬─────┘ └────┬─────┘ └──────┬──────┘ └──────────┬──────────┘ │
└───────┼────────────┼──────────────┼───────────────────┼────────────┘
        │            │              │                   │
        ▼            ▼              ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                              │
│  POST /upload   GET /stats/*   GET /wrapped   GET /export/*         │
│  POST /waitlist                                                     │
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
│   │   └── deduplication.py # Hash-based dedup
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py        # Upload endpoints
│   │   ├── stats.py         # Stats endpoints
│   │   ├── export.py        # Export endpoints
│   │   └── waitlist.py      # Waitlist endpoint
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
│       ├── email_form.py    # NOWE: Async email form
│       └── buycoffee.py     # NOWE: BuyCoffee widget
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

## 5. Data Model

### Struktura JSON paragonu (INPUT)

**UWAGA:** Struktura wymaga weryfikacji na prawdziwych danych!

```json
{
  "receiptNumber": "12345/2024",
  "shopAddress": "ul. Przykładowa 1, Warszawa",
  "date": "2024-01-15",
  "time": "14:32:45",
  "items": [
    {
      "name": "MLK UHT 2% 1L",
      "quantity": 2,
      "unit": "szt",
      "pricePerUnit": 3.49,
      "totalPrice": 6.98,
      "discount": 1.00,
      "finalPrice": 5.98,
      "vatRate": "A"
    }
  ],
  "summary": {
    "totalBeforeDiscount": 156.78,
    "totalDiscount": 23.45,
    "totalAfterDiscount": 133.33
  },
  "paymentMethod": "KARTA"
}
```

### Schema bazy danych (SQLite)

```sql
-- Tabela paragonów
CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_number TEXT UNIQUE,
    shop_address TEXT,
    date DATE NOT NULL,
    time TIME NOT NULL,
    datetime DATETIME NOT NULL,
    day_of_week INTEGER,
    hour INTEGER,
    total_before_discount REAL,
    total_discount REAL,
    total_after_discount REAL,
    payment_method TEXT,
    file_hash TEXT,  -- NOWE: SHA256 hash pliku źródłowego
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_json TEXT
);

-- Tabela pozycji
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    name_normalized TEXT,
    quantity REAL,
    unit TEXT,
    price_per_unit REAL,
    total_price REAL,
    discount REAL DEFAULT 0,
    final_price REAL,
    vat_rate TEXT,
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);

-- NOWE: Tabela hashów plików (deduplikacja globalna)
CREATE TABLE file_hashes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_hash TEXT UNIQUE NOT NULL,
    original_filename TEXT,
    file_size INTEGER,
    receipt_count INTEGER,  -- ile paragonów w pliku
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- NOWE: Tabela waitlisty
CREATE TABLE waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    source TEXT DEFAULT 'dashboard',  -- skąd się zapisał
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_hash TEXT  -- zhashowane IP dla anty-spam
);

-- NOWE: Tabela surowych produktów (dla przyszłego AI)
CREATE TABLE raw_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_original TEXT NOT NULL,
    name_normalized TEXT,
    occurrence_count INTEGER DEFAULT 1,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name_normalized)
);

-- Indeksy
CREATE INDEX idx_receipts_date ON receipts(date);
CREATE INDEX idx_receipts_hash ON receipts(file_hash);
CREATE INDEX idx_items_name ON items(name_normalized);
CREATE INDEX idx_file_hashes_hash ON file_hashes(file_hash);
CREATE INDEX idx_raw_products_name ON raw_products(name_normalized);
```

---

## 6. Deduplikacja plików

### Strategia

1. **Przy uploadzie pliku:**
   - Oblicz SHA256 hash całego pliku
   - Sprawdź czy hash istnieje w `file_hashes`
   - Jeśli TAK → pomiń plik, zwróć info "duplikat"
   - Jeśli NIE → przetwórz i zapisz hash

2. **Dodatkowa warstwa:**
   - Sprawdź `receipt_number` w tabeli `receipts`
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

def store_raw_file(content: bytes, file_hash: str, storage_path: Path):
    """Store raw JSON file for future AI training."""
    file_path = storage_path / f"{file_hash}.json"
    if not file_path.exists():
        file_path.write_bytes(content)
```

---

## 7. API Endpoints

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
  "files_skipped_duplicate": 1,
  "receipts_failed": 2,
  "errors": ["plik_3.json: Brak pola 'date'"],
  "new_products_found": 23
}
```

### Statistics (bez zmian)

### Export (NOWE)

```
GET /api/export/xlsx
GET /api/export/csv

Query params:
  - date_from, date_to (opcjonalne)

Response:
  - Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  - Content-Disposition: attachment; filename="paragonstats_export_2024.xlsx"
```

### Waitlist (NOWE)

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

Response 409 (duplicate):
{
  "success": false,
  "message": "Ten email jest już na liście."
}
```

---

## 8. UI/UX Updates

### Dashboard z Email + BuyCoffee

```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 PARAGONSTATS - Twój Dashboard                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 📧 Zostaw email - powiadomimy Cię o nowych funkcjach!       │   │
│  │ [          twoj@email.pl          ] [Zapisz się]            │   │
│  │                                      ✓ Zapisano!            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │ 15 234 zł│ │ 1 876 zł │ │   156    │ │  97.65 zł│              │
│  │ Wydano   │ │Zaoszczędz│ │  Wizyt   │ │ Średnia  │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
│                                                                     │
│  ... (reszta dashboardu) ...                                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  📥 EKSPORTUJ DANE                                          │   │
│  │  [📗 Pobierz Excel]  [📄 Pobierz CSV]                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ☕ Podoba Ci się ParagonStats?                              │   │
│  │  Wesprzyj rozwój aplikacji!                                 │   │
│  │            [☕ Postaw kawę na BuyCoffee.to]                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Upload z Consent

```
┌─────────────────────────────────────────────────────────────────────┐
│  🛒 PARAGONSTATS - Upload paragonów                                 │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │     📤 Przeciągnij pliki JSON tutaj                        │   │
│  │        lub kliknij aby wybrać                               │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ☑️ Akceptuję Regulamin i Politykę Prywatności                     │
│     Rozumiem, że moje dane będą przetwarzane zgodnie z             │
│     regulaminem. [Czytaj więcej]                                   │
│                                                                     │
│  [🚀 Przetwórz paragony]                                           │
│                                                                     │
│  Wynik: ✅ 45 paragonów | ⏭️ 3 duplikaty | ❌ 2 błędy              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 9. Success Metrics (MVP)

### Techniczne
- [ ] Upload 100 paragonów < 10 sekund
- [ ] Deduplikacja działa (0 duplikatów w bazie)
- [ ] Eksport Excel/CSV generuje się < 5 sekund
- [ ] Test coverage > 70%

### Produktowe
- [ ] 10+ emaili na waitliście (po pierwszych testach)
- [ ] 1+ kawa na BuyCoffee (walidacja modelu)
- [ ] 1000+ unikalnych produktów w bazie `raw_products`

### Edukacyjne
- [ ] Działający fullstack (FastAPI + Streamlit)
- [ ] Obsługa plików binarnych (Excel)
- [ ] Asynchroniczne formularze

---

## 10. Legal Requirements

### Wymagane dokumenty
1. **Polityka Prywatności** - osobny plik `PRIVACY_POLICY.md`
2. **Regulamin** - osobny plik `TERMS_OF_SERVICE.md`

### Checkbox consent (wymagany przed uploadem)
```
☑️ Akceptuję Regulamin i Politykę Prywatności. Rozumiem, że:
   - Moje dane z paragonów będą przetwarzane w celu analizy
   - Zanonimizowane dane produktów mogą być wykorzystane do 
     ulepszenia algorytmów kategoryzacji
   - Mogę zażądać usunięcia moich danych w każdej chwili
```

---

## 11. Open Questions

1. **Format JSON** - Jaka jest rzeczywista struktura?
2. **BuyCoffee URL** - Jaki jest Twój link do profilu?
3. **Storage** - Czy na MVP filesystem wystarczy, czy od razu S3/R2?
4. **RODO** - Czy potrzebujesz DPO? (przy >5000 użytkowników)

---

## Changelog

| Data | Wersja | Zmiany |
|------|--------|--------|
| 2025-01-14 | 0.1 | Initial MVP PRD |
| 2025-01-17 | 0.2 | Dodano: deduplikację, waitlistę, eksport, BuyCoffee, legal |
