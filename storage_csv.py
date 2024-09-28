import csv

class StorageCsv:
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        movies = {}
        try:
            with open(self.file_path, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row['title']
                    movies[title] = {
                        'title': title,
                        'year': int(row['year']),
                        'rating': float(row['rating']),
                        'poster': row.get('poster', None)
                    }
        except FileNotFoundError:
            return {}
        return movies

    def _save_movies(self, movies):
        with open(self.file_path, mode='w', newline='') as f:
            fieldnames = ['title', 'year', 'rating', 'poster']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for movie in movies.values():
                writer.writerow(movie)

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
