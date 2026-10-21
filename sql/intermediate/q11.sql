-- Q11: Compare each player's performance across different cricket formats.
-- For players who have played at least 2 different formats, show their total runs in
-- Test cricket, ODI cricket, and T20I cricket, along with their overall batting average.

SELECT 
    p.full_name AS player_name,
    COALESCE(SUM(CASE WHEN b.format = 'Test' THEN b.runs_scored END), 0) AS test_runs,
    COALESCE(SUM(CASE WHEN b.format = 'ODI' THEN b.runs_scored END), 0) AS odi_runs,
    COALESCE(SUM(CASE WHEN b.format IN ('T20I', 'T20') THEN b.runs_scored END), 0) AS t20i_runs,
    SUM(b.runs_scored) AS total_runs_all_formats,
    ROUND(
        CAST(SUM(b.runs_scored) AS REAL) / NULLIF(SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END), 0), 2
    ) AS overall_batting_average
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT b.format) >= 2
ORDER BY total_runs_all_formats DESC;
