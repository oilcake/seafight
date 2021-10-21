from django.shortcuts import render

from .consumers import game
from .shipbuild import GRID_LETTERS

user = 'You'


def battlefield(request):
    return render(request, 'battle/battlefield.html',
                  {'human_tiles': game.user.sea,
                   'bot_tiles': game.bot.sea,
                   'User': user,
                   'History': game.log,
                   'letters': GRID_LETTERS
                   })
