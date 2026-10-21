-- Q1: Find all players who represent India.
-- Display their full name, playing role, batting style, and bowling style.

SELECT 
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name ASC;
