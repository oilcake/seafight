from django.shortcuts import render

from .consumers import game
from .shipbuild import GRID_LETTERS

user = 'You'

# ht = json.dumps({game.user.sea}, default=serialize)
# bt = json.dumps({game.bot.sea}, default=serialize)

ht = game.user.sea
bt = game.bot.sea

text_data = {'human_tiles': ht,
             'bot_tiles': bt,
             'User': user,
             'History': game.log,
             'letters': GRID_LETTERS
             }


def battlefield(request):
    return render(request, 'battle/battlefield.html', text_data)
