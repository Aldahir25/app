from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('ciudadano', 'Ciudadano'),
        ('operador', 'Operador'),
        ('funcionario', 'Funcionario'),
        ('administrador', 'Administrador'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='ciudadano')
    dni = models.CharField(max_length=8, blank=True, verbose_name='DNI')
    direccion = models.CharField(max_length=255, blank=True)
    distrito = models.CharField(max_length=100, default='Villa El Salvador')
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"