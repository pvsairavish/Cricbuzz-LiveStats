-- Q16: Track how players' batting performance changes over different years.
-- For matches since 2020, show each player's average runs per match and average strike rate for each year.
-- Filter for players with consistent appearances.

SELECT 
    p.full_name AS player_name,
    strftime('%Y', m.match_date) AS match_year,
    COUNT(b.stat_id) AS innings_batted,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs_per_innings,
    ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.player_id, p.full_name, strftime('%Y', m.match_date)
HAVING COUNT(b.stat_id) >= 2
ORDER BY p.full_name ASC, match_year ASC;
