from django.shortcuts import render
from .battleships import default_grid, Tile

data = default_grid(Tile)
data[5][7].state = 'wounded'
data[3][2].state = 'killed'
data[3][3].state = 'killed'

user = 'Me'


def battlefield(request):
    return render(request, 'battle/battlefield.html',
                  {'tiles': data, 'User': user})
