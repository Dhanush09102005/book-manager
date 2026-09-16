import datetime
from typing import List

from app.data.models import Book
from app.data.repository import BookRepository
from app.business.exceptions import ValidationError, NotFoundError, BusinessRuleError


class BookService:
    def __init__(self, repository: BookRepository):
        self._repo = repository

    @staticmethod
    def _validate_title(title: str) -> None:
        if not title or not str(title).strip():
            raise ValidationError("Title cannot be empty.")

    @staticmethod
    def _validate_author(author: str) -> None:
        if not author or not str(author).strip():
            raise ValidationError("Author cannot be empty.")

    @staticmethod
    def _validate_year(year) -> None:
        current_year = datetime.date.today().year
        if not isinstance(year, int) or isinstance(year, bool):
            raise ValidationError("Publication year must be an integer.")
        if year > current_year:
            raise ValidationError("Publication year cannot be in the future.")

    @staticmethod
    def _validate_isbn(isbn: str) -> None:
        if not isinstance(isbn, str) or not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValidationError("ISBN must be exactly 10 or 13 digits.")

    @staticmethod
    def _validate_quantity(quantity) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValidationError("Quantity must be an integer.")
        if quantity < 0:
            raise ValidationError("Quantity cannot be negative.")

    def _validate_book(self, title: str, author: str, year: int, isbn: str, quantity: int) -> None:
        self._validate_title(title)
        self._validate_author(author)
        self._validate_year(year)
        self._validate_isbn(isbn)
        self._validate_quantity(quantity)

    def add_book(self, title: str, author: str, year: int, isbn: str, quantity: int) -> Book:
        self._validate_book(title, author, year, isbn, quantity)
        book = Book(title=title.strip(), author=author.strip(), year=year, isbn=isbn, quantity=quantity)
        return self._repo.add(book)

    def get_book(self, book_id: int) -> Book:
        book = self._repo.get(book_id)
        if book is None:
            raise NotFoundError(f"Book with id {book_id} not found.")
        return book

    def get_all_books(self) -> List[Book]:
        return self._repo.get_all()

    def update_book(self, book_id: int, title: str, author: str, year: int, isbn: str, quantity: int) -> Book:
        existing = self._repo.get(book_id)
        if existing is None:
            raise NotFoundError(f"Book with id {book_id} not found.")
        self._validate_book(title, author, year, isbn, quantity)
        updated = Book(id=book_id, title=title.strip(), author=author.strip(), year=year, isbn=isbn, quantity=quantity)
        self._repo.update(updated)
        return updated

    def delete_book(self, book_id: int) -> None:
        if not self._repo.delete(book_id):
            raise NotFoundError(f"Book with id {book_id} not found.")

    def search_books(self, query: str) -> List[Book]:
        if not query or not query.strip():
            raise ValidationError("Search query cannot be empty.")
        return self._repo.search(query.strip())

    def checkout_book(self, book_id: int) -> Book:
        """Checking out a book decrements quantity by 1. Fails cleanly if none available."""
        book = self._repo.get(book_id)
        if book is None:
            raise NotFoundError(f"Book with id {book_id} not found.")
        if book.quantity <= 0:
            raise BusinessRuleError(f"'{book.title}' cannot be checked out: no copies available.")
        book.quantity -= 1
        self._repo.update(book)
        return book
