-- Create type scd_type as before (uncomment this part when you need to create the type)
-- create type scd_type as (
--     scoring_class scoring_class, -- Type to store the player's scoring grade
--     is_active bool,              -- Type to store whether the player is currently active
--     start_season integer,        -- Type to store the starting season of the player's streak
--     end_season integer           -- Type to store the ending season of the player's streak
-- )

-- Step 1: Select the players whose streak ended in 2021
with last_season_scd as (
    select * 
    from players_scd
    where current_season = 2021  -- Filter for the 2021 season
    and end_season = 2021        -- Ensure the streak ended in 2021
),

-- Step 2: Select players whose streak ended before 2021 (historical data)
historical_scd as (
    select player_name,           -- Player name
           scoring_class,         -- Scoring class (grade)
           is_active,              -- Is the player still active?
           start_season,           -- The season when the streak started
           end_season              -- The season when the streak ended
    from players_scd
    where current_season = 2021  -- Filter for the 2021 season
    and end_season < 2021        -- The streak ended before 2021
),

-- Step 3: Select all players for the 2022 season
this_season_data as (
    select * 
    from players p 
    where current_season = 2022  -- Filter for the 2022 season
),

-- Step 4: Identify unchanged records between 2021 and 2022
unchanged_records as (
    select ts.player_name,        -- Player name
           ts.scoring_class,      -- Scoring class (grade)
           ts.is_active,          -- Active status
           ls.start_season,       -- The start season of the streak
           ts.current_season as end_season -- The end season of the streak (same as the current season)
    from this_season_data ts 
    join last_season_scd ls      -- Join with the data from the 2021 season
    on ls.player_name = ts.player_name
    where ts.scoring_class = ls.scoring_class  -- Ensure scoring class hasn't changed
    and ts.is_active = ls.is_active          -- Ensure active status hasn't changed
),

-- Step 5: Identify changed records (scoring class or active status changed, or new players in 2022)
changed_records as (
    select ts.player_name,                          -- Player name
           unnest(array[                           -- Unnest the array to create two rows for each change
               -- First row: 2021 record (player info from the last season)
               row(
                   ls.scoring_class, 
                   ls.is_active, 
                   ls.start_season, 
                   ls.end_season
               )::scd_type,                        -- Cast to scd_type
               -- Second row: 2022 record (player info for the current season)
               row(
                   ts.scoring_class, 
                   ts.is_active, 
                   ts.current_season, 
                   ts.current_season
               )::scd_type                         -- Cast to scd_type
           ]) as records                              -- Generate an array of two records
    from this_season_data ts 
    left join last_season_scd ls       -- Left join to ensure that we also get players who didn't exist in 2021
    on ls.player_name = ts.player_name
    where ts.scoring_class <> ls.scoring_class   -- If the scoring class has changed
       or ts.is_active <> ls.is_active         -- If the active status has changed
       or ls.player_name is NULL               -- If the player is new and doesn't exist in the 2021 data
),

-- Step 6: Unnest the array created in the previous step to extract individual records
unnested_changed_records as (
    select player_name,                         -- Player name
           (records).scoring_class,            -- Extract scoring class from the record
           (records).is_active,                -- Extract active status from the record
           (records).start_season,             -- Extract start season from the record
           (records).end_season                -- Extract end season from the record
    from changed_records
),

-- Step 7: Identify new records (players who are new in 2022 and didn't exist in 2021)
new_records as (
    select ts.player_name,             -- Player name
           ts.scoring_class,           -- Scoring class (grade)
           ts.is_active,               -- Active status
           ts.current_season as start_season, -- The start season for new players is the current season (2022)
           ts.current_season as end_season   -- The end season is also the current season (2022)
    from this_season_data ts 
    left join last_season_scd ls on ts.player_name = ls.player_name
    where ls.player_name is NULL  -- The player didn't exist in 2021 (i.e., new player in 2022)
)

-- Step 8: Combine all the results from the above steps into one result
select * 
from historical_scd                 -- Include historical records (players whose streak ended before 2021)
union all 
select * from unchanged_records      -- Include unchanged records (players whose data stayed the same)
union all
select * from unnested_changed_records -- Include changed records (players whose data changed)
union all
select * from new_records            -- Include new records (players who didn't exist in 2021)
