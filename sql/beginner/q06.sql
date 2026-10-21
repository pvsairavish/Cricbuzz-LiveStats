-- Q6: Count how many players belong to each playing role.
-- Show the role and count of players for each role.

SELECT 
    playing_role,
    COUNT(player_id) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
