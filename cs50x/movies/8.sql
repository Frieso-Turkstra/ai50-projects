SELECT name FROM movies, stars, people
WHERE stars.movie_id = movies.id
AND stars.person_id = people.id
AND title = "Toy Story";