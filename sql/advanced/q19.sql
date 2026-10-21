-- Q19: Determine which batsmen are most consistent in their scoring.
-- Calculate average runs scored and the standard deviation of runs for each player.
-- Filter for players who faced at least 10 balls per innings and played since 2022.
-- Lower standard deviation indicates more consistent performance.

SELECT 
    p.full_name AS batsman_name,
    COUNT(b.stat_id) AS innings_played,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs,
    ROUND(
        SQRT(
            MAX(0.0, AVG(b.runs_scored * b.runs_scored) - (AVG(b.runs_scored) * AVG(b.runs_scored)))
        ), 2
    ) AS std_deviation_runs,
    MIN(b.runs_scored) AS lowest_score,
    MAX(b.runs_scored) AS highest_score
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE b.balls_faced >= 10
  AND m.match_date >= '2022-01-01'
GROUP BY p.player_id, p.full_name
HAVING COUNT(b.stat_id) >= 2
ORDER BY std_deviation_runs ASC, avg_runs DESC;
