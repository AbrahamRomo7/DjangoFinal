from ..models import Predicciones

class PrediccionesFactory:
    @staticmethod
    def create(barcelona, empate, madrid):
        return Predicciones.objects.create(barcelona=barcelona, empate=empate, madrid=madrid)
