# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .shipbuild import Tile
from .game import Game


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, Tile):
        return obj.__repr__()

    return obj.__dict__


game = Game()


class BattleConsumer(WebsocketConsumer):
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
