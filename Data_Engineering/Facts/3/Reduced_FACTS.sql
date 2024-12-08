-- Lab 3: Reduced FACTS table building

-- Table we will build in this lab
--create table long_array_metrics (
--	user_id numeric,
--	month_start date,
--	metric_name text,
--	metric_array real[],
--	primary key (user_id, month_start, metric_name) 
--)
--drop table long_array_metrics;
-- delete from long_array_metrics -- delete data from table without where causes warning but can be executed 

insert into long_array_metrics
-- Create the daily aggregate function
with daily_aggregate as (

	select user_id,
		   date(event_time) as _current_date,
		   count(user_id) as num_site_hits
	from events e 
	where date(event_time) = date('2023-01-03')
	and user_id is not null 
	group by user_id, date(event_time) -- use the truncated date instead of the timestamp to avoid duplicates
),

yesterday_array as (
	select * from long_array_metrics
	where month_start = date('2023-01-01')
)
select coalesce(da.user_id, ya.user_id) as user_id,
	   coalesce(ya.month_start, date_trunc('month', da._current_date)) as month_start,
	   'site_hits' as metric_name,
	   case when ya.metric_array is not null then -- if the user alrady exists
	   		ya.metric_array || array[coalesce(da.num_site_hits, 0)] -- we concat the yesterday data to the array
	   when ya.metric_array is null then -- the user does not already exist
--	   		array[coalesce(da.num_site_hits, 0)] -- if we only fill the today value then the non existing yesterday value does not appear in the array which is bad
	   -- so we need to add the empty yesterday value
	   array_fill(0, array[coalesce(_current_date - date(date_trunc('month', _current_date)), 0)]) || array[coalesce(da.num_site_hits, 0)] -- fill the array with zeros for the previous days where the user did not exist
	   -- important note date_trunc needs to be cast to date since it returns a timestamp and not a date
	   end as metric_array
from daily_aggregate da
full outer join yesterday_array ya -- we make a full outer join to add only the yesterday values we still do not have in the yesterday array
on da.user_id = ya.user_id -- basically every data modelling problem can be solved wuth full outer joins 
on conflict (user_id, month_start, metric_name)
do 
	update set metric_array = excluded.metric_array;

-- check the cardinality of the metric_array column
--select cardinality(metric_array),
--	   count(1)
--from long_array_metrics
--	   group by 1

-- We want to aggregate and do a dimensional daily analysis from the monthly 
with agg as (
	select metric_name,
		   month_start,
		   array[sum(metric_array[1]),
		   sum(metric_array[2]),
		   sum(metric_array[3])
		  ] as summed_array
	from long_array_metrics
	group by metric_name, month_start
)

select metric_name,
	   date(month_start + cast(cast(index - 1 as text) || 'day' as interval)) as date, -- postgres indexing starts with 1
	   elem as value
from agg 
	cross join unnest(agg.summed_array) 
		with ordinality as a(elem, index) 






