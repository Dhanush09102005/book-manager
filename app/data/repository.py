"""
Data tier: repository abstraction.

The business tier depends on this interface, not on any concrete
data implementation (SQLite, in-memory, etc.). This is what allows the
data source to be swapped without changing business logic.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.data.models import Book


class BookRepository(ABC):
    """Interface every concrete data-access implementation must satisfy."""

    @abstractmethod
    def add(self, book: Book) -> Book:
        """Persist a new book and return it with its assigned id."""
        raise NotImplementedError

    @abstractmethod
    def get(self, book_id: int) -> Optional[Book]:
        """Return a single book by id, or None if it doesn't exist."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Book]:
        """Return every book."""
        raise NotImplementedError

    @abstractmethod
    def update(self, book: Book) -> Optional[Book]:
        """Overwrite an existing book. Returns None if it doesn't exist."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """Delete a book by id. Returns True if it existed and was deleted."""
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> List[Book]:
        """Return books whose title or author contains the query (case-insensitive)."""
        raise NotImplementedError
