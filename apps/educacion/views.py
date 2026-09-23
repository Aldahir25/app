from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ContenidoEducativo, Evaluacion


@login_required
def educacion(request):
    contenidos = ContenidoEducativo.objects.filter(publicado=True).order_by('orden')
    return render(request, 'educacion/educacion.html', {'contenidos': contenidos})


@login_required
def evaluacion(request):
    if request.method == 'POST':
        respuestas = [
            request.POST.get('respuesta_1', '0'),
            request.POST.get('respuesta_2', '0'),
            request.POST.get('respuesta_3', '0'),
        ]
        puntaje = sum(int(r) for r in respuestas if r.isdigit())
        Evaluacion.objects.create(
            usuario=request.user,
            puntaje=puntaje,
            total_preguntas=3,
            momento=request.POST.get('momento', 'pre'),
        )
        return render(
            request,
            'educacion/evaluacion_resultado.html',
            {'puntaje': puntaje, 'total_preguntas': 3},
        )

    return render(request, 'educacion/evaluacion.html')
