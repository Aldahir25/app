from django.conf import settings
from django.db import models
from django.utils import timezone


class CategoriaRAEE(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    peligroso = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class PuntoAcopio(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('capacidad_media', 'Capacidad media'),
        ('casi_lleno', 'Casi lleno'),
        ('lleno', 'Lleno'),
        ('cerrado', 'Temporalmente cerrado'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=255)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    horario = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    capacidad_max = models.DecimalField(max_digits=10, decimal_places=2, help_text='kg')
    capacidad_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    operador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'operador'},
        related_name='puntos_acopio',
        blank=True,
        null=True,
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class RegistroRAEE(models.Model):
    ESTADO_CHOICES = [
        ('REGISTRADO', 'Registrado'),
        ('ASIGNADO_A_PUNTO', 'Asignado a punto'),
        ('RECIBIDO_EN_PUNTO', 'Recibido en punto'),
        ('PENDIENTE_RECOLECCION', 'Pendiente de recolección'),
        ('EN_RECOLECCION', 'En recolección'),
        ('RECOLECTADO', 'Recolectado'),
        ('TRASLADADO', 'Trasladado'),
        ('TRATADO', 'Tratado / finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    codigo = models.CharField(max_length=30, unique=True, blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='raees_registrados',
        limit_choices_to={'rol': 'ciudadano'},
    )
    categoria = models.ForeignKey(CategoriaRAEE, on_delete=models.PROTECT, related_name='raees')
    tipo_aparato = models.CharField(max_length=150)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    peso_estimado = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cantidad = models.PositiveIntegerField(default=1)
    imagen = models.ImageField(upload_to='raee/', blank=True, null=True)
    punto_acopio = models.ForeignKey(PuntoAcopio, on_delete=models.PROTECT, related_name='raees', blank=True, null=True)
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES, default='REGISTRADO')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    zona = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-fecha_registro']

    def save(self, *args, **kwargs):
        if not self.codigo:
            year = timezone.now().year
            ultimo = RegistroRAEE.objects.filter(codigo__startswith=f'RAEE-{year}-').order_by('-codigo').first()
            if ultimo and ultimo.codigo:
                numero = int(ultimo.codigo.split('-')[-1]) + 1
            else:
                numero = 1
            self.codigo = f'RAEE-{year}-{numero:06d}'
        super().save(*args, **kwargs)

    def actualizar_estado(self, nuevo_estado, usuario, observacion=''):
        if nuevo_estado not in dict(self.ESTADO_CHOICES):
            raise ValueError('Estado no válido.')

        anterior = self.estado
        self.estado = nuevo_estado
        self.save(update_fields=['estado'])

        HistorialRAEE.objects.create(
            raee=self,
            estado_anterior=anterior,
            estado_nuevo=nuevo_estado,
            usuario_responsable=usuario,
            observacion=observacion,
        )

        if self.punto_acopio:
            Alerta.objects.create(
                tipo='informacion',
                titulo='Cambio de estado del residuo',
                mensaje=f'El residuo {self.codigo} cambió de {anterior} a {nuevo_estado}.',
                punto_acopio=self.punto_acopio,
                raee=self,
            )

    def __str__(self):
        return f"{self.codigo} - {self.tipo_aparato}"


class HistorialRAEE(models.Model):
    raee = models.ForeignKey(RegistroRAEE, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=25, blank=True)
    estado_nuevo = models.CharField(max_length=25)
    usuario_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='historial_raee',
    )
    observacion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.raee.codigo} - {self.estado_anterior} -> {self.estado_nuevo}"


class Alerta(models.Model):
    TIPO_CHOICES = [
        ('informacion', 'Información'),
        ('advertencia', 'Advertencia'),
        ('critica', 'Crítica'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='informacion')
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    punto_acopio = models.ForeignKey(PuntoAcopio, on_delete=models.SET_NULL, related_name='alertas', null=True, blank=True)
    raee = models.ForeignKey(RegistroRAEE, on_delete=models.SET_NULL, related_name='alertas', null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.fecha.strftime('%d/%m/%Y')}"