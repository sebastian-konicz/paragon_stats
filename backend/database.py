"""SQLite database connection and initialization."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from backend.config import get_settings

SCHEMA_SQL = """
-- Tabela paragonow
CREATE TABLE IF NOT EXISTS receipts (
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
    file_hash TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_json TEXT
);

-- Tabela pozycji
CREATE TABLE IF NOT EXISTS items (
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

-- Deduplikacja plikow
CREATE TABLE IF NOT EXISTS file_hashes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_hash TEXT UNIQUE NOT NULL,
    original_filename TEXT,
    file_size INTEGER,
    receipt_count INTEGER,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Waitlista
CREATE TABLE IF NOT EXISTS waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    source TEXT DEFAULT 'dashboard',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_hash TEXT
);

-- Baza produktow (dla AI)
CREATE TABLE IF NOT EXISTS raw_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_original TEXT NOT NULL,
    name_normalized TEXT UNIQUE,
    occurrence_count INTEGER DEFAULT 1,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indeksy
CREATE INDEX IF NOT EXISTS idx_receipts_date ON receipts(date);
CREATE INDEX IF NOT EXISTS idx_receipts_hash ON receipts(file_hash);
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name_normalized);
CREATE INDEX IF NOT EXISTS idx_items_receipt ON items(receipt_id);
CREATE INDEX IF NOT EXISTS idx_file_hashes_hash ON file_hashes(file_hash);
CREATE INDEX IF NOT EXISTS idx_raw_products_name ON raw_products(name_normalized);
"""


def get_db_path() -> Path:
    """Get database file path from settings."""
    settings = get_settings()
    return settings.db_path


def init_db(db_path: Path | None = None) -> None:
    """
    Initialize database with schema.

    Args:
        db_path: Optional path to database file. Uses settings if not provided.
    """
    if db_path is None:
        db_path = get_db_path()

    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


@contextmanager
def get_connection(db_path: Path | None = None) -> Generator[sqlite3.Connection, None, None]:
    """
    Get database connection as context manager.

    Args:
        db_path: Optional path to database file. Uses settings if not provided.

    Yields:
        SQLite connection with row factory set to sqlite3.Row.
    """
    if db_path is None:
        db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    FastAPI dependency for database connection.

    Yields:
        SQLite connection.
    """
    with get_connection() as conn:
        yield conn
