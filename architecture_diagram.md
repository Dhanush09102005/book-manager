# Book Manager Architecture

```text
Client
  |
  v
FastAPI presentation tier (app/presentation)
  |  parses HTTP requests and maps errors to responses
  v
BookService business tier (app/business)
  |  validates input and applies checkout rules
  v
BookRepository interface (app/data/repository.py)
  |
  +--> SqliteBookRepository (production SQLite)
  +--> InMemoryBookRepository (unit tests)
```

The business tier does not import FastAPI or SQLite. The SQLite repository creates
the `books` table if it does not exist and uses parameterized SQL for all values.
