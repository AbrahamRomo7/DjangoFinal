from ..models import Goles

class GolesFactory:
    @staticmethod
    def create(fecha, jugador):
        return Goles.objects.create(fecha=fecha, jugador=jugador)
