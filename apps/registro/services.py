"""Servicios inteligentes: clasificación automática y recomendación de puntos."""
import difflib
import math

# Clasificación base UNITAR (6 categorías) con aparatos representativos.
CATEGORIAS_UNITAR = {
    'Intercambio de temperatura': [
        'refrigeradora', 'refrigerador', 'heladera', 'freezer', 'aire acondicionado',
        'climatizador', 'chimbeador', 'deshumidificador',
    ],
    'Pantallas': [
        'televisor', 'tv', 'monitor', 'pantalla', 'tablet', 'computadora portátil con pantalla',
    ],
    'Lámparas': ['lampara', 'lámpara', 'foco', 'bombillo', 'tubo fluorescente', 'led'],
    'Grandes equipos': [
        'lavadora', 'secadora', 'lavavajillas', 'cocina', 'horno', 'estufa',
        'calentador', 'termas', 'radiator',
    ],
    'Pequeños equipos': [
        'licuadora', 'batidora', 'tostadora', 'cafetera', 'aspiradora', 'plancha',
        'secadora de pelo', 'microondas', 'ventilador', 'radio', 'reloj', 'juguete electrico',
    ],
    'Equipos de TIC y telecomunicaciones': [
        'celular', 'smartphone', 'telefono', 'teléfono', 'computadora', 'pc', 'laptop',
        'impresora', 'scanner', 'router', 'modem', 'cpu', 'teclado', 'mouse', 'cargador',
        'bateria', 'batería', 'power bank',
    ],
}


def clasificar_aparato(nombre):
    """Sugiere la categoría UNITAR correcta a partir del nombre del aparato.

    Usa coincidencia difusa (fuzzy matching) sobre un diccionario de aparatos.
    Retorna None si no hay una coincidencia suficientemente confiable.
    """
    if not nombre:
        return None
    normalizado = nombre.strip().lower()
    # El aparato suele mencionarse primero: analizamos las primeras palabras.
    cabecera = ' '.join(normalizado.split()[:2])

    def _singular(palabra):
        """Forma simplificada para comparar raíces de palabras."""
        if palabra.endswith('es') and len(palabra) > 4:
            return palabra[:-2]
        if palabra.endswith('s') and len(palabra) > 3:
            return palabra[:-1]
        return palabra

    def _puntaje_aparato(aparato):
        """Puntaje de coincidencia entre el texto y un aparato del diccionario."""
        if aparato in (normalizado, cabecera):
            return 1.0
        base = difflib.SequenceMatcher(None, cabecera, aparato).ratio()
        for pal in normalizado.split():
            r = difflib.SequenceMatcher(None, pal, aparato).ratio()
            r = max(r, difflib.SequenceMatcher(None, _singular(pal), _singular(aparato)).ratio())
            # Prefijo común fuerte: "refrigirador" ~ "refrigerador"
            prefijo = min(len(pal), len(aparato)) / max(len(pal), len(aparato))
            if (pal.startswith(aparato) or aparato.startswith(pal)) and prefijo >= 0.75:
                r = max(r, 0.85 + 0.15 * prefijo)
            if r > base:
                base = r
        return base

    mejor_puntaje, mejor_categoria = 0.0, None
    for categoria, aparatos in CATEGORIAS_UNITAR.items():
        for aparato in aparatos:
            puntaje = _puntaje_aparato(aparato)
            if puntaje > mejor_puntaje:
                mejor_puntaje, mejor_categoria = puntaje, categoria
    return mejor_categoria if mejor_puntaje >= 0.75 else None


def distancia_km(lat1, lng1, lat2, lng2):
    """Distancia aproximada en kilómetros entre dos coordenadas (Haversine)."""
    radio = 6371.0
    f1, f2 = math.radians(float(lat1)), math.radians(float(lat2))
    df = f2 - f1
    dl = math.radians(float(lng2) - float(lng1))
    a = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
    return radio * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def recomendar_punto(latitud, longitud, puntos=None):
    """Recomienda el punto de acopio más cercano con capacidad disponible.

    Prioriza: estado operativo (no lleno/cerrado/inactivo) y distancia mínima.
    """
    from .models import PuntoAcopio

    if puntos is None:
        puntos = PuntoAcopio.objects.filter(
            activo=True,
        ).exclude(estado__in=['lleno', 'cerrado', 'inactivo'])
    evaluados = []
    for punto in puntos:
        d = distancia_km(latitud, longitud, punto.latitud, punto.longitud)
        disponible = float(punto.capacidad_max - punto.capacidad_actual)
        if disponible <= 0:
            continue
        evaluados.append((d, punto))
    evaluados.sort(key=lambda x: x[0])
    return evaluados[0][1] if evaluados else None
