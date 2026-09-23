"""Vistas del núcleo: landing, autenticación y dashboard por roles."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from apps.registro.models import Alerta, RegistroRAEE
from apps.recoleccion.models import Recoleccion
from apps.usuarios.forms import RegistroUsuarioForm


def home(request):
    """Página pública de bienvenida (landing) del sistema RAEE VES."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    contexto = {
        'total_raees': RegistroRAEE.objects.count(),
        'peso_total': RegistroRAEE.objects.aggregate(t=Sum('peso_estimado'))['t'] or 0,
        'recolecciones_finalizadas': Recoleccion.objects.filter(estado='finalizada').count(),
    }
    return render(request, 'home.html', contexto)


def register_view(request):
    """Registro público de nuevos ciudadanos."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Bienvenido a EcoTrack! Tu cuenta fue creada correctamente.')
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard adaptado al rol del usuario autenticado."""
    rol = request.user.rol
    contexto = {'rol': rol}

    if rol == 'ciudadano':
        mis_raees = RegistroRAEE.objects.filter(usuario=request.user)
        contexto.update({
            'mis_raees': mis_raees[:5],
            'total_mis_raees': mis_raees.count(),
            'peso_mis_raees': mis_raees.aggregate(t=Sum('peso_estimado'))['t'] or 0,
            'recolecciones': Recoleccion.objects.filter(
                punto__raees__usuario=request.user
            ).distinct()[:5],
        })
    elif rol == 'operador':
        contexto.update({
            'puntos': request.user.puntos_acopio.filter(activo=True),
            'recolecciones': Recoleccion.objects.filter(operador=request.user).order_by('-fecha_solicitud')[:10],
            'pendientes': Recoleccion.objects.filter(operador=request.user, estado='pendiente').count(),
        })
    elif rol in ('funcionario', 'administrador'):
        por_estado = list(
            RegistroRAEE.objects.values('estado').annotate(cantidad=Count('id')).order_by('-cantidad')
        )
        contexto.update({
            'total_raees': RegistroRAEE.objects.count(),
            'peso_total': RegistroRAEE.objects.aggregate(t=Sum('peso_estimado'))['t'] or 0,
            'total_recolecciones': Recoleccion.objects.count(),
            'recolecciones_pendientes': Recoleccion.objects.filter(estado='pendiente').count(),
            'por_estado': por_estado,
            'alertas': Alerta.objects.filter(estado=True).order_by('-fecha')[:6],
        })

    return render(request, 'dashboard.html', contexto)


def login_view(request):
    """Autenticación de usuarios con formulario de Django."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
