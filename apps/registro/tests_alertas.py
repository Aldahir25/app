from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Alerta, CategoriaRAEE, HistorialRAEE, PuntoAcopio, RegistroRAEE


class AlertaRaeETest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='ciudadano3',
            email='ciudadano3@example.com',
            password='Test1234!',
            rol='ciudadano',
        )
        self.operador = self.User.objects.create_user(
            username='operador3',
            email='operador3@example.com',
            password='Test1234!',
            rol='operador',
        )
        self.categoria = CategoriaRAEE.objects.create(
            nombre='Laptops',
            descripcion='Equipos portátiles',
            peligroso=False,
        )
        self.punto = PuntoAcopio.objects.create(
            nombre='Punto Norte',
            descripcion='Punto de acopio',
            direccion='Calle Norte 11',
            latitud='-12.210000',
            longitud='-76.930000',
            horario='Lun-Sab 9am-5pm',
            capacidad_max='800.00',
            capacidad_actual='200.00',
            estado='disponible',
            operador=self.operador,
        )
        self.raee = RegistroRAEE.objects.create(
            usuario=self.user,
            categoria=self.categoria,
            tipo_aparato='Laptop',
            marca='Lenovo',
            modelo='ThinkPad',
            descripcion='Laptop inservible',
            peso_estimado='2.60',
            cantidad=1,
            punto_acopio=self.punto,
            codigo='RAEE-2026-000101',
        )

    def test_actualizar_estado_crea_historial_y_alerta(self):
        self.raee.actualizar_estado('RECIBIDO_EN_PUNTO', self.operador, 'Recepción confirmada.')
        self.assertEqual(self.raee.estado, 'RECIBIDO_EN_PUNTO')
        self.assertTrue(HistorialRAEE.objects.filter(raee=self.raee).exists())
        self.assertTrue(Alerta.objects.filter(raee=self.raee).exists())
