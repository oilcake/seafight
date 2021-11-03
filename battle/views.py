from django.shortcuts import render, HttpResponse

from .consumers import game


def battlefield(request, player_id):
    print(game.players)
    # username = game.players[player_id].name
    username = game.players[player_id].name

    return render(request, 'battle/battlefield.html', {
        'username': username,
        'state': game.state,
        'History': game.log,
        })
