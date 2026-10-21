-- =====================================================================
-- Cricbuzz LiveStats — Comprehensive Seed Data
-- =====================================================================

-- Clear existing data if needed
DELETE FROM fielding_stats;
DELETE FROM bowling_stats;
DELETE FROM batting_stats;
DELETE FROM matches;
DELETE FROM players;
DELETE FROM series;
DELETE FROM venues;
DELETE FROM teams;

-- ---------------------------------------------------------------------
-- TEAMS (6 International Cricket Teams)
-- ---------------------------------------------------------------------
INSERT INTO teams (team_id, team_name, short_name, country) VALUES
(1, 'India', 'IND', 'India'),
(2, 'Australia', 'AUS', 'Australia'),
(3, 'England', 'ENG', 'England'),
(4, 'South Africa', 'SA', 'South Africa'),
(5, 'Pakistan', 'PAK', 'Pakistan'),
(6, 'New Zealand', 'NZ', 'New Zealand');

-- ---------------------------------------------------------------------
-- VENUES (10 World-Class Venues with varying capacities)
-- ---------------------------------------------------------------------
INSERT INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
(2, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
(3, 'Eden Gardens', 'Kolkata', 'India', 68000),
(4, 'Wankhede Stadium', 'Mumbai', 'India', 33108),
(5, 'Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
(6, 'Lord''s Cricket Ground', 'London', 'England', 31100),
(7, 'The Oval', 'London', 'England', 27500),
(8, 'Newlands Cricket Ground', 'Cape Town', 'South Africa', 25000),
(9, 'Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
(10, 'Seddon Park', 'Hamilton', 'New Zealand', 10500);

-- ---------------------------------------------------------------------
-- SERIES (spanning 2020 to 2024)
-- ---------------------------------------------------------------------
INSERT INTO series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
(1, 'India Tour of Australia 2020-21', 'Australia', 'International', '2020-11-27', '2021-01-19', 7),
(2, 'England Tour of India 2021', 'India', 'International', '2021-02-05', '2021-03-28', 8),
(3, 'ICC T20 World Cup 2021', 'India', 'International', '2021-10-17', '2021-11-14', 12),
(4, 'Australia Tour of Pakistan 2022', 'Pakistan', 'International', '2022-03-04', '2022-04-05', 5),
(5, 'India Tour of England 2022', 'England', 'International', '2022-07-01', '2022-07-17', 6),
(6, 'ICC Men''s Cricket World Cup 2023', 'India', 'International', '2023-10-05', '2023-11-19', 15),
(7, 'England Tour of India 2024', 'India', 'International', '2024-01-25', '2024-03-11', 5),
(8, 'ICC Men''s T20 World Cup 2024', 'Australia', 'International', '2024-06-01', '2024-06-29', 10),
(9, 'India Tour of Australia 2024-25', 'Australia', 'International', '2024-11-22', '2025-01-07', 5);

-- ---------------------------------------------------------------------
-- PLAYERS (Top Stars across all 4 Playing Roles)
-- ---------------------------------------------------------------------
INSERT INTO players (player_id, full_name, team_id, country, playing_role, batting_style, bowling_style, dob) VALUES
-- India
(1, 'Virat Kohli', 1, 'India', 'Batsman', 'Right-hand bat', 'Right-arm medium', '1988-11-05'),
(2, 'Rohit Sharma', 1, 'India', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1987-04-30'),
(3, 'Ravindra Jadeja', 1, 'India', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox', '1988-12-06'),
(4, 'Jasprit Bumrah', 1, 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-12-06'),
(5, 'KL Rahul', 1, 'India', 'Wicket-keeper', 'Right-hand bat', 'None', '1992-04-18'),
(6, 'Hardik Pandya', 1, 'India', 'All-rounder', 'Right-hand bat', 'Right-arm fast', '1993-10-11'),
(7, 'Mohammed Shami', 1, 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1990-09-03'),
(8, 'Rishabh Pant', 1, 'India', 'Wicket-keeper', 'Left-hand bat', 'None', '1997-10-04'),

-- Australia
(9, 'Steve Smith', 2, 'Australia', 'Batsman', 'Right-hand bat', 'Right-arm legbreak', '1989-06-02'),
(10, 'David Warner', 2, 'Australia', 'Batsman', 'Left-hand bat', 'Right-arm legbreak', '1986-10-27'),
(11, 'Glenn Maxwell', 2, 'Australia', 'All-rounder', 'Right-hand bat', 'Right-arm offbreak', '1988-10-14'),
(12, 'Pat Cummins', 2, 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-05-08'),
(13, 'Mitchell Starc', 2, 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast', '1990-01-30'),
(14, 'Alex Carey', 2, 'Australia', 'Wicket-keeper', 'Left-hand bat', 'None', '1991-08-27'),

-- England
(15, 'Joe Root', 3, 'England', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1990-12-30'),
(16, 'Ben Stokes', 3, 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast', '1991-06-04'),
(17, 'Jos Buttler', 3, 'England', 'Wicket-keeper', 'Right-hand bat', 'None', '1990-09-08'),
(18, 'James Anderson', 3, 'England', 'Bowler', 'Left-hand bat', 'Right-arm fast', '1982-07-30'),

-- South Africa
(19, 'Quinton de Kock', 4, 'South Africa', 'Wicket-keeper', 'Left-hand bat', 'None', '1992-12-17'),
(20, 'Kagiso Rabada', 4, 'South Africa', 'Bowler', 'Left-hand bat', 'Right-arm fast', '1995-05-25'),
(21, 'Aiden Markram', 4, 'South Africa', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1994-10-04'),

-- Pakistan
(22, 'Babar Azam', 5, 'Pakistan', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1994-10-15'),
(23, 'Shaheen Afridi', 5, 'Pakistan', 'Bowler', 'Left-hand bat', 'Left-arm fast', '2000-04-06'),
(24, 'Mohammad Rizwan', 5, 'Pakistan', 'Wicket-keeper', 'Right-hand bat', 'None', '1992-06-01'),

-- New Zealand
(25, 'Kane Williamson', 6, 'New Zealand', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1990-08-08'),
(26, 'Trent Boult', 6, 'New Zealand', 'Bowler', 'Right-hand bat', 'Left-arm fast', '1989-07-22');

-- ---------------------------------------------------------------------
-- MATCHES (25+ Matches spanning 2020-2024, including recent & close games)
-- ---------------------------------------------------------------------
INSERT INTO matches (match_id, description, format, series_id, team1_id, team2_id, venue_id, match_date, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type, status) VALUES
(1, '1st ODI - India vs Australia at Sydney', 'ODI', 1, 1, 2, 5, '2020-11-27', 2, 'bat', 2, 66, 'runs', 'Completed'),
(2, '2nd ODI - India vs Australia at Sydney', 'ODI', 1, 1, 2, 5, '2020-11-29', 2, 'bat', 2, 51, 'runs', 'Completed'),
(3, '3rd ODI - India vs Australia at Canberra', 'ODI', 1, 1, 2, 5, '2020-12-02', 1, 'bat', 1, 13, 'runs', 'Completed'),
(4, '1st Test - Border-Gavaskar Trophy at Adelaide', 'Test', 1, 1, 2, 5, '2020-12-17', 1, 'bat', 2, 8, 'wickets', 'Completed'),
(5, '2nd Test - Border-Gavaskar Trophy at Melbourne', 'Test', 1, 1, 2, 2, '2020-12-26', 2, 'bat', 1, 8, 'wickets', 'Completed'),

(6, '1st Test - England in India at Chennai', 'Test', 2, 1, 3, 3, '2021-02-05', 3, 'bat', 3, 227, 'runs', 'Completed'),
(7, '2nd Test - England in India at Chennai', 'Test', 2, 1, 3, 3, '2021-02-13', 1, 'bat', 1, 317, 'runs', 'Completed'),
(8, '3rd Test - England in India at Ahmedabad', 'Test', 2, 1, 3, 1, '2021-02-24', 3, 'bat', 1, 10, 'wickets', 'Completed'),
(9, '1st T20I - England in India at Ahmedabad', 'T20I', 2, 1, 3, 1, '2021-03-12', 3, 'bowl', 3, 8, 'wickets', 'Completed'),
(10, '5th T20I - England in India at Ahmedabad', 'T20I', 2, 1, 3, 1, '2021-03-20', 3, 'bowl', 1, 36, 'runs', 'Completed'),

(11, '1st Test - Australia in Pakistan at Rawalpindi', 'Test', 4, 5, 2, 9, '2022-03-04', 5, 'bat', 5, 4, 'wickets', 'Completed'),
(12, '1st ODI - Australia in Pakistan at Lahore', 'ODI', 4, 5, 2, 9, '2022-03-29', 5, 'bowl', 2, 88, 'runs', 'Completed'),
(13, '5th Rescheduled Test - India in England at Edgbaston', 'Test', 5, 1, 3, 6, '2022-07-01', 3, 'bowl', 3, 7, 'wickets', 'Completed'),
(14, '1st ODI - India in England at The Oval', 'ODI', 5, 1, 3, 7, '2022-07-12', 1, 'bowl', 1, 10, 'wickets', 'Completed'),
(15, '3rd ODI - India in England at Manchester', 'ODI', 5, 1, 3, 6, '2022-07-17', 1, 'bowl', 1, 5, 'wickets', 'Completed'),

(16, 'Match 1 - World Cup: England vs New Zealand at Ahmedabad', 'ODI', 6, 3, 6, 1, '2023-10-05', 6, 'bowl', 6, 9, 'wickets', 'Completed'),
(17, 'Match 5 - World Cup: India vs Australia at Chennai', 'ODI', 6, 1, 2, 3, '2023-10-08', 2, 'bat', 1, 6, 'wickets', 'Completed'),
(18, 'Match 12 - World Cup: India vs Pakistan at Ahmedabad', 'ODI', 6, 1, 5, 1, '2023-10-14', 1, 'bowl', 1, 7, 'wickets', 'Completed'),
(19, 'Match 17 - World Cup: India vs Bangladesh at Pune', 'ODI', 6, 1, 4, 4, '2023-10-19', 4, 'bat', 1, 7, 'wickets', 'Completed'),
(20, 'Match 33 - World Cup: India vs Sri Lanka at Mumbai', 'ODI', 6, 1, 6, 4, '2023-11-02', 6, 'bowl', 1, 302, 'runs', 'Completed'),
(21, 'Final - World Cup: India vs Australia at Ahmedabad', 'ODI', 6, 1, 2, 1, '2023-11-19', 2, 'bowl', 2, 6, 'wickets', 'Completed'),

(22, '1st Test - England in India at Hyderabad', 'Test', 7, 1, 3, 4, '2024-01-25', 3, 'bat', 3, 28, 'runs', 'Completed'),
(23, '2nd Test - England in India at Visakhapatnam', 'Test', 7, 1, 3, 3, '2024-02-02', 1, 'bat', 1, 106, 'runs', 'Completed'),
(24, '3rd Test - England in India at Rajkot', 'Test', 7, 1, 3, 1, '2024-02-15', 1, 'bat', 1, 434, 'runs', 'Completed'),
(25, 'Final - T20 World Cup: India vs South Africa at Barbados', 'T20I', 8, 1, 4, 2, '2024-06-29', 1, 'bat', 1, 7, 'runs', 'Completed'),
(26, '1st Test - Border-Gavaskar Trophy: Australia vs India at Perth', 'Test', 9, 2, 1, 2, '2024-11-22', 1, 'bat', 1, 295, 'runs', 'Completed');

-- ---------------------------------------------------------------------
-- BATTING STATS (Granular innings entries with consecutive partnerships)
-- ---------------------------------------------------------------------
INSERT INTO batting_stats (player_id, match_id, innings, format, runs_scored, balls_faced, fours, sixes, batting_position, is_out, dismissal_info) VALUES
-- Match 1: IND vs AUS (ODI 2020)
(10, 1, 1, 'ODI', 69, 76, 6, 0, 1, 1, 'c Shami b Chahal'),
(9, 1, 1, 'ODI', 105, 66, 11, 4, 3, 1, 'c Shami b Shami'),
(11, 1, 1, 'ODI', 45, 19, 5, 3, 5, 1, 'c Jadeja b Shami'),
(1, 1, 2, 'ODI', 21, 21, 2, 1, 3, 1, 'c Finch b Hazlewood'),
(3, 1, 2, 'ODI', 25, 37, 1, 0, 7, 1, 'c Starc b Zampa'),
(6, 1, 2, 'ODI', 90, 76, 7, 4, 6, 1, 'c Starc b Zampa'),

-- Match 2: IND vs AUS (ODI 2020)
(9, 2, 1, 'ODI', 104, 64, 14, 2, 3, 1, 'c Shami b Bumrah'),
(11, 2, 1, 'ODI', 63, 29, 4, 4, 5, 0, 'not out'),
(1, 2, 2, 'ODI', 89, 87, 7, 2, 3, 1, 'c Henriques b Hazlewood'),
(5, 2, 2, 'ODI', 76, 66, 4, 5, 5, 1, 'c Hazlewood b Cummins'),

-- Match 3: IND vs AUS (ODI 2020) - 150-run consecutive partnership (pos 6 & 7)
(1, 3, 1, 'ODI', 63, 78, 5, 0, 3, 1, 'c Carey b Hazlewood'),
(6, 3, 1, 'ODI', 92, 76, 7, 1, 6, 0, 'not out'),
(3, 3, 1, 'ODI', 66, 50, 5, 3, 7, 0, 'not out'),
(11, 3, 2, 'ODI', 59, 38, 3, 4, 6, 1, 'b Bumrah'),

-- Match 5: IND vs AUS (Test 2020 at MCG)
(9, 5, 1, 'Test', 0, 8, 0, 0, 4, 1, 'c Pujara b Ashwin'),
(3, 5, 2, 'Test', 57, 159, 3, 0, 7, 1, 'c Cummins b Starc'),

-- Match 6 & 7: IND vs ENG (Test 2021)
(15, 6, 1, 'Test', 218, 377, 19, 2, 4, 1, 'lbw b Nadeem'),
(16, 6, 1, 'Test', 82, 118, 10, 3, 5, 1, 'c Pujara b Nadeem'),
(1, 6, 2, 'Test', 11, 48, 1, 0, 4, 1, 'c sub b Bess'),
(1, 6, 4, 'Test', 72, 104, 9, 0, 4, 1, 'b Leach'),
(2, 7, 1, 'Test', 161, 231, 18, 2, 1, 1, 'c Moeen b Leach'),
(1, 7, 1, 'Test', 0, 5, 0, 0, 4, 1, 'b Moeen Ali'),
(15, 7, 2, 'Test', 33, 92, 1, 0, 4, 1, 'c Patel b Patel'),

-- Match 10: IND vs ENG (T20I 2021) - 100+ opening stand
(2, 10, 1, 'T20I', 64, 34, 4, 5, 1, 1, 'b Stokes'),
(1, 10, 1, 'T20I', 80, 52, 7, 2, 2, 0, 'not out'),
(6, 10, 1, 'T20I', 39, 17, 4, 2, 4, 0, 'not out'),
(17, 10, 2, 'T20I', 52, 34, 2, 4, 1, 1, 'c Pandya b Kumar'),
(16, 10, 2, 'T20I', 14, 12, 1, 0, 5, 1, 'c Rahul b Natarajan'),

-- Match 11 & 12: PAK vs AUS (2022)
(22, 11, 1, 'Test', 36, 82, 3, 0, 3, 1, 'run out'),
(9, 11, 2, 'Test', 78, 196, 8, 0, 4, 1, 'c Rizwan b Nauman'),
(22, 12, 1, 'ODI', 57, 72, 6, 0, 3, 1, 'b Swepson'),
(24, 12, 1, 'ODI', 60, 71, 2, 1, 4, 1, 'c Carey b Ellis'),

-- Match 13, 14, 15: IND in ENG (2022)
(8, 13, 1, 'Test', 146, 111, 19, 4, 5, 1, 'c Crawley b Root'),
(3, 13, 1, 'Test', 104, 194, 13, 0, 7, 1, 'b Anderson'),
(15, 13, 4, 'Test', 142, 173, 19, 1, 4, 0, 'not out'),
(1, 15, 2, 'ODI', 17, 22, 3, 0, 3, 1, 'c Buttler b Topley'),
(8, 15, 2, 'ODI', 125, 113, 16, 2, 4, 0, 'not out'),
(6, 15, 2, 'ODI', 71, 55, 10, 0, 5, 1, 'c Stokes b Carse'),

-- Match 16: ENG vs NZ World Cup 2023
(15, 16, 1, 'ODI', 77, 86, 4, 1, 3, 1, 'b Phillips'),
(17, 16, 1, 'ODI', 43, 42, 2, 2, 5, 1, 'c Latham b Henry'),

-- Match 17: IND vs AUS World Cup 2023 (Chasing down total from 2/3)
(9, 17, 1, 'ODI', 46, 71, 5, 0, 3, 1, 'b Jadeja'),
(1, 17, 2, 'ODI', 85, 116, 6, 0, 3, 1, 'c Labuschagne b Hazlewood'),
(5, 17, 2, 'ODI', 97, 115, 8, 2, 5, 0, 'not out'),

-- Match 18: IND vs PAK World Cup 2023
(22, 18, 1, 'ODI', 50, 58, 7, 0, 3, 1, 'b Siraj'),
(24, 18, 1, 'ODI', 49, 69, 7, 0, 4, 1, 'b Bumrah'),
(2, 18, 2, 'ODI', 86, 63, 6, 6, 1, 1, 'c Iftikhar b Shaheen'),

-- Match 20: IND vs SL World Cup 2023
(1, 20, 1, 'ODI', 88, 94, 11, 0, 3, 1, 'c Nissanka b Madushanka'),

-- Match 21: World Cup Final 2023 (IND vs AUS)
(2, 21, 1, 'ODI', 47, 31, 4, 3, 1, 1, 'c Head b Maxwell'),
(1, 21, 1, 'ODI', 54, 63, 4, 0, 3, 1, 'b Cummins'),
(5, 21, 1, 'ODI', 66, 107, 1, 0, 5, 1, 'c Inglis b Starc'),
(9, 21, 2, 'ODI', 4, 9, 1, 0, 4, 1, 'lbw b Bumrah'),

-- Match 24: IND vs ENG Test 2024 (Rajkot)
(2, 24, 1, 'Test', 131, 196, 14, 3, 1, 1, 'c Stokes b Wood'),
(3, 24, 1, 'Test', 112, 225, 9, 2, 5, 1, 'c & b Root'),

-- Match 25: T20 World Cup Final 2024 (IND vs SA at Barbados) - 7 runs thriller
(1, 25, 1, 'T20I', 76, 59, 6, 2, 2, 1, 'c Jansen b Nortje'),
(21, 25, 2, 'T20I', 4, 5, 0, 0, 3, 1, 'c Pant b Arshdeep'),
(19, 25, 2, 'T20I', 39, 31, 4, 1, 1, 1, 'c Kuldeep b Arshdeep'),

-- Match 26: Border-Gavaskar Trophy Perth 2024
(1, 26, 3, 'Test', 100, 143, 8, 2, 4, 0, 'not out'),
(9, 26, 4, 'Test', 17, 35, 1, 0, 4, 1, 'c Pant b Bumrah');

-- ---------------------------------------------------------------------
-- BOWLING STATS (Granular bowling spells across formats)
-- ---------------------------------------------------------------------
INSERT INTO bowling_stats (player_id, match_id, innings, format, overs_bowled, maidens, runs_conceded, wickets_taken) VALUES
-- Match 1: AUS vs IND (ODI 2020)
(7, 1, 1, 'ODI', 10.0, 0, 59, 3),
(4, 1, 1, 'ODI', 10.0, 0, 73, 1),
(3, 1, 1, 'ODI', 10.0, 0, 63, 0),
(12, 1, 2, 'ODI', 8.0, 0, 52, 0),
(13, 1, 2, 'ODI', 9.0, 0, 74, 1),

-- Match 2: AUS vs IND (ODI 2020)
(4, 2, 1, 'ODI', 10.0, 1, 79, 1),
(7, 2, 1, 'ODI', 9.0, 0, 73, 0),
(3, 2, 1, 'ODI', 9.0, 0, 60, 0),
(12, 2, 2, 'ODI', 10.0, 0, 67, 3),

-- Match 3: AUS vs IND (ODI 2020)
(4, 3, 2, 'ODI', 9.3, 0, 43, 2),
(7, 3, 2, 'ODI', 10.0, 0, 63, 1),
(3, 3, 2, 'ODI', 10.0, 1, 44, 1),

-- Match 5: AUS vs IND (Test 2020 at MCG)
(4, 5, 1, 'Test', 16.0, 4, 56, 4),
(7, 5, 1, 'Test', 18.0, 2, 60, 2),
(3, 5, 1, 'Test', 15.0, 3, 40, 1),
(12, 5, 2, 'Test', 27.0, 9, 72, 4),
(13, 5, 2, 'Test', 25.0, 5, 78, 2),
(4, 5, 3, 'Test', 15.5, 3, 54, 2),

-- Match 6 & 7: IND vs ENG (Test 2021)
(18, 6, 2, 'Test', 16.5, 5, 46, 3),
(16, 6, 2, 'Test', 12.0, 1, 30, 1),
(4, 6, 1, 'Test', 36.0, 7, 84, 3),
(3, 6, 1, 'Test', 24.0, 4, 75, 2),
(18, 7, 1, 'Test', 5.0, 1, 15, 0),

-- Match 9 & 10: IND vs ENG (T20I 2021)
(4, 9, 2, 'T20I', 4.0, 0, 24, 1),
(16, 9, 1, 'T20I', 3.0, 0, 25, 1),
(6, 10, 2, 'T20I', 4.0, 0, 34, 1),
(4, 10, 2, 'T20I', 4.0, 0, 32, 2),

-- Match 11 & 12: PAK vs AUS (2022)
(23, 11, 2, 'Test', 30.0, 6, 88, 2),
(12, 11, 1, 'Test', 24.0, 5, 62, 1),
(23, 12, 1, 'ODI', 10.0, 0, 63, 2),

-- Match 14 & 15: IND in ENG (2022)
(4, 14, 1, 'ODI', 7.2, 3, 19, 6),
(7, 14, 1, 'ODI', 7.0, 0, 31, 3),
(6, 15, 1, 'ODI', 7.0, 3, 24, 4),
(16, 15, 2, 'ODI', 3.0, 0, 21, 0),

-- Match 17, 18, 20: World Cup 2023
(3, 17, 1, 'ODI', 10.0, 2, 28, 3),
(4, 17, 1, 'ODI', 10.0, 1, 32, 2),
(12, 17, 2, 'ODI', 6.2, 0, 33, 1),
(13, 17, 2, 'ODI', 8.0, 1, 31, 1),
(4, 18, 1, 'ODI', 7.0, 1, 19, 2),
(7, 18, 1, 'ODI', 7.0, 0, 35, 1),
(23, 18, 2, 'ODI', 6.0, 0, 36, 2),
(7, 20, 2, 'ODI', 5.0, 1, 18, 5),
(4, 20, 2, 'ODI', 5.0, 1, 8, 1),

-- Match 21: World Cup Final 2023
(12, 21, 1, 'ODI', 10.0, 0, 34, 2),
(13, 21, 1, 'ODI', 10.0, 0, 55, 3),
(11, 21, 1, 'ODI', 6.0, 0, 35, 1),
(4, 21, 2, 'ODI', 9.0, 2, 43, 2),
(7, 21, 2, 'ODI', 7.0, 0, 47, 1),

-- Match 25: T20 World Cup Final 2024
(4, 25, 2, 'T20I', 4.0, 0, 18, 2),
(6, 25, 2, 'T20I', 3.0, 0, 20, 3),
(20, 25, 1, 'T20I', 4.0, 0, 36, 1),

-- Match 26: Test Perth 2024
(4, 26, 2, 'Test', 18.0, 4, 30, 5),
(7, 26, 2, 'Test', 15.0, 2, 42, 3),
(12, 26, 1, 'Test', 15.0, 3, 67, 2),
(13, 26, 3, 'Test', 17.0, 2, 60, 1);

-- ---------------------------------------------------------------------
-- FIELDING STATS (Catches and Stumpings)
-- ---------------------------------------------------------------------
INSERT INTO fielding_stats (player_id, match_id, catches, stumpings, run_outs) VALUES
(1, 1, 1, 0, 0),
(5, 1, 1, 0, 0),
(14, 1, 2, 0, 0),
(1, 2, 2, 0, 0),
(14, 2, 1, 0, 0),
(1, 3, 1, 0, 0),
(8, 5, 2, 0, 0),
(1, 5, 1, 0, 0),
(14, 5, 3, 0, 0),
(17, 10, 1, 0, 0),
(5, 10, 2, 0, 0),
(24, 11, 2, 1, 0),
(8, 13, 3, 0, 0),
(17, 14, 0, 0, 0),
(8, 15, 2, 1, 0),
(1, 17, 2, 0, 0),
(5, 17, 1, 0, 0),
(1, 18, 1, 0, 0),
(5, 18, 2, 0, 0),
(8, 25, 2, 0, 0),
(1, 25, 1, 0, 0),
(19, 25, 1, 1, 0),
(8, 26, 4, 0, 0),
(1, 26, 2, 0, 0);
