from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Goles, EstadioGoles, Partidos

@receiver(post_save, sender=Goles)
def actualizar_puntajes_gol(sender, instance, created, **kwargs):
    if created:  # Si se crea un nuevo gol
        partido = instance.fecha
        equipo_jugador = instance.jugador.equipo

        if equipo_jugador.nombre == 'FC BARCELONA':
            partido.barcelona_total += 1
        elif equipo_jugador.nombre == 'REAL MADRID':
            partido.madrid_total += 1

        partido.save()

        # Actualizar la cantidad de goles en el estadio
        estadio_goles, _ = EstadioGoles.objects.get_or_create(estadio=partido.estadio)
        estadio_goles.goles += 1
        estadio_goles.save()

@receiver(post_delete, sender=Goles)
def actualizar_puntajes_eliminar_gol(sender, instance, **kwargs):
    partido = instance.fecha
    equipo_jugador = instance.jugador.equipo

    if equipo_jugador.nombre == 'FC BARCELONA':
        partido.barcelona_total -= 1
    elif equipo_jugador.nombre == 'REAL MADRID':
        partido.madrid_total -= 1

    partido.save()

    # Actualizar la cantidad de goles en el estadio
    estadio_goles = EstadioGoles.objects.get(estadio=partido.estadio)
    estadio_goles.goles -= 1
    estadio_goles.save()
