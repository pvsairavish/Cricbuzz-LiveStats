-- Q8: Show all cricket series that started in the year 2024.
-- Include series name, host country, match type, start date, and total matches planned.

SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date ASC;
