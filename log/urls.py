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
    path('adminJugadores/', views.adminJugadores, name='adminJugadores'),
    path('adminJugadores/crear/', views.crear_jugador, name='crear_jugador'),
    path('adminJugadores/editar/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('adminJugadores/eliminar/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
    path('adminPartidos/', views.adminPartidos, name='adminPartidos'),
    path('crear_partido/', views.crear_partido, name='crear_partido'),
    path('eliminar_partido/<int:pk>/', views.eliminar_partido, name='eliminar_partido'),
    path('adminEstadios/', views.adminEstadios, name='adminEstadios'),
    path('adminGoleadores/', views.adminGoleadores, name='adminGoleadores'),
    path('adminGoleadores/eliminar/<int:gol_id>/', views.eliminar_gol, name='eliminar_gol'),
    path('', views.salir, name='salir'),
]
