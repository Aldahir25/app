"""Rutas del módulo de recolección."""
from django.urls import path

from .views import (
    recoleccion_actualizar_estado,
    recoleccion_confirmar,
    recoleccion_detalle,
    recoleccion_nueva,
    recolecciones,
)

urlpatterns = [
    path('recoleccion/', recolecciones, name='recolecciones'),
    path('recoleccion/nueva/', recoleccion_nueva, name='recoleccion_nueva'),
    path('recoleccion/<int:pk>/', recoleccion_detalle, name='recoleccion_detalle'),
    path('recoleccion/<int:pk>/estado/', recoleccion_actualizar_estado, name='recoleccion_estado'),
    path('recoleccion/<int:pk>/confirmar/', recoleccion_confirmar, name='recoleccion_confirmar'),
]
