SELECT 'teams' AS table_name, COUNT(*) FROM teams
UNION ALL
SELECT 'players', COUNT(*) FROM players
UNION ALL
SELECT 'games', COUNT(*) FROM games
UNION ALL
SELECT 'player_game_stats', COUNT(*) FROM player_game_stats;



-- PLAYER STATS BY PPG DESCENDING
SELECT
    p.full_name,
    COUNT(*) AS games_played,
    t.full_name AS team_name,
    ROUND(AVG(pgs.points), 2) AS ppg,
    ROUND(AVG(pgs.rebounds), 2) AS rpg,
    ROUND(AVG(pgs.assists), 2) AS apg
FROM player_game_stats pgs
JOIN players p ON pgs.player_id = p.player_id
JOIN teams t ON t.team_id = pgs.team_id
GROUP BY p.full_name, t.full_name
HAVING COUNT(*) >= 20
ORDER BY ppg DESC
LIMIT 25;


-- TEAM PPG DESCENDING
WITH team_scores AS (
	SELECT home_team_id AS team_id, home_score AS points
	FROM games
	
	UNION ALL
	
	SELECT away_team_id AS team_id, away_score AS points
	FROM games
)
SELECT 
	t.full_name,
	ROUND(AVG(ts.points), 2) AS ppg
FROM team_scores ts
JOIN teams t
	ON t.team_id = ts.team_id
GROUP BY t.full_name
ORDER BY ppg DESC;

-- DOUBLE DOUBLES CALCULATIONS
WITH game_categories AS (
    SELECT
        player_id,
		team_id,
        points,
        rebounds,
        assists,
        steals,
        blocks,

        CASE WHEN points >= 10 THEN 1 ELSE 0 END +
        CASE WHEN rebounds >= 10 THEN 1 ELSE 0 END +
        CASE WHEN assists >= 10 THEN 1 ELSE 0 END +
        CASE WHEN steals >= 10 THEN 1 ELSE 0 END +
        CASE WHEN blocks >= 10 THEN 1 ELSE 0 END AS double_digit_categories
    FROM player_game_stats
),

double_double_games AS (
    SELECT
        player_id,
		team_id,
        CASE
            WHEN double_digit_categories >= 2 THEN 1
            ELSE 0
        END AS is_double_double
    FROM game_categories
)

SELECT
    p.full_name,
	t.full_name AS team_name,
    COUNT(*) AS games_played,
    SUM(ddg.is_double_double) AS double_doubles,
    ROUND(
        SUM(ddg.is_double_double)::numeric / COUNT(*) * 100,
        2
    ) AS double_double_rate
FROM double_double_games ddg
JOIN players p
    ON p.player_id = ddg.player_id
JOIN teams t
	ON t.team_id = ddg.team_id
GROUP BY p.full_name, t.full_name
ORDER BY double_doubles DESC;

-- Triple Doubles Calculations
WITH game_categories AS (
    SELECT
        player_id,
		team_id,
        points,
        rebounds,
        assists,
        steals,
        blocks,

        CASE WHEN points >= 10 THEN 1 ELSE 0 END +
        CASE WHEN rebounds >= 10 THEN 1 ELSE 0 END +
        CASE WHEN assists >= 10 THEN 1 ELSE 0 END +
        CASE WHEN steals >= 10 THEN 1 ELSE 0 END +
        CASE WHEN blocks >= 10 THEN 1 ELSE 0 END AS double_digit_categories
    FROM player_game_stats
),

triple_double_games AS (
    SELECT
        player_id,
		team_id,
        CASE
            WHEN double_digit_categories >= 3 THEN 1
            ELSE 0
        END AS is_triple_double
    FROM game_categories
)

SELECT
    p.full_name,
	t.full_name AS team_name,
    COUNT(*) AS games_played,
    SUM(tdg.is_triple_double) AS triple_doubles,
    ROUND(
        SUM(tdg.is_triple_double)::numeric / COUNT(*) * 100,
        2
    ) AS triple_double_rate
FROM triple_double_games tdg
JOIN players p
    ON p.player_id = tdg.player_id
JOIN teams t
	ON t.team_id = tdg.team_id
GROUP BY p.full_name, t.full_name
HAVING SUM(tdg.is_triple_double) > 0
ORDER BY triple_doubles DESC;


-- Compute player scoring statistics, rank players by average points overall and within each team, and filter to each team's top scorer using a CTE.
WITH player_rankings AS (
	SELECT
		p.full_name,
		t.full_name AS team_name,
		COUNT(*) AS games_played,
		ROUND(AVG(pgs.points), 2) AS ppg,
		RANK() OVER (
			ORDER BY AVG(pgs.points) DESC
		) AS scoring_rank,
		RANK() OVER (
			PARTITION BY pgs.team_id
			ORDER BY AVG(pgs.points) DESC
		) AS team_scoring_rank,
		MAX(pgs.points) AS max_pts,
		MIN(pgs.points) AS min_pts,
		ROUND(STDDEV(pgs.points), 4) AS std_dev
	FROM player_game_stats pgs
	JOIN players p 
		ON p.player_id = pgs.player_id
	JOIN teams t ON t.team_id = pgs.team_id
	GROUP BY p.full_name, p.player_id, pgs.team_id, t.full_name
	HAVING COUNT(*) >= 20
		AND AVG(pgs.points) >= 5
)
SELECT
	full_name,
	team_name,
	games_played,
	scoring_rank,
	ppg,
	max_pts,
	min_pts,
	std_dev
FROM player_rankings
WHERE team_scoring_rank = 1
ORDER BY team_name ASC, team_scoring_rank ASC;

-- Compare each player's scoring to their previous game and categorize the change in performance.
WITH previous_game AS(
	SELECT
	    p.full_name AS full_name,
	    pgs.game_id AS game_id,
	    pgs.points AS points,
	    LAG(pgs.points) OVER (
	        PARTITION BY pgs.player_id
	        ORDER BY pgs.game_id
	    ) AS previous_game_points
	FROM player_game_stats pgs
	JOIN players p
	    ON p.player_id = pgs.player_id
)
SELECT 
	full_name,
	game_id,
	points,
	previous_game_points,
	points - previous_game_points AS points_difference,
	CASE 
		WHEN points - previous_game_points <= -10 THEN 'Big Decline'
		WHEN points - previous_game_points >= 10 THEN 'Big Improvement'
		ELSE 'About the Same'
	END AS scoring_tier
FROM
	previous_game
WHERE
	previous_game_points IS NOT NULL;


-- Creates a rolling ten game scoring average (updates as you go)
WITH player_game_order AS (
    SELECT
        p.full_name,
        pgs.player_id,
        g.game_date,
        pgs.points
    FROM player_game_stats pgs
    JOIN players p ON p.player_id = pgs.player_id
    JOIN games g ON g.game_id = pgs.game_id
)
SELECT
    full_name,
    game_date,
    points,
    ROUND(AVG(points) OVER (
            PARTITION BY player_id
            ORDER BY game_date
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_10_game_ppg
FROM player_game_order
ORDER BY full_name, game_date;
	
	


-- Finds each player's hot-streaks above their own scoring average, using gaps-and-islands grouping
WITH player_baseline AS (
    SELECT
        player_id,
        AVG(points) AS avg_pts,
        STDDEV(points) AS stddev_pts
    FROM player_game_stats
    GROUP BY player_id
),
scoring_flags AS (
    SELECT
        p.full_name,
        pgs.player_id,
        g.game_date,
        pgs.points,
        pb.avg_pts,
        CASE
            WHEN pgs.points > pb.avg_pts + pb.stddev_pts THEN 1
            ELSE 0
        END AS is_high_scoring
    FROM player_game_stats pgs
    JOIN players p ON p.player_id = pgs.player_id
    JOIN games g ON g.game_id = pgs.game_id
    JOIN player_baseline pb ON pb.player_id = pgs.player_id
),
streak_groups AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_date)
        - ROW_NUMBER() OVER (PARTITION BY player_id, is_high_scoring ORDER BY game_date)
            AS streak_group
    FROM scoring_flags
)
SELECT
    full_name,
    COUNT(*) AS streak_length,
    MIN(game_date) AS streak_start,
    MAX(game_date) AS streak_end,
    ROUND(AVG(points), 2) AS avg_points_during_streak,
    ROUND(MAX(avg_pts), 2) AS player_season_avg
FROM streak_groups
WHERE is_high_scoring = 1
GROUP BY full_name, player_id, streak_group
HAVING COUNT(*) >= 2
ORDER BY streak_length DESC, avg_points_during_streak DESC
LIMIT 25;