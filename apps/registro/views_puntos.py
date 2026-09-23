from django.shortcuts import render

from .models import PuntoAcopio


def puntos_acopio(request):
    puntos = PuntoAcopio.objects.filter(activo=True).order_by('nombre')
    return render(request, 'registro/puntos_acopio.html', {'puntos': puntos})
