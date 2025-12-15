"""SQLAlchemy engine and session management."""

import base64
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import get_settings


_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def _get_fernet(key: str) -> Fernet:
    """Derive a Fernet key from a password string."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"university-db", iterations=100000)
    return Fernet(base64.urlsafe_b64encode(kdf.derive(key.encode())))


def decrypt_database() -> None:
    """Handle database encryption state on startup.

    - If .enc exists: decrypt it (delete stale .db first if present)
    - If only .db exists with encryption key: encrypt it now, then decrypt for use
    """
    settings = get_settings()
    db_path = settings.database_path
    encrypted_path = Path(str(db_path) + ".enc")

    # Case 1: Both files exist - previous shutdown failed to delete .db
    if encrypted_path.exists() and db_path.exists() and settings.encryption_key:
        db_path.unlink()

    # Case 2: Only .db exists with encryption key - encrypt it first
    if db_path.exists() and not encrypted_path.exists() and settings.encryption_key:
        fernet = _get_fernet(settings.encryption_key)
        decrypted_data = db_path.read_bytes()
        encrypted_data = fernet.encrypt(decrypted_data)
        encrypted_path.write_bytes(encrypted_data)
        db_path.unlink()

    # Case 3: Encrypted file exists - decrypt for use
    if encrypted_path.exists() and settings.encryption_key:
        fernet = _get_fernet(settings.encryption_key)
        encrypted_data = encrypted_path.read_bytes()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception:
            raise SystemExit("Failed to decrypt database. Wrong DB_ENCRYPTION_KEY?")
        db_path.write_bytes(decrypted_data)


def encrypt_database() -> None:
    """Encrypt the database file for storage at rest."""
    global _engine, _session_factory

    # Dispose of engine to release file locks
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _session_factory = None

    settings = get_settings()
    db_path = settings.database_path
    encrypted_path = Path(str(db_path) + ".enc")

    if db_path.exists() and settings.encryption_key:
        fernet = _get_fernet(settings.encryption_key)
        decrypted_data = db_path.read_bytes()
        encrypted_data = fernet.encrypt(decrypted_data)
        encrypted_path.write_bytes(encrypted_data)
        # Try to delete, but it's fine if it fails - cleaned up on next start
        try:
            db_path.unlink()
        except PermissionError:
            pass


def _configure_connection(dbapi_conn, connection_record) -> None:  # noqa: ANN001
    """Configure SQLite connection (foreign keys)."""
    settings = get_settings()
    cursor = dbapi_conn.cursor()
    if settings.foreign_keys_enabled:
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
        event.listen(_engine, "connect", _configure_connection)

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
