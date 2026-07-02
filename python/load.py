from db import get_connection
from extract import get_teams


def load_teams():
    teams = get_teams()
    


    conn = get_connection()
    cursor = conn.cursor()

    print(f"Connected to PostgreSQL.")

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
        ON CONFLICT (team_id) DO NOTHING;
        """,
        (
            team["id"],
            team["full_name"],
            team["abbreviation"],
            team["nickname"],
            team["city"]
        )
    )
        
    
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Loaded {len(teams)} teams from the NBA API.")


if __name__ == "__main__":
    load_teams()

