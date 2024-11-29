-- 1. Create a custom ENUM type for vertex types
create type vertex_type as enum('player', 'team', 'game');

-- 2. Create the vertices table to store different entities (players, teams, games)
create table vertices(
    identifier text,                       -- Unique identifier for the vertex
    type vertex_type,                      -- Type of the vertex: player, team, or game
    properties json,                        -- JSON field to store additional properties
    primary key (identifier, type)         -- Composite primary key on identifier and type
);

-- 3. Create a custom ENUM type for edge types
create type edge_type as enum(
    'plays_against',                       -- When players play against each other
    'shares_team',                         -- When players share the same team
    'plays_in',                            -- When a player plays in a game
    'plays_on'                             -- When a player plays on a team
);

-- 4. Drop the existing edge table if it exists
drop table edge;

-- 5. Create the edge table to store relationships between vertices (players, teams, and games)
create table edge(
    subject_identifier text,               -- Identifier of the subject vertex (player, team, etc.)
    subject_type vertex_type,              -- Type of the subject vertex (player, team, etc.)
    object_identifier text,                -- Identifier of the object vertex (player, team, etc.)
    object_type vertex_type,               -- Type of the object vertex (player, team, etc.)
    edge_type edge_type,                   -- Type of the edge (plays_against, shares_team, etc.)
    properties json,                        -- JSON field to store edge-related properties
    primary key(subject_identifier,         -- Composite primary key: subject and object vertices + edge type
                subject_type,
                object_identifier,
                object_type,
                edge_type)
);

-- 6. Insert data into vertices table for games
insert into vertices 
select 
    game_id as identifier,                           -- Game ID as the unique identifier
    'game'::vertex_type as type,                     -- Set type as 'game'
    json_build_object(                               -- Create a JSON object for the properties
        'pts_home', pts_home,                        -- Points scored by the home team
        'pts_away', pts_away,                        -- Points scored by the away team
        'winning_team', case when home_team_wins = 1  -- Winning team based on the home_team_wins flag
            then home_team_id else visitor_team_id end
    ) as properties
from games g;

-- 7. Insert data into vertices table for players with aggregation
WITH players_agg AS (
    SELECT 
        player_id AS identifier,                   -- Player ID as the unique identifier
        MAX(player_name) AS player_name,            -- Get the maximum player name
        COUNT(1) AS number_of_games,                -- Count the number of games played by the player
        SUM(pts) AS total_points,                   -- Sum the total points scored by the player
        ARRAY_AGG(DISTINCT team_id) AS teams        -- Aggregate distinct team IDs the player has been part of
    FROM game_details gd
    GROUP BY player_id
)
insert into vertices 
select 
    identifier, 
    'player'::vertex_type,                        -- Set type as 'player'
    jsonb_build_object(                           -- Create a JSON object for player properties
        'player_name', player_name,               -- Player's name
        'number_of_games', number_of_games,       -- Total number of games played
        'total_points', total_points,             -- Total points scored
        'teams', teams                             -- List of teams the player has been part of
    )
from players_agg;

-- 8. Insert data into vertices table for teams with deduplication (in case of duplicate entries)
WITH teams_deduped AS (
    select *, row_number() over(partition by team_id) as row_number  -- Assign row numbers to remove duplicates
    from teams
)
insert into vertices 
select 
    team_id as identifier,                          -- Team ID as the unique identifier
    'team'::vertex_type,                            -- Set type as 'team'
    jsonb_build_object(                             -- Create a JSON object for team properties
        'abbreviation', abbreviation,               -- Team abbreviation
        'nickname', nickname,                       -- Team nickname
        'city', city,                               -- Team city
        'arena', arena,                             -- Arena where the team plays
        'year_founded', yearfounded                 -- Year the team was founded
    )
from teams_deduped
where row_number = 1;                            -- Only insert the first row (deduplicated)

-- 9. Count the number of vertices by type
select type, count(1)
from vertices v 
group by 1;

-- 10. Deduplicate game details and insert 'plays_in' edges between players and games
WITH deduped AS (
    select *, row_number() over(partition by player_id, game_id) as row_number
    from game_details
)
insert into edge
select 
    player_id as subject_identifier,               -- Player ID as subject identifier
    'player'::vertex_type as subject_type,         -- Set type as 'player'
    game_id as object_identifier,                  -- Game ID as object identifier
    'game'::vertex_type as object_type,            -- Set type as 'game'
    'plays_in'::edge_type as edge_type,            -- Set edge type as 'plays_in'
    jsonb_build_object(                            -- Create a JSON object for edge properties
        'start_position', start_position,         -- Starting position of the player
        'pts', pts,                               -- Points scored by the player
        'team_id', team_id,                       -- Team ID of the player
        'team_abbreviation', team_abbreviation     -- Abbreviation of the team
    ) as properties
from deduped
where row_number = 1;                            -- Only insert the first row for each player-game pair

-- 11. Debugging data quality issues for duplicate player-game entries (example)
-- This part is commented out but provides insight into potential data quality issues:
-- select * from game_details gd where player_id = 1628960 and game_id = 22000069;

-- 12. Identify duplicate player-game entries
select player_id, game_id, count(1)
from game_details gd 
group by 1, 2
order by count asc;

-- 13. Deduplicate player vs player edges with aggregation and row_number() to handle duplicates
WITH deduped AS (
    select *, row_number() over(partition by player_id, game_id) as row_number
    from game_details
),
filtered AS (
    select *
    from deduped
    where row_number = 1
),
aggregated AS (
    select
        f1.player_id as subject_player_id,
        f1.team_abbreviation as subject_team_abbreviation,
        f2.player_id as object_player_id,
        f2.team_abbreviation as object_team_abbreviation,
        case when f1.team_abbreviation = f2.team_abbreviation
            then 'shares_team'::edge_type
        else 'plays_against'::edge_type
        end as edge_type,                           -- Edge type based on whether they share a team or play against each other
        MAX(f1.player_name) as subject_player_name,
        MAX(f2.player_name) as object_player_name,
        count(1) as num_games,                      -- Total number of games played together
        sum(f1.pts) as subject_points,              -- Total points scored by the subject player
        sum(f2.pts) as object_points               -- Total points scored by the object player
    from filtered f1
    join filtered f2
        on f1.game_id = f2.game_id                -- Ensure they played in the same game
        and f1.player_name <> f2.player_name      -- Ensure they are different players
    where f1.player_id > f2.player_id           -- Avoid duplicate edges (e.g., Tony Parker vs Kobe Bryant)
    group by 
        f1.player_id,
        f2.player_id,
        f1.team_abbreviation,
        f2.team_abbreviation,
        case when f1.team_abbreviation = f2.team_abbreviation
            then 'shares_team'::edge_type
        else 'plays_against'::edge_type
        end
),
-- 14. Deduplicate the aggregated result using ROW_NUMBER()
final_aggregated AS (
    select
        subject_player_id,
        'player'::vertex_type as subject_type,          -- Set subject type as 'player'
        object_player_id,
        'player'::vertex_type as object_type,           -- Set object type as 'player'
        edge_type,
        jsonb_build_object(                             -- Create a JSON object for edge properties
            'num_games', num_games,
            'subject_points', subject_points,
            'object_points', object_points
        ) as properties,
        row_number() over (partition by subject_player_id, object_player_id, edge_type order by subject_player_id, object_player_id) as rn -- Ensure deduplication
    from aggregated
)
-- 15. Insert only the first row for each combination of (subject_player_id, object_player_id, edge_type)
insert into edge
select 
    subject_player_id as subject_identifier,
    subject_type,
    object_player_id as object_identifier,
    object_type,
    edge_type,
    properties
from final_aggregated
where rn = 1;

--
