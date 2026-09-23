"""Tests de las funcionalidades inteligentes del módulo de registro."""
from django.test import TestCase

from .models import PuntoAcopio
from .services import clasificar_aparato, distancia_km, recomendar_punto


class ClasificacionTest(TestCase):
    def test_sugiere_categoria_por_nombre(self):
        self.assertEqual(clasificar_aparato('Refrigeradora'), 'Intercambio de temperatura')
        self.assertEqual(clasificar_aparato('celular'), 'Equipos de TIC y telecomunicaciones')
        self.assertEqual(clasificar_aparato('televisor'), 'Pantallas')

    def test_no_inventa_categoria_desconocida(self):
        # "plancha" sí es un pequeño electrodoméstico; una mesa no debe clasificarse
        self.assertEqual(clasificar_aparato('plancha'), 'Pequeños equipos')
        self.assertIsNone(clasificar_aparato('mesa de madera'))


class RecomendacionTest(TestCase):
    def setUp(self):
        # Villa El Salvador ≈ (-12.178, -76.942)
        self.cerca = PuntoAcopio.objects.create(
            nombre='Plaza principal', direccion='Av. Los Héroes 123',
            latitud=-12.1790, longitud=-76.9430, horario='Lun-Sáb 9-18',
            capacidad_max=1000, capacidad_actual=100, estado='disponible',
        )
        self.lejos = PuntoAcopio.objects.create(
            nombre='Parque lejos', direccion='Av. Azti 999',
            latitud=-12.2200, longitud=-76.9800, horario='Lun-Vie 8-17',
            capacidad_max=1000, capacidad_actual=0, estado='disponible',
        )
        self.lleno = PuntoAcopio.objects.create(
            nombre='Punto lleno', direccion='Calle Test 1',
            latitud=-12.1785, longitud=-76.9425, horario='Lun-Vie 8-17',
            capacidad_max=500, capacidad_actual=500, estado='lleno',
        )

    def test_recomienda_el_mas_cercano_con_capacidad(self):
        punto = recomendar_punto(-12.178, -76.942)
        self.assertEqual(punto, self.cerca)

    def test_excluye_puntos_llenos(self):
        self.lleno.estado = 'disponible'
        self.lleno.save()
        # Aunque esté "disponible", sin capacidad no debe recomendarse
        self.lleno.capacidad_actual = self.lleno.capacidad_max
        self.lleno.save()
        punto = recomendar_punto(-12.1785, -76.9425)
        self.assertEqual(punto, self.cerca)

    def test_distancia_km_coherente(self):
        d = distancia_km(-12.178, -76.942, -12.220, -76.980)
        self.assertTrue(4 < d < 10)
