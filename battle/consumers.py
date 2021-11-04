# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .shipbuild import Tile, GRID_LETTERS
from .game import Game


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, Tile):
        return obj.__repr__()

    return obj.__dict__


def strip_message(message):
    str_message = message.split(':')[1]
    return str_message[1:]


game = Game()


def convert_coords(message):
    '''
    convert (letter, number) to (x, y)
    '''
    message_split = message.lower().split()
    letter = message_split[1]
    number = message_split[2]
    y = GRID_LETTERS.index(letter)
    x = int(number) - 1
    return y, x


def pack_ships(players):
    dict_out = {}
    for player_id, player in players:
        dict_out[player_id] = player.sea
    return dict_out


def find_not_player(player_id):
    '''
    finds the opponent from dict with players
    '''
    for player in game.players.keys():
        if player != player_id:
            return player


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
        if text_data_json['type'] == 'chat':
            message = text_data_json['message']
            shooter = text_data_json['shooter']
            strp_message = strip_message(message)
            if strp_message.lower().startswith('bang '):
                enemy = game.find_enemy(shooter)
                shot_y, shot_x = convert_coords(strp_message)
                game.shoot(enemy, shot_y, shot_x)
                data = {'type': 'system_message',
                        'ships': game.players}
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name, data)

            async_to_sync(game.save(message))

            # construct chat message
            data = {'type': 'chat_message',
                    'message': message}

        elif text_data_json['type'] == 'game':
            if text_data_json['message'] == 'refresh':
                if game.state == 'in_progress':
                    ships = game.players
                elif game.state == 'waiting_for_enemy':
                    ships = 'some_ships'

            # construct game message
            data = {'type': 'system_message',
                    'ships': ships}

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
