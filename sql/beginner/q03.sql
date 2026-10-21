-- Q3: List the top 10 highest run scorers in ODI cricket.
-- Show player name, total runs scored, batting average, and number of centuries.
-- Display the highest run scorer first.

SELECT 
    p.full_name AS player_name,
    SUM(b.runs_scored) AS total_runs,
    ROUND(
        CAST(SUM(b.runs_scored) AS REAL) / NULLIF(SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END), 0), 2
    ) AS batting_average,
    SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
WHERE b.format = 'ODI'
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;
