from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Room, Message


@login_required
def index(request):
    all_rooms = Room.objects.filter(
        ~Q(admins__username=request.user.username) & ~Q(join_requests__username=request.user.username) & ~Q(members__username=request.user.username))

    my_rooms = Room.objects.filter(
        Q(members__username=request.user.username) | Q(
            admins__username=request.user.username)
    )

    return render(request, 'chat/index.html', {'rooms': all_rooms, 'my_rooms': my_rooms})


@login_required
def room(request, room_name):
    room = get_object_or_404(Room, Q(slug=room_name) & Q(
        Q(members=request.user) | Q(admins=request.user)))
    messages = Message.objects.filter(room=room).order_by('sent_on')
    return render(request, 'chat/room.html', {
        'room_name': room.name,
        'username': request.user.username,
        'chats': messages
    })
