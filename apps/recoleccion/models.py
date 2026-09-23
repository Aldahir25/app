from django.conf import settings
from django.db import models
from django.utils import timezone


class Recoleccion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('programada', 'Programada'),
        ('en_proceso', 'En proceso'),
        ('recolectada', 'Recolectada'),
        ('trasladada', 'Trasladada'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    punto = models.ForeignKey(
        'registro.PuntoAcopio',
        on_delete=models.PROTECT,
        related_name='recolecciones',
    )
    operador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'operador'},
        related_name='recolecciones',
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_programada = models.DateTimeField(null=True, blank=True)
    fecha_recoleccion = models.DateTimeField(null=True, blank=True)
    fecha_atencion = models.DateTimeField(null=True, blank=True)
    peso_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    cantidad_residuos = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    destino = models.CharField(max_length=255, blank=True)
    observaciones = models.TextField(blank=True)

    @property
    def tiempo_respuesta_dias(self):
        if self.fecha_atencion:
            return (self.fecha_atencion - self.fecha_solicitud).days
        return None

    def asignar_operador(self, operador):
        self.operador = operador
        self.estado = 'programada'
        self.fecha_programada = timezone.now()
        self.save()

    def __str__(self):
        return f"Recolección {self.get_estado_display()} - {self.punto}"