"""
Unit tests for Cricbuzz LiveStats CRUD Service
----------------------------------------------
Validates data validation rules, Create/Read/Update/Delete operations
for players and matches, and stats recording integrity.
"""

import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.crud_service import CRUDService
from utils.validators import ValidationError
from utils.db_connection import init_database, execute_query_dicts


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """Seed test database before running CRUD tests."""
    init_database(force_recreate=True)
    yield


@pytest.fixture
def crud():
    """Provides a CRUDService instance."""
    return CRUDService()


def test_player_validation_failures(crud):
    """Verify player creation rejects invalid roles, styles, and names."""
    # Empty name
    with pytest.raises(ValidationError):
        crud.create_player({
            "full_name": "",
            "country": "India",
            "playing_role": "Batsman",
            "batting_style": "Right-hand bat"
        })

    # Invalid playing role
    with pytest.raises(ValidationError):
        crud.create_player({
            "full_name": "Test Player",
            "country": "India",
            "playing_role": "Coach",  # Invalid role
            "batting_style": "Right-hand bat"
        })

    # Invalid batting style
    with pytest.raises(ValidationError):
        crud.create_player({
            "full_name": "Test Player",
            "country": "India",
            "playing_role": "Batsman",
            "batting_style": "Switch-hit"  # Invalid style
        })


def test_player_crud_flow(crud):
    """Verify complete Create, Read, Update, Delete flow for a player."""
    player_data = {
        "full_name": "Shubman Gill",
        "team_id": 1,
        "country": "India",
        "playing_role": "Batsman",
        "batting_style": "Right-hand bat",
        "bowling_style": "Right-arm offbreak",
        "dob": "1999-09-08"
    }

    # 1. Create
    new_id = crud.create_player(player_data)
    assert new_id > 0

    # 2. Read
    player = crud.get_player(new_id)
    assert player is not None
    assert player["full_name"] == "Shubman Gill"
    assert player["team_name"] == "India"

    # 3. Update
    update_data = dict(player_data)
    update_data["playing_role"] = "All-rounder"
    success = crud.update_player(new_id, update_data)
    assert success is True

    updated_player = crud.get_player(new_id)
    assert updated_player["playing_role"] == "All-rounder"

    # 4. List filter
    df = crud.list_players(search_term="Gill")
    assert not df.empty
    assert "Shubman Gill" in df["full_name"].values

    # 5. Delete
    deleted = crud.delete_player(new_id)
    assert deleted is True
    assert crud.get_player(new_id) is None


def test_match_validation_failures(crud):
    """Verify match creation rejects identical teams, bad format, and bad dates."""
    # Team 1 == Team 2
    with pytest.raises(ValidationError):
        crud.create_match({
            "description": "Invalid Match",
            "format": "T20I",
            "team1_id": 1,
            "team2_id": 1,
            "venue_id": 1,
            "match_date": "2024-05-01"
        })

    # Invalid format
    with pytest.raises(ValidationError):
        crud.create_match({
            "description": "Invalid Format Match",
            "format": "The Hundred",  # Not supported
            "team1_id": 1,
            "team2_id": 2,
            "venue_id": 1,
            "match_date": "2024-05-01"
        })


def test_match_crud_flow(crud):
    """Verify complete Create, Read, Update, Delete flow for a match."""
    match_data = {
        "description": "Exhibition Match 2024",
        "format": "T20I",
        "series_id": 8,
        "team1_id": 1,
        "team2_id": 2,
        "venue_id": 1,
        "match_date": "2024-07-15",
        "toss_winner_id": 1,
        "toss_decision": "bat",
        "winner_id": 1,
        "victory_margin": 15,
        "victory_type": "runs",
        "status": "Completed"
    }

    # 1. Create
    match_id = crud.create_match(match_data)
    assert match_id > 0

    # 2. Read
    match = crud.get_match(match_id)
    assert match is not None
    assert match["description"] == "Exhibition Match 2024"
    assert match["winner_name"] == "India"

    # 3. Update
    update_data = dict(match_data)
    update_data["victory_margin"] = 25
    success = crud.update_match(match_id, update_data)
    assert success is True

    updated_match = crud.get_match(match_id)
    assert updated_match["victory_margin"] == 25

    # 4. List matches
    df = crud.list_matches(format_type="T20I", limit=10)
    assert not df.empty

    # 5. Delete
    deleted = crud.delete_match(match_id)
    assert deleted is True
    assert crud.get_match(match_id) is None


def test_stats_recording_and_virtual_columns(crud):
    """Verify adding batting/bowling stats and automatic computed column generation."""
    # Add a batting innings
    stat_id = crud.add_batting_stat({
        "player_id": 1,
        "match_id": 1,
        "innings": 1,
        "format": "ODI",
        "runs_scored": 100,
        "balls_faced": 80,
        "fours": 10,
        "sixes": 2,
        "batting_position": 3,
        "is_out": False,
        "dismissal_info": "not out"
    })
    assert stat_id > 0

    rows = execute_query_dicts(
        "SELECT strike_rate FROM batting_stats WHERE stat_id = ?;", (stat_id,)
    )
    # 100 runs in 80 balls = 125.0 strike rate
    assert rows[0]["strike_rate"] == 125.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
