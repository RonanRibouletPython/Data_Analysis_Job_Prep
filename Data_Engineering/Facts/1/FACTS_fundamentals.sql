-- Lab 1 on FACT data


-- We are going to use the game_details table
--select * from game_details gd 
--
---- Identify the duplicates in the table
--select 
--	game_id,
--	team_id,
--	player_id,
--	count(1)
--from game_details gd 
--group by game_id, team_id, player_id
--having count(1) > 1 

-- Delete the duplicates off of the table and join data from game data table
--with deduplicated as (
--	select g.game_date_est,
--		   g.season,
--		   g.home_team_id,
--		   g.visitor_team_id,
--		   gd.*,
--		   row_number() over(partition by gd.game_id, team_id, player_id order by g.game_date_est) as row_num
--	from game_details gd 
--	join games g on gd.game_id = g.game_id
--)
--insert into fact_game_details
--select game_date_est as dim_game_date,
--	   season as dim_season,
--	   team_id as dim_team_id,
--	   game_id as dim_game_id,
--	   team_id = home_team_id as dim_is_playing_home,
--	   player_id as dim_player_id,
--	   player_name as dim_player_name,
--	   start_position as dim_start_position,
--	   coalesce(position('DNP' in comment), 0) > 0 as dim_did_not_play, -- create the bool column to track if a player does not play 
--	   coalesce(position('DND' in comment), 0) > 0 as dim_did_not_dress, -- we can remove the comment column since we parsed every info into boolean columns
--	   coalesce(position('NWT' in comment), 0) > 0 as dim_not_with_team,
--	   cast(split_part(min, ':', 1) as real) -- modify the string data into minutes as a float
--	   + cast(split_part(min, ':', 2) as real) / 60 as m_minutes,
--	   fgm as m_fgm,
--	   fga as m_fga,
--	   fg3a as m_fg3a,
--	   fg3m as m_fg3m,
--	   oreb as m_oreb,
--	   dreb as m_dreb,
--	   reb as m_reb,
--	   ast as m_ast,
--	   stl as m_stl,
--	   blk as m_blk,
--	   "TO" as m_turnovers, -- rename the column because to is a sql keyword
--	   pts as m_pts,
--	   plus_minus as m_plus_minus
--from deduplicated
--where row_num = 1


-- Create the DDL
-- dim columns are the one you should group by or filter on
-- m columns are the one where you should do aggregations and statistical analysis
--create table fact_game_details (
--	dim_game_date date,
--	dim_season int,
--	dim_team_id int,
--	dim_game_id int,
--	dim_is_playing_home bool,
--	dim_player_id int,
--	dim_player_name text,
--	dim_start_position text,
--	dim_did_not_play bool,
--	dim_did_not_dress bool,
--	dim_not_with_team bool,
--	m_minutes real,
--	m_fgm int,
--	m_fga int,
--	m_fg3m int,
--	m_fg3a int,
--	m_oreb int,
--	m_dreb int,
--	m_reb int,
--	m_ast int,
--	m_stl int,
--	m_blk int,
--	m_turnovers int,
--	m_pts int,
--	m_plus_minus int,
--	primary key(dim_game_date, dim_player_id, dim_team_id)
--)

-- Join with the teams table to retrieve lost team data very fast
--select t.team_id, 
--	   t.abbreviation,
--	   t.headcoach,
--	   fgd.* 
--from fact_game_details fgd join teams t 
--	on t.team_id = fgd.dim_team_id

-- Idea behing fact modeling is to perform this kind of aggregation queries very efficiently and quickly
select dim_player_name,
	   dim_is_playing_home,
	   sum(m_pts) as most_pts
--	   count(case when dim_not_with_team then 1 end) as m_most_not_show_up
from fact_game_details fgd 
where m_pts is not null
group by dim_is_playing_home, dim_player_name
order by most_pts desc



