from source.parsers import Parser
from source.settings import URL

if __name__ == "__main__":
    parser = Parser(URL)
    parser.get_data()
    parser.clean_data()
    parser.save_to_db()
