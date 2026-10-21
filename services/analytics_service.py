"""
Cricbuzz LiveStats — SQL Analytics Service
-------------------------------------------
Registry and execution engine for all 25 SQL practice questions (Beginner, Intermediate, Advanced).
Loads external .sql files, provides analytical metadata, and executes queries with performance telemetry.
"""

import sys
from pathlib import Path
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.db_connection import execute_query

logger = logging.getLogger(__name__)

SQL_DIR = PROJECT_ROOT / "sql"

QUERY_CATALOG: List[Dict[str, Any]] = [
    # ---------------- Beginner (Q1 - Q8) ----------------
    {
        "id": 1,
        "level": "Beginner",
        "title": "Indian National Team Roster",
        "question": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "concepts": ["SELECT", "WHERE", "ORDER BY"],
        "file": "beginner/q01.sql"
    },
    {
        "id": 2,
        "level": "Beginner",
        "title": "Recent Matches (Last 30 Days)",
        "question": "Show all cricket matches that were played in the last 30 days. Include match description, both team names, venue name with city, and match date. Sort by most recent matches first.",
        "concepts": ["INNER JOIN", "DATE arithmetic", "ORDER BY DESC"],
        "file": "beginner/q02.sql"
    },
    {
        "id": 3,
        "level": "Beginner",
        "title": "Top 10 ODI Run Scorers",
        "question": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display highest run scorer first.",
        "concepts": ["GROUP BY", "SUM", "NULLIF", "LIMIT"],
        "file": "beginner/q03.sql"
    },
    {
        "id": 4,
        "level": "Beginner",
        "title": "Mega Venues (>50k Capacity)",
        "question": "Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.",
        "concepts": ["SELECT", "WHERE filter", "ORDER BY capacity DESC"],
        "file": "beginner/q04.sql"
    },
    {
        "id": 5,
        "level": "Beginner",
        "title": "Total Wins Per Team",
        "question": "Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.",
        "concepts": ["JOIN", "COUNT aggregate", "GROUP BY"],
        "file": "beginner/q05.sql"
    },
    {
        "id": 6,
        "level": "Beginner",
        "title": "Squad Playing Role Breakdown",
        "question": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.",
        "concepts": ["GROUP BY", "COUNT"],
        "file": "beginner/q06.sql"
    },
    {
        "id": 7,
        "level": "Beginner",
        "title": "Highest Batting Score by Format",
        "question": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display format and highest score.",
        "concepts": ["GROUP BY", "MAX aggregate"],
        "file": "beginner/q07.sql"
    },
    {
        "id": 8,
        "level": "Beginner",
        "title": "Series Inaugurated in 2024",
        "question": "Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.",
        "concepts": ["strftime()", "WHERE filtering", "ORDER BY start_date"],
        "file": "beginner/q08.sql"
    },

    # ---------------- Intermediate (Q9 - Q16) ----------------
    {
        "id": 9,
        "level": "Intermediate",
        "title": "All-Rounder Milestone Analysis",
        "question": "Find all-rounder players who have scored significant runs and taken wickets in their career. Display player name, total runs, total wickets, and format.",
        "concepts": ["Common Table Expressions (CTE)", "LEFT JOIN", "HAVING / WHERE"],
        "file": "intermediate/q09.sql"
    },
    {
        "id": 10,
        "level": "Intermediate",
        "title": "Last 20 Completed Matches",
        "question": "Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Display most recent matches first.",
        "concepts": ["Multi-table JOINs", "COALESCE", "LIMIT 20"],
        "file": "intermediate/q10.sql"
    },
    {
        "id": 11,
        "level": "Intermediate",
        "title": "Cross-Format Performance Comparison",
        "question": "Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show their total runs in Test, ODI, and T20I along with overall batting average.",
        "concepts": ["Conditional Aggregation (CASE WHEN)", "HAVING COUNT(DISTINCT) >= 2"],
        "file": "intermediate/q11.sql"
    },
    {
        "id": 12,
        "level": "Intermediate",
        "title": "Home vs Away Win Analysis",
        "question": "Analyze each international team's performance when playing at home versus playing away. Determine home/away based on venue country matching team country. Count wins for each team in both home and away conditions.",
        "concepts": ["CASE WHEN conditional logic", "LEFT JOIN", "Comparative aggregation"],
        "file": "intermediate/q12.sql"
    },
    {
        "id": 13,
        "level": "Intermediate",
        "title": "Century Partnerships (100+ Runs)",
        "question": "Identify batting partnerships where two consecutive batsmen (batting positions next to each other) scored a combined total of 100 or more runs in the same innings. Show both player names, combined partnership runs, and innings.",
        "concepts": ["Self-JOIN on consecutive positions", "Relational arithmetic", "Multi-table Joins"],
        "file": "intermediate/q13.sql"
    },
    {
        "id": 14,
        "level": "Intermediate",
        "title": "Venue Bowling Specialization",
        "question": "Examine bowling performance at different venues. For bowlers who have played at least 2 matches at the same venue, calculate average economy rate, total wickets taken, and matches played. Focus on bowlers with >= 4 overs bowled.",
        "concepts": ["COUNT(DISTINCT)", "HAVING criteria", "GROUP BY multiple keys"],
        "file": "intermediate/q14.sql"
    },
    {
        "id": 15,
        "level": "Intermediate",
        "title": "Clutch Performers in Close Matches",
        "question": "Identify players who perform exceptionally well in close matches (< 50 runs OR < 5 wickets). Calculate average runs scored, total close matches played, and how many close matches team won when they batted.",
        "concepts": ["Compound WHERE conditions", "Conditional SUM", "AVG aggregates"],
        "file": "intermediate/q15.sql"
    },
    {
        "id": 16,
        "level": "Intermediate",
        "title": "Year-Over-Year Batting Trajectory",
        "question": "Track how players' batting performance changes over different years since 2020. Show each player's average runs per match and average strike rate for each year.",
        "concepts": ["strftime('%Y')", "Temporal aggregation", "HAVING COUNT >= 2"],
        "file": "intermediate/q16.sql"
    },

    # ---------------- Advanced (Q17 - Q25) ----------------
    {
        "id": 17,
        "level": "Advanced",
        "title": "Toss Impact & Advantage Analysis",
        "question": "Investigate whether winning the toss gives teams an advantage in winning matches. Calculate percentage of matches won by team winning toss, broken down by toss decision (bat vs bowl/field).",
        "concepts": ["CASE conditional grouping", "Percentage calculations", "COUNT filtering"],
        "file": "advanced/q17.sql"
    },
    {
        "id": 18,
        "level": "Advanced",
        "title": "Most Economical Limited-Overs Bowlers",
        "question": "Find the most economical bowlers in limited-overs cricket (ODI and T20). Calculate overall economy rate and total wickets taken. Filter for min 3 matches and >= 2 overs per match.",
        "concepts": ["Format filtering", "Weighted economy calculation", "HAVING constraints"],
        "file": "advanced/q18.sql"
    },
    {
        "id": 19,
        "level": "Advanced",
        "title": "Batting Consistency via Standard Deviation",
        "question": "Determine which batsmen are most consistent in their scoring. Calculate average runs and standard deviation of runs for each player who faced >= 10 balls per innings since 2022. Lower standard deviation = higher consistency.",
        "concepts": ["Mathematical SQRT variance formulation", "HAVING threshold", "Statistical dispersion"],
        "file": "advanced/q19.sql"
    },
    {
        "id": 20,
        "level": "Advanced",
        "title": "Multi-Format Career Batting Breakdown",
        "question": "Analyze matches played across cricket formats and format-specific batting averages for each player. Show count of Test, ODI, and T20 innings along with respective batting averages.",
        "concepts": ["Multi-pivot CASE aggregations", "NULLIF division safeguard", "Format partitioning"],
        "file": "advanced/q20.sql"
    },
    {
        "id": 21,
        "level": "Advanced",
        "title": "Weighted MVP Performance Ranking System",
        "question": "Comprehensive performance ranking system combining Batting, Bowling, and Fielding points into a weighted composite score and rank players per format.",
        "concepts": ["Window Functions (RANK OVER PARTITION)", "Multiple CTEs", "Composite scoring formula"],
        "file": "advanced/q21.sql"
    },
    {
        "id": 22,
        "level": "Advanced",
        "title": "Head-to-Head Team Rivalry Prediction",
        "question": "Build head-to-head match prediction analysis between pairs of teams: total encounters, wins, win percentages, and average victory margins.",
        "concepts": ["Symmetric pair grouping (LEAST / GREATEST)", "Win-rate calculations", "CTEs"],
        "file": "advanced/q22.sql"
    },
    {
        "id": 23,
        "level": "Advanced",
        "title": "Recent Form & Momentum Index",
        "question": "Analyze recent player form using window functions. Calculate avg runs in last 5 vs last 10 innings, 50+ scores, and categorize into 'Excellent', 'Good', 'Average', or 'Poor Form'.",
        "concepts": ["Window Functions (ROW_NUMBER)", "Rolling temporal recency", "Categorical CASE logic"],
        "file": "advanced/q23.sql"
    },
    {
        "id": 24,
        "level": "Advanced",
        "title": "Batting Partnership Success Evaluation",
        "question": "Study successful batting partnerships for pairs of consecutive batsmen: average stand runs, 50+ stands count, highest stand, and success rate percentage.",
        "concepts": ["Pair permutation normalization", "Self-joins on consecutive positions", "RANK() OVER"],
        "file": "advanced/q24.sql"
    },
    {
        "id": 25,
        "level": "Advanced",
        "title": "Quarterly Performance Evolution Time-Series",
        "question": "Perform a time-series analysis of player performance evolution across quarters using LAG() to identify quarter momentum ('Improving', 'Declining', 'Stable') and career trajectory.",
        "concepts": ["Window Functions (LAG OVER PARTITION)", "Time-series quarter bucketing", "Trajectory classification"],
        "file": "advanced/q25.sql"
    }
]


class AnalyticsService:
    """
    Service managing the catalog and execution of the 25 analytical SQL questions.
    """

    def __init__(self):
        self._catalog = self._load_sql_statements()

    def _load_sql_statements(self) -> List[Dict[str, Any]]:
        """Loads SQL query contents from filesystem into the catalog."""
        catalog = []
        for item in QUERY_CATALOG:
            q = dict(item)
            file_path = SQL_DIR / q["file"]
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    q["sql_query"] = f.read().strip()
            else:
                q["sql_query"] = "-- SQL file not found"
            catalog.append(q)
        return catalog

    def get_all_queries(self, level: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all questions, optionally filtered by difficulty level."""
        if not level or level == "All":
            return self._catalog
        return [q for q in self._catalog if q["level"].lower() == level.lower()]

    def get_query(self, query_id: int) -> Optional[Dict[str, Any]]:
        """Returns metadata and SQL for a specific query ID (1 to 25)."""
        for q in self._catalog:
            if q["id"] == query_id:
                return q
        return None

    def execute_analytics_query(self, query_id: int) -> Tuple[pd.DataFrame, float]:
        """
        Executes a catalog query by ID and returns (DataFrame, execution_time_ms).
        """
        q = self.get_query(query_id)
        if not q:
            raise ValueError(f"Query ID {query_id} not found in catalog.")

        start_time = time.time()
        df = execute_query(q["sql_query"])
        elapsed_ms = round((time.time() - start_time) * 1000.0, 2)
        return df, elapsed_ms

    def execute_custom_sql(self, sql: str) -> Tuple[pd.DataFrame, float]:
        """
        Executes a user-provided SELECT query in a safe read-only sandbox.
        """
        clean_sql = sql.strip()
        # Security check: Read-only SELECT operations only
        disallowed = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "DETACH"]
        for word in disallowed:
            if word in clean_sql.upper().split():
                raise PermissionError(f"Security Alert: '{word}' statements are disallowed in the read-only SQL runner.")

        start_time = time.time()
        df = execute_query(clean_sql)
        elapsed_ms = round((time.time() - start_time) * 1000.0, 2)
        return df, elapsed_ms


# Singleton analytics service
analytics_service = AnalyticsService()
