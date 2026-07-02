import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="nba_analytics",
        user="postgres",
        password="Chase8519!"
    )