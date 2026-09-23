from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RecoleccionForm
from .models import Recoleccion


@login_required
def recolecciones(request):
    if request.user.rol == 'operador':
        colecciones = Recoleccion.objects.filter(operador=request.user).order_by('-fecha_solicitud')
    else:
        colecciones = Recoleccion.objects.all().order_by('-fecha_solicitud')
    return render(request, 'recoleccion/recolecciones.html', {'recolecciones': colecciones})


@login_required
def recoleccion_nueva(request):
    if request.user.rol not in ['funcionario', 'administrador']:
        messages.error(request, 'No tienes permisos para crear recolecciones.')
        return redirect('home')

    if request.method == 'POST':
        form = RecoleccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recolección registrada correctamente.')
            return redirect('recolecciones')
    else:
        form = RecoleccionForm()

    return render(request, 'recoleccion/recoleccion_form.html', {'form': form})
