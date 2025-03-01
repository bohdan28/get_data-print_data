import pandas as pd
from sqlalchemy.orm import Session
from models import Country, engine
from datafetchers import PopulationDataFetcher

URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"

tables = pd.read_html(URL)
df = tables[0]

df.columns = ["country", "population_2022", "population_2023", "change_percent", "region", "subregion"]
df = df[["country", "population_2022", "population_2023", "change_percent", "region", "subregion"]]

# df["population_2022"] = df["population_2022"].str.replace(",", "").astype(int)
# df["population_2023"] = df["population_2023"].str.replace(",", "").astype(int)
df["change_percent"].fillna("0.00%", inplace=True)
df["population_2022"].fillna("", inplace=True)
df["population_2023"].fillna("", inplace=True)

session = Session(bind=engine)

for _, row in df.iterrows():
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

print("Data saved to SQLite!")
