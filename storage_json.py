import json

class StorageJson:
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_movies(self, movies):
        with open(self.file_path, 'w') as f:
            json.dump(movies, f, indent=4)

    def list_movies(self):
        return self._load_movies()

    def add_movie(self, title, year, rating, poster=None):
        movies = self._load_movies()
        movies[title] = {'title': title, 'year': year, 'rating': rating, 'poster': poster}
        self._save_movies(movies)

    def delete_movie(self, title):
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            return True
        return False

    def update_movie(self, title, rating):
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
            return True
        return False
