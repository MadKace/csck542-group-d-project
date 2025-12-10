"""Base repository providing common database operations using SQLAlchemy."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database import get_session
from src.exceptions import EntityNotFoundError
from src.models.orm.base import Base

T = TypeVar("T", bound=Base)


class BaseORMRepository(ABC, Generic[T]):
    """Abstract base repository for SQLAlchemy ORM operations."""

    def __init__(self, session: Session | None = None) -> None:
        self._session = session or get_session()

    @property
    @abstractmethod
    def model_class(self) -> type[T]:
        """The ORM model class for this repository."""
        pass

    @property
    def _primary_key(self) -> str:
        """Get the primary key column name from the model."""
        return self.model_class.__mapper__.primary_key[0].name

    def get_by_id(self, entity_id: int) -> T:
        """Retrieve an entity by its primary key."""
        entity = self._session.get(self.model_class, entity_id)
        if entity is None:
            raise EntityNotFoundError(self.model_class.__tablename__, entity_id)
        return entity

    def get_all(self) -> list[T]:
        """Retrieve all entities."""
        stmt = select(self.model_class)
        return list(self._session.scalars(stmt).all())

    def exists(self, entity_id: int) -> bool:
        """Check if an entity exists by its primary key."""
        entity = self._session.get(self.model_class, entity_id)
        return entity is not None

    def count(self) -> int:
        """Count the total number of entities."""
        stmt = select(func.count()).select_from(self.model_class)
        return self._session.scalar(stmt) or 0

    def create(self, **kwargs: Any) -> T:
        """Create a new entity and return it."""
        if not kwargs:
            raise ValueError("No fields provided for create")

        entity = self.model_class(**kwargs)
        self._session.add(entity)
        self._session.flush()
        self._session.refresh(entity)
        return entity

    def update(self, entity_id: int, **kwargs: Any) -> T:
        """Update an existing entity and return it."""
        if not kwargs:
            raise ValueError("No fields provided for update")

        entity = self._session.get(self.model_class, entity_id)
        if entity is None:
            raise EntityNotFoundError(self.model_class.__tablename__, entity_id)

        for key, value in kwargs.items():
            setattr(entity, key, value)

        self._session.flush()
        self._session.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        """Delete an entity by its primary key."""
        entity = self._session.get(self.model_class, entity_id)
        if entity is None:
            return False

        self._session.delete(entity)
        self._session.flush()
        return True

    def commit(self) -> None:
        """Commit the current transaction."""
        self._session.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._session.rollback()
