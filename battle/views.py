from django.shortcuts import render, HttpResponse

from .consumers import game


def battlefield(request, player_id):
    if player_id in game.players.keys():
        player = game.players[player_id]
        username = player.name
        return render(request, 'battle/battlefield.html', {
            'username': username,
            'state': game.state,
            'History': game.log,
            })
    else:
        return HttpResponse('sorryan - tretiy lishniy')
