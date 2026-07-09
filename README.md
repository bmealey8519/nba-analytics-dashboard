# 🏀 NBA Analytics Dashboard

An end-to-end data analytics project that extracts NBA statistics from the NBA API, stores them in a PostgreSQL database, analyzes player and team performance using advanced SQL, and visualizes key insights through interactive Tableau dashboards.

This project demonstrates a complete analytics workflow including ETL development, relational database design, SQL analytics, and business intelligence visualization.

---

## Project Overview

The goal of this project was to build a professional sports analytics dashboard that allows users to explore player and team performance throughout the 2023–24 NBA season.

The project includes:

- Python ETL pipeline
- PostgreSQL relational database
- Advanced SQL analysis using CTEs and window functions
- Interactive Tableau dashboards with dashboard actions

---

## Technologies Used

- Python
- PostgreSQL
- SQL
- Tableau
- NBA API (`nba_api`)
- Pandas
- Psycopg2

---

## Data Pipeline

```
NBA API
    ↓
Python ETL
    ↓
PostgreSQL Database
    ↓
Advanced SQL Views
    ↓
Tableau Dashboards
```

The Python ETL process:

- Extracts NBA team, player, game, and box score data
- Cleans and transforms raw API responses
- Loads data into a normalized PostgreSQL database
- Creates reusable SQL views for Tableau reporting

---

## Database Schema

The PostgreSQL database consists of four primary tables:

### Teams
Stores NBA team information.

### Players
Stores player information and team affiliations.

### Games
Stores game dates, teams, and final scores.

### Player Game Stats
Stores individual player box score statistics for every game.

---

## SQL Analysis

Several analytical SQL views were created to support the Tableau dashboards.

### Team Scoring

Calculates average points scored by each NBA team.

Skills demonstrated:

- Aggregations
- GROUP BY
- SQL Views

---

### Player Season Averages

Ranks players by season scoring averages while enforcing minimum games played.

Skills demonstrated:

- Aggregations
- HAVING
- Ranking
- SQL Views

---

### Double-Double Leaders

Calculates the number of double-doubles recorded by each player.

Skills demonstrated:

- CASE statements
- CTEs
- Aggregations

---

### Triple-Double Leaders

Calculates triple-double totals for every player.

Skills demonstrated:

- Multi-level CTEs
- Conditional logic
- Aggregations

---

### High Scoring Streak Analysis

Identifies consecutive games where a player significantly exceeded their normal scoring average.

Skills demonstrated:

- Window Functions
- ROW_NUMBER()
- Statistical calculations
- Standard deviation analysis

---

### Performance Change Distribution

Measures scoring volatility by comparing every player's points to their previous game.

Skills demonstrated:

- LAG()
- Window Functions
- CASE statements
- Performance trend analysis

---

## Tableau Dashboards

### Dashboard 1 — Team & Player Performance

Link: https://public.tableau.com/app/profile/brandon.mealey/viz/NBA_Analytics_Dashboard/PlayerTeamOverview

Features:

- Team scoring comparison
- Top player scoring averages
- Double-double leaders
- Triple-double leaders
- Interactive team filtering using dashboard actions

---

### Dashboard 2 — Player Trends

Link: https://public.tableau.com/app/profile/brandon.mealey/viz/NBA_Analytics_Dashboard_Continued/AdvancedPlayerPerformanceAnalytics

Features:

- High scoring streak visualization
- Performance change distribution
- Interactive player drill-down
- Game-to-game consistency analysis

---

## Skills Demonstrated

### SQL

- Common Table Expressions (CTEs)
- Window Functions
- LAG()
- RANK()
- Aggregations
- CASE Expressions
- Statistical Functions
- SQL Views
- Joins
- Filtering
- GROUP BY / HAVING

### Python

- API Integration
- ETL Development
- Data Cleaning
- Database Loading
- Pandas
- PostgreSQL Connectivity

### Tableau

- Dashboard Design
- Interactive Dashboard Actions
- Tooltips
- Filters
- Custom Formatting
- Multiple Data Sources

---

## Future Improvements

Potential future enhancements include:

- Multi-season historical analysis
- Team defensive metrics
- Advanced shooting analytics
- Interactive player comparison dashboard
- Automated daily ETL updates
- Predictive modeling using machine learning

---

## Dashboard Preview

### Dashboard 1

<img width="1634" height="1200" alt="Screenshot 2026-07-09 093734" src="https://github.com/user-attachments/assets/9118861d-d8e1-4096-9fac-3307ce0ac60c" />


---

### Dashboard 2

<img width="1613" height="1100" alt="Screenshot 2026-07-09 093740" src="https://github.com/user-attachments/assets/400f8cb2-bac2-426f-bbea-ad7ad63ddb09" />


---

