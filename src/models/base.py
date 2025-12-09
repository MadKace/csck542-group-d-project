"""Base model class for all domain entities."""

import sqlite3
from dataclasses import dataclass
from datetime import date
from typing import Any, TypeVar

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """Base class for all domain model entities."""

    @classmethod
    def from_row(cls: type[T], row: sqlite3.Row | dict[str, Any]) -> T:
        """Create a model instance from a database row."""
        if isinstance(row, sqlite3.Row):
            data = dict(row)
        else:
            data = row

        field_names = set(cls.__dataclass_fields__.keys())
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        return cls(**filtered_data)

    def to_dict(self) -> dict[str, Any]:
        """Convert the model to a dictionary."""
        result = {}
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if isinstance(value, date):
                result[field_name] = value.isoformat()
            else:
                result[field_name] = value
        return result
