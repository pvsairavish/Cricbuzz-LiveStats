-- Q25: Time-series analysis of player performance evolution across quarters.
-- Uses LAG() window function to compare consecutive quarters and classify momentum:
-- 'Improving', 'Declining', or 'Stable', and categorizes career trajectory.

WITH quarterly_stats AS (
    SELECT 
        b.player_id,
        strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3 + 1) AS year_quarter,
        COUNT(b.stat_id) AS matches_in_quarter,
        ROUND(AVG(b.runs_scored), 2) AS qtr_avg_runs,
        ROUND(AVG(b.strike_rate), 2) AS qtr_avg_sr
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, year_quarter
),
quarterly_trend AS (
    SELECT 
        player_id,
        year_quarter,
        matches_in_quarter,
        qtr_avg_runs,
        qtr_avg_sr,
        LAG(qtr_avg_runs) OVER (PARTITION BY player_id ORDER BY year_quarter ASC) AS prev_qtr_runs,
        ROUND(
            qtr_avg_runs - LAG(qtr_avg_runs) OVER (PARTITION BY player_id ORDER BY year_quarter ASC), 2
        ) AS runs_diff
    FROM quarterly_stats
)
SELECT 
    p.full_name AS player_name,
    qt.year_quarter,
    qt.matches_in_quarter,
    qt.qtr_avg_runs,
    COALESCE(qt.prev_qtr_runs, qt.qtr_avg_runs) AS prev_qtr_runs,
    COALESCE(qt.runs_diff, 0.0) AS net_change_runs,
    CASE 
        WHEN qt.runs_diff > 10.0 THEN 'Performance Improving'
        WHEN qt.runs_diff < -10.0 THEN 'Performance Declining'
        ELSE 'Stable'
    END AS quarter_trend,
    CASE 
        WHEN qt.qtr_avg_runs >= 60 THEN 'Career Ascending / Prime'
        WHEN qt.qtr_avg_runs >= 35 THEN 'Career Stable'
        ELSE 'Career Under Pressure'
    END AS career_trajectory
FROM quarterly_trend qt
JOIN players p ON qt.player_id = p.player_id
ORDER BY p.full_name ASC, qt.year_quarter DESC;
