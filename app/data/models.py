"""
Data tier: plain data structure only.
No validation, no business logic, no knowledge of how data is displayed.
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Book:
    title: str
    author: str
    year: int
    isbn: str
    quantity: int
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)
