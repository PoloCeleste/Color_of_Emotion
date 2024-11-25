from django.apps import AppConfig
import sys

class EmotionServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emotion_server'

    def ready(self):
        if 'runserver' not in sys.argv and 'daphne' not in sys.argv:
            return True
            
        # 웹소켓 서버가 두 번 시작되는 것을 방지
        if not sys.argv[0].endswith('manage.py'):
            return True
            
        # runserver나 daphne로 실행될 때만 모델 로드
        from .consumers import load_model
        load_model()