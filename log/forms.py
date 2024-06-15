from django.forms import DateField, DateInput, Form, ModelForm
from .models import Jugador,Estadio,Partidos,Goles

class JugadorForm(ModelForm):
    class Meta:
        model = Jugador
        fields = '__all__'

class EstadioForm(ModelForm):
    class Meta:
        model = Estadio
        fields = ['nombre', 'pais']

class PartidosForm(ModelForm):
    fecha = DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Partidos
        fields = ['fecha', 'barcelona_total', 'madrid_total', 'ganador', 'estadio']

class GolesForm(ModelForm):
    class Meta:
        model = Goles
        fields = ['fecha', 'jugador']

class FiltroPartidosForm(Form):
    fecha_inicio = DateField(label='Fecha de Inicio', required=False, widget=DateInput(attrs={'type': 'date'}))
    fecha_fin = DateField(label='Fecha de Fin', required=False, widget=DateInput(attrs={'type': 'date'}))