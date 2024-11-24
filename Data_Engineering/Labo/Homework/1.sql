-- DDL for actors table (create types and table) - Run this only ONCE
CREATE TYPE films AS (
    film TEXT,
    votes INTEGER,
    rating REAL,
    filmid text
);

CREATE TYPE quality_class AS ENUM('star', 'good', 'average', 'bad');

CREATE TABLE actors (
    actor_name text,
    actor_id text,
    films films[],
    quality_class quality_class,
    is_active boolean,
    current_year int,
    PRIMARY KEY(actor_name, current_year)
);
drop table actors

-- Get the minimum and maximum years - Run this only ONCE
SELECT MIN(year), MAX(year) FROM actor_films; -- Let's say it returns 1970 and 1975


-- Iteration 1:  (Manually adjust years in each iteration)
INSERT INTO actors (actor_name, actor_id, films, quality_class, is_active, current_year)
WITH yesterday AS (
    SELECT * FROM actors WHERE current_year = 1973 - 1  -- No data initially, so empty
),
today AS (
    SELECT 
        actor, actorid,
        ARRAY_AGG(ROW(film, votes, rating, filmid)::films) AS films_array,
        AVG(rating) AS avg_rating, year
    FROM actor_films
    WHERE year = 1972  -- First year's data
    GROUP BY actor, actorid, year
)
SELECT COALESCE(t.actor, y.actor_name), COALESCE(t.actorid, y.actor_id), 
       COALESCE(t.films_array, y.films),
       CASE WHEN t.year IS NOT NULL THEN
           CASE WHEN t.avg_rating > 8 THEN 'star'::quality_class
                WHEN t.avg_rating > 7 THEN 'good'::quality_class
                WHEN t.avg_rating > 6 THEN 'average'::quality_class
                ELSE 'bad'::quality_class END
           ELSE y.quality_class
       END,
       t.year IS NOT null as is_active,
       COALESCE(t.year, y.current_year + 1) as current_year 
       
FROM today t FULL OUTER JOIN yesterday y ON t.actor = y.actor_name;

select * from actors a 