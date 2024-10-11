"""
ASGI config for pong project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from websockets.routing import websocket_urlpatterns
from django.urls import path
import websockets.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pong.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websockets.routing.websocket_urlpatterns
        )
    ),
})