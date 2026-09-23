from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_generacion', 'tipo')
    list_filter = ('tipo', 'fecha_generacion')
    search_fields = ('titulo', 'descripcion')