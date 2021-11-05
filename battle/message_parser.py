import json

from .shipbuild import GRID_LETTERS


def strip_message(message):
    str_message = message.split(':')[1]
    return str_message[1:]


def convert_coords(message):
    '''
    convert (letter, number) to (y, x)
    '''
    message_split = message.lower().split()
    letter = message_split[1]
    number = message_split[2]
    y = GRID_LETTERS.index(letter)
    x = int(number) - 1
    return y, x


class MessageParser:

    def __init__(self, game):
        self.game = game

    def parse(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'chat':
            message = text_data_json['message']
            self.game.save(message)
            shooter = text_data_json['shooter']
            striped_message = strip_message(message)
            if striped_message.lower().startswith('bang '):
                return self.shoot(shooter, striped_message)
            return self.chat(message)

        elif text_data_json['type'] == 'game':
            if text_data_json['message'] == 'refresh':
                return self.ships()

    def shoot(self, shooter, striped_message):
        enemy = self.game.find_enemy(shooter)
        shot_y, shot_x = convert_coords(striped_message)
        self.game.shoot(enemy, shot_y, shot_x)
        data = {'type': 'system_message',
                'ships': self.game.players}
        return data

    def ships(self):
        if self.game.state == 'in_progress':
            ships = self.game.players
        elif self.game.state == 'waiting_for_enemy':
            ships = 'some_ships'
        # construct game message
        data = {'type': 'system_message',
                'ships': ships}
        return data

    def chat(self, message):
        # construct chat message
        data = {'type': 'chat_message',
                'message': message}
        return data
