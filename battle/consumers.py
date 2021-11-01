# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .shipbuild import Tile
from .game import Game


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, Tile):
        return obj.__repr__()

    return obj.__dict__


game = Game()


class BattleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(game.save(message))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        if event:
            message = event['message']
        print(game.players)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            # 'message': bot_reply,
            'user_sea': game.players[0].sea,
            'bot_sea': game.players[1].sea,
        },
            default=serialize
        ))
