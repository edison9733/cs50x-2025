SELECT DISTINCT name FROM poeple
JOIN stars on stars.person_id = poeple.id
JOIN movies on movies.id = stars.movie_id
WHERE movies.year = 2004
ORDER BY people.birth ASC;
