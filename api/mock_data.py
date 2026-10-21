"""
Cricbuzz LiveStats — High-Fidelity Mock API Responses
------------------------------------------------------
Provides authentic Cricbuzz API response payloads for live matches,
recent results, upcoming fixtures, match scorecards, and player stats.
Used for offline development, tests, or when RapidAPI keys are absent.
"""

from typing import Dict, Any, List

import time

MOCK_LIVE_MATCHES: Dict[str, Any] = {
    "typeMatches": [
        {
            "matchType": "International",
            "seriesMatches": [
                {
                    "seriesAdWrapper": {
                        "seriesId": 8501,
                        "seriesName": "ICC Champions Trophy 2025",
                        "matches": [
                            {
                                "matchInfo": {
                                    "matchId": 90101,
                                    "seriesId": 8501,
                                    "seriesName": "ICC Champions Trophy 2025",
                                    "matchDesc": "Grand Final (Live • Over 19.4)",
                                    "matchFormat": "T20",
                                    "startDate": str(int(time.time() * 1000) - 10800000),
                                    "endDate": str(int(time.time() * 1000) + 3600000),
                                    "state": "In Progress",
                                    "status": "⚡ LIVE • Australia need 5 runs in 2 balls! CRR: 10.57 | RRR: 15.00",
                                    "team1": {
                                        "teamId": 2,
                                        "teamName": "India",
                                        "teamSName": "IND",
                                        "imageId": 172188
                                    },
                                    "team2": {
                                        "teamId": 3,
                                        "teamName": "Australia",
                                        "teamSName": "AUS",
                                        "imageId": 172189
                                    },
                                    "venueInfo": {
                                        "id": 1,
                                        "ground": "Narendra Modi Stadium",
                                        "city": "Ahmedabad",
                                        "timezone": "+05:30"
                                    },
                                    "currBatTeamId": 3
                                },
                                "matchScore": {
                                    "team1Score": {
                                        "inngs1": {
                                            "inningsId": 1,
                                            "runs": 212,
                                            "wickets": 4,
                                            "overs": 20.0
                                        }
                                    },
                                    "team2Score": {
                                        "inngs1": {
                                            "inningsId": 2,
                                            "runs": 208,
                                            "wickets": 7,
                                            "overs": 19.4
                                        }
                                    }
                                }
                            },
                            {
                                "matchInfo": {
                                    "matchId": 90102,
                                    "seriesId": 8501,
                                    "seriesName": "World Test Championship 2025-27",
                                    "matchDesc": "5th Test - Day 4 (Session 3)",
                                    "matchFormat": "TEST",
                                    "startDate": str(int(time.time() * 1000) - 86400000 * 3),
                                    "endDate": str(int(time.time() * 1000) + 86400000 * 2),
                                    "state": "In Progress",
                                    "status": "⚡ LIVE • India lead by 311 runs with 4 wickets in hand",
                                    "team1": {
                                        "teamId": 2,
                                        "teamName": "India",
                                        "teamSName": "IND"
                                    },
                                    "team2": {
                                        "teamId": 1,
                                        "teamName": "England",
                                        "teamSName": "ENG"
                                    },
                                    "venueInfo": {
                                        "id": 204,
                                        "ground": "Lord's Cricket Ground",
                                        "city": "London",
                                        "timezone": "+00:00"
                                    },
                                    "currBatTeamId": 2
                                },
                                "matchScore": {
                                    "team1Score": {
                                        "inngs1": {
                                            "inningsId": 1,
                                            "runs": 345,
                                            "wickets": 10,
                                            "overs": 98.4
                                        },
                                        "inngs2": {
                                            "inningsId": 3,
                                            "runs": 278,
                                            "wickets": 6,
                                            "overs": 82.4
                                        }
                                    },
                                    "team2Score": {
                                        "inngs1": {
                                            "inningsId": 2,
                                            "runs": 312,
                                            "wickets": 10,
                                            "overs": 94.2
                                        }
                                    }
                                }
                            },
                            {
                                "matchInfo": {
                                    "matchId": 90103,
                                    "seriesId": 8502,
                                    "seriesName": "Indian Premier League 2025",
                                    "matchDesc": "Match 24 • High-Scoring Chase",
                                    "matchFormat": "T20",
                                    "startDate": str(int(time.time() * 1000) - 7200000),
                                    "endDate": str(int(time.time() * 1000) + 1800000),
                                    "state": "In Progress",
                                    "status": "⚡ LIVE • CSK need 24 runs in 10 balls! CRR: 10.63 | RRR: 14.40",
                                    "team1": {
                                        "teamId": 5,
                                        "teamName": "Royal Challengers Bengaluru",
                                        "teamSName": "RCB"
                                    },
                                    "team2": {
                                        "teamId": 6,
                                        "teamName": "Chennai Super Kings",
                                        "teamSName": "CSK"
                                    },
                                    "venueInfo": {
                                        "id": 5,
                                        "ground": "M. Chinnaswamy Stadium",
                                        "city": "Bengaluru",
                                        "timezone": "+05:30"
                                    },
                                    "currBatTeamId": 6
                                },
                                "matchScore": {
                                    "team1Score": {
                                        "inngs1": {
                                            "inningsId": 1,
                                            "runs": 218,
                                            "wickets": 5,
                                            "overs": 20.0
                                        }
                                    },
                                    "team2Score": {
                                        "inngs1": {
                                            "inningsId": 2,
                                            "runs": 195,
                                            "wickets": 4,
                                            "overs": 18.2
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}

MOCK_RECENT_MATCHES: Dict[str, Any] = {
    "typeMatches": [
        {
            "matchType": "International",
            "seriesMatches": [
                {
                    "seriesAdWrapper": {
                        "seriesId": 7950,
                        "seriesName": "ICC Men's Cricket World Cup 2023",
                        "matches": [
                            {
                                "matchInfo": {
                                    "matchId": 70350,
                                    "seriesId": 7950,
                                    "seriesName": "ICC Men's Cricket World Cup 2023",
                                    "matchDesc": "Final",
                                    "matchFormat": "ODI",
                                    "startDate": "1700377200000",
                                    "endDate": "1700413200000",
                                    "state": "Complete",
                                    "status": "Australia won by 6 wkts",
                                    "team1": {"teamId": 2, "teamName": "India", "teamSName": "IND"},
                                    "team2": {"teamId": 3, "teamName": "Australia", "teamSName": "AUS"},
                                    "venueInfo": {
                                        "id": 1,
                                        "ground": "Narendra Modi Stadium",
                                        "city": "Ahmedabad"
                                    }
                                },
                                "matchScore": {
                                    "team1Score": {"inngs1": {"runs": 240, "wickets": 10, "overs": 50.0}},
                                    "team2Score": {"inngs1": {"runs": 241, "wickets": 4, "overs": 43.0}}
                                }
                            },
                            {
                                "matchInfo": {
                                    "matchId": 70349,
                                    "seriesId": 7950,
                                    "seriesName": "ICC Men's Cricket World Cup 2023",
                                    "matchDesc": "Semi-Final 1",
                                    "matchFormat": "ODI",
                                    "startDate": "1700031600000",
                                    "endDate": "1700067600000",
                                    "state": "Complete",
                                    "status": "India won by 70 runs",
                                    "team1": {"teamId": 2, "teamName": "India", "teamSName": "IND"},
                                    "team2": {"teamId": 6, "teamName": "New Zealand", "teamSName": "NZ"},
                                    "venueInfo": {
                                        "id": 4,
                                        "ground": "Wankhede Stadium",
                                        "city": "Mumbai"
                                    }
                                },
                                "matchScore": {
                                    "team1Score": {"inngs1": {"runs": 397, "wickets": 4, "overs": 50.0}},
                                    "team2Score": {"inngs1": {"runs": 327, "wickets": 10, "overs": 48.5}}
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}

MOCK_MATCH_SCORECARD: Dict[str, Any] = {
    "matchId": 90101,
    "matchHeader": {
        "matchDescription": "Grand Final - ICC Champions Trophy 2025",
        "matchFormat": "T20",
        "matchType": "International",
        "status": "⚡ LIVE • Australia need 5 runs in 2 balls! Target: 213 in 20.0 ov",
        "state": "In Progress",
        "tossResults": {
            "tossWinnerName": "India",
            "decision": "bat"
        }
    },
    "scoreCard": [
        {
            "matchId": 90101,
            "inningsId": 1,
            "batTeamDetails": {"batTeamId": 2, "batTeamName": "India", "batTeamShortName": "IND"},
            "scoreDetails": {"runs": 212, "wickets": 4, "overs": 20.0, "runRate": 10.60},
            "batAuthors": [
                {"name": "Rohit Sharma (c)", "runs": 48, "balls": 24, "fours": 6, "sixes": 3, "strikeRate": 200.0, "outDesc": "c Maxwell b Starc"},
                {"name": "Virat Kohli", "runs": 82, "balls": 52, "fours": 8, "sixes": 3, "strikeRate": 157.69, "outDesc": "not out"},
                {"name": "Rishabh Pant (wk)", "runs": 14, "balls": 8, "fours": 2, "sixes": 0, "strikeRate": 175.0, "outDesc": "c Carey b Zampa"},
                {"name": "Suryakumar Yadav", "runs": 38, "balls": 18, "fours": 4, "sixes": 2, "strikeRate": 211.11, "outDesc": "c Warner b Cummins"},
                {"name": "Hardik Pandya", "runs": 28, "balls": 12, "fours": 2, "sixes": 2, "strikeRate": 233.33, "outDesc": "not out"}
            ],
            "bowlAuthors": [
                {"name": "Mitchell Starc", "overs": 4.0, "maidens": 0, "runs": 44, "wickets": 1, "economy": 11.00},
                {"name": "Josh Hazlewood", "overs": 4.0, "maidens": 0, "runs": 38, "wickets": 0, "economy": 9.50},
                {"name": "Pat Cummins", "overs": 4.0, "maidens": 0, "runs": 42, "wickets": 1, "economy": 10.50},
                {"name": "Adam Zampa", "overs": 4.0, "maidens": 0, "runs": 36, "wickets": 1, "economy": 9.00},
                {"name": "Glenn Maxwell", "overs": 4.0, "maidens": 0, "runs": 50, "wickets": 1, "economy": 12.50}
            ]
        },
        {
            "matchId": 90101,
            "inningsId": 2,
            "batTeamDetails": {"batTeamId": 3, "batTeamName": "Australia", "batTeamShortName": "AUS"},
            "scoreDetails": {"runs": 208, "wickets": 7, "overs": 19.4, "runRate": 10.57},
            "batAuthors": [
                {"name": "Travis Head", "runs": 64, "balls": 32, "fours": 8, "sixes": 3, "strikeRate": 200.0, "outDesc": "c Jadeja b Bumrah"},
                {"name": "David Warner", "runs": 18, "balls": 11, "fours": 3, "sixes": 0, "strikeRate": 163.63, "outDesc": "b Arshdeep"},
                {"name": "Mitchell Marsh (c)", "runs": 42, "balls": 24, "fours": 4, "sixes": 2, "strikeRate": 175.0, "outDesc": "c Pant b Kuldeep"},
                {"name": "Glenn Maxwell", "runs": 54, "balls": 26, "fours": 5, "sixes": 4, "strikeRate": 207.69, "outDesc": "c Axar b Hardik"},
                {"name": "Marcus Stoinis", "runs": 12, "balls": 9, "fours": 1, "sixes": 0, "strikeRate": 133.33, "outDesc": "c & b Bumrah"},
                {"name": "Tim David", "runs": 4, "balls": 5, "fours": 0, "sixes": 0, "strikeRate": 80.0, "outDesc": "b Bumrah"},
                {"name": "Pat Cummins (c)", "runs": 14, "balls": 7, "fours": 1, "sixes": 1, "strikeRate": 200.0, "outDesc": "not out"}
            ],
            "bowlAuthors": [
                {"name": "Jasprit Bumrah", "overs": 4.0, "maidens": 0, "runs": 24, "wickets": 3, "economy": 6.00},
                {"name": "Arshdeep Singh", "overs": 4.0, "maidens": 0, "runs": 42, "wickets": 1, "economy": 10.50},
                {"name": "Axar Patel", "overs": 3.4, "maidens": 0, "runs": 38, "wickets": 1, "economy": 10.36},
                {"name": "Kuldeep Yadav", "overs": 4.0, "maidens": 0, "runs": 45, "wickets": 1, "economy": 11.25},
                {"name": "Hardik Pandya", "overs": 4.0, "maidens": 0, "runs": 48, "wickets": 1, "economy": 12.00}
            ]
        }
    ]
}

MOCK_PLAYER_SEARCH: Dict[str, Any] = {
    "player": [
        {"id": "1413", "name": "Virat Kohli", "teamName": "India"},
        {"id": "576", "name": "Rohit Sharma", "teamName": "India"},
        {"id": "9311", "name": "Jasprit Bumrah", "teamName": "India"},
        {"id": "2250", "name": "Steve Smith", "teamName": "Australia"}
    ]
}

MOCK_PLAYER_CAREER: Dict[str, Any] = {
    "values": [
        {
            "format": "Test",
            "matches": "118",
            "runs": "9040",
            "highest": "254*",
            "avg": "48.86",
            "strikeRate": "55.88",
            "hundreds": "29",
            "fifties": "31"
        },
        {
            "format": "ODI",
            "matches": "295",
            "runs": "13906",
            "highest": "183",
            "avg": "58.18",
            "strikeRate": "93.54",
            "hundreds": "50",
            "fifties": "72"
        },
        {
            "format": "T20I",
            "matches": "125",
            "runs": "4188",
            "highest": "122*",
            "avg": "48.69",
            "strikeRate": "137.04",
            "hundreds": "1",
            "fifties": "38"
        }
    ]
}
