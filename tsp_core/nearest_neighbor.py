"""Algoritmo heurístico del vecino más cercano para TSP."""
from data import nombres_ciudades, n


def vecino_mas_cercano(matriz_dist, inicio=0):
    print("\n" + "=" * 80)
    print(f"{' INICIANDO VECINO MÁS CERCANO (GREEDY) ':^80}")
    print("=" * 80)

    ruta = [inicio]
    visitadas = {inicio}
    actual = inicio
    dist_total = 0.0
    historial = [list(ruta)]

    print(f"Comenzamos en: {nombres_ciudades[inicio].upper()}")

    while len(visitadas) < n:
        print(f"\nEstoy en {nombres_ciudades[actual]}... buscando destino más cercano:")
        mejor_dist_local = float('inf')
        siguiente = None

        # buscar el vecino no visitado más cercano
        for vecino in range(n):
            if vecino in visitadas:
                continue

            d = matriz_dist[actual, vecino]
            print(f"   - ¿Ir a {nombres_ciudades[vecino]}? Distancia: {d:.2f}", end="")

            if d < mejor_dist_local:
                print(" (¡Candidato actual!)")
                mejor_dist_local = d
                siguiente = vecino
            else:
                print("")

        # mover al siguiente
        print(f" >>> DECISIÓN: Viajo a {nombres_ciudades[siguiente]} (Dist: {mejor_dist_local:.2f})")
        dist_total += mejor_dist_local
        actual = siguiente
        ruta.append(actual)
        visitadas.add(actual)
        historial.append(list(ruta))

    # volver al inicio
    dist_retorno = matriz_dist[actual, inicio]
    print(f"\nTodas visitadas. Regresando al inicio ({nombres_ciudades[inicio]})...")
    print(f" >>> Retorno: {dist_retorno:.2f}")

    dist_total += dist_retorno
    ruta.append(inicio)
    historial.append(list(ruta))

    return ruta, dist_total, historial