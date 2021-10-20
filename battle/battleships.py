import random


BOARDHEIGHT = 10
BOARDWIDTH = 10

# list of tuples with ships' properties - (ship_size, ship_shape)
# 0 - ship is straight, 1 - ship is twisted
SHIPS = [
        (1, 'straight'),
        # (1, 'straight'),
        # (2, 'straight'),
        # (3, 'straight'),
        # (3, 'twisted'),
        # (4, 'straight')
    ]


def letter_range(start, stop="{", step=1):
    """Yield a range of lowercase letters."""
    for ord_ in range(ord(start.upper()), ord(stop.upper()), step):
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


def look_for_ship(grid: object, coords: tuple):
    """
    returns what's going on the board within given coordinates
    """
    (x, y) = coords
    return grid[y][x]


def go_random(grid: object):
    y = random.randint(0, BOARDHEIGHT - 1)
    x = random.randint(0, BOARDWIDTH - 1)
    coords = x, y
    what_is_there = look_for_ship(grid, coords)
    return what_is_there


def valid(ship):
    """
    checks if ship is not placed too close to other ships
    and not falls outside the gameboard
    """
    pass


class Tile(object):
    """
    color represents the state of the tile:
    blue - default
    green - missed shot
    red - wounded ship
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
            case 'wounded':
                self.color = 'red'
            case 'killed':
                self.color = 'gray'

    state = property(get_state, set_state)

    def __repr__(self):
        return self.color

    def __iter__(self):
        yield self.color


class Ship:

    def __init__(self, ship_properties):
        self.ship_size, self.ship_shape = ship_properties

    def build(self):
        for part in self.ship_size:
            x, y = go_random(grid)


class Game:
    pass


class Sea:

    def __init__(self):
        pass


class Bot:
    pass


class Chat:
    pass
