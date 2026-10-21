"""
Unit tests for Cricbuzz LiveStats Database Module
-------------------------------------------------
Validates schema integrity, constraints, indexes, CRUD transactions,
and virtual/generated column calculations.
"""

import sys
from pathlib import Path
import sqlite3
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config
from utils.db_connection import (
    get_db_connection,
    execute_query,
    execute_query_dicts,
    execute_non_query,
    init_database,
    get_table_row_counts,
)


@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    """Ensure database is seeded before running tests."""
    init_database(force_recreate=True)
    yield


def test_table_row_counts():
    """Check that all core tables contain populated seed rows."""
    counts = get_table_row_counts()
    assert counts["teams"] >= 6
    assert counts["venues"] >= 10
    assert counts["players"] >= 20
    assert counts["matches"] >= 20
    assert counts["batting_stats"] > 0
    assert counts["bowling_stats"] > 0
    assert counts["fielding_stats"] > 0


def test_foreign_key_enforcement():
    """Verify that foreign key constraints prevent invalid relationship inserts."""
    with pytest.raises(sqlite3.IntegrityError):
        execute_non_query(
            "INSERT INTO matches (description, format, team1_id, team2_id, venue_id, match_date) "
            "VALUES ('Test Match', 'ODI', 9999, 1, 1, '2024-01-01');"
        )


def test_generated_columns_batting():
    """Verify generated column strike_rate computes correctly: (runs / balls) * 100."""
    row = execute_query_dicts(
        "SELECT runs_scored, balls_faced, strike_rate FROM batting_stats WHERE balls_faced = 50 LIMIT 1;"
    )
    if row:
        expected = round((row[0]["runs_scored"] / row[0]["balls_faced"]) * 100.0, 2)
        assert abs(row[0]["strike_rate"] - expected) < 0.01


def test_player_crud_lifecycle():
    """Verify full Create, Read, Update, Delete lifecycle on players table."""
    # 1. Create (Insert)
    player_id = execute_non_query(
        """
        INSERT INTO players (full_name, team_id, country, playing_role, batting_style, bowling_style, dob)
        VALUES ('Test Cricketer', 1, 'India', 'Batsman', 'Right-hand bat', 'None', '2000-01-01');
        """
    )
    assert player_id > 0

    # 2. Read
    players = execute_query_dicts("SELECT * FROM players WHERE player_id = ?;", (player_id,))
    assert len(players) == 1
    assert players[0]["full_name"] == "Test Cricketer"

    # 3. Update
    execute_non_query(
        "UPDATE players SET playing_role = 'All-rounder' WHERE player_id = ?;",
        (player_id,)
    )
    updated = execute_query_dicts("SELECT playing_role FROM players WHERE player_id = ?;", (player_id,))
    assert updated[0]["playing_role"] == "All-rounder"

    # 4. Delete
    execute_non_query("DELETE FROM players WHERE player_id = ?;", (player_id,))
    deleted = execute_query_dicts("SELECT * FROM players WHERE player_id = ?;", (player_id,))
    assert len(deleted) == 0


def test_indexes_exist():
    """Verify that custom performance indexes are registered in SQLite."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%';")
        indexes = {row[0] for row in cursor.fetchall()}

    expected_indexes = {
        "idx_players_country",
        "idx_players_role",
        "idx_matches_date",
        "idx_matches_format",
        "idx_batting_player",
        "idx_bowling_player",
    }
    for idx in expected_indexes:
        assert idx in indexes, f"Index {idx} was not found in database!"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
