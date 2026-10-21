-- Q21: Comprehensive performance ranking system combining batting, bowling, and fielding into a single score:
-- Batting points: (runs_scored * 0.01) + (batting_average * 0.5) + (strike_rate * 0.3)
-- Bowling points: (wickets_taken * 2) + ((50 - bowling_average) * 0.5) + ((6 - economy_rate) * 2)
-- Fielding points: (catches * 3) + (stumpings * 5)
-- Rank players in each format using window functions.

WITH player_batting AS (
    SELECT 
        player_id,
        format,
        SUM(runs_scored) AS total_runs,
        ROUND(AVG(runs_scored), 2) AS batting_avg,
        ROUND(AVG(strike_rate), 2) AS avg_sr,
        ROUND(
            (SUM(runs_scored) * 0.01) + (AVG(runs_scored) * 0.5) + (AVG(strike_rate) * 0.3), 2
        ) AS batting_points
    FROM batting_stats
    GROUP BY player_id, format
),
player_bowling AS (
    SELECT 
        player_id,
        format,
        SUM(wickets_taken) AS total_wickets,
        ROUND(AVG(COALESCE(bowling_average, 30.0)), 2) AS avg_bowl_avg,
        ROUND(AVG(economy_rate), 2) AS avg_econ,
        ROUND(
            (SUM(wickets_taken) * 2.0) + 
            ((50.0 - AVG(COALESCE(bowling_average, 30.0))) * 0.5) + 
            ((6.0 - AVG(economy_rate)) * 2.0), 2
        ) AS bowling_points
    FROM bowling_stats
    GROUP BY player_id, format
),
player_fielding AS (
    SELECT 
        player_id,
        ROUND((SUM(catches) * 3.0) + (SUM(stumpings) * 5.0), 2) AS fielding_points
    FROM fielding_stats
    GROUP BY player_id
),
combined_scores AS (
    SELECT 
        p.full_name AS player_name,
        pb.format,
        COALESCE(pb.batting_points, 0) AS batting_pts,
        COALESCE(pw.bowling_points, 0) AS bowling_pts,
        COALESCE(pf.fielding_points, 0) AS fielding_pts,
        ROUND(
            COALESCE(pb.batting_points, 0) + 
            COALESCE(pw.bowling_points, 0) + 
            COALESCE(pf.fielding_points, 0), 2
        ) AS total_points
    FROM players p
    JOIN player_batting pb ON p.player_id = pb.player_id
    LEFT JOIN player_bowling pw ON p.player_id = pw.player_id AND pb.format = pw.format
    LEFT JOIN player_fielding pf ON p.player_id = pf.player_id
)
SELECT 
    RANK() OVER (PARTITION BY format ORDER BY total_points DESC) AS format_rank,
    player_name,
    format,
    batting_pts,
    bowling_pts,
    fielding_pts,
    total_points
FROM combined_scores
ORDER BY format ASC, total_points DESC;
