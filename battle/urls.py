from django.urls import path

from . import views

urlpatterns = [
    path('<str:player_id>/', views.battlefield, name='battle'),
]
