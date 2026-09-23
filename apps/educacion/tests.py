from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ContenidoEducativo


class EducacionFlowTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='ciudadano_edu',
            email='ciudadano_edu@example.com',
            password='Test1234!',
            rol='ciudadano',
        )
        self.contenido = ContenidoEducativo.objects.create(
            titulo='Cómo separar residuos electrónicos',
            descripcion='Separar baterías, cables y placas.',
            orden=1,
            publicado=True,
        )

    def test_educacion_list_is_available_for_authenticated_user(self):
        self.client.login(username='ciudadano_edu', password='Test1234!')
        response = self.client.get(reverse('educacion'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cómo separar residuos electrónicos')

    def test_evaluacion_can_save_score(self):
        self.client.login(username='ciudadano_edu', password='Test1234!')
        response = self.client.post(
            reverse('evaluacion'),
            {
                'momento': 'pre',
                'respuesta_1': '1',
                'respuesta_2': '2',
                'respuesta_3': '1',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'puntaje')
