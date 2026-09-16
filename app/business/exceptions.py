"""
Business tier: exceptions used to propagate errors cleanly across tiers.
The presentation tier catches these and maps them to appropriate responses.
"""


class ValidationError(Exception):
    """Raised when input data violates a business rule."""


class NotFoundError(Exception):
    """Raised when a requested book does not exist."""


class BusinessRuleError(Exception):
    """Raised when an operation violates a business rule (e.g. checkout with 0 quantity)."""
