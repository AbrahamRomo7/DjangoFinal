from ..models import Equipo

class EquipoFactory:
    @staticmethod
    def create(nombre):
        return Equipo.objects.create(nombre=nombre)
