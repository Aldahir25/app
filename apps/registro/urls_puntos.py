from django.urls import path
from .views_puntos import puntos_acopio

urlpatterns = [
    path('puntos-acopio/', puntos_acopio, name='puntos_acopio'),
]
