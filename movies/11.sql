SELECT title
FROM movies
JOIN rating ON rating.movie_id = movies.id
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = 'Chadwick Boseman'
ORDER BY rating.rating DESC
LIMIT 5;
