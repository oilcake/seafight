import random

from django.shortcuts import render
from .battleships import default_grid, Tile
from django.template.response import TemplateResponse

from .consumers import game


data = default_grid(Tile)

user = 'Me'


def battlefield(request):
    return render(request, 'battle/battlefield.html',
                  {'human_tiles': data, 
                    'bot_tiles': data,
                  'User': user,
                  'History': game.get_history_back()})

