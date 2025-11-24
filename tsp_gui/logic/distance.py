import numpy as np
from .data import coordenadas, nombres_ciudades, n

def distancia_euclidiana(c1_idx, c2_idx):
    lat1, lon1 = coordenadas[nombres_ciudades[c1_idx]]
    lat2, lon2 = coordenadas[nombres_ciudades[c2_idx]]
    return np.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)

def construir_matriz_distancias():
    matriz = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia_euclidiana(i, j)
            matriz[i, j] = d
            matriz[j, i] = d
    return matriz
