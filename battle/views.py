from django.shortcuts import render, HttpResponse

from .game import Player
from .consumers import game


def index(request):
    return render(request, 'battle/index.html')


def battlefield(request, username):
    if game.state == 'in_progress':
        return HttpResponse('сорян, третий лишний')

    elif game.state == 'idle' or game.state == 'waiting_for_enemy':
        sailor = request.META['HTTP_COOKIE']
        player = Player(sailor, username)
        game.add(player)

        return render(request, 'battle/battlefield.html', {
            'username': username,
            'state': game.state,
            'History': game.log,
            })
