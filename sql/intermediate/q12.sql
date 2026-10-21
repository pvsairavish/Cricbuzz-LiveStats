-- Q12: Analyze each international team's performance playing at home versus playing away.
-- Determine whether a team played at home or away based on whether venue country matches team country.
-- Count wins for each team in both home and away conditions.

SELECT 
    t.team_name,
    SUM(CASE WHEN v.country = t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN v.country != t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS away_wins,
    COUNT(CASE WHEN m.winner_id = t.team_id THEN 1 END) AS total_wins
FROM teams t
LEFT JOIN matches m ON t.team_id IN (m.team1_id, m.team2_id)
LEFT JOIN venues v ON m.venue_id = v.venue_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
