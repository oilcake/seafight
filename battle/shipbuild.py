import random


BOARDHEIGHT = 10
BOARDWIDTH = 10

# list of tuples with ships' properties:
# ship_size and ship_shape - straight/twisted
SHIPS = [
        (1, 'straight'),
        (1, 'straight'),
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

    state = property(get_state, set_state)

    def __repr__(self):
        return self.state

    def __iter__(self):
        yield self.state
