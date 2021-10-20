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

game = Game()


class BattleConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        human_signed_message = 'you: ' + message
        game.save(human_signed_message)

        self.send(text_data=json.dumps({
            'message': human_signed_message
        }))
        
        bot_reply = 'bot: ' + game.choose_action(message)
        game.save(bot_reply)

        self.send(text_data=json.dumps({
            'message': bot_reply,
            'user_sea': game.user.sea,
            'bot_sea': game.bot.sea,
        },
            default=serialize
        ))
