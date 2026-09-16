"""
Data tier: raw SQLite connection/schema setup only.
No validation logic. No knowledge of how data will be displayed.
"""
import sqlite3


def get_connection(db_path: str = "library.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            isbn TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
    )
    conn.commit()
