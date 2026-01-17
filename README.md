# 🛒 ParagonStats

Analizuj swoje zakupy w Biedronce w stylu "Spotify Wrapped"!

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 O projekcie

ParagonStats to aplikacja webowa do analizy e-paragonów ze sklepu Biedronka. Uploadujesz pliki JSON i odkrywasz:

- 💰 Ile wydajesz miesięcznie/rocznie
- 🏷️ Ile oszczędzasz na promocjach  
- 🍌 Jakie produkty kupujesz najczęściej
- 📅 Kiedy najczęściej robisz zakupy
- 🎉 Twoje osobiste "Wrapped" - podsumowanie w stylu Spotify
- 📊 Eksport danych do Excel/CSV

## 🚀 Quick Start

### Wymagania

- Python 3.11+
- pip

### Instalacja

```bash
git clone https://github.com/yourusername/paragonstats.git
cd paragonstats

python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### Uruchomienie

```bash
# Terminal 1: Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2: Frontend
streamlit run frontend/app.py
```

Otwórz http://localhost:8501

## 📁 Struktura

```
paragonstats/
├── backend/           # FastAPI backend
│   ├── models/        # Pydantic models
│   ├── services/      # Business logic
│   ├── routes/        # API endpoints
│   └── tests/         # Testy
├── frontend/          # Streamlit frontend
├── storage/           # Surowe pliki JSON
├── data/              # SQLite database
└── legal/             # Regulamin, Polityka prywatności
```

## 🔌 API

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/api/health` | GET | Health check |
| `/api/upload` | POST | Upload paragonów |
| `/api/stats/basic` | GET | Podstawowe statystyki |
| `/api/stats/top-products` | GET | Ranking produktów |
| `/api/stats/time-distribution` | GET | Rozkład czasowy |
| `/api/wrapped` | GET | Wrapped summary |
| `/api/export/xlsx` | GET | Eksport Excel |
| `/api/export/csv` | GET | Eksport CSV |
| `/api/waitlist` | POST | Zapis na waitlistę |

## 📊 Jak uzyskać e-paragony?

1. Zaloguj się na [moja.biedronka.pl](https://moja.biedronka.pl)
2. Przejdź do "Moje paragony"
3. Pobierz paragony w formacie JSON
4. Upload do ParagonStats!

## ☕ Wsparcie

Jeśli podoba Ci się projekt, możesz postawić mi kawę:
[BuyCoffee.to - link do uzupełnienia]

## 📄 Licencja

MIT License

## ⚠️ Disclaimer

Projekt nie jest powiązany z siecią Biedronka ani Jeronimo Martins.

---

Made with ❤️ by Sebastian
