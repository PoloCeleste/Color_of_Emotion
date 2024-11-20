import json
from django.core.management.base import BaseCommand
from movies.models import Genre, Provider, Movie

class Command(BaseCommand):
    help = 'Load data from JSON files into the database'

    def handle(self, *args, **options):
        self.load_genres()
        self.load_providers()
        self.load_movies()

    def load_genres(self):
        with open('genres.json', 'r', encoding='utf-8') as file:
            genres_data = json.load(file)
            for genre in genres_data:
                Genre.objects.get_or_create(id=genre['id'], name=genre['name'])
        self.stdout.write(self.style.SUCCESS('Successfully loaded genres'))

    def load_providers(self):
        with open('providers.json', 'r', encoding='utf-8') as file:
            providers_data = json.load(file)
            for provider in providers_data:
                Provider.objects.get_or_create(
                    provider_id=provider['provider_id'],
                    provider_name=provider['provider_name'],
                    logo_path=provider['logo_path']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded providers'))

    def load_movies(self):
        with open('movies.json', 'r', encoding='utf-8') as file:
            movies_data = json.load(file)
            for movie_data in movies_data:
                movie, created = Movie.objects.get_or_create(
                    original_title=movie_data['original_title'],
                    defaults={
                        'original_language': movie_data['original_language'],
                        'overview': movie_data['overview'],
                        'poster_path': movie_data['poster_path'],
                        'release_date': movie_data['release_date'],
                        'title': movie_data['title'],
                        'tmdb_vote_average': movie_data['tmdb_vote_average'],
                        'picture_url': movie_data['picture_url'],
                        'video_url': movie_data['video_url'],
                        'reviews': movie_data['reviews'],
                        'poster_palette': movie_data['poster_palette'],
                    }
                )

                for genre_id in movie_data['genre_ids']:
                    genre = Genre.objects.get(id=genre_id)
                    movie.genre_ids.add(genre)

                for provider_id in movie_data['watch_providers']:
                    provider = Provider.objects.get(provider_id=provider_id)
                    movie.watch_providers.add(provider)

        self.stdout.write(self.style.SUCCESS('Successfully loaded movies'))