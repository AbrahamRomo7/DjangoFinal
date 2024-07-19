from ..models import Jugador

class JugadorFactory:
    @staticmethod
    def create(nombre, posicion, equipo):
        return Jugador.objects.create(nombre=nombre, posicion=posicion, equipo=equipo)
