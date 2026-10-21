# 🌐 Cricbuzz LiveStats — API Reference & Data Contracts

Comprehensive documentation of all external Cricbuzz REST endpoints (via RapidAPI) and internal Service Layer interfaces.

---

## 🔑 RapidAPI Authentication

All requests to Cricbuzz endpoints require authentication headers:

```http
GET /matches/v1/live HTTP/1.1
Host: cricbuzz-cricket.p.rapidapi.com
x-rapidapi-key: YOUR_RAPIDAPI_KEY
x-rapidapi-host: cricbuzz-cricket.p.rapidapi.com
CB-Loc: IN
CB-TZ: +0530
```

---

## 📡 External Cricbuzz Endpoints

### 1. `GET /matches/v1/live`
Fetches all active and live cricket fixtures worldwide.

**Response Structure (excerpt):**
```json
{
  "typeMatches": [
    {
      "matchType": "International",
      "seriesMatches": [
        {
          "seriesAdWrapper": {
            "seriesId": 11595,
            "seriesName": "Australia tour of South Africa, 2026",
            "matches": [
              {
                "matchInfo": {
                  "matchId": 147931,
                  "matchDesc": "2nd Test",
                  "matchFormat": "TEST",
                  "state": "In Progress",
                  "status": "Day 4: 2nd Session",
                  "team1": {"teamName": "Australia", "teamSName": "AUS"},
                  "team2": {"teamName": "South Africa", "teamSName": "SA"},
                  "venueInfo": {"ground": "St George's Park", "city": "Gqeberha"}
                },
                "matchScore": {
                  "team1Score": {"inngs1": {"runs": 285, "wickets": 10, "overs": 92.4}}
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

---

### 2. `GET /matches/v1/recent`
Fetches recently concluded match fixtures with results and margins.

---

### 3. `GET /mcenter/v1/{match_id}/scard`
Fetches complete innings-by-innings scorecard data.

**Response Structure (excerpt):**
```json
{
  "matchHeader": {
    "matchDescription": "Final",
    "status": "India won by 7 runs"
  },
  "scoreCard": [
    {
      "inningsId": 1,
      "batTeamDetails": {"batTeamName": "India"},
      "scoreDetails": {"runs": 176, "wickets": 7, "overs": 20.0},
      "batAuthors": [
        {"name": "Virat Kohli", "runs": 76, "balls": 59, "strikeRate": 128.81}
      ],
      "bowlAuthors": [
        {"name": "Anrich Nortje", "overs": 4.0, "maidens": 0, "runs": 26, "wickets": 2, "economy": 6.50}
      ]
    }
  ]
}
```

---

### 4. `GET /stats/v1/player/search?name={name}`
Searches international cricketers by name.

**Query Parameters:**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `string` | Yes | Player name (e.g. `Kohli`, `Bumrah`) |

---

## ⚙️ Internal Business Services API

### `MatchService` (`services/match_service.py`)
- `get_live_matches() -> List[Dict]`: Returns cleaned list of live match cards.
- `get_recent_matches() -> List[Dict]`: Returns recently concluded matches.
- `get_detailed_scorecard(match_id: int) -> Dict`: Returns full innings batting & bowling breakdown.
- `get_db_matches(limit: int) -> List[Dict]`: Returns match history from local SQLite.

### `PlayerService` (`services/player_service.py`)
- `get_top_run_scorers(format_type: str, limit: int) -> pd.DataFrame`: Batting leaderboards.
- `get_top_wicket_takers(format_type: str, limit: int) -> pd.DataFrame`: Bowling leaderboards.
- `get_player_career_summary(player_id: int) -> Dict`: Multi-format career statistics.

### `CRUDService` (`services/crud_service.py`)
- `create_player(data: Dict) -> int`: Validates and inserts player.
- `update_player(player_id: int, data: Dict) -> bool`: Updates player attributes.
- `delete_player(player_id: int) -> bool`: Removes player and related stats.
- `create_match(data: Dict) -> int`: Creates fixture.
- `update_match(match_id: int, data: Dict) -> bool`: Updates fixture result.

### `AnalyticsService` (`services/analytics_service.py`)
- `execute_analytics_query(query_id: int) -> Tuple[pd.DataFrame, float]`: Runs any of the 25 SQL practice questions and reports execution time in milliseconds.
- `execute_custom_sql(sql: str) -> Tuple[pd.DataFrame, float]`: Safe read-only custom SQL runner.
