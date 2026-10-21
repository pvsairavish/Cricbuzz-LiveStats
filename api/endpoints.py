"""
Cricbuzz LiveStats — RapidAPI Endpoint Definitions
---------------------------------------------------
Centralizes endpoint routes and URL builders for the Cricbuzz Cricket API on RapidAPI.
"""

from typing import Dict

# Cricbuzz API versioned routes
MATCHES_LIVE = "/matches/v1/live"
MATCHES_RECENT = "/matches/v1/recent"
MATCHES_UPCOMING = "/matches/v1/upcoming"

MATCH_SCORECARD = "/mcenter/v1/{match_id}/scard"
MATCH_MINI_SCORECARD = "/mcenter/v1/{match_id}/hsc"
MATCH_DETAILS = "/mcenter/v1/{match_id}"

SERIES_INTERNATIONAL = "/series/v1/international"
SERIES_ARCHIVES = "/series/v1/archives"

PLAYER_SEARCH = "/stats/v1/player/search"
PLAYER_CAREER = "/stats/v1/player/{player_id}/career"
PLAYER_INFO = "/stats/v1/player/{player_id}"


def get_headers(api_key: str, api_host: str) -> Dict[str, str]:
    """
    Constructs the necessary HTTP headers required by RapidAPI.
    """
    return {
        "x-rapidapi-key": api_key.strip(),
        "x-rapidapi-host": api_host.strip(),
        "Accept": "application/json",
    }
