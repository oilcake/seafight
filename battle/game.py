from battle.shipbuild import SHIPS
from battle.shipbuild import Tile
from battle.shipbuild import default_sea, valid_ship
from battle.shipbuild import generate_start_point


class Ship:

    alive = True
    desks = []

    def __init__(self, ship_properties: tuple):
        self.size, self.shape = (ship_properties)

    def shot_down(self):
        if self.size:
            self.size -= 1
        else:
            self.alive = False

    def build_desk(self, y, x):
        desk = (y, x)
        self.desks.append(desk)


class Player:
    sea = [[]]  # player's grid
    shots_log = []
    player_id = None  # it's gonna be player's url
    name = None
    alive = True
    ships = []

    def __init__(self, name):
        self.sea = default_sea(Tile)
        self.name = name

    def place_ships_randomly(self, ships: list):
        for ship_properties in ships:
            self.build_ship(Ship(ship_properties))

    def build_ship(self, ship: object):
        y, x = generate_start_point(self.sea)
        self.sea[y][x].ship = ship
        self.sea[y][x].state = 'ship'
        self.ships.append(id(ship))

    def reset_sea(self):
        self.sea.clear()
        self.sea = default_sea(Tile)

    def __repr__(self):
        return self.name

    def __iter__(self):
        yield self.sea


class Game:

    state = 'idle'
    log = []

    players = {}

    def add_player(self, player_id, name):
        '''
        player_id is essentially a player's url
        player's ships will be available at <some_address>/player_id
        '''
        if self.number_of_players() < 2:
            self.players[player_id] = Player(name)
            result = 'accepted'
        else:
            result = 'refused'
        self.switch_state()
        return result

    def switch_state(self):
        if self.number_of_players() == 2 and self.state != 'in_progress':
            self.start_game()
            self.state = 'in_progress'
        elif self.number_of_players() == 1:
            self.state = 'waiting_for_enemy'
        elif self.number_of_players() == 0:
            self.state = 'idle'

    def number_of_players(self):
        return len(set(self.players))

    def start_game(self):
        for player_id in self.players:
            player = self.players[player_id]
            player.place_ships_randomly(SHIPS)
            print(player.ships)

    def reset(self):
        self.players.clear()
        self.state = 'idle'
        self.log.clear()

    def find_enemy(self, shooter):
        for player in self.players.keys():
            if player != shooter:
                return player

    def shoot(self, enemy, y, x):
        target = self.players[enemy].sea[y][x]
        if target.state == 'default':
            target.state = 'missed'
        elif target.state == 'ship':
            target.ship.shot_down()

            print('alive', target.ship.alive)
            print('size', target.ship.size)

            if target.ship.alive:
                target.state = 'wounded'
            else:
                for desk in target.ship.desks:
                    desk_y, desk_x = (desk)
                    target.sea[desk_y][desk_x].state = 'killed'

    def save(self, message):
        self.log.append(message)
