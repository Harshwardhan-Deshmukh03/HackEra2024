import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        mis = data['mis']
        room = data['room']
        name=data['name']
        user=sync_to_async(User.objects.get)
        try:
            user = await user(username='mis')
            print(user)
        except User.DoesNotExist:
            print("User does not exist")

        await self.save_message(mis, room, message,user)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'mis': mis,
                'name':name,
                'room':room,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        mis = event['mis']
        name=event['name']
        room=event['room']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'mis': mis,
            'name':name,
            
            'room':room,
        }))

    @sync_to_async
    def save_message(self, mis, room, message,user):
        print(mis)
        users=User.objects.get(username=mis)
        print(users)
        room = Room.objects.get(slug=room)
        Message.objects.create(user=users, room=room, content=message)