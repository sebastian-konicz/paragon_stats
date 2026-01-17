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
│   │   └── waitlist.py      # Email waitlist
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── stats.py
│   │   ├── wrapped.py
│   │   ├── exporter.py      # Excel/CSV export
│   │   ├── storage.py       # Raw file storage
│   │   └── deduplication.py # Hash-based dedup
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   ├── stats.py
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
│       ├── __init__.py
│       ├── charts.py
│       ├── metrics.py
│       ├── email_form.py    # Async email form
│       └── buycoffee.py     # BuyCoffee widget
│
├── storage/
│   └── raw_receipts/        # Surowe pliki JSON
│
├── data/
│   └── .gitkeep
│
└── legal/
    ├── privacy_policy.md
    └── terms_of_service.md
```

---

## 📊 Model danych

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
    day_of_week INTEGER,  -- 0=Monday
    hour INTEGER,
    total_before_discount REAL,
    total_discount REAL,
    total_after_discount REAL,
    payment_method TEXT,
    file_hash TEXT,
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
    name_original TEXT NOT NULL,
    name_normalized TEXT UNIQUE,
    occurrence_count INTEGER DEFAULT 1,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
);
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

---

## 🔐 Deduplikacja plików

### Algorytm:

```python
import hashlib

def calculate_file_hash(content: bytes) -> str:
    """SHA256 hash pliku."""
    return hashlib.sha256(content).hexdigest()

def is_duplicate(file_hash: str, db) -> bool:
    """Sprawdź czy plik już był przetworzony."""
    return db.execute(
        "SELECT 1 FROM file_hashes WHERE file_hash = ?", 
        (file_hash,)
    ).fetchone() is not None
```

### Flow:
1. Upload pliku → oblicz hash
2. Sprawdź `file_hashes` → jeśli istnieje, pomiń
3. Sprawdź `receipts.receipt_number` → jeśli istnieje, pomiń
4. Przetwórz i zapisz hash + surowy plik

---

## 📐 Konwencje kodu

### Python
- **Type hints** - ZAWSZE
- **Docstrings** - Google style
- **Nazewnictwo** - snake_case dla funkcji, PascalCase dla klas
- **Formatowanie** - black, isort, ruff

### Przykład:

```python
def save_to_waitlist(
    email: str,
    source: str = "dashboard",
    db_conn: Connection | None = None
) -> bool:
    """
    Zapisz email na waitlistę.
    
    Args:
        email: Adres email użytkownika
        source: Źródło zapisu (dashboard, landing, etc.)
        db_conn: Opcjonalne połączenie do DB
    
    Returns:
        True jeśli zapisano, False jeśli email już istnieje
        
    Raises:
        ValueError: Jeśli email jest nieprawidłowy
    """
    ...
```

### Git commits:
```
feat(waitlist): add email subscription endpoint
fix(export): handle empty receipts gracefully
refactor(parser): extract normalization to separate function
```

---

## 📧 Komponenty UI

### Email Form (bez przeładowania strony):

```python
# frontend/components/email_form.py
import streamlit as st
import requests

def email_signup_form():
    """Formularz email z async submit."""
    
    with st.container():
        st.markdown("### 📧 Bądź na bieżąco!")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            email = st.text_input(
                "Email",
                placeholder="twoj@email.pl",
                label_visibility="collapsed"
            )
        
        with col2:
            submitted = st.button("Zapisz się", type="primary")
        
        if submitted and email:
            # Wywołanie API bez przeładowania
            response = requests.post(
                "http://localhost:8000/api/waitlist",
                json={"email": email, "source": "dashboard"}
            )
            if response.status_code == 200:
                st.success("✅ Zapisano! Powiadomimy Cię o nowościach.")
            elif response.status_code == 409:
                st.info("📬 Ten email jest już na liście.")
            else:
                st.error("❌ Coś poszło nie tak. Spróbuj ponownie.")
```

### BuyCoffee Widget:

```python
# frontend/components/buycoffee.py
import streamlit as st

BUYCOFFEE_URL = "https://buycoffee.to/[TWOJ_PROFIL]"

def buycoffee_widget():
    """Widget do wsparcia projektu."""
    
    st.markdown("---")
    
    with st.container():
        st.markdown("""
        ### ☕ Podoba Ci się ParagonStats?
        
        Jeśli aplikacja była dla Ciebie przydatna, możesz wesprzeć jej rozwój!
        """)
        
        st.link_button(
            "☕ Postaw kawę na BuyCoffee.to",
            BUYCOFFEE_URL,
            type="secondary"
        )
        
        st.caption("Twoje wsparcie pomoże rozwijać nowe funkcje!")
```

---

## 📤 Eksport danych

### Excel (.xlsx):

```python
# backend/services/exporter.py
from openpyxl import Workbook
from io import BytesIO

def export_to_xlsx(receipts: list[dict]) -> BytesIO:
    """Eksportuj paragony do Excel."""
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Paragony"
    
    # Nagłówki
    headers = ["Data", "Godzina", "Produkt", "Ilość", "Cena", "Rabat", "Suma"]
    ws.append(headers)
    
    # Dane
    for receipt in receipts:
        for item in receipt["items"]:
            ws.append([
                receipt["date"],
                receipt["time"],
                item["name"],
                item["quantity"],
                item["price_per_unit"],
                item["discount"],
                item["final_price"]
            ])
    
    # Zapisz do BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output
```

---

## ⚠️ Ważne decyzje

1. **MVP bez autentykacji** - dane w session, prostsze testowanie
2. **Deduplikacja hash-based** - SHA256 całego pliku + receipt_number
3. **Storage surowych plików** - lokalny filesystem, później S3/R2
4. **Waitlista w SQLite** - wystarczy dla MVP
5. **Eksport bez limitów** - MVP nie wymaga płatności

---

## 🚫 Czego NIE robić

- ❌ Autentykacja w MVP
- ❌ Płatności za eksport (na razie)
- ❌ Inne sieci niż Biedronka
- ❌ Scraping paragonów
- ❌ Kategoryzacja AI (post-MVP)

---

## 💡 Wskazówki dla Claude Code

### Dla ADHD-friendly development:
1. **Jeden task na raz** - nie mieszaj featury
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
