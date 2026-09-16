"""FastAPI application factory and dependency wiring."""

from fastapi import FastAPI

from app.business.book_service import BookService
from app.data.repository import BookRepository
from app.data.sqlite_repository import SqliteBookRepository
from app.presentation.routes import books_router, register_exception_handlers


def create_app(repository: BookRepository | None = None, db_path: str = "library.db") -> FastAPI:
    app = FastAPI(title="Book Manager API", version="1.0.0")
    app.state.book_service = BookService(
        repository or SqliteBookRepository(db_path)
    )
    app.include_router(books_router)
    register_exception_handlers(app)
    return app


app = create_app()
