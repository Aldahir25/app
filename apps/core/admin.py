from django.contrib import admin
from .models import Core

@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')