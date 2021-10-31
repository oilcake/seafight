from django.shortcuts import render

from .consumers import game
from .shipbuild import GRID_LETTERS

user = 'You'

# ht = json.dumps({game.user.sea}, default=serialize)
# bt = json.dumps({game.bot.sea}, default=serialize)

ht = game.user.sea
bt = game.bot.sea

text_data = {'human_tiles': ht,
             'bot_tiles': bt,
             'User': user,
             'History': game.log,
             'letters': GRID_LETTERS
             }


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    # ip = get_client_ip(request)
    # print(ip)
    print(request.META['HTTP_COOKIE'])
    request.session['sailor_id'] = request.META['HTTP_COOKIE']
    return render(request, 'battle/index.html')


def battlefield(request, room_name):
    print(request.META['HTTP_COOKIE'])
    return render(request, 'battle/battlefield.html', {
        'room_name': room_name,
        'History': game.log,
        })
