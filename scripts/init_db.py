"""Initialise the database with schema and seed data."""

import sqlite3
from pathlib import Path


def main() -> None:
    """Create the database from schema and seed data."""
    project_root = Path(__file__).parent.parent
    db_path = project_root / "database" / "university.db"
    schema_path = project_root / "database" / "schema.sql"
    seed_path = project_root / "database" / "seed_data.sql"

    # Ensure database directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing database
    if db_path.exists():
        db_path.unlink()
        print(f"Removed existing database: {db_path}")

    # Create new database
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    # Load and execute schema
    print(f"Loading schema from: {schema_path}")
    schema_sql = schema_path.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    print("Schema created successfully")

    # Load and execute seed data
    print(f"Loading seed data from: {seed_path}")
    seed_sql = seed_path.read_text(encoding="utf-8")
    conn.executescript(seed_sql)
    print("Seed data inserted successfully")

    conn.close()
    print(f"\nDatabase created at: {db_path}")


if __name__ == "__main__":
    main()
