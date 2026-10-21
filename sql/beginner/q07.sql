-- Q7: Find the highest individual batting score achieved in each cricket format.
-- Display the format and the highest score for that format.

SELECT 
    format,
    MAX(runs_scored) AS highest_score
FROM batting_stats
GROUP BY format
ORDER BY highest_score DESC;
