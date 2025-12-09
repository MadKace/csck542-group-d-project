"""Application configuration settings.

Uses the singleton pattern to ensure consistent configuration
throughout the application.

Example:
    from src.config import get_settings

    settings = get_settings()
    print(settings.database_path)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from src.exceptions import ConfigurationError


def _get_default_db_path() -> Path:
    """Return the default database path (database/university.db)."""
    project_root = Path(__file__).parent.parent.parent
    return project_root / "database" / "university.db"


@dataclass
class Settings:
    """Application configuration settings.

    Attributes:
        database_path: Path to the SQLite database file.
        foreign_keys_enabled: Whether to enforce foreign keys.
        echo_sql: Whether to log SQL queries (for debugging).
    """

    database_path: Path = field(default_factory=_get_default_db_path)
    foreign_keys_enabled: bool = True
    echo_sql: bool = False

    _instance: ClassVar["Settings | None"] = None

    @classmethod
    def get_instance(cls) -> "Settings":
        """Get or create the singleton Settings instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def validate(self) -> bool:
        """Validate the configuration settings.

        Returns:
            True if all settings are valid.

        Raises:
            ConfigurationError: If any setting is invalid.
        """
        if not self.database_path.parent.exists():
            raise ConfigurationError(
                f"Database directory does not exist: {self.database_path.parent}"
            )

        if self.database_path.exists():
            if not os.access(self.database_path, os.R_OK):
                raise ConfigurationError(
                    f"Database file is not readable: {self.database_path}"
                )
            if not os.access(self.database_path, os.W_OK):
                raise ConfigurationError(
                    f"Database file is not writable: {self.database_path}"
                )

        return True


def get_settings() -> Settings:
    """Get the application settings singleton."""
    return Settings.get_instance()
