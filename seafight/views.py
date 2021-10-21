from django.shortcuts import redirect


def hello(request):
    return redirect('/battle')
