import requests
from django.conf import settings
from rest_framework import generics
from .models import Movie, EmotionColor
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MovieSerializer, EmotionColorSerializer

tmdb = settings.API_KEY

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class EmotionColorList(generics.ListAPIView):
    queryset = EmotionColor.objects.all()
    serializer_class = EmotionColorSerializer

@api_view(['GET'])
def Actors(request, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb}"
    }
    try:
        response = requests.get(url, headers=headers).json()['cast']
        if response:
            data={
                'cast':response
            }
    except:
        data={
            'error':"Can't access TMDB API."
        }
    return Response(data)