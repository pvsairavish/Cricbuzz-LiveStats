-- Q23: Analyze recent player form and momentum using window functions.
-- For each player's latest batting performances:
-- Calculate avg runs in last 5 vs last 10 innings, 50+ scores, strike rate,
-- and categorize form: 'Excellent Form', 'Good Form', 'Average Form', or 'Poor Form'.

WITH ranked_innings AS (
    SELECT 
        b.player_id,
        b.runs_scored,
        b.strike_rate,
        ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC, b.stat_id DESC) AS innings_recency
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
),
form_metrics AS (
    SELECT 
        player_id,
        COUNT(*) AS total_recent_innings,
        ROUND(AVG(CASE WHEN innings_recency <= 5 THEN runs_scored END), 2) AS avg_last_5,
        ROUND(AVG(runs_scored), 2) AS avg_last_10,
        ROUND(AVG(strike_rate), 2) AS recent_strike_rate,
        SUM(CASE WHEN runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_plus,
        ROUND(
            SQRT(MAX(0.0, AVG(runs_scored * runs_scored) - (AVG(runs_scored) * AVG(runs_scored)))), 2
        ) AS consistency_score
    FROM ranked_innings
    WHERE innings_recency <= 10
    GROUP BY player_id
    HAVING COUNT(*) >= 2
)
SELECT 
    p.full_name AS player_name,
    fm.total_recent_innings,
    fm.avg_last_5,
    fm.avg_last_10,
    fm.recent_strike_rate,
    fm.fifties_plus,
    fm.consistency_score,
    CASE 
        WHEN fm.avg_last_5 >= 60 OR fm.fifties_plus >= 3 THEN 'Excellent Form'
        WHEN fm.avg_last_5 >= 40 THEN 'Good Form'
        WHEN fm.avg_last_5 >= 25 THEN 'Average Form'
        ELSE 'Poor Form'
    END AS form_category
FROM form_metrics fm
JOIN players p ON fm.player_id = p.player_id
ORDER BY fm.avg_last_5 DESC;
