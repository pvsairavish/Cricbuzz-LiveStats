-- Q20: Analyze matches played in different formats and format-specific batting averages.
-- Show count of Test matches, ODI matches, and T20 matches along with respective batting averages.

SELECT 
    p.full_name AS player_name,
    COUNT(CASE WHEN b.format = 'Test' THEN 1 END) AS test_innings,
    ROUND(
        CAST(SUM(CASE WHEN b.format = 'Test' THEN b.runs_scored ELSE 0 END) AS REAL) / 
        NULLIF(SUM(CASE WHEN b.format = 'Test' AND b.is_out = 1 THEN 1 ELSE 0 END), 0), 2
    ) AS test_batting_avg,
    
    COUNT(CASE WHEN b.format = 'ODI' THEN 1 END) AS odi_innings,
    ROUND(
        CAST(SUM(CASE WHEN b.format = 'ODI' THEN b.runs_scored ELSE 0 END) AS REAL) / 
        NULLIF(SUM(CASE WHEN b.format = 'ODI' AND b.is_out = 1 THEN 1 ELSE 0 END), 0), 2
    ) AS odi_batting_avg,
    
    COUNT(CASE WHEN b.format IN ('T20I', 'T20') THEN 1 END) AS t20_innings,
    ROUND(
        CAST(SUM(CASE WHEN b.format IN ('T20I', 'T20') THEN b.runs_scored ELSE 0 END) AS REAL) / 
        NULLIF(SUM(CASE WHEN b.format IN ('T20I', 'T20') AND b.is_out = 1 THEN 1 ELSE 0 END), 0), 2
    ) AS t20_batting_avg,
    
    COUNT(b.stat_id) AS total_career_innings
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_career_innings DESC;
