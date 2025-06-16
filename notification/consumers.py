import json
from rest_framework.authtoken.models import Token
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from post.models import Post, SavedPost

User = get_user_model()

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('=')[-1]

        if not token:
            await self.close()  
            return
        
        user = await self.get_user_from_token(token)
        if user is None:
            await self.close()  
            return

        self.user = user
        self.group_name = f"notifications_{self.user.id}"
        # print(f" Connecting to group: {self.group_name} for user: {self.user.username}")
        
        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Send a welcome message
        await self.send_json({
            'message': 'Welcome to the notifications channel!'
        })
    
    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None
    
    
    async def send_notification(self, event):
        notification = event['notification']
        
        # Send the notification to WebSocket
        await self.send_json({
            'type': 'notification',
            'notification': notification
        })


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.close()