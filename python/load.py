from db import get_connection
from extract import get_teams, get_players, get_games
from transform import transform_games


def load_teams():
    teams = get_teams()

    conn = get_connection()
    cursor = conn.cursor()

    print("Connected to PostgreSQL.")

    loaded = 0

    try:
        for team in teams:
            cursor.execute(
                """
                INSERT INTO teams (
                    team_id,
                    full_name,
                    abbreviation,
                    nickname,
                    city
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (team_id) DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    abbreviation = EXCLUDED.abbreviation,
                    nickname = EXCLUDED.nickname,
                    city = EXCLUDED.city;
                """,
                (
                    team["id"],
                    team["full_name"],
                    team["abbreviation"],
                    team["nickname"],
                    team["city"],
                ),
            )
            loaded += 1

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error loading teams: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

    print(f"Loaded {loaded} teams from the NBA API.")


def load_players():
    players = get_players()

    conn = get_connection()
    cursor = conn.cursor()

    print("Connected to PostgreSQL.")

    loaded = 0

    try:
        for player in players:
            cursor.execute(
                """
                INSERT INTO players (
                    player_id,
                    first_name,
                    last_name,
                    full_name,
                    active
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (player_id) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    full_name = EXCLUDED.full_name,
                    active = EXCLUDED.active;
                """,
                (
                    player["id"],
                    player["first_name"],
                    player["last_name"],
                    player["full_name"],
                    player["is_active"],
                ),
            )
            loaded += 1

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error loading players: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

    print(f"Loaded {loaded} players from the NBA API.")


def load_games():
    raw_games = get_games("2023-24")
    teams = get_teams()

    valid_team_ids = {team["id"] for team in teams}

    raw_games = raw_games[raw_games["TEAM_ID"].isin(valid_team_ids)]

    games = transform_games(raw_games)

    conn = get_connection()
    cursor = conn.cursor()

    loaded = 0

    try:
        for _, game in games.iterrows():
            cursor.execute(
                """
                INSERT INTO games (
                    game_id,
                    season_id,
                    game_date,
                    home_team_id,
                    away_team_id,
                    home_score,
                    away_score
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id) DO UPDATE SET
                    season_id = EXCLUDED.season_id,
                    game_date = EXCLUDED.game_date,
                    home_team_id = EXCLUDED.home_team_id,
                    away_team_id = EXCLUDED.away_team_id,
                    home_score = EXCLUDED.home_score,
                    away_score = EXCLUDED.away_score;
                """,
                (
                    game["game_id"],
                    game["season_id"],
                    game["game_date"],
                    game["home_team_id"],
                    game["away_team_id"],
                    game["home_score"],
                    game["away_score"],
                ),
            )
            loaded += 1
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error loading game: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

    print(f"Loaded {loaded} games into PostgreSQL. ")


if __name__ == "__main__":
    load_teams()
    load_players()
    load_games()