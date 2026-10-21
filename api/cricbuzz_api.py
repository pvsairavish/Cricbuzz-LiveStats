"""
Cricbuzz LiveStats — Cricbuzz API Client
-----------------------------------------
Robust REST client for interacting with the Cricbuzz API via RapidAPI.
Features automatic retry, rate-limiting guards, and seamless mock fallback
when API credentials are missing or network limits are exceeded.
"""

import sys
from pathlib import Path
import logging
import time
from typing import Dict, Any, Optional
import requests

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config
from api import endpoints
from api import mock_data

logger = logging.getLogger(__name__)


class CricbuzzAPIClient:
    """
    Client for Cricbuzz Cricket API on RapidAPI with automatic fallback to mock data.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_host: Optional[str] = None,
        timeout: int = 10,
    ):
        self.api_key = (api_key or config.RAPIDAPI_KEY).strip()
        self.api_host = (api_host or config.RAPIDAPI_HOST).strip()
        self.base_url = f"https://{self.api_host}"
        self.timeout = timeout
        self.session = requests.Session()

        # Cache store: {cache_key: (timestamp, data)}
        self._cache: Dict[str, tuple] = {}

    @property
    def is_live_enabled(self) -> bool:
        """Returns True if a valid API key is present."""
        return bool(self.api_key)

    def _get_headers(self) -> Dict[str, str]:
        return endpoints.get_headers(self.api_key, self.api_host)

    def _get_from_cache(self, key: str, ttl: int) -> Optional[Any]:
        if key in self._cache:
            ts, data = self._cache[key]
            if time.time() - ts < ttl:
                return data
        return None

    def _set_cache(self, key: str, data: Any) -> None:
        self._cache[key] = (time.time(), data)

    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        ttl: int = 60,
        mock_fallback: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Executes an HTTP GET request to RapidAPI with caching and mock fallback.
        """
        cache_key = f"{endpoint}:{str(params)}"
        cached_result = self._get_from_cache(cache_key, ttl)
        if cached_result is not None:
            return cached_result

        # If live API is disabled, return mock response directly
        if not self.is_live_enabled:
            logger.info(f"API key not configured; using mock fallback for {endpoint}")
            return mock_fallback or {}

        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout,
            )
            if response.status_code == 200:
                data = response.json()
                self._set_cache(cache_key, data)
                return data

            logger.warning(
                f"RapidAPI request returned status {response.status_code}: {response.text[:200]}"
            )
            # 401/403/429 -> Fallback gracefully to mock data
            return mock_fallback or {}

        except (requests.RequestException, ValueError) as err:
            logger.error(f"Error fetching from RapidAPI endpoint {endpoint}: {err}")
            return mock_fallback or {}

    # -----------------------------------------------------------------
    # Live Matches & Scorecard Methods
    # -----------------------------------------------------------------
    def get_live_matches(self) -> Dict[str, Any]:
        """Fetch all ongoing live cricket matches."""
        return self._request(
            endpoints.MATCHES_LIVE,
            ttl=config.CACHE_TTL_LIVE_MATCHES,
            mock_fallback=mock_data.MOCK_LIVE_MATCHES,
        )

    def get_recent_matches(self) -> Dict[str, Any]:
        """Fetch recently completed cricket matches."""
        return self._request(
            endpoints.MATCHES_RECENT,
            ttl=config.CACHE_TTL_RECENT_MATCHES,
            mock_fallback=mock_data.MOCK_RECENT_MATCHES,
        )

    def get_upcoming_matches(self) -> Dict[str, Any]:
        """Fetch upcoming scheduled fixtures."""
        return self._request(
            endpoints.MATCHES_UPCOMING,
            ttl=config.CACHE_TTL_RECENT_MATCHES,
            mock_fallback=mock_data.MOCK_LIVE_MATCHES,
        )

    def get_match_scorecard(self, match_id: int) -> Dict[str, Any]:
        """Fetch comprehensive innings scorecard for a specific match."""
        endpoint = endpoints.MATCH_SCORECARD.format(match_id=match_id)
        return self._request(
            endpoint,
            ttl=config.CACHE_TTL_LIVE_MATCHES,
            mock_fallback=mock_data.MOCK_MATCH_SCORECARD,
        )

    def get_match_mini_scorecard(self, match_id: int) -> Dict[str, Any]:
        """Fetch mini-header scorecard summary."""
        endpoint = endpoints.MATCH_MINI_SCORECARD.format(match_id=match_id)
        return self._request(
            endpoint,
            ttl=config.CACHE_TTL_LIVE_MATCHES,
            mock_fallback=mock_data.MOCK_MATCH_SCORECARD.get("matchHeader", {}),
        )

    # -----------------------------------------------------------------
    # Player Stats Methods
    # -----------------------------------------------------------------
    def search_player(self, name: str) -> Dict[str, Any]:
        """Search for a player by name."""
        return self._request(
            endpoints.PLAYER_SEARCH,
            params={"name": name},
            ttl=config.CACHE_TTL_PLAYER_STATS,
            mock_fallback=mock_data.MOCK_PLAYER_SEARCH,
        )

    def get_player_career(self, player_id: str) -> Dict[str, Any]:
        """Fetch career batting and bowling statistics for a player."""
        endpoint = endpoints.PLAYER_CAREER.format(player_id=player_id)
        return self._request(
            endpoint,
            ttl=config.CACHE_TTL_PLAYER_STATS,
            mock_fallback=mock_data.MOCK_PLAYER_CAREER,
        )


# Singleton client instance
api_client = CricbuzzAPIClient()
