-- New task: A DDL for hosts_cumulated table
-- with a host_activity_datelist which logs to see which dates
-- each host is experiencing any activity

-- Create the DDL table for hosts_cumulated
--create table hosts_cumulated (
--	host text,
--	active_days date[],
--	_current_date date,
--	primary key(host, _current_date)
--)
--
--drop table hosts_cumulated;
--delete from hosts_cumulated;

-- Get the minimum date and max date
--select min(event_time) as min_date,
--	   max(event_time) as max_date
--from events e 

insert into hosts_cumulated
with yesterday as (
	select * 
	from hosts_cumulated hc 
	where _current_date = date('2023-01-31') -- day before the first day of the events table
),
today as (
	select 
	    cast(e.host as text) AS host,
	    date(e.event_time) AS date_active 
	from events e
	where 
	    e.user_id is not null 
	    and date(e.event_time) = '2023-02-01'
	group by e.host,
			 date_active
)
-- Outer join the yesterday and today data to populate the user_devices_cumulated table
select coalesce(t.host, y.host) as host,
	   case
		    when y.active_days is null then array [t.date_active]
		    when t.date_active is null then y.active_days
		    else y.active_days || array [t.date_active]
		end as dates_active,
	   coalesce(t.date_active, y._current_date + interval '1 day') as _current_date 
from today t full outer join  yesterday y
on y.host = t.host
  
 select * from hosts_cumulated hc;




