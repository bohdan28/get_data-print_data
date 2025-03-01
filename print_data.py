from flask import Flask
from datafetchers import PopulationDataFetcher

app = Flask(__name__)

@app.route('/')
def print_data():
    fetcher = PopulationDataFetcher('postgres', 'postgres', 'postgres')
    df = fetcher.fetch_population_data()
    return df.to_html()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)