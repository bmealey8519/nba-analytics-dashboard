from nba_api.stats.static import teams
from nba_api.stats.static import players

def get_teams():
    """Retrieve all NBA teams from the API."""
    return teams.get_teams()

def get_players():
    """Retrieve all NBA players from the API"""
    return players.get_players()


if __name__ == "__main__":
    nba_teams = get_teams()

    print(f"Number of teams: {len(nba_teams)}\n")

    for key, value in nba_teams[0].items():
        print(f"{key}: {value}")

    nba_players = get_players()

    for key, value in nba_players[0].items():
        print(f"{key}: {value}")

