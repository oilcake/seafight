from django.urls import path

from . import views

urlpatterns = [
    path('', views.battlefield, name='battlefield'),
    path('<str:user>/', views.battlefield, name='battle'),
]