"""
Swap test: proves BookService (business tier) behaves identically
regardless of which concrete data implementation it's given, with
zero changes to BookService itself.

Run with: python swap_test.py
"""
import os
import tempfile

from app.business.book_service import BookService
from app.data.memory_repository import InMemoryBookRepository
from app.data.sqlite_repository import SqliteBookRepository


def run_scenario(repo, label: str):
    service = BookService(repo)

    book = service.add_book(
        title="The Pragmatic Programmer",
        author="Andrew Hunt",
        year=1999,
        isbn="9780135957059",
        quantity=1,
    )
    assert book.id is not None

    fetched = service.get_book(book.id)
    assert fetched.title == "The Pragmatic Programmer"

    checked_out = service.checkout_book(book.id)
    assert checked_out.quantity == 0

    try:
        service.checkout_book(book.id)
        raise AssertionError("Expected BusinessRuleError on zero-quantity checkout")
    except Exception as e:
        assert type(e).__name__ == "BusinessRuleError"

    results = service.search_books("pragmatic")
    assert len(results) == 1

    service.delete_book(book.id)

    print(f"[{label}] All operations behaved identically. ✔")


if __name__ == "__main__":
    # 1. In-memory repository
    run_scenario(InMemoryBookRepository(), "InMemoryBookRepository")

    # 2. SQLite repository (temp file, cleaned up afterwards)
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        run_scenario(SqliteBookRepository(path), "SqliteBookRepository")
    finally:
        os.remove(path)

    print("\nSame BookService code, two different data sources, identical behavior.")
