import random


BOARDHEIGHT = 10
BOARDWIDTH = 10

# list of tuples with ships' properties - (ship_size, ship_shape)
SHIPS = [
        (1, 'straight'),
        (1, 'straight'),
        # (2, 'straight'),
        # (3, 'straight'),
        # (3, 'twisted'),
        # (4, 'straight')
    ]


def letter_range(start, stop="{", step=1):
    """Yield a range of lowercase letters."""
    for ord_ in range(ord(start.lower()), ord(stop.lower()), step):
        yield chr(ord_)


GRID_LETTERS = list(letter_range("a", "k"))


def default_grid(empty_tile):
    """
    Function generates a list of 10 x 10 tiles with default values
    """
    default_grid = [[]*BOARDWIDTH]*BOARDHEIGHT
    for y in range(BOARDHEIGHT):
        default_grid[y] = [empty_tile() for x in range(BOARDWIDTH)]

    return default_grid


def print_grid(grid):
    for _ in grid:
        print(_)


def go_random():
    y = random.randint(0, BOARDHEIGHT - 1)
    x = random.randint(0, BOARDWIDTH - 1)
    return y, x

def place_ship(sea: object, coords: tuple):
    y, x = (coords)
    sea[y][x].state = 'ship'

def valid(ship):
    """
    checks if ship is not placed too close to other ships
    and not falls outside the gameboard
    """
    pass


class Tile(object):
    """
    color represents the state of the tile:
    white - default
    blue - missed
    green - there's a ship
    red - wounded part of the ship
    gray - part of dead ship
    """
    color = None

    def __init__(self):
        self.set_state('default')

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        self.paint()

    def paint(self):
        match self._state:
            case 'default':
                self.color = 'white'
            case 'missed':
                self.color = 'blue'
            case 'ship':
                self.color = 'green'
            case 'wounded':
                self.color = 'red'
            case 'killed':
                self.color = 'gray'

    state = property(get_state, set_state)

    def __repr__(self):
        return self.color

    def __iter__(self):
        yield self.color


class Player:
    sea = [[]]
    shots_log = []

    def __init__(self):
        self.sea = default_grid(Tile)

    def place_ships(self, ships):
        for ship in ships:
            place_ship(self.sea, go_random())

    def reset_sea(self):
        del self.sea
        self.__init__()


class Game:

    state = 'idle'
    log = []
    reply = 'prepare to be killed'
    user = Player()
    bot = Player()

    def __init__(self):
        pass
    
    def startgame(self):
        self.user.place_ships(SHIPS)
        self.bot.place_ships(SHIPS)

    def __init__(self):
        default_grid(Tile)

    def reset(self):
        self.user.reset_sea()
        self.bot.reset_sea()
        self.state = 'idle'
        del self.log
        self.log = []

    def choose_action(self, message):

        message_split = message.lower().split() 
        match message_split:

            case ['start']:
                match self.state:
                    case 'idle':
                        self.state = 'in progress'
                        self.startgame()
                        self.reply = 'ok, let the battle start!'
                    case 'in progress':
                        self.reply = "we are already playing, aren't we?"

            case letter, number if letter in GRID_LETTERS:
                self.reply = self.shoot(self.bot, GRID_LETTERS.index(letter), int(number) - 1)

            case 'hi', *greetings:
                self.reply = 'prepare to die!'
            case 'fuck', *details:
                self.reply = 'why are you so rude?'
            case ['reset']:
                self.reset()
                self.reply = 'ok, buy'
            case _:
                self.reply = "can't get you. you are strange"

        return self.reply

    def shoot(self, target, y, x):
        match target.sea[y][x].state:
            case 'default':
                target.sea[y][x].state = 'missed'
                reply = 'Nope. My turn!'
                self.bot_move()
            case 'ship':
                target.sea[y][x].state = 'killed'
                reply = 'Omg. You are killing me!'
            case 'wounded':
                reply = 'Why again?! It is already hurts!'
            case 'killed':
                reply = 'Why again?! It is already hurts!'
        return reply

    def bot_move(self):
        while True:
            bot_shot = go_random()
            if bot_shot not in self.bot.shots_log:
                break
        self.bot.shots_log.append(bot_shot)
        y, x = bot_shot
        match self.user.sea[y][x].state:                
            case 'ship':
                self.user.sea[y][x].state = 'killed'
            case 'default':
                self.user.sea[y][x].state = 'missed'

    def save(self, message):
        self.log.append(message)


