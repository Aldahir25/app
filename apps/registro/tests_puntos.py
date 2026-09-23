from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CategoriaRAEE, PuntoAcopio, RegistroRAEE


class PuntosAcopioTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.operador = self.User.objects.create_user(
            username='operador2',
            email='operador2@example.com',
            password='Test1234!',
            rol='operador',
        )
        self.user = self.User.objects.create_user(
            username='ciudadano2',
            email='ciudadano2@example.com',
            password='Test1234!',
            rol='ciudadano',
        )
        self.categoria = CategoriaRAEE.objects.create(
            nombre='Televisores',
            descripcion='Pantallas',
            peligroso=False,
        )
        self.punto = PuntoAcopio.objects.create(
            nombre='San José',
            descripcion='Punto principal de acopio',
            direccion='Jr. San José 101',
            latitud='-12.200000',
            longitud='-76.900000',
            horario='Lun-Sab 8am-6pm',
            capacidad_max='1000.00',
            capacidad_actual='150.00',
            estado='disponible',
            operador=self.operador,
        )

    def test_listado_puntos_acopio(self):
        response = self.client.get(reverse('puntos_acopio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'San José')

    def test_recomendacion_de_punto_para_raee(self):
        self.client.login(username='ciudadano2', password='Test1234!')
        RegistroRAEE.objects.create(
            usuario=self.user,
            categoria=self.categoria,
            tipo_aparato='Televisor',
            marca='LG',
            modelo='43LM',
            descripcion='Pantalla dañada',
            peso_estimado='7.50',
            cantidad=1,
            punto_acopio=self.punto,
            estado='REGISTRADO',
            codigo='RAEE-2026-000011',
        )
        response = self.client.get(reverse('puntos_acopio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'San José')
