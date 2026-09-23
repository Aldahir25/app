from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render

from apps.registro.models import RegistroRAEE, PuntoAcopio
from apps.recoleccion.models import Recoleccion


@login_required
def reportes(request):
    if request.user.rol not in ['funcionario', 'administrador']:
        return render(request, 'reportes/no_access.html')

    total_raees = RegistroRAEE.objects.count()
    total_puntos = PuntoAcopio.objects.filter(activo=True).count()
    total_recolecciones = Recoleccion.objects.count()
    total_por_estado = list(
        RegistroRAEE.objects.values('estado').annotate(cantidad=Count('id')).order_by('-cantidad')
    )
    peso_total = RegistroRAEE.objects.aggregate(total=Sum('peso_estimado'))['total'] or 0

    context = {
        'total_raees': total_raees,
        'total_puntos': total_puntos,
        'total_recolecciones': total_recolecciones,
        'peso_total': peso_total,
        'total_por_estado': total_por_estado,
    }
    return render(request, 'reportes/dashboard.html', context)
