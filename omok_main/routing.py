from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/omok/<room_name>/', consumers.ChatConsumer),
]