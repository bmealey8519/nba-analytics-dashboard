SELECT 'teams' AS table_name, COUNT(*) FROM teams
UNION ALL
SELECT 'players', COUNT(*) FROM players
UNION ALL
SELECT 'games', COUNT(*) FROM games
UNION ALL
SELECT 'player_game_stats', COUNT(*) FROM player_game_stats;

SELECT
    p.full_name AS player,
    t.full_name AS team,
    g.game_date,
    pgs.points,
    pgs.rebounds,
    pgs.assists
FROM player_game_stats pgs
JOIN players p ON pgs.player_id = p.player_id
JOIN games g ON pgs.game_id = g.game_id
LIMIT 20;


SELECT
    p.full_name,
    COUNT(*) AS games_played,
    ROUND(AVG(pgs.points), 2) AS ppg,
    ROUND(AVG(pgs.rebounds), 2) AS rpg,
    ROUND(AVG(pgs.assists), 2) AS apg
FROM player_game_stats pgs
JOIN players p ON pgs.player_id = p.player_id
GROUP BY p.full_name
HAVING COUNT(*) >= 20
ORDER BY ppg DESC
LIMIT 25;