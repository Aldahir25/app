from django.conf import settings
from django.db import models


class ContenidoEducativo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.IntegerField(default=0)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo


class Evaluacion(models.Model):
    MOMENTO_CHOICES = [
        ('pre', 'Pre-evaluación'),
        ('post', 'Post-evaluación'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='evaluaciones',
    )
    puntaje = models.IntegerField()
    total_preguntas = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    momento = models.CharField(max_length=4, choices=MOMENTO_CHOICES)

    def __str__(self):
        return f"{self.usuario} - {self.get_momento_display()} ({self.puntaje}/{self.total_preguntas})"


class Educacion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.titulo