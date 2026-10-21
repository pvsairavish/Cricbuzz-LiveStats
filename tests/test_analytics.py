"""
Unit tests for Cricbuzz LiveStats SQL Analytics Service
-------------------------------------------------------
Verifies that all 25 practice queries (Beginner, Intermediate, Advanced)
execute cleanly against SQLite and return valid tabular datasets.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.analytics_service import AnalyticsService
from utils.db_connection import init_database


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """Ensure seeded database exists before running analytics tests."""
    init_database(force_recreate=False)
    yield


@pytest.fixture
def analytics():
    """Provides an AnalyticsService instance."""
    return AnalyticsService()


def test_catalog_completeness(analytics):
    """Verify that all 25 questions are registered and all .sql files are present."""
    all_queries = analytics.get_all_queries()
    assert len(all_queries) == 25, f"Expected 25 queries, found {len(all_queries)}"

    beginner = analytics.get_all_queries(level="Beginner")
    intermediate = analytics.get_all_queries(level="Intermediate")
    advanced = analytics.get_all_queries(level="Advanced")

    assert len(beginner) == 8
    assert len(intermediate) == 8
    assert len(advanced) == 9

    for q in all_queries:
        assert q["sql_query"] != "-- SQL file not found", f"Missing SQL file for Q{q['id']}"
        assert len(q["sql_query"]) > 10


@pytest.mark.parametrize("query_id", range(1, 26))
def test_all_25_queries_execute_successfully(analytics, query_id):
    """Executes each of the 25 SQL queries and validates dataframe return."""
    df, elapsed_ms = analytics.execute_analytics_query(query_id)
    assert isinstance(df, pd.DataFrame), f"Q{query_id} did not return a DataFrame"
    assert not df.empty, f"Q{query_id} returned an empty DataFrame! Check seed data."
    assert elapsed_ms >= 0


def test_custom_sql_security_guard(analytics):
    """Verify that DROP/DELETE/INSERT statements are blocked in read-only runner."""
    with pytest.raises(PermissionError):
        analytics.execute_custom_sql("DROP TABLE players;")

    with pytest.raises(PermissionError):
        analytics.execute_custom_sql("DELETE FROM teams WHERE 1=1;")

    # Valid SELECT should work
    df, _ = analytics.execute_custom_sql("SELECT COUNT(*) AS total_teams FROM teams;")
    assert df["total_teams"].iloc[0] == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
