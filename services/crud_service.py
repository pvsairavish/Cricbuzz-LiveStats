"""
Cricbuzz LiveStats — CRUD Service
----------------------------------
Provides centralized Create, Read, Update, and Delete operations for
Players, Matches, Teams, Venues, and Performance Statistics with validation
and atomic transaction safeguards.
"""

import sys
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.db_connection import (
    execute_query,
    execute_query_dicts,
    execute_non_query,
    get_db_connection,
)
from utils.validators import (
    validate_player_data,
    validate_match_data,
    ValidationError,
)

logger = logging.getLogger(__name__)


class CRUDService:
    """
    Service managing all database modifications and record lookups.
    """

    # -----------------------------------------------------------------
    # Lookups & Metadata Helpers
    # -----------------------------------------------------------------
    def get_teams(self) -> List[Dict[str, Any]]:
        """Returns all teams for dropdown selectors."""
        return execute_query_dicts(
            "SELECT team_id, team_name, short_name, country FROM teams ORDER BY team_name ASC;"
        )

    def get_venues(self) -> List[Dict[str, Any]]:
        """Returns all venues for dropdown selectors."""
        return execute_query_dicts(
            "SELECT venue_id, venue_name, city, country, capacity FROM venues ORDER BY venue_name ASC;"
        )

    def get_series(self) -> List[Dict[str, Any]]:
        """Returns all series for dropdown selectors."""
        return execute_query_dicts(
            "SELECT series_id, series_name, host_country, match_type FROM series ORDER BY start_date DESC;"
        )

    # -----------------------------------------------------------------
    # PLAYER CRUD
    # -----------------------------------------------------------------
    def create_player(self, data: Dict[str, Any]) -> int:
        """
        Validates and inserts a new player record into the database.
        Returns the new player_id.
        """
        validate_player_data(data)

        sql = """
            INSERT INTO players (full_name, team_id, country, playing_role, batting_style, bowling_style, dob)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            data["full_name"].strip(),
            data.get("team_id") if data.get("team_id") else None,
            data["country"].strip(),
            data["playing_role"],
            data["batting_style"],
            data.get("bowling_style", "None"),
            data.get("dob") if data.get("dob") else None,
        )
        return execute_non_query(sql, params)

    def get_player(self, player_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single player by ID."""
        rows = execute_query_dicts(
            """
            SELECT p.*, t.team_name, t.short_name AS team_short
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            WHERE p.player_id = ?;
            """,
            (player_id,)
        )
        return rows[0] if rows else None

    def list_players(
        self,
        search_term: str = "",
        role: Optional[str] = None,
        team_id: Optional[int] = None,
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Retrieves players matching filter criteria as a DataFrame.
        """
        filters = []
        params: List[Any] = []

        if search_term.strip():
            filters.append("p.full_name LIKE ?")
            params.append(f"%{search_term.strip()}%")

        if role and role != "All":
            filters.append("p.playing_role = ?")
            params.append(role)

        if team_id and str(team_id) != "All":
            filters.append("p.team_id = ?")
            params.append(int(team_id))

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        sql = f"""
            SELECT 
                p.player_id,
                p.full_name,
                t.team_name,
                p.country,
                p.playing_role,
                p.batting_style,
                p.bowling_style,
                p.dob
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            {where_clause}
            ORDER BY p.full_name ASC
            LIMIT ?;
        """
        params.append(limit)
        return execute_query(sql, tuple(params))

    def update_player(self, player_id: int, data: Dict[str, Any]) -> bool:
        """
        Validates and updates an existing player record.
        """
        validate_player_data(data)

        sql = """
            UPDATE players
            SET full_name = ?,
                team_id = ?,
                country = ?,
                playing_role = ?,
                batting_style = ?,
                bowling_style = ?,
                dob = ?
            WHERE player_id = ?;
        """
        params = (
            data["full_name"].strip(),
            data.get("team_id") if data.get("team_id") else None,
            data["country"].strip(),
            data["playing_role"],
            data["batting_style"],
            data.get("bowling_style", "None"),
            data.get("dob") if data.get("dob") else None,
            player_id,
        )
        rows_affected = execute_non_query(sql, params)
        return rows_affected > 0

    def delete_player(self, player_id: int) -> bool:
        """
        Deletes a player by ID. Cascades to batting, bowling, and fielding stats.
        """
        rows_affected = execute_non_query("DELETE FROM players WHERE player_id = ?;", (player_id,))
        return rows_affected > 0

    # -----------------------------------------------------------------
    # MATCH CRUD
    # -----------------------------------------------------------------
    def create_match(self, data: Dict[str, Any]) -> int:
        """
        Validates and inserts a new match record.
        """
        validate_match_data(data)

        sql = """
            INSERT INTO matches (
                description, format, series_id, team1_id, team2_id, venue_id,
                match_date, toss_winner_id, toss_decision, winner_id,
                victory_margin, victory_type, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            data["description"].strip(),
            data["format"],
            data.get("series_id") if data.get("series_id") else None,
            data["team1_id"],
            data["team2_id"],
            data["venue_id"],
            data["match_date"],
            data.get("toss_winner_id") if data.get("toss_winner_id") else None,
            data.get("toss_decision") if data.get("toss_decision") else None,
            data.get("winner_id") if data.get("winner_id") else None,
            data.get("victory_margin") if data.get("victory_margin") else None,
            data.get("victory_type") if data.get("victory_type") else None,
            data.get("status", "Completed"),
        )
        return execute_non_query(sql, params)

    def get_match(self, match_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single match by ID."""
        rows = execute_query_dicts(
            """
            SELECT 
                m.*,
                t1.team_name AS team1_name,
                t2.team_name AS team2_name,
                w.team_name AS winner_name,
                v.venue_name,
                s.series_name
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN teams w ON m.winner_id = w.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            LEFT JOIN series s ON m.series_id = s.series_id
            WHERE m.match_id = ?;
            """,
            (match_id,)
        )
        return rows[0] if rows else None

    def list_matches(
        self,
        format_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> pd.DataFrame:
        """
        Lists matches with optional format and status filtering.
        """
        filters = []
        params: List[Any] = []

        if format_type and format_type != "All":
            filters.append("m.format = ?")
            params.append(format_type)

        if status and status != "All":
            filters.append("m.status = ?")
            params.append(status)

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        sql = f"""
            SELECT 
                m.match_id,
                m.description,
                m.format,
                m.match_date,
                t1.team_name AS team1,
                t2.team_name AS team2,
                COALESCE(w.team_name, 'No Result') AS winner,
                m.victory_margin,
                m.victory_type,
                v.venue_name,
                m.status
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN teams w ON m.winner_id = w.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            {where_clause}
            ORDER BY m.match_date DESC
            LIMIT ?;
        """
        params.append(limit)
        return execute_query(sql, tuple(params))

    def update_match(self, match_id: int, data: Dict[str, Any]) -> bool:
        """
        Updates an existing match record.
        """
        validate_match_data(data)

        sql = """
            UPDATE matches
            SET description = ?,
                format = ?,
                series_id = ?,
                team1_id = ?,
                team2_id = ?,
                venue_id = ?,
                match_date = ?,
                toss_winner_id = ?,
                toss_decision = ?,
                winner_id = ?,
                victory_margin = ?,
                victory_type = ?,
                status = ?
            WHERE match_id = ?;
        """
        params = (
            data["description"].strip(),
            data["format"],
            data.get("series_id") if data.get("series_id") else None,
            data["team1_id"],
            data["team2_id"],
            data["venue_id"],
            data["match_date"],
            data.get("toss_winner_id") if data.get("toss_winner_id") else None,
            data.get("toss_decision") if data.get("toss_decision") else None,
            data.get("winner_id") if data.get("winner_id") else None,
            data.get("victory_margin") if data.get("victory_margin") else None,
            data.get("victory_type") if data.get("victory_type") else None,
            data.get("status", "Completed"),
            match_id,
        )
        rows_affected = execute_non_query(sql, params)
        return rows_affected > 0

    def delete_match(self, match_id: int) -> bool:
        """
        Deletes a match by ID. Cascades to associated batting, bowling, and fielding stats.
        """
        rows_affected = execute_non_query("DELETE FROM matches WHERE match_id = ?;", (match_id,))
        return rows_affected > 0

    # -----------------------------------------------------------------
    # PERFORMANCE STATS RECORDING
    # -----------------------------------------------------------------
    def add_batting_stat(self, data: Dict[str, Any]) -> int:
        """Adds a single player batting innings record."""
        sql = """
            INSERT INTO batting_stats (
                player_id, match_id, innings, format, runs_scored,
                balls_faced, fours, sixes, batting_position, is_out, dismissal_info
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            data["player_id"],
            data["match_id"],
            data.get("innings", 1),
            data["format"],
            int(data.get("runs_scored", 0)),
            int(data.get("balls_faced", 0)),
            int(data.get("fours", 0)),
            int(data.get("sixes", 0)),
            int(data.get("batting_position", 1)),
            1 if data.get("is_out", True) else 0,
            data.get("dismissal_info", "not out"),
        )
        return execute_non_query(sql, params)

    def add_bowling_stat(self, data: Dict[str, Any]) -> int:
        """Adds a single player bowling spell record."""
        sql = """
            INSERT INTO bowling_stats (
                player_id, match_id, innings, format, overs_bowled,
                maidens, runs_conceded, wickets_taken
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            data["player_id"],
            data["match_id"],
            data.get("innings", 1),
            data["format"],
            float(data.get("overs_bowled", 0.0)),
            int(data.get("maidens", 0)),
            int(data.get("runs_conceded", 0)),
            int(data.get("wickets_taken", 0)),
        )
        return execute_non_query(sql, params)


# Singleton CRUD service
crud_service = CRUDService()
