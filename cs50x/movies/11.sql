SELECT title FROM stars, people, movies, ratings
WHERE person_id = people.id
AND stars.movie_id = movies.id
AND ratings.movie_id = movies.id
AND name = "Chadwick Boseman"
ORDER BY rating DESC LIMIT 5;