from django.shortcuts import render
from .battleships import default_grid, Tile
from django.template.response import TemplateResponse

from .consumers import game
from .battleships import GRID_LETTERS

user = 'You'


def battlefield(request):
    return render(request, 'battle/battlefield.html',
                  {'human_tiles': data, 
                    'bot_tiles': data,
                  'User': user,
                  'History': game.get_history_back(),
                  'letters': GRID_LETTERS
                  })
