-- Q18: Find the most economical bowlers in limited-overs cricket (ODI and T20 formats).
-- Calculate each bowler's overall economy rate and total wickets taken.
-- Filter for bowlers with sufficient appearances and average overs bowled.

SELECT 
    p.full_name AS bowler_name,
    COUNT(DISTINCT bw.match_id) AS matches_bowled,
    ROUND(SUM(bw.overs_bowled), 1) AS total_overs,
    SUM(bw.runs_conceded) AS total_runs_conceded,
    SUM(bw.wickets_taken) AS total_wickets,
    ROUND(
        CASE WHEN SUM(bw.overs_bowled) > 0 
             THEN CAST(SUM(bw.runs_conceded) AS REAL) / SUM(bw.overs_bowled) 
             ELSE 0.0 END, 2
    ) AS overall_economy_rate
FROM bowling_stats bw
JOIN players p ON bw.player_id = p.player_id
WHERE bw.format IN ('ODI', 'T20I', 'T20')
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT bw.match_id) >= 3
   AND (SUM(bw.overs_bowled) / COUNT(DISTINCT bw.match_id)) >= 2.0
ORDER BY overall_economy_rate ASC, total_wickets DESC;
