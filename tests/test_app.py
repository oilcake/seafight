import json

from django.urls import reverse


def test_home(client):
    url = reverse('hello')
    response = client.get(url)
    assert response.status_code == 200


def test_form(client):
    url = reverse('hello')
    response = client.get(url)
    assert b'Welcome to battleships, prepare to be killed' in response.content


def test_stamp_client(client):
    url = reverse('hello')
    name = 'Misha'
    encoded_name = name.encode('utf-8')
    body = {'client': {'name': name}}

    response = client.post(url, json.dumps(body), content_type="application/json")

    assert b'client' in response.content
    assert b'name' in response.content
    assert b'key' in response.content
    assert encoded_name in response.content

    test_key = json.loads(response.content)['client']['key']

    assert test_key is not None
