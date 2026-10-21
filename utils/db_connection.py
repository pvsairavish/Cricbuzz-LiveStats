"""
Cricbuzz LiveStats — Centralized Database Connection Manager
-------------------------------------------------------------
Provides thread-safe connections, transaction management, query execution helpers,
and automated database bootstrapping with schema, indexes, and seed data.
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Generator, List, Dict, Any, Optional
import pandas as pd

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config

logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager yielding a thread-safe SQLite connection with foreign keys enabled
    and Row factory configured for dict-like column access.
    """
    conn = sqlite3.connect(str(config.DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


def execute_query(sql: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Executes a SELECT query and returns the results as a pandas DataFrame.
    """
    with get_db_connection() as conn:
        if params:
            return pd.read_sql_query(sql, conn, params=params)
        return pd.read_sql_query(sql, conn)


def execute_query_dicts(sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Executes a SELECT query and returns the results as a list of dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def execute_non_query(sql: str, params: Optional[tuple] = None) -> int:
    """
    Executes an INSERT, UPDATE, or DELETE query within a transaction.
    Returns the lastrowid (for INSERT) or rowcount (for UPDATE/DELETE).
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount


def execute_script(script_path: Any) -> None:
    """
    Executes an entire multi-statement SQL script file.
    """
    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read()

    with get_db_connection() as conn:
        conn.executescript(script)
        conn.commit()


def init_database(force_recreate: bool = False) -> Dict[str, int]:
    """
    Initializes the database schema, indexes, and seed data.
    If force_recreate is True, removes existing DB and creates everything afresh.
    Returns a dictionary of table names and their row counts.
    """
    if force_recreate and config.DB_PATH.exists():
        logger.info(f"Removing existing database at {config.DB_PATH}")
        config.DB_PATH.unlink()

    # Ensure parent directory exists
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. Execute schema.sql
    logger.info(f"Executing schema from {config.SCHEMA_PATH}")
    execute_script(config.SCHEMA_PATH)

    # 2. Execute indexes.sql
    logger.info(f"Executing indexes from {config.INDEXES_PATH}")
    execute_script(config.INDEXES_PATH)

    # 3. Populate seed data if database was empty or re-created
    counts = get_table_row_counts()
    total_rows = sum(counts.values())

    if force_recreate or total_rows == 0:
        logger.info(f"Loading seed data from {config.SEED_DATA_PATH}")
        execute_script(config.SEED_DATA_PATH)
        counts = get_table_row_counts()

    return counts


def get_table_row_counts() -> Dict[str, int]:
    """
    Returns a mapping of table name to row count for all tables in the database.
    """
    tables = [
        "teams",
        "venues",
        "series",
        "players",
        "matches",
        "batting_stats",
        "bowling_stats",
        "fielding_stats"
    ]
    counts = {}
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for tbl in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
                counts[tbl] = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                counts[tbl] = 0
    return counts


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Bootstrapping Cricbuzz LiveStats Database...")
    result_counts = init_database(force_recreate=True)
    print("\nDatabase Initialized Successfully! Table Row Counts:")
    for table, count in result_counts.items():
        print(f"  • {table:<16}: {count:>4} rows")
