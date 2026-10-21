"""
Cricbuzz LiveStats — Data Validation Module
-------------------------------------------
Enforces business domain rules, schema constraints, and format validation
before executing database operations.
"""

from typing import Dict, Any, List, Optional
import re
from datetime import datetime

VALID_PLAYING_ROLES = {"Batsman", "Bowler", "All-rounder", "Wicket-keeper"}
VALID_BATTING_STYLES = {"Right-hand bat", "Left-hand bat"}
VALID_BOWLING_STYLES = {
    "Right-arm fast", "Right-arm medium", "Right-arm offbreak", "Right-arm legbreak",
    "Left-arm fast", "Left-arm medium", "Left-arm orthodox", "Left-arm unorthodox", "None"
}
VALID_FORMATS = {"Test", "ODI", "T20I", "T20"}
VALID_TOSS_DECISIONS = {"bat", "bowl", "field"}
VALID_VICTORY_TYPES = {"runs", "wickets", "tie", "no result"}
VALID_MATCH_STATUS = {"Scheduled", "Live", "Completed", "Abandoned"}


class ValidationError(Exception):
    """Custom exception raised when input validation fails."""
    pass


def validate_player_data(data: Dict[str, Any]) -> None:
    """
    Validates player creation/update fields.
    """
    full_name = str(data.get("full_name", "")).strip()
    if not full_name or len(full_name) < 2:
        raise ValidationError("Player full name must be at least 2 characters long.")

    country = str(data.get("country", "")).strip()
    if not country:
        raise ValidationError("Country is required.")

    role = data.get("playing_role")
    if role not in VALID_PLAYING_ROLES:
        raise ValidationError(f"Invalid playing role: '{role}'. Must be one of {VALID_PLAYING_ROLES}.")

    bat_style = data.get("batting_style")
    if bat_style not in VALID_BATTING_STYLES:
        raise ValidationError(f"Invalid batting style: '{bat_style}'. Must be one of {VALID_BATTING_STYLES}.")

    bowl_style = data.get("bowling_style", "None")
    if bowl_style not in VALID_BOWLING_STYLES:
        raise ValidationError(f"Invalid bowling style: '{bowl_style}'. Must be one of {VALID_BOWLING_STYLES}.")

    dob = data.get("dob")
    if dob:
        try:
            if isinstance(dob, str):
                datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Date of birth must be in YYYY-MM-DD format.")


def validate_match_data(data: Dict[str, Any]) -> None:
    """
    Validates match creation/update fields.
    """
    desc = str(data.get("description", "")).strip()
    if not desc:
        raise ValidationError("Match description is required.")

    fmt = data.get("format")
    if fmt not in VALID_FORMATS:
        raise ValidationError(f"Invalid match format: '{fmt}'. Must be one of {VALID_FORMATS}.")

    team1_id = data.get("team1_id")
    team2_id = data.get("team2_id")
    if not team1_id or not team2_id:
        raise ValidationError("Both Team 1 and Team 2 must be specified.")
    if int(team1_id) == int(team2_id):
        raise ValidationError("Team 1 and Team 2 cannot be the same team.")

    venue_id = data.get("venue_id")
    if not venue_id:
        raise ValidationError("Venue is required.")

    match_date = data.get("match_date")
    if not match_date:
        raise ValidationError("Match date is required.")
    try:
        if isinstance(match_date, str):
            datetime.strptime(match_date, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Match date must be in YYYY-MM-DD format.")

    toss_decision = data.get("toss_decision")
    if toss_decision and toss_decision not in VALID_TOSS_DECISIONS:
        raise ValidationError(f"Invalid toss decision: '{toss_decision}'. Must be one of {VALID_TOSS_DECISIONS}.")

    status = data.get("status", "Scheduled")
    if status not in VALID_MATCH_STATUS:
        raise ValidationError(f"Invalid status: '{status}'. Must be one of {VALID_MATCH_STATUS}.")
