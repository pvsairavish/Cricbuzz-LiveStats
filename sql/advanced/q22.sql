-- Q22: Build a head-to-head match analysis between teams.
-- For each pair of rival teams, calculate:
-- Total matches played between them, wins for each team, average victory margin,
-- and overall win percentage.

WITH rival_matches AS (
    SELECT 
        CASE WHEN team1_id < team2_id THEN team1_id ELSE team2_id END AS tA_id,
        CASE WHEN team1_id < team2_id THEN team2_id ELSE team1_id END AS tB_id,
        match_id,
        winner_id,
        victory_margin
    FROM matches
    WHERE status = 'Completed' AND winner_id IS NOT NULL
)
SELECT 
    tA.team_name AS team_A,
    tB.team_name AS team_B,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN rm.winner_id = rm.tA_id THEN 1 ELSE 0 END) AS wins_team_A,
    SUM(CASE WHEN rm.winner_id = rm.tB_id THEN 1 ELSE 0 END) AS wins_team_B,
    ROUND(
        (CAST(SUM(CASE WHEN rm.winner_id = rm.tA_id THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100.0, 1
    ) AS win_pct_team_A,
    ROUND(
        (CAST(SUM(CASE WHEN rm.winner_id = rm.tB_id THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100.0, 1
    ) AS win_pct_team_B,
    ROUND(AVG(CASE WHEN rm.winner_id = rm.tA_id THEN rm.victory_margin END), 1) AS avg_margin_team_A,
    ROUND(AVG(CASE WHEN rm.winner_id = rm.tB_id THEN rm.victory_margin END), 1) AS avg_margin_team_B
FROM rival_matches rm
JOIN teams tA ON rm.tA_id = tA.team_id
JOIN teams tB ON rm.tB_id = tB.team_id
GROUP BY rm.tA_id, rm.tB_id, tA.team_name, tB.team_name
HAVING COUNT(*) >= 2
ORDER BY total_encounters DESC;
