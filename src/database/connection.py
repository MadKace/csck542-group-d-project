"""Database connection management module.

Provides a singleton database connection manager for SQLite with
context managers for cursor and transaction handling.

Example:
    from src.database import get_connection

    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
"""

import logging
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

from src.config import get_settings
from src.exceptions import DatabaseError

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Singleton class managing SQLite database connections."""

    _instance: "DatabaseConnection | None" = None
    _connection: sqlite3.Connection | None = None

    def __new__(cls) -> "DatabaseConnection":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialise the database connection if not already connected."""
        if self._connection is None:
            self._connect()

    def _connect(self) -> None:
        """Establish the database connection."""
        settings = get_settings()
        db_path = settings.database_path

        try:
            logger.info("Connecting to database: %s", db_path)
            self._connection = sqlite3.connect(db_path)
            self._connection.row_factory = sqlite3.Row

            if settings.foreign_keys_enabled:
                self._connection.execute("PRAGMA foreign_keys = ON")
                logger.debug("Foreign key enforcement enabled")

        except sqlite3.Error as e:
            logger.error("Failed to connect to database: %s", e)
            raise DatabaseError(
                f"Failed to connect to database: {db_path}",
                original_error=e,
            ) from e

    @property
    def connection(self) -> sqlite3.Connection:
        """Get the underlying SQLite connection."""
        if self._connection is None:
            raise DatabaseError("No database connection available")
        return self._connection

    @contextmanager
    def cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Get a database cursor as a context manager."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            yield cursor
        except sqlite3.Error as e:
            logger.error("Cursor error: %s", e)
            raise DatabaseError("Database cursor error", original_error=e) from e
        finally:
            if cursor is not None:
                cursor.close()

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        """Execute operations within a transaction with auto commit/rollback."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            yield cursor
            self.connection.commit()
            logger.debug("Transaction committed successfully")
        except sqlite3.Error as e:
            self.connection.rollback()
            logger.error("Transaction rolled back: %s", e)
            raise DatabaseError("Transaction failed", original_error=e) from e
        finally:
            if cursor is not None:
                cursor.close()

    def execute(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> list[sqlite3.Row]:
        """Execute a query and return all results."""
        with self.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def execute_one(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> sqlite3.Row | None:
        """Execute a query and return a single result (or None)."""
        with self.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()

    def execute_write(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> int:
        """Execute a write operation (INSERT/UPDATE/DELETE) and return lastrowid."""
        with self.transaction() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.lastrowid or 0

    def execute_delete(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> int:
        """Execute a DELETE operation and return number of rows affected."""
        with self.transaction() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.rowcount

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            logger.info("Closing database connection")
            self._connection.close()
            self._connection = None


def get_connection() -> DatabaseConnection:
    """Get the database connection singleton."""
    return DatabaseConnection()
