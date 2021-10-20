import random

from django.shortcuts import render
from .battleships import default_grid, Tile
from django.template.response import TemplateResponse


data = default_grid(Tile)
x = random.randint(0, 9)
y = random.randint(0, 9)
data[y][x].state = 'wounded'
x = random.randint(0, 9)
y = random.randint(0, 9)
data[y][x].state = 'killed'
x = random.randint(0, 9)
y = random.randint(0, 9)
data[y][x].state = 'killed'

user = 'Me'


def battlefield(request):
    return render(request, 'battle/battlefield.html',
                  {'human_tiles': data, 
                    'bot_tiles': data,
                  'User': user})

