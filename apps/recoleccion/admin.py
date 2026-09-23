from django.contrib import admin
from .models import Recoleccion


@admin.register(Recoleccion)
class RecoleccionAdmin(admin.ModelAdmin):
    list_display = ('punto', 'operador', 'estado', 'fecha_solicitud', 'fecha_atencion', 'peso_total', 'destino', 'tiempo_respuesta_dias')
    list_filter = ('estado', 'operador', 'punto')
    search_fields = ('destino', 'punto__nombre')
    list_select_related = ('punto', 'operador')
    readonly_fields = ('fecha_solicitud', 'tiempo_respuesta_dias')