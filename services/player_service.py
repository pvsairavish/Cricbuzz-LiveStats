"""
Cricbuzz LiveStats — Player Service
------------------------------------
Encapsulates business logic for retrieving player statistics, career records,
leaderboards, and API search integration.
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

from api.cricbuzz_api import api_client, CricbuzzAPIClient
from utils.db_connection import execute_query, execute_query_dicts

logger = logging.getLogger(__name__)


class PlayerService:
    """
    Service layer providing player statistics and leaderboards.
    """

    def __init__(self, client: Optional[CricbuzzAPIClient] = None):
        self.client = client or api_client

    def get_top_run_scorers(self, format_type: str = "ODI", limit: int = 10) -> pd.DataFrame:
        """
        Retrieves top run scorers for a given format from the database.
        """
        sql = """
            SELECT 
                p.player_id,
                p.full_name AS player_name,
                p.country,
                p.playing_role,
                COUNT(b.stat_id) AS innings_played,
                SUM(b.runs_scored) AS total_runs,
                MAX(b.runs_scored) AS highest_score,
                ROUND(AVG(b.runs_scored), 2) AS batting_average,
                ROUND(
                    CASE WHEN SUM(b.balls_faced) > 0 
                         THEN (CAST(SUM(b.runs_scored) AS REAL) / SUM(b.balls_faced)) * 100.0 
                         ELSE 0.0 END, 2
                ) AS career_strike_rate,
                SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries,
                SUM(CASE WHEN b.runs_scored >= 50 AND b.runs_scored < 100 THEN 1 ELSE 0 END) AS fifties
            FROM players p
            JOIN batting_stats b ON p.player_id = b.player_id
            WHERE (? = 'ALL' OR b.format = ?)
            GROUP BY p.player_id, p.full_name, p.country, p.playing_role
            ORDER BY total_runs DESC
            LIMIT ?;
        """
        return execute_query(sql, (format_type, format_type, limit))

    def get_top_wicket_takers(self, format_type: str = "ODI", limit: int = 10) -> pd.DataFrame:
        """
        Retrieves top wicket takers for a given format from the database.
        """
        sql = """
            SELECT 
                p.player_id,
                p.full_name AS player_name,
                p.country,
                p.bowling_style,
                COUNT(bw.stat_id) AS matches_bowled,
                ROUND(SUM(bw.overs_bowled), 1) AS total_overs,
                SUM(bw.maidens) AS total_maidens,
                SUM(bw.runs_conceded) AS runs_conceded,
                SUM(bw.wickets_taken) AS total_wickets,
                ROUND(
                    CASE WHEN SUM(bw.wickets_taken) > 0 
                         THEN CAST(SUM(bw.runs_conceded) AS REAL) / SUM(bw.wickets_taken) 
                         ELSE 0.0 END, 2
                ) AS bowling_average,
                ROUND(
                    CASE WHEN SUM(bw.overs_bowled) > 0 
                         THEN CAST(SUM(bw.runs_conceded) AS REAL) / SUM(bw.overs_bowled) 
                         ELSE 0.0 END, 2
                ) AS economy_rate
            FROM players p
            JOIN bowling_stats bw ON p.player_id = bw.player_id
            WHERE (? = 'ALL' OR bw.format = ?)
            GROUP BY p.player_id, p.full_name, p.country, p.bowling_style
            ORDER BY total_wickets DESC
            LIMIT ?;
        """
        return execute_query(sql, (format_type, format_type, limit))

    def get_all_players(self, country: Optional[str] = None, role: Optional[str] = None) -> pd.DataFrame:
        """
        Lists players with optional filtering by country or role.
        """
        filters = []
        params = []
        if country and country != "All":
            filters.append("p.country = ?")
            params.append(country)
        if role and role != "All":
            filters.append("p.playing_role = ?")
            params.append(role)

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
            ORDER BY p.full_name ASC;
        """
        return execute_query(sql, tuple(params) if params else None)

    def search_players(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches players locally in SQLite, with Cricbuzz API search as fallback/enrichment.
        """
        sql = """
            SELECT player_id, full_name, country, playing_role, batting_style, bowling_style
            FROM players
            WHERE full_name LIKE ?
            LIMIT 10;
        """
        local_results = execute_query_dicts(sql, (f"%{query}%",))
        if local_results:
            return local_results

        # Search via API
        api_res = self.client.search_player(query)
        players = api_res.get("player", [])
        return [
            {
                "player_id": p.get("id"),
                "full_name": p.get("name"),
                "country": p.get("teamName", "International"),
                "playing_role": "Player",
                "batting_style": "N/A",
                "bowling_style": "N/A"
            }
            for p in players
        ]

    def get_player_career_summary(self, player_id: int) -> Dict[str, Any]:
        """
        Aggregates player performance statistics across Test, ODI, and T20I formats.
        """
        player_info = execute_query_dicts(
            "SELECT * FROM players WHERE player_id = ?;", (player_id,)
        )
        if not player_info:
            return {}

        player = player_info[0]

        batting_df = execute_query(
            """
            SELECT 
                format,
                COUNT(stat_id) AS innings,
                SUM(runs_scored) AS runs,
                MAX(runs_scored) AS high_score,
                ROUND(AVG(runs_scored), 2) AS average,
                SUM(CASE WHEN runs_scored >= 100 THEN 1 ELSE 0 END) AS hundreds,
                SUM(CASE WHEN runs_scored >= 50 AND runs_scored < 100 THEN 1 ELSE 0 END) AS fifties
            FROM batting_stats
            WHERE player_id = ?
            GROUP BY format;
            """,
            (player_id,)
        )

        bowling_df = execute_query(
            """
            SELECT 
                format,
                COUNT(stat_id) AS matches_bowled,
                ROUND(SUM(overs_bowled), 1) AS overs,
                SUM(wickets_taken) AS wickets,
                ROUND(AVG(economy_rate), 2) AS avg_economy,
                MAX(wickets_taken) AS best_wickets
            FROM bowling_stats
            WHERE player_id = ?
            GROUP BY format;
            """,
            (player_id,)
        )

        return {
            "profile": player,
            "batting": batting_df.to_dict(orient="records"),
            "bowling": bowling_df.to_dict(orient="records")
        }


# Singleton player service
player_service = PlayerService()
