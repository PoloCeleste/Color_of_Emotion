from django.urls import path
from .views import Actors, recommend_movies, emotion_colors

app_name = 'movies'

urlpatterns = [
    path('recommend_movies/', recommend_movies, name='recommend_movies'),
    path('recommend_movies', recommend_movies, name='recommend_movies'),
    path('emotion-colors/', emotion_colors, name='emotion_color'),
    path('emotion-colors', emotion_colors, name='emotion_color'),
    path('movies/<int:movie_id>/', Actors, name='actors'),
    path('movies/<int:movie_id>', Actors, name='actors'),
]
