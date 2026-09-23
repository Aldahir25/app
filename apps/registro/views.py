"""Vistas del módulo de registro y control de RAEE."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistroRAEEForm
from .models import RegistroRAEE


@login_required
def raee_registrar(request):
    """Registro de un aparato en desuso con sugerencia automática de categoría."""
    if request.method == 'POST':
        form = RegistroRAEEForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            registro = form.save(commit=False)
            # El ciudadano siempre registra a nombre propio
            if request.user.rol == 'ciudadano':
                registro.usuario = request.user
            elif not registro.usuario:
                messages.error(request, 'Selecciona el ciudadano dueño del residuo.')
                return render(request, 'registro/raee_form.html', {'form': form})
            registro.save()
            messages.success(request, f'Registro guardado correctamente. Código: {registro.codigo}')
            return redirect('raee_mis_registros')
    else:
        form = RegistroRAEEForm(user=request.user)

    return render(request, 'registro/raee_form.html', {'form': form})


@login_required
def sugerir_categoria(request):
    """API interna: sugiere la categoría UNITAR según el nombre del aparato."""
    from django.http import JsonResponse

    from .services import clasificar_aparato

    nombre = request.GET.get('q', '')
    return JsonResponse({'categoria': clasificar_aparato(nombre)})


@login_required
def raee_mis_registros(request):
    """Listado de residuos registrados por el usuario autenticado."""
    registros = RegistroRAEE.objects.filter(usuario=request.user).order_by('-fecha_registro')
    return render(request, 'registro/raee_list.html', {'registros': registros})
