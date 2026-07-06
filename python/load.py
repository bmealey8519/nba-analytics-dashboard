from db import get_connection
from extract import get_teams, get_players, get_games, get_box_score
from transform import transform_games, transform_box
import time


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


def get_existing_ids(cursor, table, column):
    cursor.execute(f"SELECT {column} FROM {table}")
    return {row[0] for row in cursor.fetchall()}

def load_box(limit_games=10):
    conn = get_connection()
    cursor = conn.cursor()

    loaded = 0
    skipped = 0

    try:
        valid_game_ids = get_existing_ids(cursor, "games", "game_id")
        valid_player_ids = get_existing_ids(cursor, "players", "player_id")
        valid_team_ids = get_existing_ids(cursor, "teams", "team_id")

        cursor.execute("""
            SELECT game_id
            FROM games
            ORDER BY game_date
        """)
        game_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT DISTINCT game_id
            FROM player_game_stats
        """)
        already_loaded_game_ids = {row[0] for row in cursor.fetchall()}

        if limit_games is not None:
            game_ids = game_ids[:limit_games]

        for index, game_id in enumerate(game_ids, start=1):

            if game_id in already_loaded_game_ids:
                print(f"Skipping already-loaded game {game_id}")
                continue

            print(f"Loading box score {index}/{len(game_ids)}: {game_id}")

            boxscore = get_box_score(game_id)
            stats = transform_box(boxscore)

            for _, stat in stats.iterrows():

                if (
                    stat["game_id"] not in valid_game_ids
                    or stat["player_id"] not in valid_player_ids
                    or stat["team_id"] not in valid_team_ids
                ):
                    skipped += 1
                    continue

                cursor.execute(
                    """
                    INSERT INTO player_game_stats (
                        game_id,
                        player_id,
                        team_id,
                        minutes,
                        points,
                        rebounds,
                        assists,
                        steals,
                        blocks,
                        turnovers,
                        personal_fouls,
                        fgm,
                        fga,
                        fg_pct,
                        fg3m,
                        fg3a,
                        fg3_pct,
                        ftm,
                        fta,
                        ft_pct,
                        plus_minus
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s
                    )
                    ON CONFLICT (game_id, player_id) DO UPDATE SET
                        team_id = EXCLUDED.team_id,
                        minutes = EXCLUDED.minutes,
                        points = EXCLUDED.points,
                        rebounds = EXCLUDED.rebounds,
                        assists = EXCLUDED.assists,
                        steals = EXCLUDED.steals,
                        blocks = EXCLUDED.blocks,
                        turnovers = EXCLUDED.turnovers,
                        personal_fouls = EXCLUDED.personal_fouls,
                        fgm = EXCLUDED.fgm,
                        fga = EXCLUDED.fga,
                        fg_pct = EXCLUDED.fg_pct,
                        fg3m = EXCLUDED.fg3m,
                        fg3a = EXCLUDED.fg3a,
                        fg3_pct = EXCLUDED.fg3_pct,
                        ftm = EXCLUDED.ftm,
                        fta = EXCLUDED.fta,
                        ft_pct = EXCLUDED.ft_pct,
                        plus_minus = EXCLUDED.plus_minus;
                    """,
                    (
                        stat["game_id"],
                        stat["player_id"],
                        stat["team_id"],
                        stat["minutes"],
                        stat["points"],
                        stat["rebounds"],
                        stat["assists"],
                        stat["steals"],
                        stat["blocks"],
                        stat["turnovers"],
                        stat["personal_fouls"],
                        stat["fgm"],
                        stat["fga"],
                        stat["fg_pct"],
                        stat["fg3m"],
                        stat["fg3a"],
                        stat["fg3_pct"],
                        stat["ftm"],
                        stat["fta"],
                        stat["ft_pct"],
                        stat["plus_minus"],
                    ),
                )
                
                loaded += 1
            conn.commit()    
            time.sleep(0.75)
            
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error loading player game stats: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

    print(f"Loaded {loaded} player game stat rows.")
    print(f"Skipped {skipped} rows due to missing foreign keys. (game_id/team_id/player_id)")





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