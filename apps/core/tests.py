from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class CoreViewsTest(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_authenticated_user_can_access_dashboard(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='operador1',
            email='operador@example.com',
            password='Test1234!',
            rol='operador'
        )
        self.client.login(username='operador1', password='Test1234!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
