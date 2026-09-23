from django.urls import path
from .views import recolecciones, recoleccion_nueva

urlpatterns = [
    path('recolecciones/', recolecciones, name='recolecciones'),
    path('recolecciones/nueva/', recoleccion_nueva, name='recoleccion_nueva'),
]
