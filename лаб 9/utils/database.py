import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any

_IN_MEMORY_DB: sqlite3.Connection = None


def get_db() -> sqlite3.Connection:
    """Возвращает глобальное соединение с БД в памяти"""
    global _IN_MEMORY_DB
    # глобальная переменная
    if _IN_MEMORY_DB is None:
        _IN_MEMORY_DB = sqlite3.connect(":memory:", check_same_thread=False)
        _IN_MEMORY_DB.row_factory = sqlite3.Row
        _create_tables(_IN_MEMORY_DB)
    return _IN_MEMORY_DB


def _create_tables(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cbr_id TEXT UNIQUE,
            num_code INTEGER,
            char_code TEXT UNIQUE,
            name TEXT,
            value REAL,
            nominal INTEGER
        )
    """)
    conn.commit()


@contextmanager
def db_cursor():
    conn = get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()


# ========== CRUD функции ==========
def save_currencies_from_cbr(currencies):
    with db_cursor() as cur:
        cur.executemany("""
            INSERT INTO currency 
            (cbr_id, num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(char_code) DO UPDATE SET
                value=excluded.value,
                nominal=excluded.nominal
        """, [(c.id, c.num_code, c.char_code, c.name, c.value, c.nominal) for c in currencies])


def get_all_currencies_from_db() -> List[Dict]:
    with db_cursor() as cur:
        cur.execute("SELECT * FROM currency ORDER BY char_code")
        return [dict(row) for row in cur.fetchall()]


def delete_currency(char_code: str):
    with db_cursor() as cur:
        cur.execute("DELETE FROM currency WHERE char_code = ?", (char_code,))
