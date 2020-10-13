import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.recent_messages(self)
        content = {
            'messages': self.serialize_to_json(messages)
        }
        self.send_message(content)

    def send_message(self, data):
        author = data['from']
        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            author=author_user, message=data['message'])
        content = {
            'command': 'new_message',
            'message': self.get_json_data(message)
        }
        return self.send_chat_message(content)

    def serialize_to_json(self, messages):
        return [self.get_json_data(message) for message in messages]

    def get_json_data(self, message):
        return {
            'author': message.author.username,
            'message': message.message,
            'sent_on': str(message.sent_on),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'send_message': send_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['commands']](self, data)

    def send_chat_message(self, data):
        message = data['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
