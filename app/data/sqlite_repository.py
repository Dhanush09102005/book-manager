"""
Data tier: concrete SQLite implementation of BookRepository.
Only reads/writes data. No validation, no business rules.
"""
import sqlite3
from typing import List, Optional
from app.data.models import Book
from app.data.repository import BookRepository
from app.data.db import get_connection, init_db


class SqliteBookRepository(BookRepository):
    def __init__(self, db_path: str = "library.db"):
        self._conn: sqlite3.Connection = get_connection(db_path)
        init_db(self._conn)

    @staticmethod
    def _row_to_book(row: sqlite3.Row) -> Book:
        return Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            year=row["year"],
            isbn=row["isbn"],
            quantity=row["quantity"],
        )

    def add(self, book: Book) -> Book:
        cur = self._conn.execute(
            "INSERT INTO books (title, author, year, isbn, quantity) VALUES (?, ?, ?, ?, ?)",
            (book.title, book.author, book.year, book.isbn, book.quantity),
        )
        self._conn.commit()
        book.id = cur.lastrowid
        return book

    def get(self, book_id: int) -> Optional[Book]:
        row = self._conn.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        return self._row_to_book(row) if row else None

    def get_all(self) -> List[Book]:
        rows = self._conn.execute("SELECT * FROM books").fetchall()
        return [self._row_to_book(r) for r in rows]

    def update(self, book: Book) -> Optional[Book]:
        if book.id is None or self.get(book.id) is None:
            return None
        self._conn.execute(
            "UPDATE books SET title = ?, author = ?, year = ?, isbn = ?, quantity = ? WHERE id = ?",
            (book.title, book.author, book.year, book.isbn, book.quantity, book.id),
        )
        self._conn.commit()
        return book

    def delete(self, book_id: int) -> bool:
        cur = self._conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self._conn.commit()
        return cur.rowcount > 0

    def search(self, query: str) -> List[Book]:
        like = f"%{query.lower()}%"
        rows = self._conn.execute(
            "SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?",
            (like, like),
        ).fetchall()
        return [self._row_to_book(r) for r in rows]

    def close(self) -> None:
        self._conn.close()
