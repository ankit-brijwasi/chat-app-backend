import json
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.forms import model_to_dict

from .models import Message, Room
from .serializers import RoomSerializer, MessageSerializer, UserSerializer
from core.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            # close the websocket if the user is not authenticated
            await self.close()
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route'].get('kwargs').get('room_name')
        self.room_group_name = f"chat_{self.room_name}"

        # Joining the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, data):
        '''saves message to database and returns a serialized object'''
        message = Message.objects.create(
            author=self.user, message=data.get('message'), room=Room.objects.get(slug=self.room_name))

        serializer = MessageSerializer(message, many=False)
        return serializer.data

    async def receive(self, text_data=None, bytes_data=None):
        '''recieve method will recieve the data from the client
           and then send it to the group, after which the message
           will be pushed to all the connected channels in that group'''

        data = json.loads(text_data)
        message = await self.save_message(data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # <-- function
                # <-- arguments, these will be recieved as event
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event.get('message')

        await self.send(text_data=json.dumps({'data': message}))


class RoomConsumer(AsyncWebsocketConsumer):
    '''Consumer for rooms'''

    @database_sync_to_async
    def fetch_user(self):
        '''returns the user and its profile'''
        user = User.objects.get(id=self.scope['user'].id)
        return user

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            self.disconnect()
        self.user = await self.fetch_user()
        self.group_name = "rooms"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)

    @database_sync_to_async
    def add_room(self, data):
        '''adds a new room in the database and return a serialized object'''
        room = Room.objects.create(name=data.get('name'))
        room.admins.add(self.user)
        room.save()
        serializer = RoomSerializer(room, many=False)
        return serializer.data

    @database_sync_to_async
    def join_room_req(self, data):
        '''adds the current user request to join a room'''
        # for now add anyone directly to the room
        room = get_object_or_404(Room, slug=data.get('slug'))
        room.join_requests.add(self.user)
        room.members.add(self.user)
        room.save()
        serializer = RoomSerializer(room, many=False)
        return serializer.data, self.user.username

    @database_sync_to_async
    def online_users(self):
        '''Returns all the online users'''
        users = User.objects.filter(profile__online=True)
        serializer = UserSerializer(users, many=True)
        return serializer.data

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        if data.get('action') == "add_room":
            room = await self.add_room(data)
            # await self.send(text_data=json.dumps({'room': room, 'type': 'add_room'}))

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'new_room',  # <-- function
                    'room': room  # <-- arguments, these will be recieved as event
                }
            )

        if data.get('action') == "join_room_request":
            room, username = await self.join_room_req(data)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'join_room_request',
                    'room': room,
                    'join_req_user': username
                }
            )

        if data.get('action') == "fetch_online_users":
            users = await self.online_users()

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'get_online_users',
                    'users': users
                }
            )

    async def new_room(self, event):
        room = event.get('room')
        await self.send(text_data=json.dumps({'room': room, 'type': 'add_room'}))

    async def join_room_request(self, event):
        room = event.get('room')
        join_req_user = event.get('join_req_user')
        await self.send(text_data=json.dumps({'room': room, 'join_req_user': join_req_user, 'type': 'join_room_request'}))

    async def get_online_users(self, event):
        users = event.get('users')
        await self.send(text_data=json.dumps({'type': 'fetch_online_users', 'users': users}))
