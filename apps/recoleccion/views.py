"""Vistas del módulo de seguimiento y gestión de recolecciones."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ConfirmarRecoleccionForm, RecoleccionForm
from .models import Recoleccion


@login_required
def recolecciones(request):
    """Bandeja de recolecciones según el rol del usuario."""
    if request.user.rol == 'operador':
        coleccion = Recoleccion.objects.filter(operador=request.user).order_by('-fecha_solicitud')
    elif request.user.rol == 'ciudadano':
        coleccion = Recoleccion.objects.filter(
            punto__raees__usuario=request.user
        ).distinct().order_by('-fecha_solicitud')
    else:
        coleccion = Recoleccion.objects.all().order_by('-fecha_solicitud')
    return render(request, 'recoleccion/recolecciones.html', {'recolecciones': coleccion})


@login_required
def recoleccion_detalle(request, pk):
    """Timeline de trazabilidad de una recolección."""
    recoleccion = get_object_or_404(Recoleccion, pk=pk)
    if request.user.rol == 'operador' and recoleccion.operador != request.user:
        messages.error(request, 'Esta recolección no está asignada a ti.')
        return redirect('recolecciones')
    if request.user.rol == 'ciudadano' and not recoleccion.punto.raees.filter(usuario=request.user).exists():
        messages.error(request, 'No tienes acceso a esta recolección.')
        return redirect('recolecciones')
    return render(request, 'recoleccion/recoleccion_detalle.html', {'recoleccion': recoleccion})


@login_required
def recoleccion_nueva(request):
    """Solicitud de recolección (funcionarios y administradores)."""
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


@login_required
def recoleccion_actualizar_estado(request, pk):
    """Cambio de estado controlado por el operador asignado o un funcionario."""
    recoleccion = get_object_or_404(Recoleccion, pk=pk)
    permitido = (
        request.user.rol in ('administrador', 'funcionario')
        or (request.user.rol == 'operador' and recoleccion.operador == request.user)
    )
    if not permitido:
        messages.error(request, 'No tienes permisos sobre esta recolección.')
        return redirect('recolecciones')

    if request.method == 'POST':
        nuevo = request.POST.get('estado')
        if nuevo not in dict(Recoleccion.ESTADO_CHOICES):
            messages.error(request, 'Estado no válido.')
        elif nuevo == 'recolectada':
            messages.error(request, 'Usa el formulario de confirmación para registrar peso real.')
        else:
            recoleccion.estado = nuevo
            if nuevo == 'programada' and not recoleccion.fecha_programada:
                recoleccion.fecha_programada = timezone.now()
            recoleccion.save()
            messages.success(request, f'Recolección actualizada a "{recoleccion.get_estado_display()}".')
    return redirect('recoleccion_detalle', pk=recoleccion.pk)


@login_required
def recoleccion_confirmar(request, pk):
    """Confirmación de recolección con peso real y destino final."""
    recoleccion = get_object_or_404(Recoleccion, pk=pk)
    es_operador_asignado = request.user.rol == 'operador' and recoleccion.operador == request.user
    if not es_operador_asignado and request.user.rol != 'administrador':
        messages.error(request, 'Solo el operador asignado puede confirmar esta recolección.')
        return redirect('recolecciones')

    if request.method == 'POST':
        form = ConfirmarRecoleccionForm(request.POST, instance=recoleccion)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.estado = 'recolectada'
            rec.fecha_recoleccion = timezone.now()
            rec.save()
            # Sincroniza capacidad del punto y estado de los RAEE asociados
            for raee in rec.punto.raees.filter(estado__in=['REGISTRADO', 'ASIGNADO_A_PUNTO']):
                raee.actualizar_estado('RECOLECTADO', request.user, observacion=f'Recolección #{rec.pk}')
            messages.success(request, 'Recolección confirmada. ¡Gracias por reciclar con responsabilidad!')
            return redirect('recoleccion_detalle', pk=rec.pk)
    else:
        form = ConfirmarRecoleccionForm(instance=recoleccion)

    return render(request, 'recoleccion/recoleccion_confirmar.html', {
        'form': form, 'recoleccion': recoleccion,
    })
