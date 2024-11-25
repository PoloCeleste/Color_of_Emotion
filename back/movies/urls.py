from django.urls import path
from .views import MovieList, EmotionColorList, Actors, recommend_movies

app_name = 'movies'

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies', MovieList.as_view(), name='movie-list'),
    path('recommend_movies/', recommend_movies, name='recommend_movies'),
    path('recommend_movies', recommend_movies, name='recommend_movies'),
    path('emotion-colors/', EmotionColorList.as_view(), name='emotion-color-list'),
    path('emotion-colors', EmotionColorList.as_view(), name='emotion-color-list'),
    path('movies/<int:movie_id>/', Actors, name='actors'),
    path('movies/<int:movie_id>', Actors, name='actors'),
]
