# chat/consumers.py
import random
import json
from channels.generic.websocket import WebsocketConsumer

from .battleships import default_grid, Tile, Game


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, Tile):
        return obj.__repr__()

    return obj.__dict__


data = default_grid(Tile)

x = random.randint(0, 9)
y = random.randint(0, 9)
data[y][x].state = 'wounded'
x = random.randint(0, 9)
y = random.randint(0, 9)
data[y][x].state = 'killed'
x = random.randint(0, 9)
y = random.randint(0, 9)
data[y][x].state = 'killed'


class BattleConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']



        self.send(text_data=json.dumps({
            'message': 'you: ' + message
        }))

        bot_message = 'prepare to die'
        self.send(text_data=json.dumps({
            'message': 'bot: ' + bot_message,
            'field': data
        },
            default=serialize
        ))
