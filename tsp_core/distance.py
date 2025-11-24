"""Funciones para calcular distancias entre ciudades."""
import numpy as np
from data import coordenadas, nombres_ciudades, n


def distancia_euclidiana(c1_idx, c2_idx):
    """Distancia euclidiana entre ciudad índice c1_idx y c2_idx.
    (Se usa diferencia en latitud y longitud en grados.)"""
    lat1, lon1 = coordenadas[nombres_ciudades[c1_idx]]
    lat2, lon2 = coordenadas[nombres_ciudades[c2_idx]]
    return np.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)


def construir_matriz_distancias():
    """Construye la matriz simétrica n x n de distancias."""
    matriz = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia_euclidiana(i, j)
            matriz[i, j] = d
            matriz[j, i] = d
    return matriz


def mostrar_matriz_bonita(matriz):
    """Imprime la matriz en formato tabular legible."""
    print("\n" + "█" * 80)
    print(f"{' MATRIZ DE DISTANCIAS (GRADOS) ':^80}")
    print("█" * 80)
    # Encabezado (recorta nombre para mantener columnas razonables)
    print(f"{'':<12}", end="")
    for nombre in nombres_ciudades:
        print(f"{nombre[:9]:>10}", end="")
    print("\n" + "-" * 85)
    # Filas
    for i, fila in enumerate(matriz):
        print(f"{nombres_ciudades[i]:<12}", end="")
        for val in fila:
            if val == 0:
                print(f"{'-':>10}", end="")
            else:
                print(f"{val:>10.2f}", end="")
        print()
    print("-" * 85)