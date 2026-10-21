-- Q5: Calculate how many matches each team has won.
-- Show team name and total number of wins.
-- Display teams with most wins first.

SELECT 
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM teams t
JOIN matches m ON t.team_id = m.winner_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
