from typing import List, Optional, Dict
from app.data.models import Book
from app.data.repository import BookRepository


class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self._books: Dict[int, Book] = {}
        self._next_id = 1

    def add(self, book: Book) -> Book:
        book.id = self._next_id
        self._books[self._next_id] = book
        self._next_id += 1
        return book

    def get(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)

    def get_all(self) -> List[Book]:
        return list(self._books.values())

    def update(self, book: Book) -> Optional[Book]:
        if book.id not in self._books:
            return None
        self._books[book.id] = book
        return book

    def delete(self, book_id: int) -> bool:
        return self._books.pop(book_id, None) is not None

    def search(self, query: str) -> List[Book]:
        q = query.lower()
        return [
            b for b in self._books.values()
            if q in b.title.lower() or q in b.author.lower()
        ]
