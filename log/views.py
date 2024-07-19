from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

from .models import Jugador,Estadio,Partidos,Goles, Predicciones
from .forms import JugadorForm,EstadioForm,PartidosForm,GolesForm,FiltroPartidosForm
from django.contrib import messages
from sklearn.linear_model import LinearRegression
import numpy as np
from django.db.models import Count
from .factories import EquipoFactory, JugadorFactory, EstadioFactory, PartidosFactory, PrediccionesFactory, GolesFactory

# Crear un equipo
barcelona = EquipoFactory.create(nombre="FC BARCELONA")

# Crear un jugador
messi = JugadorFactory.create(nombre="Lionel Messi", posicion="Delantero", equipo=barcelona)

# Crear un estadio
camp_nou = EstadioFactory.create(nombre="Camp Nou", pais="España")

# Crear un partido
partido = PartidosFactory.create(fecha="2024-07-18", barcelona_total=0, madrid_total=0, estadio=camp_nou)

# Crear una predicción
prediccion = PrediccionesFactory.create(barcelona=2, empate=1, madrid=1)

# Crear un gol
gol = GolesFactory.create(fecha=partido, jugador=messi)

def home(request):
    return render(request,'log/home.html')

@login_required
def administrador(request):
    return render(request,'log/admin.html')

@login_required
def adminEstadios(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['action'] == 'edit':
            estadio = get_object_or_404(Estadio, pk=request.POST['id'])
            form = EstadioForm(request.POST, instance=estadio)
            if form.is_valid():
                form.save()
                return redirect('adminEstadios')
        elif 'id' in request.POST and request.POST['action'] == 'delete':
            estadio = get_object_or_404(Estadio, pk=request.POST['id'])
            estadio.delete()
            return redirect('adminEstadios')
        else:
            form = EstadioForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('adminEstadios')
    else:
        form = EstadioForm()

    estadios = Estadio.objects.all()
    context = {'form': form, 'estadios': estadios}
    return render(request, 'log/adminEstadios.html', context)

@login_required
def adminGoleadores(request):
    goles = Goles.objects.all()
    form = GolesForm()

    if request.method == 'POST':
        if 'crear_gol' in request.POST:
            form = GolesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('adminGoleadores')
        elif 'eliminar_gol' in request.POST:
            gol_id = request.POST.get('gol_id')
            gol = get_object_or_404(Goles, pk=gol_id)
            gol.delete()
            return redirect('adminGoleadores')

    context = {
        'goles': goles,
        'form': form,
    }
    return render(request, 'log/adminGoleadores.html', context)

@login_required
def eliminar_gol(request, gol_id):
    gol = get_object_or_404(Goles, pk=gol_id)
    if request.method == 'POST':
        gol.delete()
        return redirect('adminGoleadores')
    context = {'gol': gol}
    return render(request, 'log/eliminar_gol.html', context)

@login_required
def adminJugadores(request):
    jugadores = Jugador.objects.all()
    form = JugadorForm()

    if request.method == 'POST':
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminJugadores')

    context = {
        'form': form,
        'jugadores': jugadores
    }
    return render(request, 'log/adminJugadores.html', context)

@login_required
def crear_jugador(request):
    if request.method == 'POST':
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminJugadores')
    else:
        form = JugadorForm()
    
    return render(request, 'log/crear_jugador.html', {'form': form})

@login_required
def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, pk=jugador_id)

    if request.method == 'POST':
        form = JugadorForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            return redirect('adminJugadores')
    else:
        form = JugadorForm(instance=jugador)
    
    return render(request, 'log/editar_jugador.html', {'form': form, 'jugador': jugador})

@login_required
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, pk=jugador_id)
    
    if request.method == 'POST':
        jugador.delete()
        return redirect('adminJugadores')
    
    return render(request, 'log/eliminar_jugador.html', {'jugador': jugador})

@login_required
def adminPartidos(request):
    if request.method == 'POST':
        if 'id' in request.POST and 'action' in request.POST and request.POST['action'] == 'delete':
            partido = get_object_or_404(Partidos, pk=request.POST['id'])
            partido.delete()
            return redirect('adminPartidos')
        else:
            form = PartidosForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('adminPartidos')
    else:
        form = PartidosForm()

    partidos = Partidos.objects.all()
    context = {'form': form, 'partidos': partidos}
    return render(request, 'log/adminPartidos.html', context)

@login_required
def crear_partido(request):
    if request.method == 'POST':
        form = PartidosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPartidos')
    else:
        form = PartidosForm()
    return render(request, 'log/adminPartidos.html', {'form': form})

@login_required
def eliminar_partido(request, pk):
    partido = get_object_or_404(Partidos, pk=pk)
    if request.method == 'POST':
        partido.delete()
        return redirect('adminPartidos')
    return render(request, 'log/confirmar_eliminar_partido.html', {'partido': partido})

def jugadores(request):
    return render(request,'log/jugadores.html')

def partidos(request):
    return render(request,'log/partidos.html')

def salir(request):
    logout(request)
    return redirect('home/')

def actualizar_predicciones(fecha_inicio=None, fecha_fin=None):
    # Primero, vaciamos la tabla Predicciones
    Predicciones.objects.all().delete()

    # Filtramos los partidos según las fechas si están especificadas
    partidos = Partidos.objects.all()
    if fecha_inicio:
        partidos = partidos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        partidos = partidos.filter(fecha__lte=fecha_fin)

    # Contamos los registros para cada campo
    barcelona_count = partidos.filter(ganador='barcelona').count()
    empate_count = partidos.filter(ganador='empate').count()
    madrid_count = partidos.filter(ganador='madrid').count()

    # Sumamos el total de los registros para asignarlo a 'suma'
    total = barcelona_count + empate_count + madrid_count

    # Creamos una nueva instancia de Predicciones y la guardamos
    predicciones = Predicciones.objects.create(
        barcelona=barcelona_count,
        empate=empate_count,
        madrid=madrid_count,
        suma=total
    )
    predicciones.save()

    # Opcionalmente, puedes devolver las predicciones actualizadas
    return predicciones

def estadisticas(request):
    if request.method == 'GET':
        form = FiltroPartidosForm(request.GET)
        if form.is_valid():
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')

            # Asegúrate de que las fechas no sean None antes de usarlas en la consulta
            partidos = Partidos.objects.all()
            if fecha_inicio:
                partidos = partidos.filter(fecha__gte=fecha_inicio)
            if fecha_fin:
                partidos = partidos.filter(fecha__lte=fecha_fin)

            # Llamar a la función para actualizar las predicciones
            predicciones_actualizadas = actualizar_predicciones(fecha_inicio, fecha_fin)

            # Renderizar la plantilla con los datos actualizados
            context = {
                'form': form,
                'predicciones': predicciones_actualizadas,
                'partidos': partidos  # Utiliza la lista de partidos filtrada
            }
            return render(request, 'log/estadisticas.html', context)
    else:
        form = FiltroPartidosForm()

    context = {
        'form': form,
    }
    return render(request, 'log/estadisticas.html', context)