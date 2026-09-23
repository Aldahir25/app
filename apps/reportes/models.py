from django.db import models

class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    
    def __str__(self):
        return self.titulo