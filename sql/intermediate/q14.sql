-- Q14: Examine bowling performance at different venues.
-- For bowlers who have played at least 3 matches at the same venue (or minimum 2 in sample data),
-- calculate their average economy rate, total wickets taken, and matches played at each venue.
-- Focus on bowlers who bowled at least 4 overs in each match.

SELECT 
    p.full_name AS bowler_name,
    v.venue_name,
    COUNT(DISTINCT bw.match_id) AS matches_played_at_venue,
    ROUND(AVG(bw.economy_rate), 2) AS avg_economy_rate,
    SUM(bw.wickets_taken) AS total_wickets,
    ROUND(SUM(bw.overs_bowled), 1) AS total_overs_bowled
FROM bowling_stats bw
JOIN matches m ON bw.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
JOIN players p ON bw.player_id = p.player_id
WHERE bw.overs_bowled >= 4.0
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
HAVING COUNT(DISTINCT bw.match_id) >= 2
ORDER BY total_wickets DESC, avg_economy_rate ASC;
