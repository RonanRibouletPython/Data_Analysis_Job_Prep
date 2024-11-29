-- Last task of the first homework is to use an incremental approach to backfill the scd
-- table

-- Setup: Backfill the SCD table until last_year - 1 = 2021 - 1 = 2020 and
-- Create an SCD type
--create type actors_scd_type as (
--	quality_class quality_class,
--	is_active bool,
--	start_year int,
--	end_year int
--)

-- First step is to select the actors whose streak ends in 2020
with last_year_scd as (
	select * 
	from actors_history_scd ahs 
	where current_year = 2020
	and end_date = 2020
),
-- Second step take the historical data so before last year
historical_scd as(
select actor_name,
	   actor_id,
	   quality_class,
	   is_active,
	   start_date,
	   end_date
from actors_history_scd ahs
where current_year = 2020
and end_date < 2020
),
-- Select the actors from the last season so 2021 from the actors table
this_year_data as (
select * from actors
where current_year = 2021
),

-- Now let's identify records unchanged between years in the past and 2021
records_unchanged as (
	select ty.actor_name,
		   ty.actor_id,
		   ty.quality_class,
		   ty.is_active,
		   ly.start_date,
		   ty.current_year as end_date
	from this_year_data ty
	join last_year_scd ly
	on ty.actor_name = ly.actor_name and ty.actor_id = ly.actor_id
	where ty.quality_class = ly.quality_class
	and ty.is_active = ly.is_active
),

-- Records that have been changed or added last year
changed_records as (
select ty.actor_name,
       ty.actor_id,
	   unnest(array[
	   		-- first row with data until 2020
	   		row(
	   			ly.quality_class,
	   			ly.is_active,
	   			ly.start_date,
	   			ly.end_date
	   		)::actors_scd_type,
	   		-- second row with data from last year
	   		row(
	   			ty.quality_class,
	   			ty.is_active,
	   			ty.current_year,
	   			ty.current_year
	   		)::actors_scd_type
	   		]) as records
	   	from this_year_data ty
	   	left join last_year_scd ly
	   	on ty.actor_name = ly.actor_name and ty.actor_id = ly.actor_id
	   	where ty.quality_class <> ly.quality_class
	   	or ty.is_active <> ly.is_active
	   	or ty.actor_name is null
	   	or ty.actor_id is null
),

-- You can extract individual data from the new records like that
unnested_changed_records as (
	select actor_name,
		   actor_id,
		   (records).quality_class,
		   (records).is_active,
		   (records).start_year,
		   (records).end_year
	from changed_records
		   

),
--select * from unnested_changed_records
-- Add the new actors that starts in the last year
new_records as (
select ty.actor_name,
	   ty.actor_id,
	   ty.quality_class,
	   ty.is_active,
	   ty.current_year as start_year,
	   ty.current_year as end_year
from this_year_data ty
left join  last_year_scd ly
on ty.actor_name = ly.actor_name and ty.actor_id = ly.actor_id
where ly.actor_name is null
)

-- Combine all the results
select * 
from historical_scd
union all
select *
from records_unchanged
union all
select * 
from unnested_changed_records
union all 
select * 
from new_records
	   		
	   		
	   		
	   		
	   		
	   		
