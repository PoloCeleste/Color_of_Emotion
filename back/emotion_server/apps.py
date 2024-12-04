from django.apps import AppConfig
import sys

class EmotionServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emotion_server'

    def ready(self):
        if any(arg in sys.argv[0] for arg in ['daphne', 'manage.py']):
            from .consumers import load_model
            try:
                load_model()
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")