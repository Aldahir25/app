from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CategoriaRAEE, PuntoAcopio, RegistroRAEE


class RegistroRaeETest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='ciudadano1',
            email='ciudadano@example.com',
            password='Test1234!',
            first_name='Ana',
            last_name='Pérez',
            rol='ciudadano',
        )
        self.operador = self.User.objects.create_user(
            username='operador1',
            email='operador@example.com',
            password='Test1234!',
            rol='operador',
        )
        self.categoria = CategoriaRAEE.objects.create(
            nombre='Celulares',
            descripcion='Dispositivos móviles',
            peligroso=False,
        )
        self.punto = PuntoAcopio.objects.create(
            nombre='Punto Central',
            direccion='Av. Principal 123',
            latitud='-12.123456',
            longitud='-76.987654',
            capacidad_max='500.00',
            horario='Lun-Sab 8:00-18:00',
            operador=self.operador,
            estado='disponible',
        )

    def test_registrar_raee_requires_login(self):
        response = self.client.get(reverse('raee_registrar'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_citizen_can_register_raee(self):
        self.client.login(username='ciudadano1', password='Test1234!')
        payload = {
            'categoria': self.categoria.id,
            'tipo_aparato': 'Celular',
            'marca': 'Samsung',
            'modelo': 'A14',
            'descripcion': 'Celular roto con pantalla agrietada',
            'peso_estimado': '0.35',
            'cantidad': 1,
            'punto_acopio': self.punto.id,
            'estado': 'REGISTRADO',
        }

        response = self.client.post(reverse('raee_registrar'), payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RegistroRAEE.objects.count(), 1)
        registro = RegistroRAEE.objects.get()
        self.assertTrue(registro.codigo.startswith('RAEE-'))
        self.assertEqual(registro.usuario, self.user)

    def test_user_can_list_own_raee(self):
        self.client.login(username='ciudadano1', password='Test1234!')
        RegistroRAEE.objects.create(
            usuario=self.user,
            categoria=self.categoria,
            tipo_aparato='Laptop',
            marca='Dell',
            modelo='Latitude 3300',
            descripcion='Laptop en desuso',
            peso_estimado='2.10',
            cantidad=1,
            punto_acopio=self.punto,
            estado='REGISTRADO',
            codigo='RAEE-2026-000001',
        )

        response = self.client.get(reverse('raee_mis_registros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RAEE-2026-000001')
