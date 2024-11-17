-- Create the custom type for season statistics
CREATE TYPE season_stats AS (
    season INTEGER,  -- Season number
    gp INTEGER,      -- Games played
    pts REAL,        -- Points scored
    reb REAL,        -- Rebounds
    ast REAL         -- Assists
);

-- Create the custom type for scoring grades (A, B, C, D, E, F)
CREATE TYPE scoring_grade AS ENUM('A', 'B', 'C', 'D', 'E', 'F');

-- Drop the players table if it exists (commented out)
-- DROP TABLE players;

-- Create the players table with columns to hold player data
CREATE TABLE players (
    player_name TEXT,         -- Player's name
    height TEXT,              -- Player's height
    college TEXT,             -- College the player attended
    country TEXT,             -- Player's country
    draft_year TEXT,         -- Year the player was drafted
    draft_round TEXT,        -- Round the player was drafted in
    draft_number TEXT,       -- Draft number of the player
    season_stats season_stats[], -- Array of season statistics for the player
    scoring_grade scoring_grade,  -- Player's scoring grade (A, B, C, etc.)
    years_since_last_season INTEGER, -- Years since the player's last season
    current_season INTEGER,   -- The current season of the player
    PRIMARY KEY(player_name, current_season) -- Primary key is a combination of player name and current season
);

-- Insert data into the players table, comparing data from two seasons (2000 and 2001)
INSERT INTO players
WITH yesterday AS (
    -- Select all players from the 2000 season in the players table
    SELECT * 
    FROM players
    WHERE current_season = 2000
),
today AS (
    -- Select all players from the 2001 season in the player_seasons table
    SELECT * 
    FROM player_seasons
    WHERE season = 2001
)
SELECT 
    -- Merge data from both 2000 and 2001 seasons using COALESCE to get the first non-null value
    COALESCE(t.player_name, y.player_name) AS player_name,
    COALESCE(t.height, y.height) AS height,
    COALESCE(t.college, y.college) AS college,
    COALESCE(t.country, y.country) AS country,
    COALESCE(t.draft_year, y.draft_year) AS draft_year,
    COALESCE(t.draft_round, y.draft_round) AS draft_round,
    COALESCE(t.draft_number, y.draft_number) AS draft_number,
    CASE 
        WHEN y.season_stats IS NULL THEN 
            -- If no data for the 2000 season, use data from 2001 season
            ARRAY[ROW(t.season, t.gp, t.pts, t.reb, t.ast)::season_stats]
        WHEN t.season IS NOT NULL THEN 
            -- If both seasons have data, merge them
            y.season_stats || ARRAY[ROW(t.season, t.gp, t.pts, t.reb, t.ast)::season_stats]
        ELSE 
            -- If no data from 2001, keep the 2000 season data
            y.season_stats
    END AS season_stats,
    CASE 
        WHEN t.season IS NOT NULL THEN
            -- Assign scoring grades based on points in 2001 season
            CASE 
                WHEN t.pts > 25 THEN 'A'::scoring_grade
                WHEN t.pts > 20 THEN 'B'::scoring_grade
                WHEN t.pts > 15 THEN 'C'::scoring_grade
                WHEN t.pts > 10 THEN 'D'::scoring_grade
                WHEN t.pts > 5 THEN 'E'::scoring_grade
                ELSE 'F'::scoring_grade
            END
        ELSE y.scoring_grade
    END AS scoring_grade,
    CASE 
        WHEN t.season IS NOT NULL THEN 0
        ELSE y.years_since_last_season + 1
    END AS years_since_last_season,
    COALESCE(t.season, y.current_season + 1) AS current_season
FROM today t
FULL OUTER JOIN yesterday y
    -- Full outer join ensures we include players from both seasons, even if they only exist in one of them
    ON t.player_name = y.player_name;

-- Select player performance data for players in the 2001 season with 'A' or 'B' scoring grades
SELECT 
    player_name,
    (season_stats[1]).pts AS first_season_pts,  -- Points in the first season
    (season_stats[cardinality(season_stats)]).pts AS latest_season_pts,  -- Points in the latest season
    -- Calculate improvement ratio based on points between the first and latest seasons
    ((season_stats[cardinality(season_stats)]).pts / 
        CASE 
            WHEN (season_stats[1]).pts = 0 THEN 1  -- Avoid division by zero if points in the first season is 0
            ELSE (season_stats[1]).pts
        END) AS improvement_ratio
FROM players p
WHERE current_season = 2001 
  AND scoring_grade IN ('A', 'B')
--ORDER BY improvement_ratio DESC;  -- Uncomment to order by improvement ratio in descending order

-- Select player data for 'Michael Jordan' in the 2000 season
SELECT * 
FROM players 
WHERE player_name LIKE 'Michael Jordan%' 
  AND current_season = 2000;

-- Unnest the season_stats array and display individual season stats for 'Michael Jordan' in the 2001 season
SELECT player_name,
       unnest(season_stats) AS season_stats
FROM players
WHERE current_season = 2001

-- Another approach to unnesting and displaying season stats for 'Michael Jordan'
WITH unnested AS (
    SELECT player_name,
           unnest(season_stats)::season_stats AS season_stats
    FROM players 
    WHERE current_season = 2001
      AND player_name = 'Michael Jordan'
)
SELECT player_name,
       (season_stats::season_stats).*
FROM unnested;
