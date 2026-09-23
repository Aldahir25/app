from django.contrib import admin
from .models import Educacion, ContenidoEducativo, Evaluacion

@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('titulo', 'descripcion')


@admin.register(ContenidoEducativo)
class ContenidoEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'publicado')
    list_filter = ('publicado',)
    search_fields = ('titulo', 'descripcion')
    list_editable = ('orden', 'publicado')


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'momento', 'puntaje', 'total_preguntas', 'fecha')
    list_filter = ('momento', 'fecha')
    search_fields = ('usuario__username',)
    readonly_fields = ('fecha',)