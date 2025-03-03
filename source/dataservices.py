import pandas as pd
from sqlalchemy import create_engine


class CountryDataService:
    def __init__(self, db_name, user, password, host='db', port=5432):
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(self.db_url)

    def get_population_data(self):
        """Executes the SQL query."""
        query = """
            WITH RankedCountries AS (
                SELECT
                    country, region, population_2023,
                    RANK() OVER (PARTITION BY region ORDER BY "population_2023" DESC) AS rank_high,
                    RANK() OVER (PARTITION BY region ORDER BY "population_2023" ASC) AS rank_low
                FROM countries
            )
            SELECT 
                region,
                MAX(CASE WHEN rank_high = 1 THEN country END) AS highest_population_country,
                MAX(CASE WHEN rank_high = 1 THEN population_2023 END) AS highest_population,
                MAX(CASE WHEN rank_low = 1 THEN country END) AS lowest_population_country,
                MAX(CASE WHEN rank_low = 1 THEN population_2023 END) AS lowest_population
            FROM RankedCountries
            GROUP BY region;
        """

        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(query, connection)
                return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
