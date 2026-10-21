-- Q13: Identify batting partnerships where two consecutive batsmen (batting positions next to each other)
-- scored a combined total of 100 or more runs in the same innings.
-- Show both player names, their combined partnership runs, match description, and the innings.

SELECT 
    m.description AS match_description,
    b1.innings,
    p1.full_name AS batsman_1,
    b1.batting_position AS pos_1,
    b1.runs_scored AS runs_1,
    p2.full_name AS batsman_2,
    b2.batting_position AS pos_2,
    b2.runs_scored AS runs_2,
    (b1.runs_scored + b2.runs_scored) AS combined_partnership_runs
FROM batting_stats b1
JOIN batting_stats b2 
    ON b1.match_id = b2.match_id 
   AND b1.innings = b2.innings 
   AND b2.batting_position = b1.batting_position + 1
JOIN matches m ON b1.match_id = m.match_id
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
WHERE (b1.runs_scored + b2.runs_scored) >= 100
ORDER BY combined_partnership_runs DESC;
