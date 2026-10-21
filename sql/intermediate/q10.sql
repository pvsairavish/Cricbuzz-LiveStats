-- Q10: Get details of the last 20 completed matches.
-- Show match description, both team names, winning team, victory margin,
-- victory type (runs/wickets), and venue name. Display most recent matches first.

SELECT 
    m.description AS match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    COALESCE(w.team_name, 'No Result') AS winning_team,
    m.victory_margin,
    m.victory_type,
    v.venue_name,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams w ON m.winner_id = w.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.status = 'Completed'
ORDER BY m.match_date DESC
LIMIT 20;
