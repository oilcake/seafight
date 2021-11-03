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


class Game:

    state = 'idle'
    log = []
    '''
    TODO:
    Players is a dictionary
    '''
    players = {}

    def add_player(self, player_id, name):
        number_of_players = len(set(self.players))
        if number_of_players < 2:
            self.players[player_id] = Player(name)
            if number_of_players == 2:
                self.startgame()
                self.state = 'in_progress'
            elif number_of_players == 1:
                self.state = 'waiting_for_enemy'

    def startgame(self):
        for player_id, player in self.players:
            player.place_ships()

    def reset(self):
        self.user.reset_sea()
        self.bot.reset_sea()
        self.state = 'idle'
        self.log.clear()

    def choose_action(self, message):
        self.reply = None
        message_split = message.lower().split()
        if message_split == ['start']:
            if self.state == 'idle':
                self.state = 'in progress'
                self.startgame()
                self.reply = 'ok, let the battle start!'
            elif self.state == 'in progress':
                self.reply = "we are already playing, aren't we?"

        elif len(message_split) == 2 and message_split[0] in GRID_LETTERS:
            letter = message_split[0]
            number = message_split[1]
            x = GRID_LETTERS.index(letter)
            y = int(number) - 1
            self.reply = self.shoot(self.bot, x, y)

        elif message_split[0].lower() == 'fuck':
            self.reply = 'why are you so rude?'
        elif message_split[0].lower() == 'reset':
            self.reply = 'ok, buy!'
            self.reset()
        elif not self.reply:
            self.reply = "can't get you. you are strange"

        return self.reply

    def shoot(self, target, y, x):
        if target.sea[y][x].state == 'default':
            target.sea[y][x].state = 'missed'
            reply = 'Nope. My turn!'
            self.bot_move()
        elif target.sea[y][x].state == 'ship':
            target.sea[y][x].state = 'killed'
            reply = 'Omg. You are killing me!'
        elif target.sea[y][x].state == 'wounded':
            reply = 'Why again?! It is already hurts!'
        elif target.sea[y][x].state == 'killed':
            reply = 'Why again?! It is already hurts!'
        return reply

    def bot_move(self):
        while True:
            bot_shot = go_random()
            if bot_shot not in self.bot.shots_log:
                break
        self.bot.shots_log.append(bot_shot)
        y, x = bot_shot

        if self.user.sea[y][x].state == 'ship':
            self.user.sea[y][x].state = 'killed'
        if self.user.sea[y][x].state == 'default':
            self.user.sea[y][x].state = 'missed'

    def save(self, message):
        self.log.append(message)
