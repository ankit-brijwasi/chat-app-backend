from chat.views import index, room
from django.urls import path

urlpatterns = [
    path('<str:room_name>/', room, name='room'),
    path('', index, name="home"),
]
