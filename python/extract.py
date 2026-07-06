from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import boxscoretraditionalv3
from transform import transform_games

def get_teams():
    """Retrieve all NBA teams from the API."""
    return teams.get_teams()

def get_players():
    """Retrieve all NBA players from the API"""
    return players.get_players()

def get_games(season="2023-24"):
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season)
    return gamefinder.get_data_frames()[0]

def get_box_score(game_id):
    boxscore = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)
    return boxscore.get_data_frames()[0]


if __name__ == "__main__":
    nba_teams = get_teams()

    print(f"Number of teams: {len(nba_teams)}\n")

    for key, value in nba_teams[0].items():
        print(f"{key}: {value}")

    nba_players = get_players()

    for key, value in nba_players[0].items():
        print(f"{key}: {value}")

    games = get_games("2023-24")
    clean_games = transform_games(games)

    print(clean_games.head())
    print(clean_games.columns)
    print(len(clean_games))

    box_score = get_box_score('0012300001')
    print(box_score["points"].head())
    print(box_score.columns)

