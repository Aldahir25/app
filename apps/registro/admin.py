from django.contrib import admin
from .models import CategoriaRAEE, PuntoAcopio, RegistroRAEE


@admin.register(CategoriaRAEE)
class CategoriaRAEEAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'peligroso', 'estado')
    list_filter = ('peligroso', 'estado')
    search_fields = ('nombre', 'descripcion')


@admin.register(PuntoAcopio)
class PuntoAcopioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'capacidad_max', 'capacidad_actual', 'estado', 'operador', 'activo')
    list_filter = ('estado', 'activo', 'operador')
    search_fields = ('nombre', 'direccion')


@admin.register(RegistroRAEE)
class RegistroRAEEAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'usuario', 'categoria', 'tipo_aparato', 'estado', 'punto_acopio', 'fecha_registro')
    list_filter = ('estado', 'categoria', 'punto_acopio', 'fecha_registro')
    search_fields = ('codigo', 'tipo_aparato', 'usuario__username')