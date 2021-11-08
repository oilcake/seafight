from random import randint

from battle.error import ShipPlacementError


BOARDHEIGHT = 10
BOARDWIDTH = 10

# list of tuples with ships' properties:
# ship_size and ship_shape - straight/twisted
SHIPS = [
        (3, 'straight'),
        (5, 'straight'),
        (2, 'straight')
    ]


def letter_range(start, stop="{", step=1):
    """Yield a range of lowercase letters."""
    for ord_ in range(ord(start.lower()), ord(stop.lower()), step):
        yield chr(ord_)


GRID_LETTERS = list(letter_range("a", "k"))


def default_sea(empty_tile):
    """
    Function generates a list of 10 x 10 tiles with default values
    """
    default_sea = [[]*BOARDWIDTH]*BOARDHEIGHT
    for y in range(BOARDHEIGHT):
        default_sea[y] = [empty_tile() for x in range(BOARDWIDTH)]

    return default_sea


def go_random():
    y = randint(0, BOARDHEIGHT - 1)
    x = randint(0, BOARDWIDTH - 1)
    return y, x


def random_direction():
    return randint(-1, 1)


def generate_start_point(sea: object):
    while True:
        y, x = go_random()
        if (tile_is_empty(sea[y][x]) and
                enough_room_around(sea, y, x)):
            break
    return y, x


def valid_ship(sea: object, ship: object):
    print('ID', id(ship))
    y, x = (generate_start_point(sea))
    print('start point', y, x)
    while True:
        try:
            direction_y = 0
            direction_x = 0
            while abs(direction_y) == abs(direction_x):
                direction_y = random_direction()
                direction_x = random_direction()
            for desk in range(ship.size):
                ship.build_desk(y, x)
                y += direction_y
                x += direction_x
                if (not tile_is_valid(y, x)) or (not tile_is_empty(sea[y][x])):
                    ship.desks.clear()
                    print('cleared desks', ship.desks)
                    print('error raised')
                    raise ShipPlacementError
                    break
                sea[y][x].ship = ship
                ship.build_desk(y, x)
                sea[y][x].state = 'ship'
            return ship
        except ShipPlacementError:
            pass


def tile_is_valid(y, x):
    valid_y = y in range(BOARDHEIGHT)
    valid_x = x in range(BOARDWIDTH)
    return valid_x and valid_y


def tile_is_empty(tile):
    return tile.ship is None


def enough_room_around(sea: object, center_y, center_x):
    for y_delta in range(-1, 2):
        y = center_y + y_delta
        for x_delta in range(-1, 2):
            x = center_x + x_delta
            if (not tile_is_valid(y, x)) or (not tile_is_empty(sea[y][x])):
                return False
    return True


def ship_is_valid(ship):
    """
    checks if ship is not placed too close to other ships
    and not falls outside the gameboard
    """
    return True


def ships_are_valid(ships):
    pass


class Tile(object):
    """
    color represents the state of a tile:
    white - default
    blue - missed
    green - there's a ship
    red - wounded part of the ship
    black - part of dead ship
    """
    color = None
    ship = None

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
