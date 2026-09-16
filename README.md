# Book Manager - FastAPI + SQLite

A small library management API with separate presentation, business, and data tiers.

## Run

```powershell
pip install -r requirements.txt
python run.py
```

The API runs at `http://127.0.0.1:8000` and stores data in `library.db`.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/books` | Add a book |
| GET | `/books` | List all books |
| GET | `/books/search?q=...` | Search by title or author |
| GET | `/books/{id}` | Get one book |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |
| POST | `/books/{id}/checkout` | Check out a copy |

Interactive API documentation is available at `/docs`.

## Tests

```powershell
python -m unittest discover -s tests -v
python swap_test.py
```

The business tier depends only on `BookRepository`. Production uses
`SqliteBookRepository`; tests can use `InMemoryBookRepository` without changing
business logic.

The repository interface keeps database details out of `BookService`. This lets
the same business logic run against SQLite in production and an in-memory
repository in tests, proving that the data source can be swapped without changing
validation or orchestration code.

## Structure

```text
app/presentation/  FastAPI routes and application factory
app/business/      Validation, business rules, and orchestration
app/data/          Models, repository interface, and implementations
tests/              Business-layer tests
run.py             Uvicorn entry point
```
