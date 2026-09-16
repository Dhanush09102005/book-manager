"""FastAPI HTTP routes for the presentation tier."""
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.business.book_service import BookService
from app.business.exceptions import BusinessRuleError, NotFoundError, ValidationError

books_router = APIRouter()


class BookRequest(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    quantity: int


def _get_service(request: Request) -> BookService:
    return request.app.state.book_service


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def handle_validation_error(request: Request, exc: ValidationError):
        return JSONResponse(status_code=400, content={"error": str(exc)})

    @app.exception_handler(NotFoundError)
    async def handle_not_found_error(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(BusinessRuleError)
    async def handle_business_rule_error(request: Request, exc: BusinessRuleError):
        return JSONResponse(status_code=409, content={"error": str(exc)})


@books_router.post("/books", status_code=201)
def add_book(data: BookRequest, request: Request):
    return _get_service(request).add_book(
        title=data.title, author=data.author, year=data.year,
        isbn=data.isbn, quantity=data.quantity,
    ).to_dict()


@books_router.get("/books")
def get_all_books(request: Request):
    return [book.to_dict() for book in _get_service(request).get_all_books()]


@books_router.get("/books/search")
def search_books(request: Request, q: str = ""):
    return [book.to_dict() for book in _get_service(request).search_books(q)]


@books_router.get("/books/{book_id}")
def get_book(book_id: int, request: Request):
    return _get_service(request).get_book(book_id).to_dict()


@books_router.put("/books/{book_id}")
def update_book(book_id: int, data: BookRequest, request: Request):
    return _get_service(request).update_book(
        book_id=book_id, title=data.title, author=data.author,
        year=data.year, isbn=data.isbn, quantity=data.quantity,
    ).to_dict()


@books_router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, request: Request):
    _get_service(request).delete_book(book_id)
    return None


@books_router.post("/books/{book_id}/checkout")
def checkout_book(book_id: int, request: Request):
    return _get_service(request).checkout_book(book_id).to_dict()
