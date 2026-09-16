"""
Unit tests for BookService (business tier).

These tests use InMemoryBookRepository — a fake data source — so they
never touch a real database. The same tests are re-run in swap_test.py
against SqliteBookRepository to prove the business logic behaves
identically regardless of which data implementation is used.
"""
import datetime
import unittest

from app.business.book_service import BookService
from app.business.exceptions import ValidationError, NotFoundError, BusinessRuleError
from app.data.memory_repository import InMemoryBookRepository


class TestBookService(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryBookRepository()
        self.service = BookService(self.repo)

    def _add_sample_book(self, quantity=3):
        return self.service.add_book(
            title="Clean Code",
            author="Robert C. Martin",
            year=2008,
            isbn="9780132350884",
            quantity=quantity,
        )

    def test_add_book_with_valid_data_succeeds(self):
        book = self._add_sample_book()
        self.assertIsNotNone(book.id)
        self.assertEqual(book.title, "Clean Code")

    def test_add_book_with_empty_title_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self.service.add_book(
                title="   ", author="Someone", year=2020, isbn="1234567890", quantity=1
            )

    def test_add_book_with_empty_author_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self.service.add_book(
                title="Some Title", author="", year=2020, isbn="1234567890", quantity=1
            )

    def test_add_book_with_future_year_raises_validation_error(self):
        future_year = datetime.date.today().year + 1
        with self.assertRaises(ValidationError):
            self.service.add_book(
                title="Future Book", author="Someone", year=future_year,
                isbn="1234567890", quantity=1,
            )

    def test_add_book_with_invalid_isbn_length_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self.service.add_book(
                title="Bad ISBN", author="Someone", year=2020, isbn="12345", quantity=1
            )

    def test_add_book_with_negative_quantity_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self.service.add_book(
                title="Negative Qty", author="Someone", year=2020,
                isbn="1234567890", quantity=-1,
            )

    def test_checkout_book_decrements_quantity(self):
        book = self._add_sample_book(quantity=2)
        updated = self.service.checkout_book(book.id)
        self.assertEqual(updated.quantity, 1)

    def test_checkout_book_with_zero_quantity_raises_business_rule_error(self):
        book = self._add_sample_book(quantity=0)
        with self.assertRaises(BusinessRuleError):
            self.service.checkout_book(book.id)

    def test_get_nonexistent_book_raises_not_found_error(self):
        with self.assertRaises(NotFoundError):
            self.service.get_book(9999)

    def test_delete_book_removes_it(self):
        book = self._add_sample_book()
        self.service.delete_book(book.id)
        with self.assertRaises(NotFoundError):
            self.service.get_book(book.id)

    def test_search_books_finds_by_title(self):
        self._add_sample_book()
        results = self.service.search_books("clean")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Clean Code")


if __name__ == "__main__":
    unittest.main()
