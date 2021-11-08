import json

from django.urls import reverse

from battle.consumers import game


def test_home(client):
    url = reverse('hello')
    response = client.get(url)
    assert response.status_code == 200


def test_form(client):
    url = reverse('hello')
    response = client.get(url)
    assert b'Welcome to battleships, prepare to be killed' in response.content


def test_stamp_client(client):
    game.reset()
    url = reverse('hello')
    statuses = ['accepted', 'refused']
    name = 'Misha'
    encoded_name = name.encode('utf-8')
    body = {'client': {'name': name}}

    response = client.post(url, json.dumps(body),
                           content_type="application/json")

    assert b'client' in response.content
    assert b'name' in response.content
    assert b'key' in response.content
    assert b'status' in response.content
    assert encoded_name in response.content

    test_key = json.loads(response.content)['client']['key']
    status = json.loads(response.content)['client']['status']

    assert test_key is not None
    assert status in statuses


def test_refused_client(client):
    game.reset()
    url = reverse('hello')
    clients = ['Jim', 'Jack', 'Athur III']
    for pending_client in clients:
        body = {'client': {'name': pending_client}}
        response = client.post(url, json.dumps(body),
                               content_type="application/json")
        test_key = json.loads(response.content)['client']['key']
    battle_url = reverse('battle', kwargs={'player_id': test_key})
    response = client.get(battle_url)

    assert b'sorryan' in response.content


def test_player_is_added(client):
    game.reset()
    url = reverse('hello')
    pending_client = 'Henry'
    body = {'client': {'name': pending_client}}
    response = client.post(url, json.dumps(body),
                           content_type="application/json")
    test_key = json.loads(response.content)['client']['key']
    battle_url = reverse('battle', kwargs={'player_id': test_key})
    response = client.get(battle_url)

    assert b'your ships' in response.content
    assert game.state == 'waiting_for_enemy'


def test_two_players_are_added(client):
    game.reset()
    url = reverse('hello')
    clients = ['Jim', 'Jack']
    for pending_client in clients:
        body = {'client': {'name': pending_client}}
        response = client.post(url, json.dumps(body),
                               content_type="application/json")
    test_key = json.loads(response.content)['client']['key']
    battle_url = reverse('battle', kwargs={'player_id': test_key})
    response = client.get(battle_url)

    assert b'your ships' in response.content
    assert game.state == 'in_progress'
