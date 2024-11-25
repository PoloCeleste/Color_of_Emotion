from django.db import models

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Provider(models.Model):
    provider_id = models.IntegerField(primary_key=True)
    provider_name = models.CharField(max_length=100)
    logo_path = models.URLField()

    def __str__(self):
        return self.provider_name

class Movie(models.Model):
    genre_ids = models.ManyToManyField(Genre, related_name='movies')
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.URLField()
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    tmdb_vote_average = models.FloatField()
    watch_providers = models.ManyToManyField(Provider, related_name='movies')
    movie_id = models.IntegerField()
    picture_url = models.JSONField(null=True, blank=True)
    video_url = models.JSONField(null=True, blank=True)
    reviews = models.JSONField(null=True, blank=True)
    poster_palette = models.JSONField(null=True, blank=True)
    watchapedia = models.URLField()

    def __str__(self):
        return self.title

class Emotion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EmotionColor(models.Model):
    color_id = models.IntegerField(primary_key=True)
    emotion_id = models.ManyToManyField(Emotion, related_name='emotion_colors')
    genres_id = models.ManyToManyField(Genre, related_name='emotion_colors')
    emotions_color = models.JSONField()

    def __str__(self):
        return f"Color ID: {self.color_id}"