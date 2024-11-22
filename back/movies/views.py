from rest_framework import generics
from .models import Movie, EmotionColor
from .serializers import MovieSerializer, EmotionColorSerializer

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class EmotionColorList(generics.ListAPIView):
    queryset = EmotionColor.objects.all()
    serializer_class = EmotionColorSerializer