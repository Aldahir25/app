from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistroRAEEForm
from .models import RegistroRAEE


@login_required
def raee_registrar(request):
    if request.method == 'POST':
        form = RegistroRAEEForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            registro.save()
            messages.success(request, f'Registro guardado correctamente. Código: {registro.codigo}')
            return redirect('raee_mis_registros')
    else:
        form = RegistroRAEEForm(user=request.user)

    return render(request, 'registro/raee_form.html', {'form': form})


@login_required
def raee_mis_registros(request):
    registros = RegistroRAEE.objects.filter(usuario=request.user).order_by('-fecha_registro')
    return render(request, 'registro/raee_list.html', {'registros': registros})
