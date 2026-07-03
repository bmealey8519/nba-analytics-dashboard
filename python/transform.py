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