from django.urls import path
from .consumers import QAConsumer

websocket_urlpatterns = [
    path('ws/qa/', QAConsumer.as_asgi()),
]
