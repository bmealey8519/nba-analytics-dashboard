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

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    full_name VARCHAR(100) NOT NULL,

    birth_date DATE,

    height VARCHAR(10),

    weight INTEGER,

    position VARCHAR(10),

    active BOOLEAN NOT NULL DEFAULT TRUE


);


CREATE TABLE games (

    game_id VARCHAR(20) PRIMARY KEY,

    season_id VARCHAR(10),

    game_date DATE NOT NULL,

    home_team_id INTEGER NOT NULL,

    away_team_id INTEGER NOT NULL,

    home_score INTEGER,

    away_score INTEGER,

    FOREIGN KEY (home_team_id)
        REFERENCES teams(team_id),

    FOREIGN KEY (away_team_id)
        REFERENCES teams(team_id)
);

CREATE TABLE player_game_stats (

    game_id VARCHAR(20),

    player_id INTEGER,

    team_id INTEGER,

    minutes VARCHAR(10),

    points INTEGER,

    rebounds INTEGER,

    assists INTEGER,

    steals INTEGER,

    blocks INTEGER,

    turnovers INTEGER,

    personal_fouls INTEGER,

    fgm INTEGER,

    fga INTEGER,

    fg_pct NUMERIC(5,3),

    fg3m INTEGER,

    fg3a INTEGER,

    fg3_pct NUMERIC(5,3),

    ftm INTEGER,

    fta INTEGER,

    ft_pct NUMERIC(5,3),

    plus_minus INTEGER,

    PRIMARY KEY (game_id, player_id),

    FOREIGN KEY (game_id)
        REFERENCES games(game_id),

    FOREIGN KEY (player_id)
        REFERENCES players(player_id),

    FOREIGN KEY (team_id)
        REFERENCES teams(team_id)
);