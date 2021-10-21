from .shipbuild import default_grid, Tile, SHIPS, place_ship, go_random, GRID_LETTERS


class Player:
    sea = [[]]
    shots_log = []

    def __init__(self):
        self.sea = default_grid(Tile)

    def place_ships(self, ships):
        for ship in ships:
            place_ship(self.sea, go_random())

    def reset_sea(self):
        self.sea.clear()
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
        self.log.clear()

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
                self.reply = 'ok, buy!'
                self.reset()
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
