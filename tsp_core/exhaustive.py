"""Algoritmo de búsqueda exhaustiva para TSP."""
import itertools
import math
from data import nombres_ciudades, n


def busqueda_exhaustiva(matriz_dist):
    """Búsqueda exhaustiva con prints cada vez que se encuentra un nuevo récord."""
    print("\n" + "=" * 80)
    print(f"{' INICIANDO BÚSQUEDA EXHAUSTIVA (FUERZA BRUTA) ':^80}")
    print("=" * 80)

    indices = list(range(n))
    inicio = 0
    otros = indices[1:]
    mejor_dist = float('inf')
    mejor_ruta = None
    historial = []
    contador = 0

    total_perms = math.factorial(n - 1)
    print(f" -> Se evaluarán {total_perms} rutas posibles...")

    for perm in itertools.permutations(otros):
        contador += 1
        ruta_actual = [inicio] + list(perm) + [inicio]

        # calc distancia total de la ruta_actual
        dist_actual = 0.0
        for i in range(len(ruta_actual) - 1):
            a = ruta_actual[i]
            b = ruta_actual[i + 1]
            dist_actual += matriz_dist[a, b]

        if dist_actual < mejor_dist:
            mejor_dist = dist_actual
            mejor_ruta = list(ruta_actual)
            historial.append((list(mejor_ruta), mejor_dist))

            ruta_nombres = " -> ".join([nombres_ciudades[idx][:9] for idx in mejor_ruta])
            print(f" [Intento {contador}/{total_perms}] ¡NUEVO RÉCORD! Distancia: {mejor_dist:.4f}")
            print(f"    Ruta: {ruta_nombres}")

    print("-" * 80)
    print(f" FIN EXHAUSTIVA. Mejor distancia encontrada: {mejor_dist:.4f}")
    return mejor_ruta, mejor_dist, historial