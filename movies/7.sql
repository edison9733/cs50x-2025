SELECT title, rating
FROM movies
JOIN ratings on moivies.id = ratings.movie_id
ORDER BY rating DESC;
