from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    return render(request,'log/base.html')

@login_required
def administrador(request):
    return render(request,'log/admin.html')

def estadisticas(request):
    return render(request,'log/estadisticas.html')

def jugadores(request):
    return render(request,'log/jugadores.html')

def partidos(request):
    return render(request,'log/partidos.html')

def salir(request):
    logout(request)
    return redirect('home/')

