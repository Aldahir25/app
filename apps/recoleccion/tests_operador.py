from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.registro.models import CategoriaRAEE, PuntoAcopio, RegistroRAEE
from .models import Recoleccion


class OperadorRecoleccionTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.operador = self.User.objects.create_user(
            username='operador4',
            email='operador4@example.com',
            password='Test1234!',
            rol='operador',
        )
        self.user = self.User.objects.create_user(
            username='ciudadano4',
            email='ciudadano4@example.com',
            password='Test1234!',
            rol='ciudadano',
        )
        self.categoria = CategoriaRAEE.objects.create(nombre='Impresoras', descripcion='Impresoras', peligroso=False)
        self.punto = PuntoAcopio.objects.create(
            nombre='Punto Este',
            descripcion='Punto de prueba',
            direccion='Av. Este 22',
            latitud='-12.220000',
            longitud='-76.920000',
            horario='Lun-Sab 9am-5pm',
            capacidad_max='500.00',
            capacidad_actual='100.00',
            estado='disponible',
            operador=self.operador,
        )
        self.raee = RegistroRAEE.objects.create(
            usuario=self.user,
            categoria=self.categoria,
            tipo_aparato='Impresora',
            descripcion='Impresora dañada',
            peso_estimado='4.50',
            cantidad=1,
            punto_acopio=self.punto,
            codigo='RAEE-2026-001001',
        )

    def test_operador_can_list_recolecciones(self):
        Recoleccion.objects.create(
            punto=self.punto,
            operador=self.operador,
            estado='pendiente',
            destino='Planta de tratamiento',
            peso_total='4.50',
        )
        self.client.login(username='operador4', password='Test1234!')
        response = self.client.get(reverse('recolecciones'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Punto Este')
