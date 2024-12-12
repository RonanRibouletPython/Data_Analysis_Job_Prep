-- Now the whole user_devices_cumulated is populated for the month of January
 
-- Next task is to create the A datelist_int generation query
-- And convert the active_days column into a datelist_int column

-- Generate a datelist_int column from the active_days column
with users as (
	select * 
	from user_devices_cumulated udc
	where _current_date = date('2023-01-31')
),
date_series as (
	-- Generate a series of dates between January 1st and January 31st
	select generate_series(date('2023-01-01'), date('2023-01-31'), interval '1 day')::date as date_serie
),
integer_values as (
	select 
		user_id,
		browser_type,
		date_serie,
		-- Calculate the placeholder integer value for each date
		case 
			when active_days @> array[date_serie]
			then power(2, (date_serie - date('2023-01-01')))
			else 0 
		end as placeholder_int_value
	from users 
	cross join date_series
)
select
	cast(cast(sum(placeholder_int_value) as bigint) as bit(32)) as datelist_int, -- Ensure output column is `datelist_int`
	user_id,
	browser_type
from integer_values
group by user_id,
	     browser_type;
