-- Q4: Display all cricket venues that have a seating capacity of more than 50,000 spectators.
-- Show venue name, city, country, and capacity.
-- Order by largest capacity first.

SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
