import requests
import os

class MovieApp:
    def __init__(self, storage, api_key):
        self._storage = storage
        self._api_key = api_key

    def _command_list_movies(self):
        """List all movies in storage."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            return
        for title, details in movies.items():
            print(f"Title: {details['title']}, Year: {details['year']}, Rating: {details['rating']}, Poster URL: {details['poster']}")

    def _command_add_movie(self):
        """Add a movie using the OMDb API."""
        title = input("Enter the movie title: ")
        movie_info = self._fetch_movie_from_omdb(title)
        if movie_info:
            self._storage.add_movie(
                title=movie_info['title'],
                year=movie_info['year'],
                rating=movie_info['rating'],
                poster=movie_info['poster']
            )
            print(f"Movie '{movie_info['title']}' added successfully.")
        else:
            print(f"Failed to add movie '{title}'.")

    def _command_delete_movie(self):
        """Delete a movie by title from the storage."""
        title = input("Enter the title of the movie to delete: ")
        success = self._storage.delete_movie(title)
        if success:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def _command_update_movie(self):
        """Update the rating of a movie by title."""
        title = input("Enter the title of the movie you want to update: ")
        new_rating = float(input("Enter the new rating: "))
        success = self._storage.update_movie(title, new_rating)
        if success:
            print(f"Movie '{title}' rating updated successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def _command_movie_stats(self):
        """Display statistics such as total movies and average rating."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found to calculate statistics.")
            return
        total_movies = len(movies)
        total_rating = sum(movie['rating'] for movie in movies.values())
        average_rating = total_rating / total_movies if total_movies > 0 else 0
        print(f"Total number of movies: {total_movies}")
        print(f"Average movie rating: {average_rating:.2f}")

    def _generate_website(self):
        """Generate an HTML website that displays the list of movies."""
        # Load the template
        with open("_static/index_template.html", "r") as file:
            template = file.read()

        # Get the list of movies
        movies = self._storage.list_movies()

        # Generate the movie grid HTML
        movie_grid_html = ""
        for movie in movies.values():
            movie_grid_html += f"""
        <div class="movie" style="
            border: 2px solid #333;
            border-radius: 10px;
            background-color: #fff;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: calc(33.333% - 40px); /* Width for 3 columns minus margin */
            box-sizing: border-box;
            transition: transform 0.2s;
        ">
            <img src="{movie['poster']}" alt="{movie['title']} poster" style="max-width: 100%; height: auto; border-radius: 5px;">
            <h2 style="font-size: 1.2em; color: #333;">{movie['title']}</h2>
            <p style="font-size: 0.9em; color: #666;">Year: {movie['year']}</p>
            <p style="font-size: 0.9em; color: #666;">Rating: {movie['rating']}</p>
        </div>
        """

        # Replace the placeholders in the template
        generated_html = template.replace("__TEMPLATE_TITLE__", "Alperen's Movie Collection")
        generated_html = generated_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

        # Write the generated HTML to index.html
        output_path = "index.html"
        with open(output_path, "w") as output_file:
            output_file.write(generated_html)

        print("Website was generated successfully.")

    def _fetch_movie_from_omdb(self, title):
        """Fetch movie details from the OMDb API."""
        url = f"http://www.omdbapi.com/?apikey={self._api_key}&t={title}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get('Response') == 'True':
                return {
                    'title': data['Title'],
                    'year': int(data['Year']),
                    'rating': float(data['imdbRating']),
                    'poster': data['Poster']
                }
            else:
                print(f"Movie '{title}' not found in the OMDb database.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to connect to OMDb API: {e}")
            return None

    def run(self):
        """Display a menu and execute user commands in a loop."""
        while True:
            print("\nMenu:")
            print("1. List movies")
            print("2. Add a movie")
            print("3. Delete a movie")
            print("4. Update a movie's rating")
            print("5. Show movie statistics")
            print("6. Generate website")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._generate_website()
            elif choice == "7":
                print("Exiting the app. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
