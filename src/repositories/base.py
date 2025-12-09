"""Base repository providing common database operations."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from src.database import get_connection
from src.exceptions import EntityNotFoundError
from src.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository for database operations."""

    def __init__(self) -> None:
        self._connection = get_connection()

    @property
    @abstractmethod
    def table_name(self) -> str:
        """The database table name."""
        pass

    @property
    @abstractmethod
    def model_class(self) -> type[T]:
        """The model class for this repository."""
        pass

    @property
    @abstractmethod
    def primary_key(self) -> str:
        """The primary key column name."""
        pass

    def get_by_id(self, entity_id: int) -> T:
        """Retrieve an entity by its primary key."""
        query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = ?"
        row = self._connection.execute_one(query, (entity_id,))

        if row is None:
            raise EntityNotFoundError(self.table_name, entity_id)

        return self.model_class.from_row(row)

    def get_all(self) -> list[T]:
        """Retrieve all entities from the table."""
        query = f"SELECT * FROM {self.table_name}"
        rows = self._connection.execute(query)
        return [self.model_class.from_row(row) for row in rows]

    def exists(self, entity_id: int) -> bool:
        """Check if an entity exists by its primary key."""
        query = (
            f"SELECT 1 FROM {self.table_name} "
            f"WHERE {self.primary_key} = ? LIMIT 1"
        )
        row = self._connection.execute_one(query, (entity_id,))
        return row is not None

    def count(self) -> int:
        """Count the total number of entities in the table."""
        query = f"SELECT COUNT(*) as cnt FROM {self.table_name}"
        row = self._connection.execute_one(query)
        return row["cnt"] if row else 0

    def _execute_query(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[T]:
        """Execute a query and return model instances."""
        rows = self._connection.execute(query, params)
        return [self.model_class.from_row(row) for row in rows]

    # Method to avoid "result[0] if result else None" kinda stuff
    def _execute_query_one(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> T | None:
        """Execute a query and return a single model instance (or None)."""
        row = self._connection.execute_one(query, params)
        if row is None:
            return None
        return self.model_class.from_row(row)
