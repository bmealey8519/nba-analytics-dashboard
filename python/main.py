from load import load_teams, load_players, load_games, load_box


def main():
    print("Starting NBA Analytics Pipeline...\n")

    load_teams()

    load_players()

    load_games()

    load_box(limit_games=None)

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()