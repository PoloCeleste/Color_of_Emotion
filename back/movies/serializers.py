from rest_framework import serializers
from .models import Genre, Provider, Movie, Emotion, EmotionColor

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['provider_name', 'logo_path']

class MovieSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True, read_only=True)
    watch_providers = ProviderSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'original_language', 'original_title', 'overview', 'poster_path',
            'release_date', 'title', 'tmdb_vote_average', 'movie_id',
            'picture_url', 'video_url', 'reviews', 'watchapedia',
            'poster_palette', 'genre_ids', 'watch_providers'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre_ids'] = [genre['name'] for genre in representation['genre_ids']]
        return representation

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['name']

class EmotionColorSerializer(serializers.ModelSerializer):
    emotion_id = EmotionSerializer(many=True, read_only=True)
    genres_id = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = EmotionColor
        fields = ['color_id', 'emotion_id', 'genres_id', 'emotions_color']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['emotion_id'] = [emotion['name'] for emotion in representation['emotion_id']]
        representation['genres_id'] = [genre['name'] for genre in representation['genres_id']]
        return representation