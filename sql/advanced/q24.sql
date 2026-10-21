-- Q24: Study successful batting partnerships to identify the best player combinations.
-- For pairs of players who batted together as consecutive batsmen:
-- Calculate avg partnership runs, 50+ stands, highest stand, and success rate.
-- Rank the most successful batting combinations.

WITH consecutive_stands AS (
    SELECT 
        CASE WHEN b1.player_id < b2.player_id THEN b1.player_id ELSE b2.player_id END AS p1_id,
        CASE WHEN b1.player_id < b2.player_id THEN b2.player_id ELSE b1.player_id END AS p2_id,
        b1.match_id,
        b1.innings,
        (b1.runs_scored + b2.runs_scored) AS stand_runs
    FROM batting_stats b1
    JOIN batting_stats b2 
        ON b1.match_id = b2.match_id 
       AND b1.innings = b2.innings 
       AND b2.batting_position = b1.batting_position + 1
),
partnership_metrics AS (
    SELECT 
        p1_id,
        p2_id,
        COUNT(*) AS total_partnerships,
        ROUND(AVG(stand_runs), 2) AS avg_partnership_runs,
        MAX(stand_runs) AS highest_partnership,
        SUM(CASE WHEN stand_runs >= 50 THEN 1 ELSE 0 END) AS stands_over_50,
        ROUND(
            (CAST(SUM(CASE WHEN stand_runs >= 50 THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100.0, 1
        ) AS success_rate_pct
    FROM consecutive_stands
    GROUP BY p1_id, p2_id
)
SELECT 
    RANK() OVER (ORDER BY pm.avg_partnership_runs DESC, pm.highest_partnership DESC) AS partnership_rank,
    p1.full_name AS batsman_A,
    p2.full_name AS batsman_B,
    pm.total_partnerships,
    pm.avg_partnership_runs,
    pm.highest_partnership,
    pm.stands_over_50,
    pm.success_rate_pct
FROM partnership_metrics pm
JOIN players p1 ON pm.p1_id = p1.player_id
JOIN players p2 ON pm.p2_id = p2.player_id
ORDER BY partnership_rank ASC;
