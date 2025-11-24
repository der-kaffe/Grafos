import time
import pandas as pd
from logic.data import coordenadas, nombres_ciudades
from logic.distance import construir_matriz_distancias
from logic.exhaustive import busqueda_exhaustiva
from logic.nearest_neighbor import vecino_mas_cercano
from logic.graphics import grafico_solo_puntos_fig, comparativa_fig

def get_coordenadas_dataframe():
    """Retorna un DataFrame con las coordenadas de las ciudades."""
    return pd.DataFrame([
        {"Ciudad": ciudad, "Latitud": lat, "Longitud": lon}
        for ciudad, (lat, lon) in coordenadas.items()
    ])

def get_matriz_distancias():
    """Construye y retorna la matriz de distancias como DataFrame con nombres de ciudades."""
    matriz = construir_matriz_distancias()

    # Convertir a DataFrame con nombres de ciudades en filas y columnas
    df_matriz = pd.DataFrame(
        matriz,
        index=nombres_ciudades,      # Filas: ciudades origen
        columns=nombres_ciudades     # Columnas: ciudades destino
    )

    return df_matriz

def get_matriz_distancias_numpy():
    """Construye y retorna la matriz de distancias como NumPy array (para algoritmos)."""
    return construir_matriz_distancias()

def get_mapa_puntos():
    """Retorna la figura del mapa de ciudades (solo puntos)."""
    return grafico_solo_puntos_fig()

def ejecutar_busqueda_exhaustiva(matriz, logger):
    """
    Ejecuta la búsqueda exhaustiva y retorna (ruta, distancia, tiempo, historial).
    Usa time.perf_counter() para mayor precisión.
    """
    logger("Iniciando búsqueda exhaustiva...")
    t0 = time.perf_counter()
    ruta, dist, historial = busqueda_exhaustiva(matriz, logger=logger)
    t1 = time.perf_counter()
    tiempo = t1 - t0
    logger(f"Exhaustivo terminado en {tiempo:.6f} s. Distancia: {dist:.4f}")
    return ruta, dist, tiempo, historial

def ejecutar_vecino_mas_cercano(matriz, inicio, logger):
    """
    Ejecuta el algoritmo de vecino más cercano y retorna (ruta, distancia, tiempo, historial).
    Usa time.perf_counter() para mayor precisión.
    """
    logger("Iniciando Vecino Más Cercano...")
    t0 = time.perf_counter()
    ruta, dist, historial = vecino_mas_cercano(matriz, inicio=inicio, logger=logger)
    t1 = time.perf_counter()
    tiempo = t1 - t0
    logger(f"Vecino Más Cercano terminado en {tiempo:.6f} s. Distancia: {dist:.4f}")
    return ruta, dist, tiempo, historial

def convertir_ruta_a_nombres(ruta):
    """Convierte una ruta de índices a nombres de ciudades."""
    return [nombres_ciudades[i] for i in ruta]

def crear_dataframe_comparativo(tiempo_ex, dist_ex, tiempo_nn, dist_nn):
    """
    Crea un DataFrame comparativo de ambos métodos.
    Asegura conversión explícita a float para evitar problemas de tipo.
    """
    return pd.DataFrame([
        {
            "Método": "Exhaustivo (Óptimo)", 
            "Tiempo (s)": float(tiempo_ex), 
            "Distancia": float(dist_ex)
        },
        {
            "Método": "Vecino Más Cercano", 
            "Tiempo (s)": float(tiempo_nn), 
            "Distancia": float(dist_nn)
        }
    ])

def calcular_gap(dist_ex, dist_nn):
    """Calcula el gap de optimalidad entre ambos métodos."""
    if dist_ex and dist_ex > 0:
        return (dist_nn - dist_ex) / dist_ex * 100
    return None

def get_grafico_comparativo(ruta_ex, dist_ex, ruta_nn, dist_nn):
    """Retorna la figura comparativa con ambas rutas superpuestas."""
    return comparativa_fig(ruta_ex, dist_ex, ruta_nn, dist_nn)