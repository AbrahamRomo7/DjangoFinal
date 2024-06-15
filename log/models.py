from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.forms import DateField, DateInput, Form

# Create your models here.
class Equipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    nombre = models.CharField(max_length=150)
    posicion = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Estadio(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Partidos(models.Model):
    fecha = models.DateField()
    barcelona_total = models.IntegerField(default=0)
    madrid_total = models.IntegerField(default=0)
    ganador = models.CharField(max_length=50,null=True,blank=True)
    estadio = models.ForeignKey(Estadio, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.fecha)
    
    def determinar_ganador(self):
        if self.barcelona_total > self.madrid_total:
            self.ganador = 'Barcelona'
        elif self.madrid_total > self.barcelona_total:
            self.ganador = 'Madrid'
        else:
            self.ganador = 'Empate'

    def save(self, *args, **kwargs):
        self.determinar_ganador()
        super().save(*args, **kwargs)


class Predicciones(models.Model):
    barcelona = models.IntegerField()
    empate = models.IntegerField()
    madrid = models.IntegerField()
    suma = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.barcelona} - {self.empate}- {self.madrid}"

class FiltroPartidosForm(Form):
    fecha_inicio = DateField(label='Fecha de Inicio', required=False, widget=DateInput(attrs={'type': 'date'}))
    fecha_fin = DateField(label='Fecha de Fin', required=False, widget=DateInput(attrs={'type': 'date'}))

class Goles(models.Model):
    fecha = models.ForeignKey(Partidos, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.fecha} - {self.jugador.nombre}"
    
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

@receiver(post_delete, sender=Goles)
def actualizar_puntajes_eliminar_gol(sender, instance, **kwargs):
    partido = instance.fecha
    equipo_jugador = instance.jugador.equipo

    if equipo_jugador.nombre == 'FC BARCELONA':
        partido.barcelona_total -= 1
    elif equipo_jugador.nombre == 'REAL MADRID':
        partido.madrid_total -= 1
    
    partido.save()

