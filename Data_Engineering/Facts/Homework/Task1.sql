-- Homework for FACT data modeling

-- First task is to deduplicate the game_details table
with row_num as (
    select 
        gd.*,
        row_number() over ( -- row number assigns a unique row number to each record within the same group
            partition by gd.game_id, gd.team_id, gd.player_id -- the group is defined by the partition by keyword
            order by gd.game_id -- if there are duplicates they will be assigned different row numbers
        ) as row_num
    from game_details gd
),
deduplication as (
	select * -- this CTE filters to only show the first row number of each record
	from row_num
	where row_num = 1
)
select game_id,
	   team_id,
	   team_abbreviation,
	   team_city,
	   player_id,
	   player_name,
	   nickname,
	   start_position,
	   comment,
	   min,
	   fgm,
	   fga,
	   fg_pct,
	   fg3m,
	   fg3a,
	   fg3_pct,
	   ftm,
	   fta,
	   ft_pct,
	   oreb,
	   dreb,
	   reb,
	   ast,
	   stl,
	   blk,
	   "TO" as turnovers,
	   pf,
	   pts,
	   plus_minus
from deduplication;

