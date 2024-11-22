from django.urls import path
from .views import MovieList, EmotionColorList

app_name = 'movies'

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('emotion-colors/', EmotionColorList.as_view(), name='emotion-color-list'),
]
