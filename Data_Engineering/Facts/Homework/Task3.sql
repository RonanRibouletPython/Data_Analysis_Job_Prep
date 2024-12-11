-- Task 2 of the creation of the DDL for table user_devices_cumulated

-- duplicates in events
-- Create the table 
create table user_devices_cumulated (
	user_id text,
	browser_type text,
	active_days date[],
	_current_date date,
	primary key(user_id, browser_type, _current_date)
)
-- drop table user_devices_cumulated;
delete from user_devices_cumulated udc;

-- Get the minimum date 
select min(event_time) as min_date,
	   max(event_time) as max_date
from events e 

-- Create the cumulative query to populate the device_activity_datelist
-- which tracks a users active days by browser_type

insert into user_devices_cumulated
-- Query the user_devices_cumulated with yesterday values
with yesterday as (
	select * 
	from user_devices_cumulated udc 
	where _current_date = date('2023-01-06') -- day before the first day of the events table
),
today as (
	select 
	    cast(e.user_id as text) AS user_id,
	    date(e.event_time) AS date_active, 
	    d.browser_type
	from 
	    events e
	join 
	    devices d
	    on e.device_id = d.device_id
	where 
	    e.user_id is not null 
	    and date(e.event_time) = '2023-01-07'
	group by user_id,
			 date_active,
			 d.browser_type
)
-- Outer join the yesterday and today data to populate the user_devices_cumulated table
select coalesce(t.user_id, y.user_id) as user_id,
	   coalesce(t.browser_type, y.browser_type) as browser_type,
	   case
		    when y.active_days is null then array [t.date_active]
		    when t.date_active is null then y.active_days
		    else y.active_days || array [t.date_active]
		end as dates_active,
	   coalesce(t.date_active, y._current_date + interval '1 day') as _current_date
--	   
from today t full outer join  yesterday y
on y.user_id = t.user_id and t.browser_type = y.browser_type

	   
 select * from user_devices_cumulated udc;
	     



