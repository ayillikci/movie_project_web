from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    api_key = "71aff867"

    # Choose storage type (JSON or CSV)
    storage_choice = input("Choose storage type (json/csv): ").strip().lower()

    if storage_choice == "csv":
        storage = StorageCsv('movies.csv')
    else:
        storage = StorageJson('movies.json')

    # Create MovieApp instance and run it
    movie_app = MovieApp(storage, api_key)
    movie_app.run()


if __name__ == "__main__":
    main()
