from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home),
    path('administrador/', views.administrador, name='administrador'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('jugadores/', views.jugadores, name='jugadores'),
    path('partidos/', views.partidos, name='partidos'),
    path('', views.salir, name='salir'),
]
