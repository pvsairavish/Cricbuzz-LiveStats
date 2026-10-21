-- =====================================================================
-- Cricbuzz LiveStats — Relational Database Schema
-- Dialect: SQLite / ANSI SQL compatible
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Table 1: TEAMS
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    short_name TEXT NOT NULL,
    country TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table 2: VENUES
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table 3: SERIES
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name TEXT NOT NULL,
    host_country TEXT NOT NULL,
    match_type TEXT NOT NULL CHECK (match_type IN ('International', 'Domestic', 'League')),
    start_date DATE NOT NULL,
    end_date DATE,
    total_matches INTEGER NOT NULL DEFAULT 1 CHECK (total_matches > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table 4: PLAYERS
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    team_id INTEGER REFERENCES teams(team_id) ON DELETE SET NULL,
    country TEXT NOT NULL,
    playing_role TEXT NOT NULL CHECK (playing_role IN ('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper')),
    batting_style TEXT NOT NULL CHECK (batting_style IN ('Right-hand bat', 'Left-hand bat')),
    bowling_style TEXT NOT NULL CHECK (bowling_style IN (
        'Right-arm fast', 'Right-arm medium', 'Right-arm offbreak', 'Right-arm legbreak',
        'Left-arm fast', 'Left-arm medium', 'Left-arm orthodox', 'Left-arm unorthodox', 'None'
    )),
    dob DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table 5: MATCHES
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    format TEXT NOT NULL CHECK (format IN ('Test', 'ODI', 'T20I', 'T20')),
    series_id INTEGER REFERENCES series(series_id) ON DELETE SET NULL,
    team1_id INTEGER NOT NULL REFERENCES teams(team_id) ON DELETE RESTRICT,
    team2_id INTEGER NOT NULL REFERENCES teams(team_id) ON DELETE RESTRICT,
    venue_id INTEGER NOT NULL REFERENCES venues(venue_id) ON DELETE RESTRICT,
    match_date DATE NOT NULL,
    toss_winner_id INTEGER REFERENCES teams(team_id) ON DELETE SET NULL,
    toss_decision TEXT CHECK (toss_decision IN ('bat', 'bowl', 'field', NULL)),
    winner_id INTEGER REFERENCES teams(team_id) ON DELETE SET NULL,
    victory_margin INTEGER,
    victory_type TEXT CHECK (victory_type IN ('runs', 'wickets', 'tie', 'no result', NULL)),
    status TEXT NOT NULL DEFAULT 'Completed' CHECK (status IN ('Scheduled', 'Live', 'Completed', 'Abandoned')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (team1_id != team2_id)
);

-- ---------------------------------------------------------------------
-- Table 6: BATTING_STATS
-- Granular per-innings scorecard records
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS batting_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    match_id INTEGER NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    innings INTEGER NOT NULL DEFAULT 1 CHECK (innings IN (1, 2, 3, 4)),
    format TEXT NOT NULL CHECK (format IN ('Test', 'ODI', 'T20I', 'T20')),
    runs_scored INTEGER NOT NULL DEFAULT 0 CHECK (runs_scored >= 0),
    balls_faced INTEGER NOT NULL DEFAULT 0 CHECK (balls_faced >= 0),
    fours INTEGER NOT NULL DEFAULT 0 CHECK (fours >= 0),
    sixes INTEGER NOT NULL DEFAULT 0 CHECK (sixes >= 0),
    strike_rate REAL GENERATED ALWAYS AS (
        CASE WHEN balls_faced > 0 THEN ROUND((CAST(runs_scored AS REAL) / balls_faced) * 100.0, 2) ELSE 0.0 END
    ) STORED,
    batting_position INTEGER NOT NULL CHECK (batting_position BETWEEN 1 AND 11),
    is_out BOOLEAN NOT NULL DEFAULT 1 CHECK (is_out IN (0, 1)),
    dismissal_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table 7: BOWLING_STATS
-- Granular per-innings bowling spells
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bowling_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    match_id INTEGER NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    innings INTEGER NOT NULL DEFAULT 1 CHECK (innings IN (1, 2, 3, 4)),
    format TEXT NOT NULL CHECK (format IN ('Test', 'ODI', 'T20I', 'T20')),
    overs_bowled REAL NOT NULL DEFAULT 0.0 CHECK (overs_bowled >= 0.0),
    maidens INTEGER NOT NULL DEFAULT 0 CHECK (maidens >= 0),
    runs_conceded INTEGER NOT NULL DEFAULT 0 CHECK (runs_conceded >= 0),
    wickets_taken INTEGER NOT NULL DEFAULT 0 CHECK (wickets_taken >= 0),
    economy_rate REAL GENERATED ALWAYS AS (
        CASE 
            WHEN overs_bowled > 0 THEN 
                ROUND(CAST(runs_conceded AS REAL) / (CAST(overs_bowled AS INTEGER) + ((overs_bowled - CAST(overs_bowled AS INTEGER)) * 10.0 / 6.0)), 2)
            ELSE 0.0 
        END
    ) STORED,
    bowling_average REAL GENERATED ALWAYS AS (
        CASE 
            WHEN wickets_taken > 0 THEN ROUND(CAST(runs_conceded AS REAL) / wickets_taken, 2)
            ELSE NULL 
        END
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table 8: FIELDING_STATS
-- Fielding contributions per match
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fielding_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    match_id INTEGER NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    catches INTEGER NOT NULL DEFAULT 0 CHECK (catches >= 0),
    stumpings INTEGER NOT NULL DEFAULT 0 CHECK (stumpings >= 0),
    run_outs INTEGER NOT NULL DEFAULT 0 CHECK (run_outs >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
