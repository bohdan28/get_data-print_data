import pandas as pd
from sqlalchemy.orm import Session
from source.models import Country, engine
import re

class Parser:
    def __init__(self, url):
        self.url = url
        self.df = None

    def get_data(self):
        tables = pd.read_html(self.url)
        self.df = tables[0]

    def clean_data(self):
        self.df.columns = ["country", "population_2022", "population_2023", "change_percent", "region", "subregion"]
        self.df = self.df[["country", "population_2022", "population_2023", "change_percent", "region", "subregion"]]
        self.df["change_percent"].fillna("0.00%", inplace=True)
        self.df["population_2022"].fillna("", inplace=True)
        self.df["population_2023"].fillna("", inplace=True)
        self.df["country"] = self.df["country"].apply(lambda x: re.sub(r'\[.*?\]', '', x).strip())


    def save_to_db(self):
        session = Session(bind=engine)
        for _, row in self.df.iterrows():
            if row["country"] != "World" and row["population_2023"]:
                country = Country(
                    country=row["country"],
                    population_2022=row["population_2022"],
                    population_2023=row["population_2023"],
                    change_percent=row["change_percent"],
                    region=row["region"],
                    subregion=row["subregion"],
                )
                session.add(country)
        session.commit()
        session.close()
        print("Data saved successfully")