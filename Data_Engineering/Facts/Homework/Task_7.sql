-- Task 7: Create the DDL host_activity_reduced
create table host_activity_reduced (
	month_start date,
	host text,
	hit_array INTEGER[],
    unique_visitors_array INTEGER[],
    primary key(host, month_start)
)

--drop table host_activity_reduced;
--delete from host_activity_reduced;

-- Task 8 : Incremental query to load host_activity_reduced
-- TODO