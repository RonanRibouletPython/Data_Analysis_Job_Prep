-- In this second lab we will work with events table
-- This lab focuses on how to build a datelist data type 

--select min(event_time) as min_date,
--	   max(event_time) as max_date
--from events e 
--
-- Create a table for the cumulated users
--create table users_cumulated (
--	user_id text, -- bigint instead of int because user_id is over the limit of integers
--	dates_active date[], -- list pf the dates in the past where the user was active
--	_current_date date, -- current date 
--	primary key(user_id, _current_date)
--)
--drop table users_cumulated;

--insert into users_cumulated
--with yesterday as(
--	select *
--	from users_cumulated 
--	where _current_date = date('2023-01-31') -- day before the first day of the events table 
--),
--	today as(
--	select cast(user_id as text),
--		   date(cast(event_time as timestamp)) as date_active
--	from events e 
--	where date(cast(event_time as timestamp)) = date('2023-02-01') -- cast the string data as a timestamp for the match to work
--	and user_id is not null
--	group by user_id,
--		 	 date_active
--)
--
---- outer join on yesterday and today to add the new data
---- we want this query to match the schema of table users_cumulated
--select coalesce(t.user_id, y.user_id), -- take the first data between the today or yesterday user_id
--	   -- collect the array of values with multiple cases
--	   -- first case: 
--	   case 
--		   -- if the user was not active yesterday but active today add only the today date
--		   when y.dates_active is null 
--	       then array [t.date_active]
--	       -- if the user is not active today then put the yesterday date
--	       when t.date_active is null then y.dates_active
--	       -- if the user was active yesterday and is still active today then concatenate both dates to the array
--	       else array [t.date_active] || y.dates_active
--	       end as dates_active,
--	   coalesce(t.date_active, y._current_date + interval '1 day') as _current_date
--	   
--	from today t full outer join  yesterday y
--	on y.user_id = t.user_id 

with users as (
    -- Data for the bit mapping done 
    select * from users_cumulated
    where _current_date = date('2023-01-31')
),
date_series as (
    -- generate a series between jan 2nd and jan 31st, explicitly casting as date
    select generate_series(date('2023-01-01'), date('2023-01-31'), interval '1 day')::date as date_serie
),
placeholder_ints as (
	select 
    case 
        when dates_active @> array[date_serie]
        then power(2, 32 - (_current_date - date_serie))
        else 0 
    end as placeholder_int_value,
    *
	from users 
	cross join date_series
--	where user_id = '17155952271109500000'

)

select user_id,
	   cast(cast(sum(placeholder_int_value) as bigint) as bit(32)) as bit_user_active,
	   bit_count(cast(cast(sum(placeholder_int_value) as bigint) as bit(32))) > 0 as dim_is_monthly_active,
	   -- use bitweise AND to notice the activity in different days
	   bit_count(cast('1' as bit(32)) & cast(cast(sum(placeholder_int_value) as bigint) as bit(32))) > 0 as active_on_last_day
from placeholder_ints
group by user_id



	