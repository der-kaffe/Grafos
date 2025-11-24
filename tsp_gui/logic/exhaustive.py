import itertools
import math
from .data import n, nombres_ciudades

def busqueda_exhaustiva(matriz_dist, logger=None):
    """
    Búsqueda exhaustiva con posibilidad de enviar logs mediante `logger(msg)`.
    Retorna: mejor_ruta, mejor_dist, historial
    (historial contiene tuples (ruta, dist) cada vez que se encuentra nuevo record)
    """
    if logger:
        logger("\n" + "=" * 80)
        logger(f"{' INICIANDO BÚSQUEDA EXHAUSTIVA (FUERZA BRUTA) ':^80}")
        logger("=" * 80)

    indices = list(range(n))
    inicio = 0
    otros = indices[1:]
    mejor_dist = float('inf')
    mejor_ruta = None
    historial = []
    contador = 0

    total_perms = math.factorial(n - 1)
    if logger:
        logger(f" -> Se evaluarán {total_perms} rutas posibles...")

    for perm in itertools.permutations(otros):
        contador += 1
        ruta_actual = [inicio] + list(perm) + [inicio]

        # calcular distancia total de la ruta_actual
        dist_actual = 0.0
        for i in range(len(ruta_actual) - 1):
            a = ruta_actual[i]; b = ruta_actual[i + 1]
            dist_actual += matriz_dist[a, b]

        if dist_actual < mejor_dist:
            mejor_dist = dist_actual
            mejor_ruta = list(ruta_actual)
            historial.append((list(mejor_ruta), mejor_dist))

            if logger:
                ruta_nombres = " -> ".join([nombres_ciudades[idx][:9] for idx in mejor_ruta])
                logger(f" [Intento {contador}/{total_perms}] ¡NUEVO RÉCORD! Distancia: {mejor_dist:.4f}")
                logger(f"    Ruta: {ruta_nombres}")

    if logger:
        logger("-" * 80)
        logger(f" FIN EXHAUSTIVA. Mejor distancia encontrada: {mejor_dist:.4f}")

    return mejor_ruta, mejor_dist, historial