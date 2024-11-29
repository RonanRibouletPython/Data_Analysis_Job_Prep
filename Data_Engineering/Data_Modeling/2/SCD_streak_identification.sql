-- Lab preparation

--drop table players;
--
----DROP TYPE scoring_class CASCADE;
--
--CREATE TYPE scoring_class AS ENUM('star', 'good', 'average', 'bad');
--
--CREATE TABLE players (
--    player_name TEXT,         -- Player's name
--    height TEXT,              -- Player's height
--    college TEXT,             -- College the player attended
--    country TEXT,             -- Player's country
--    draft_year TEXT,         -- Year the player was drafted
--    draft_round TEXT,        -- Round the player was drafted in
--    draft_number TEXT,       -- Draft number of the player
--    season_stats season_stats[], -- Array of season statistics for the player
--    scoring_class scoring_class,  -- Player's scoring grade (A, B, C, etc.)
--    years_since_last_season INTEGER, -- Years since the player's last season
--    current_season INTEGER,   -- The current season of the player
--    is_active BOOLEAN,
--    PRIMARY KEY(player_name, current_season) -- Primary key is a combination of player name and current season
--);
--
--
--INSERT INTO players
--WITH years AS (
--    SELECT *
--    FROM GENERATE_SERIES(1996, 2022) AS season
--), p AS (
--    SELECT
--        player_name,
--        MIN(season) AS first_season
--    FROM player_seasons
--    GROUP BY player_name
--), players_and_seasons AS (
--    SELECT *
--    FROM p
--    JOIN years y
--        ON p.first_season <= y.season
--), windowed AS (
--    SELECT
--        pas.player_name,
--        pas.season,
--        ARRAY_REMOVE(
--            ARRAY_AGG(
--                CASE
--                    WHEN ps.season IS NOT NULL
--                        THEN ROW(
--                            ps.season,
--                            ps.gp,
--                            ps.pts,
--                            ps.reb,
--                            ps.ast
--                        )::season_stats
--                END)
--            OVER (PARTITION BY pas.player_name ORDER BY COALESCE(pas.season, ps.season)),
--            NULL
--        ) AS seasons
--    FROM players_and_seasons pas
--    LEFT JOIN player_seasons ps
--        ON pas.player_name = ps.player_name
--        AND pas.season = ps.season
--    ORDER BY pas.player_name, pas.season
--), static AS (
--    SELECT
--        player_name,
--        MAX(height) AS height,
--        MAX(college) AS college,
--        MAX(country) AS country,
--        MAX(draft_year) AS draft_year,
--        MAX(draft_round) AS draft_round,
--        MAX(draft_number) AS draft_number
--    FROM player_seasons
--    GROUP BY player_name
--)
--SELECT
--    w.player_name,
--    s.height,
--    s.college,
--    s.country,
--    s.draft_year,
--    s.draft_round,
--    s.draft_number,
--    seasons AS season_stats,
--    CASE
--        WHEN (seasons[CARDINALITY(seasons)]::season_stats).pts > 20 THEN 'star'
--        WHEN (seasons[CARDINALITY(seasons)]::season_stats).pts > 15 THEN 'good'
--        WHEN (seasons[CARDINALITY(seasons)]::season_stats).pts > 10 THEN 'average'
--        ELSE 'bad'
--    END::scoring_class AS scoring_class,
--    w.season - (seasons[CARDINALITY(seasons)]::season_stats).season as years_since_last_active,
--    w.season,
--    (seasons[CARDINALITY(seasons)]::season_stats).season = season AS is_active
--FROM windowed w
--JOIN static s
--    ON w.player_name = s.player_name;


create table players_scd(
	player_name text,
	scoring_class scoring_class,
	is_active bool,
	start_season integer,
	end_season integer,
	current_season integer,
	primary key(player_name, start_season)
)

insert into players_scd
WITH with_previous AS (
    SELECT 
        player_name,
        current_season,
        scoring_class,
        is_active,
        LAG(scoring_class, 1) OVER (PARTITION BY player_name ORDER BY current_season) AS previous_scoring_class,
        LAG(is_active, 1) OVER (PARTITION BY player_name ORDER BY current_season) AS previous_is_active
    FROM players
    WHERE current_season <= 2021 -- filter for earlier than 2021 to use 2022 data later
),
with_indicators AS (
    SELECT *, 
        CASE
            WHEN scoring_class <> previous_scoring_class THEN 1
            WHEN is_active <> previous_is_active THEN 1
            ELSE 0
        END AS change_indicator
    FROM with_previous
),
with_streaks AS (
    SELECT *, 
        SUM(change_indicator) 
            OVER (PARTITION BY player_name ORDER BY current_season ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS streak_identifier
    FROM with_indicators
)
SELECT 
    player_name,
    scoring_class,
    is_active, 
    MIN(current_season) AS start_season, 
    MAX(current_season) AS end_season,
    2021 as current_season
FROM with_streaks
GROUP BY 
    player_name, 
    streak_identifier, 
    is_active, 
    scoring_class
ORDER BY player_name, streak_identifier;

select * from players_scd;

--Slowly Changing Dimensions (SCD): The players_scd table is used to track changes in player attributes over time.
--Instead of overwriting data, it keeps historical records of changes (like scoring class, active status) so we can see how a player's performance evolves.
--
--Window Functions (LAG and SUM): These are used to look at the previous season's data and track changes across seasons.
--The LAG function allows us to compare the current row with the previous one, while SUM is used to group consecutive rows with similar values.
--
--Change Detection: The change_indicator field identifies if a player's scoring class or active status has changed between seasons. 
--This helps to track periods of consistency or change in the player's performance or status.




