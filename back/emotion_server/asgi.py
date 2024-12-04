"""
ASGI config for emotion_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os, django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from channels.auth import AuthMiddlewareStack
from .consumers import VideoStreamConsumer
from django.urls import path
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotion_server.settings')
django.setup()

BACK_SERVER_URL = settings.BACK_SERVER_URL
FRONT_URL = settings.FRONT_URL

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("ws/stream/", VideoStreamConsumer.as_asgi()),
            ])
        ),
        allowed_origins=[f"https://{BACK_SERVER_URL}", f"https://{FRONT_URL}"]
    ),
})
