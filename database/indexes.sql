-- =====================================================================
-- Cricbuzz LiveStats — Database Performance Indexes
-- =====================================================================

-- Indexes on Players
CREATE INDEX IF NOT EXISTS idx_players_country ON players(country);
CREATE INDEX IF NOT EXISTS idx_players_role ON players(playing_role);
CREATE INDEX IF NOT EXISTS idx_players_team ON players(team_id);

-- Indexes on Venues
CREATE INDEX IF NOT EXISTS idx_venues_country ON venues(country);
CREATE INDEX IF NOT EXISTS idx_venues_capacity ON venues(capacity);

-- Indexes on Series
CREATE INDEX IF NOT EXISTS idx_series_start_date ON series(start_date);
CREATE INDEX IF NOT EXISTS idx_series_host_country ON series(host_country);

-- Indexes on Matches
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(format);
CREATE INDEX IF NOT EXISTS idx_matches_venue ON matches(venue_id);
CREATE INDEX IF NOT EXISTS idx_matches_teams ON matches(team1_id, team2_id);
CREATE INDEX IF NOT EXISTS idx_matches_winner ON matches(winner_id);
CREATE INDEX IF NOT EXISTS idx_matches_toss ON matches(toss_winner_id, toss_decision);

-- Indexes on Batting Stats
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_batting_match ON batting_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_batting_player_format ON batting_stats(player_id, format);
CREATE INDEX IF NOT EXISTS idx_batting_partnership ON batting_stats(match_id, innings, batting_position);

-- Indexes on Bowling Stats
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_match ON bowling_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player_format ON bowling_stats(player_id, format);

-- Indexes on Fielding Stats
CREATE INDEX IF NOT EXISTS idx_fielding_player ON fielding_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_fielding_match ON fielding_stats(match_id);
