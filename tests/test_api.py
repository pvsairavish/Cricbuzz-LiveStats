"""
Unit tests for Cricbuzz LiveStats API & Services Integration
------------------------------------------------------------
Validates API client requests, mock fallback resiliency, caching,
and service layer data parsing.
"""

import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.cricbuzz_api import CricbuzzAPIClient
from services.match_service import MatchService
from services.player_service import PlayerService


@pytest.fixture
def api_client():
    """Provides an API client instance."""
    return CricbuzzAPIClient()


@pytest.fixture
def match_svc(api_client):
    """Provides a MatchService instance."""
    return MatchService(client=api_client)


@pytest.fixture
def player_svc(api_client):
    """Provides a PlayerService instance."""
    return PlayerService(client=api_client)


def test_api_client_live_matches(api_client):
    """Verify live matches endpoint returns structured data."""
    data = api_client.get_live_matches()
    assert isinstance(data, dict)
    assert "typeMatches" in data


def test_api_client_recent_matches(api_client):
    """Verify recent matches endpoint returns structured data."""
    data = api_client.get_recent_matches()
    assert isinstance(data, dict)
    assert "typeMatches" in data


def test_api_client_match_scorecard(api_client):
    """Verify scorecard endpoint returns matchHeader and scoreCard."""
    card = api_client.get_match_scorecard(90101)
    assert isinstance(card, dict)
    assert "matchHeader" in card
    assert "scoreCard" in card


def test_api_client_caching(api_client):
    """Verify client in-memory cache returns cached data on second call."""
    first = api_client.get_live_matches()
    second = api_client.get_live_matches()
    assert first == second


def test_match_service_parsing(match_svc):
    """Verify MatchService flattens complex API hierarchies into clean match items."""
    live_matches = match_svc.get_live_matches()
    assert isinstance(live_matches, list)
    assert len(live_matches) > 0

    first = live_matches[0]
    assert "match_id" in first
    assert "team1_name" in first
    assert "team2_name" in first
    assert "status" in first


def test_match_service_detailed_scorecard(match_svc):
    """Verify MatchService detailed scorecard extraction."""
    sc = match_svc.get_detailed_scorecard(90101)
    assert sc["match_id"] == 90101
    assert "innings" in sc
    assert len(sc["innings"]) >= 2
    assert "batsmen" in sc["innings"][0]
    assert "bowlers" in sc["innings"][0]


def test_match_service_db_matches(match_svc):
    """Verify MatchService fetches completed matches from SQLite."""
    db_matches = match_svc.get_db_matches(limit=5)
    assert isinstance(db_matches, list)
    assert len(db_matches) > 0
    assert "match_id" in db_matches[0]
    assert "winner_name" in db_matches[0]


def test_player_service_top_scorers(player_svc):
    """Verify PlayerService computes top run scorers leaderboard."""
    df = player_svc.get_top_run_scorers(format_type="ODI", limit=5)
    assert not df.empty
    assert "player_name" in df.columns
    assert "total_runs" in df.columns
    # Ensure descending sort
    assert df["total_runs"].iloc[0] >= df["total_runs"].iloc[-1]


def test_player_service_top_wicket_takers(player_svc):
    """Verify PlayerService computes top wicket takers leaderboard."""
    df = player_svc.get_top_wicket_takers(format_type="ODI", limit=5)
    assert not df.empty
    assert "player_name" in df.columns
    assert "total_wickets" in df.columns


def test_player_service_career_summary(player_svc):
    """Verify PlayerService generates complete career summary for a player."""
    summary = player_svc.get_player_career_summary(1)  # Virat Kohli
    assert "profile" in summary
    assert summary["profile"]["full_name"] == "Virat Kohli"
    assert "batting" in summary
    assert len(summary["batting"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
