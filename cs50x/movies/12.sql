SELECT title FROM movies, stars, people
WHERE movies.id = movie_id
AND person_id = people.id
AND (name = "Johnny Depp" OR name = "Helena Bonham Carter")
GROUP by title HAVING COUNT(title) > 1;