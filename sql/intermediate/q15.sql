-- Q15: Identify players who perform exceptionally well in close matches.
-- A close match is defined as one decided by less than 50 runs OR less than 5 wickets.
-- For these close matches, calculate each player's average runs scored, total close matches played,
-- and how many of those close matches their team won when they batted.

SELECT 
    p.full_name AS player_name,
    COUNT(DISTINCT m.match_id) AS close_matches_played,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs_in_close_matches,
    SUM(CASE WHEN m.winner_id = p.team_id THEN 1 ELSE 0 END) AS close_matches_won_by_team
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
   OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.full_name
ORDER BY avg_runs_in_close_matches DESC;
