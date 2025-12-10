"""SQLAlchemy engine and session management."""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import get_settings


_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def _enable_foreign_keys(dbapi_conn, connection_record) -> None:  # noqa: ANN001
    """Enable foreign key support for SQLite connections."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


def get_engine() -> Engine:
    """Get or create the SQLAlchemy engine singleton."""
    global _engine

    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.database_url,
            echo=settings.echo_sql,
        )

        if settings.foreign_keys_enabled:
            event.listen(_engine, "connect", _enable_foreign_keys)

    return _engine


def get_session_factory() -> sessionmaker[Session]:
    """Get or create the session factory singleton."""
    global _session_factory

    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine())

    return _session_factory


def get_session() -> Session:
    """Create a new database session."""
    return get_session_factory()()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
