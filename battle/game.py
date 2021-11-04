from .shipbuild import default_grid, Tile, SHIPS, place_ship, go_random, GRID_LETTERS


class Player:
    sea = [[]]
    shots_log = []
    player_id = None
    name = None

    def __init__(self, name):
        self.sea = default_grid(Tile)
        self.name = name

    def place_ships(self, ships):
        for ship in ships:
            place_ship(self.sea, go_random())

    def reset_sea(self):
        self.sea.clear()
        self.sea = default_grid(Tile)

    def __repr__(self):
        return self.name

    def __iter__(self):
        yield self.sea


class Game:

    state = 'idle'
    log = []
    '''
    TODO:
    Players is a dictionary
    '''
    players = {}

    def add_player(self, player_id, name):
        '''
        player_id is essentially a player's url
        player's ships will be available at <some_address>/player_id
        '''
        number_of_players = len(set(self.players))
        if number_of_players < 2:
            self.players[player_id] = Player(name)
            result = 'accepted'
        else:
            result = 'refused'
        self.check_state()
        return result

    def check_state(self):
        number_of_players = len(set(self.players))
        if number_of_players == 2 and self.state != 'in_progress':
            self.startgame()
            self.state = 'in_progress'
        elif number_of_players == 1:
            self.state = 'waiting_for_enemy'
        elif number_of_players == 0:
            self.state = 'idle'

    def startgame(self):
        for player_id in self.players:
            player = self.players[player_id]
            player.place_ships(SHIPS)

    def reset(self):
        self.players.clear()
        self.state = 'idle'
        self.log.clear()

    def find_enemy(self, shooter):
        for player in self.players.keys():
            if player != shooter:
                return player

    def shoot(self, enemy, y, x):
        target = self.players[enemy]
        if target.sea[y][x].state == 'default':
            target.sea[y][x].state = 'missed'
        elif target.sea[y][x].state == 'ship':
            target.sea[y][x].state = 'killed'

    def save(self, message):
        self.log.append(message)
