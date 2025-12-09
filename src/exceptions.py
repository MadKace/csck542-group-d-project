"""Custom exceptions for the University Record Management System.

All exceptions inherit from UniversityDBError, allowing consumers to
catch all application-specific errors with a single except clause.

Example:
    from src.exceptions import EntityNotFoundError

    try:
        student = repository.get_by_id(999)
    except EntityNotFoundError as e:
        print(f"Student not found: {e}")
"""


class UniversityDBError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str = "An error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class DatabaseError(UniversityDBError):
    """Raised for database connection or query errors.

    Wraps the original database exception if one was caught.
    """

    def __init__(
        self,
        message: str = "Database error occurred",
        original_error: Exception | None = None,
    ) -> None:
        self.original_error = original_error
        super().__init__(message)


class EntityNotFoundError(UniversityDBError):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity_type: str, entity_id: int) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} with ID {entity_id} not found"
        super().__init__(message)


class ValidationError(UniversityDBError):
    """Raised when data validation fails."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        full_message = f"Validation error for '{field}': {message}"
        super().__init__(full_message)


class ConfigurationError(UniversityDBError):
    """Raised for configuration-related errors."""

    def __init__(self, message: str = "Configuration error") -> None:
        super().__init__(message)
