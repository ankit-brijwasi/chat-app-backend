from chat.views import index, room
from django.urls import path

urlpatterns = [
    path('', index),
    path('<str:room_name>/', room, name='room'),
]
