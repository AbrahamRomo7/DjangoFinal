from django.contrib import admin
from .models import Equipo,Jugador,Estadio,Goles,Partidos
# Register your models here.
admin.site.register(Equipo)
admin.site.register(Estadio)
admin.site.register(Goles)
admin.site.register(Partidos)
admin.site.register(Jugador)