CREATE TEMP TABLE year_range AS
SELECT generate_series(
    (SELECT MIN(year) - 1 FROM actor_films),
    (SELECT MAX(year) FROM actor_films),
    1
) AS year;

DO $$
DECLARE
    yr INT; -- Holds the current year in the loop
BEGIN
    -- Loop through each year in the generated range
    FOR yr IN SELECT year FROM year_range LOOP
        -- Insert aggregated data for the current year
        WITH yesterday AS (
            SELECT * FROM actors WHERE current_year = yr - 1
        ),
        today AS (
            SELECT 
                actor, actorid,
                ARRAY_AGG(ROW(film, votes, rating, filmid)::films) AS films_array,
                AVG(rating) AS avg_rating, year
            FROM actor_films
            WHERE year = yr
            GROUP BY actor, actorid, year
        )
        INSERT INTO actors (actor_name, actor_id, films, quality_class, is_active, current_year)
        SELECT 
            COALESCE(t.actor, y.actor_name), 
            COALESCE(t.actorid, y.actor_id),
            COALESCE(t.films_array, y.films),
            CASE 
                WHEN t.year IS NOT NULL THEN
                    CASE 
                        WHEN t.avg_rating > 8 THEN 'star'::quality_class
                        WHEN t.avg_rating > 7 THEN 'good'::quality_class
                        WHEN t.avg_rating > 6 THEN 'average'::quality_class
                        ELSE 'bad'::quality_class 
                    END
                ELSE y.quality_class
            END,
            t.year IS NOT NULL AS is_active,
            COALESCE(t.year, y.current_year + 1) AS current_year
        FROM today t
        FULL OUTER JOIN yesterday y
        ON t.actor = y.actor_name AND t.actorid = y.actor_id;
    END LOOP;
END $$;



select	actor_name, 
		quality_class,
		is_active
from actors a
where current_year = 1970
order by actor_name asc;

 

-- New task to do is create a table with type 2 Slowly Changing Dimension (SCD)
-- 2 features need to be tracked the quality class and the is_active
-- We need to add a start_date and an end_date 

-- First step: create the create actors_scd table
create table actors_history_scd(
	actor_name text,
    actor_id text,
    films films[],
    quality_class quality_class, -- column to track
    is_active boolean, -- column to track
    current_year int, 
    start_date int, -- add the start date of the actor's carreer because SCD type 2
    end_date int, -- add the end date of the actor's carreer because SCD type 2
    PRIMARY KEY(actor_name, start_date)
)


