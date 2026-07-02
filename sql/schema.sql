DROP TABLE IF EXISTS player_game_stats CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS seasons CASCADE;

CREATE TABLE teams (

	team_id INTEGER PRIMARY KEY,

	abbreviation VARCHAR(5) NOT NULL,

	city VARCHAR(50) NOT NULL,

	nickname VARCHAR(50) NOT NULL,

	full_name VARCHAR(100) NOT NULL,

	conference VARCHAR(20), 

	division VARCHAR(30)
	
);

CREATE TABLE players (

    player_id INTEGER PRIMARY KEY,

    team_id INTEGER NOT NULL,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    full_name VARCHAR(100) NOT NULL,

    birth_date DATE,

    height VARCHAR(10),

    weight INTEGER,

    position VARCHAR(10),

    active BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (team_id)
        REFERENCES team(team_id)

);