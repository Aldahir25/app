from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ReportesDashboardTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.funcionario = self.User.objects.create_user(
            username='funcionario_reportes',
            email='funcionario_reportes@example.com',
            password='Test1234!',
            rol='funcionario',
        )

    def test_funcionario_can_access_reports_dashboard(self):
        self.client.login(username='funcionario_reportes', password='Test1234!')
        response = self.client.get(reverse('reportes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard de gestión')
