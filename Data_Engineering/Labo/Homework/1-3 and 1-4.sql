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
-- Single query to backfill the SCD table

-- First step: create the create actors_scd table
create table actors_history_scd(
	actor_name text,
	actor_id text,
    quality_class quality_class, -- column to track
    is_active boolean, -- column to track
    start_date int, -- add the start date of the actor's carreer because SCD type 2
    end_date int, -- add the end date of the actor's carreer because SCD type 2
    current_year int, 
    PRIMARY KEY(actor_name, actor_id, start_date)
)
drop table actors_history_scd;

-- Insert the values into the scd table
insert into actors_history_scd
-- Create a CTE called with_previous to store the previous data
with with_previous as (
    -- Use a window function to get the data from the previous season for the comparison
    select 
        actor_name,
        actor_id,
        current_year,
        quality_class,
        is_active,
        lag(quality_class, 1) over (partition by actor_name order by current_year) as previous_quality_class,
        lag(is_active, 1) over (partition by actor_name order by current_year) as previous_is_active
    from actors
),
with_indicator as (
	-- Select data from the CTE and create an indicator if a change in either is_active or quality_class appears between two consecutive years
	select *,
		case 
			when quality_class <> previous_quality_class then 1
			when is_active <> previous_is_active then 1
			else 0
		end as change_indicator
	from with_previous
),
-- Create a CTE to find the streak of change indicators
with_streak as (
select *,
	sum(change_indicator)
		over (partition by actor_name order by current_year rows BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ) AS streak_identifier
	from with_indicator
)
select
	actor_name,
	actor_id,
	quality_class,
	is_active,
	min(current_year) as start_year_of_streak,
	max(current_year) as end_year_of_streak,
	2022 as current_year
from with_streak
group by 
	actor_name,
	actor_id,
	streak_identifier,
	is_active,
	quality_class
order by actor_name, streak_identifier asc;

select * from actors_history_scd;