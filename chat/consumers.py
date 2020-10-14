import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.serializers import serialize

from .models import Message


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
            author=self.user, message=data.get('message'))
        return {
            'author': {
                'username': message.author.username,
                'first_name': message.author.first_name,
                'last_name': message.author.last_name
            },
            'message': message.message,
            'sent_on': str(message.sent_on)
        }

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
