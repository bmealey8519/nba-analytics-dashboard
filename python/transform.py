import pandas as pd

def transform_games(games_df):

    transformed_games = []

    for game_id, group in games_df.groupby("GAME_ID"):

        home_row = group[group["MATCHUP"].str.contains("vs.")]
        away_row = group[group["MATCHUP"].str.contains("@")]

        if home_row.empty or away_row.empty:
            continue

        home_row = home_row.iloc[0]
        away_row = away_row.iloc[0]

        transformed_games.append({
            "game_id": game_id,
            "season_id": home_row["SEASON_ID"],
            "game_date": home_row["GAME_DATE"],
            "home_team_id": int(home_row["TEAM_ID"]),
            "away_team_id": int(away_row["TEAM_ID"]),
            "home_score": int(home_row["PTS"]),
            "away_score": int(away_row["PTS"])
        })

    return pd.DataFrame(transformed_games)


def transform_box(box_df):

    transformed_box = []

    for _, row in box_df.iterrows():

        transformed_box.append({
            "game_id": row["gameId"],
            "player_id": int(row["personId"]),
            "team_id": int(row["teamId"]),
            "minutes": row["minutes"],
            "points": int(row["points"]),
            "rebounds": int(row["reboundsTotal"]),
            "assists": int(row["assists"]),
            "steals": int(row["steals"]),
            "blocks": int(row["blocks"]),
            "turnovers": int(row["turnovers"]),
            "personal_fouls": int(row["foulsPersonal"]),

            "fgm": int(row["fieldGoalsMade"]),
            "fga": int(row["fieldGoalsAttempted"]),
            "fg_pct": row["fieldGoalsPercentage"],

            "fg3m": int(row["threePointersMade"]),
            "fg3a": int(row["threePointersAttempted"]),
            "fg3_pct": row["threePointersPercentage"],

            "ftm": int(row["freeThrowsMade"]),
            "fta": int(row["freeThrowsAttempted"]),
            "ft_pct": row["freeThrowsPercentage"],

            "plus_minus": row["plusMinusPoints"]
        })
    
    return pd.DataFrame(transformed_box)