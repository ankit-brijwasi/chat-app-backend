from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room


@login_required
def index(request):
    rooms = Room.objects.filter(~Q(admins__username=request.user.username))
    return render(request, 'chat/index.html', {'rooms': rooms})


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })
