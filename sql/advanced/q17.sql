-- Q17: Investigate whether winning the toss gives teams an advantage in winning matches.
-- Calculate what percentage of matches are won by the team that wins the toss,
-- broken down by their toss decision (choosing to bat first or bowl/field first).

SELECT 
    CASE 
        WHEN toss_decision IN ('bowl', 'field') THEN 'Field First'
        WHEN toss_decision = 'bat' THEN 'Bat First'
        ELSE 'Unrecorded'
    END AS toss_decision_type,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS toss_winner_won_match,
    ROUND(
        (CAST(SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100.0, 2
    ) AS win_percentage_after_toss_win
FROM matches
WHERE toss_decision IS NOT NULL AND winner_id IS NOT NULL
GROUP BY toss_decision_type
ORDER BY win_percentage_after_toss_win DESC;
