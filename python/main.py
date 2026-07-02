from load import load_teams


def main():
    print("Starting NBA Analytics Pipeline...\n")

    load_teams()

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()