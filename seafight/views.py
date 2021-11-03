import uuid
import json

from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse

from battle.consumers import game


def serialize(data):
    return serializers.serialize('json', data)


def json_decode(data):
    return json.loads(data.decode("utf-8"))


def stamp_client(name):
    return str(uuid.uuid4())


def index(request):
    if request.method == 'GET':
        return render(request, 'battle/index.html')
    if request.method == 'POST':
        decoded = json.loads(request.body)
        name = decoded['client']['name']
        unique_id = stamp_client(name)
        game.add_player(unique_id, name)
        response = {'client': {'name': name, 'key': unique_id}}
        return JsonResponse(response)
