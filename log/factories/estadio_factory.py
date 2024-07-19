from ..models import Estadio

class EstadioFactory:
    @staticmethod
    def create(nombre, pais):
        return Estadio.objects.create(nombre=nombre, pais=pais)
