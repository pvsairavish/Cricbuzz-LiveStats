-- Q9: Find all-rounder players who have scored significant runs and taken wickets in their career.
-- Display player name, total runs, total wickets, and the cricket format.

WITH player_batting AS (
    SELECT 
        player_id,
        format,
        SUM(runs_scored) AS total_runs
    FROM batting_stats
    GROUP BY player_id, format
),
player_bowling AS (
    SELECT 
        player_id,
        format,
        SUM(wickets_taken) AS total_wickets
    FROM bowling_stats
    GROUP BY player_id, format
)
SELECT 
    p.full_name AS player_name,
    pb.format,
    pb.total_runs,
    COALESCE(pw.total_wickets, 0) AS total_wickets
FROM players p
JOIN player_batting pb ON p.player_id = pb.player_id
LEFT JOIN player_bowling pw ON p.player_id = pw.player_id AND pb.format = pw.format
WHERE p.playing_role = 'All-rounder'
  AND (pb.total_runs >= 100 OR pw.total_wickets >= 5)
ORDER BY pb.total_runs DESC, total_wickets DESC;
