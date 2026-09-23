"""Rutas del módulo de registro de RAEE."""
from django.urls import path

from .views import raee_mis_registros, raee_registrar, sugerir_categoria

urlpatterns = [
    path('raee/registrar/', raee_registrar, name='raee_registrar'),
    path('raee/mis-registros/', raee_mis_registros, name='raee_mis_registros'),
    path('raee/sugerir-categoria/', sugerir_categoria, name='sugerir_categoria'),
]
