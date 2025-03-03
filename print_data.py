from source.dataservices import CountryDataService
from source.settings import db_name, user, password, host, port

if __name__ == "__main__":
    service = CountryDataService(db_name, user, password, host, port)

    df = service.get_population_data()

    if df is not None:
        print(df.to_string())
