from ..models import Partidos

class PartidosFactory:
    @staticmethod
    def create(fecha, barcelona_total, madrid_total, estadio):
        return Partidos.objects.create(fecha=fecha, barcelona_total=barcelona_total, madrid_total=madrid_total, estadio=estadio)
