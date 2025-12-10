import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope['url_route']['kwargs']['user_pk']
        self.room_name = self.get_room_name(self.user.id, self.other_user_id)
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        created_at = text_data_json['created_at'] 
        receiver = text_data_json["receiver"]
        from chat.models import Message
        from django.contrib.auth import get_user_model
        sender = self.user
        receiver = await database_sync_to_async(get_user_model().objects.get)(pk=receiver["pk"])
        await database_sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            text=message,
            created_at=created_at
            )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': {
                    "username": self.user.username,
                    "pk": self.user.pk
                },
                'created_at': created_at, 
                'receiver': {
                    "pk": receiver.pk
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'created_at': event['created_at'],
            'receiver': event['receiver']
        }))

    def get_room_name(self, user1_id, user2_id):
        if user1_id > int(user2_id):
            user1_id, user2_id = user2_id, user1_id
        return f"{user1_id}_{user2_id}"