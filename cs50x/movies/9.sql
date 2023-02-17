SELECT name FROM people WHERE people.id IN
(SELECT DISTINCT(person_id) FROM stars WHERE movie_id IN
(SELECT movies.id FROM movies WHERE year = 2004))
ORDER BY birth;