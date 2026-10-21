-- Q2: Show all cricket matches played in the last 30 days (relative to latest fixture).
-- Include match description, both team names, venue name with city, and match date.
-- Sort by most recent matches first.

SELECT 
    m.description AS match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    v.venue_name || ', ' || v.city AS venue,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= DATE((SELECT MAX(match_date) FROM matches), '-30 days')
ORDER BY m.match_date DESC;
