import uuid
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse

from battle.consumers import game


def stamp(username):
    return str(uuid.uuid4())


def reset(request):
    game.reset()
    return redirect('hello')


def index(request):

    if request.method == 'GET':
        return render(request, 'battle/index.html')

    if request.method == 'POST':
        decoded = json.loads(request.body)
        client = decoded['client']['name']
        unique_id = stamp(client)
        player_added = game.add_player(unique_id, client)
        response = {'client': {'name': client,
                               'key': unique_id,
                               'status': player_added}}
        return JsonResponse(response)
