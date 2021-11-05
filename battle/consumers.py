# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .message_parser import MessageParser
from .shipbuild import Tile
from .game import Game


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Tile):
        return obj.__repr__()
    return obj.__dict__


game = Game()
parser = MessageParser(game)


# def pack_ships(players):
#     dict_out = {}
#     for player_id, player in players:
#         dict_out[player_id] = player.sea
#     return dict_out


# def find_not_player(player_id):
#     '''
#     finds the opponent from dict with players
#     '''
#     for player in game.players.keys():
#         if player != player_id:
#             return player


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
        data = parser.parse(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, data)

    # Receive message from room group
    async def chat_message(self, event):
        if event:
            message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
        }))

    # Receive message from room group
    async def system_message(self, event):
        if event:
            message = event['ships']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game',
            'ships': message,
        }, default=serialize))
