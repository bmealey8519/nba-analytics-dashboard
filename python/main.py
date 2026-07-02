from load import load_teams, load_players


def main():
    print("Starting NBA Analytics Pipeline...\n")

    load_teams()

    load_players()

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()