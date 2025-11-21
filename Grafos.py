import numpy as np
import itertools
import matplotlib.pyplot as plt
import time

# ----------------------------
#  Datos (cámbialos si quieres)
# ----------------------------
coordenadas = {
    "Nueva York": (40.670, -73.940),
    "Los Ángeles": (34.110, -118.410),
    "Chicago": (41.840, -87.680),
    "Houston": (29.7407, -95.4636),
    "Phoenix": (33.540, -112.070),
    "Filadelfia": (40.010, -75.130),
    "San Antonio": (29.460, -98.510)
}

# Lista de nombres y cantidad
nombres_ciudades = list(coordenadas.keys())
n = len(nombres_ciudades)

# ---------------------------------------------------
#  Funciones matemáticas y construcción de la matriz
# ---------------------------------------------------
def distancia_euclidiana(c1_idx, c2_idx):
    """Distancia euclidiana entre ciudad índice c1_idx y c2_idx."""
    lat1, lon1 = coordenadas[nombres_ciudades[c1_idx]]
    lat2, lon2 = coordenadas[nombres_ciudades[c2_idx]]
    return np.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)

def construir_matriz_distancias():
    """Construye la matriz simétrica n x n de distancias."""
    matriz = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia_euclidiana(i, j)
            matriz[i, j] = d
            matriz[j, i] = d
    return matriz

def mostrar_matriz(matriz, nombres):
    """Muestra la matriz de distancias en consola con formato."""
    ancho_col = 16
    ancho_nombre_fila = 16
    ancho_total = ancho_nombre_fila + (ancho_col * len(nombres))
    print("\n" + "="*ancho_total)
    print(f"{'MATRIZ DE DISTANCIAS (Grados Euclidianos)':^{ancho_total}}")
    print("="*ancho_total)

    header = f"{'':<{ancho_nombre_fila}}" + "".join([f"{nombre:>{ancho_col}}" for nombre in nombres])
    print(header)
    print("-" * len(header))
    for i, fila in enumerate(matriz):
        linea = f"{nombres[i]:<{ancho_nombre_fila}}"
        for val in fila:
            if val == 0:
                linea += f"{'-':>{ancho_col}}"
            else:
                linea += f"{val:{ancho_col}.4f}"
        print(linea)
    print("-" * len(header))

# ---------------------------------------------------
#  Búsqueda exhaustiva (exacta)
# ---------------------------------------------------
def busqueda_exhaustiva(matriz_dist):
    """
    Prueba todas las permutaciones (fija inicio en 0) y devuelve:
    mejor_ruta (lista de índices empezando y terminando en 0),
    mejor_dist, historial_de_record [(ruta, dist), ...]
    """
    indices = list(range(n))
    inicio = 0
    otros = indices[1:]
    mejor_dist = float('inf')
    mejor_ruta = None
    historial = []  # guardamos solo cuando aparece un nuevo record
    contador = 0

    for perm in itertools.permutations(otros):
        contador += 1
        ruta_actual = [inicio] + list(perm) + [inicio]
        # calc distancia total de la ruta_actual
        dist_actual = 0.0
        for i in range(len(ruta_actual) - 1):
            a = ruta_actual[i]; b = ruta_actual[i+1]
            dist_actual += matriz_dist[a, b]

        if dist_actual < mejor_dist:
            mejor_dist = dist_actual
            mejor_ruta = route_copy = list(ruta_actual)
            historial.append((route_copy, mejor_dist))  # guardamos el nuevo record
            print(f"[Intento #{contador}] ¡RECORD ENCONTRADO!")
            print(f"   Ruta: {' -> '.join([nombres_ciudades[idx] for idx in mejor_ruta])}")
            print(f"   Distancia: {mejor_dist:.4f}")
            print("-" * 20)

    print(f"Total de rutas evaluadas: {contador}")
    return mejor_ruta, mejor_dist, historial

# ---------------------------------------------------
#  Heurística: Vecino Más Cercano (NN)
# ---------------------------------------------------
def vecino_mas_cercano(matriz_dist, inicio=0):
    """
    Realiza la construcción greedy desde 'inicio'.
    Devuelve ruta (lista índices, cerrada), distancia total, y historial de rutas parciales.
    """
    ruta = [inicio]
    visitadas = {inicio}
    actual = inicio
    dist_total = 0.0
    historial = [list(ruta)]  # iremos agregando pasos para la animación

    while len(visitadas) < n:
        mejor_dist_local = float('inf')
        siguiente = None
        # buscar el vecino no visitado más cercano
        for vecino in range(n):
            if vecino in visitadas:
                continue
            d = matriz_dist[actual, vecino]
            if d < mejor_dist_local:
                mejor_dist_local = d
                siguiente = vecino
        # mover al siguiente
        dist_total += mejor_dist_local
        actual = siguiente
        ruta.append(actual)
        visitadas.add(actual)
        historial.append(list(ruta))

    # volver al inicio
    dist_total += matriz_dist[actual, inicio]
    ruta.append(inicio)
    historial.append(list(ruta))
    return ruta, dist_total, historial

# ---------------------------------------------------
#  Visualización: grafo completo + resaltado de ruta
# ---------------------------------------------------
def dibujar_grafo_completo(ax, ciudades, color_arista='#cccccc'):
    """
    Dibuja en el eje ax todas las aristas del grafo completo con color ligero.
    ciudades: lista de (lat, lon) en el orden de nombres_ciudades
    """
    lats = [c[0] for c in ciudades]
    lons = [c[1] for c in ciudades]

    # dibujar todas las aristas (i,j) con i<j
    for i in range(len(ciudades)):
        for j in range(i+1, len(ciudades)):
            ax.plot([lons[i], lons[j]], [lats[i], lats[j]], color=color_arista, linewidth=0.8, zorder=1)

    # dibujar nodos y etiquetas
    ax.scatter(lons, lats, c='blue', s=80, zorder=3)
    for idx, name in enumerate(nombres_ciudades):
        ax.annotate(name, (lons[idx], lats[idx]), xytext=(5,5), textcoords='offset points', fontsize=9, zorder=4)

def resaltar_ruta(ax, ruta_idxs, color='red', ancho=3, etiqueta=None):
    """
    Dibuja la ruta (lista de índices, por ejemplo [0,2,3,0]) sobre ax
    """
    lats_r = [coordenadas[nombres_ciudades[i]][0] for i in ruta_idxs]
    lons_r = [coordenadas[nombres_ciudades[i]][1] for i in ruta_idxs]
    ax.plot(lons_r, lats_r, color=color, linewidth=ancho, zorder=5, label=etiqueta)

# ---------------------------------------------------
#  Animación simple (paso a paso)
# ---------------------------------------------------
def animar_historial(historial, titulo, velocidad=0.8, es_exhaustivo=False):
    """
    historial: para NN -> lista de rutas parciales [ [0], [0,3], [0,3,1], ... ]
              para exhaustivo -> historial de records -> [(ruta,dist), ...]
    es_exhaustivo: si True, cada elemento de historial es (ruta, dist)
    """
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    plt.ion()
    fig, ax = plt.subplots(figsize=(8,8))
    fig.canvas.manager.set_window_title(titulo)

    for i, paso in enumerate(historial):
        ax.clear()
        ax.set_title(f"{titulo}  (Paso {i+1}/{len(historial)})")
        ax.set_xlabel("Longitud (lon)")
        ax.set_ylabel("Latitud (lat)")

        # dibujar grafo completo en gris
        dibujar_grafo_completo(ax, ciudades)

        # dependiendo del tipo, extraemos la ruta
        if es_exhaustivo:
            ruta_idxs, dist = paso
            etiqueta = f"Record actual: {dist:.4f}"
            resaltar_ruta(ax, ruta_idxs, color='red', ancho=3, etiqueta=etiqueta)
            ax.legend(loc='upper right')
        else:
            ruta_idxs = paso
            etiqueta = f"Construcción NN (paso {i+1})"
            resaltar_ruta(ax, ruta_idxs + [] , color='green', ancho=3, etiqueta=etiqueta)
            ax.legend(loc='upper right')

        ax.grid(True, linestyle='--', alpha=0.4)
        plt.draw()
        plt.pause(velocidad)

    plt.ioff()
    plt.show()

# ---------------------------------------------------
#  Ejecución principal
# ---------------------------------------------------
def main():
    print("\nMostrando gráfico de puntos (sin conexiones)...")
    grafico_solo_puntos()

    matriz = construir_matriz_distancias()

    # imprime matriz (detallada)
    print("\nMatriz de distancias (euclidiana):")
    mostrar_matriz(matriz, nombres_ciudades)

    # 1) Exhaustivo (medición de tiempo)
    t0 = time.time()
    ruta_ex, dist_ex, hist_ex = busqueda_exhaustiva(matriz)
    t1 = time.time()
    tiempo_ex = t1 - t0
    print("\nExhaustivo: ruta óptima (índices) =", ruta_ex)
    print("Exhaustivo: distancia óptima =", dist_ex)
    print(f"Tiempo exhaustivo: {tiempo_ex:.4f} s")

    # 2) Vecino más cercano (medición de tiempo)
    t0 = time.time()
    ruta_nn, dist_nn, hist_nn = vecino_mas_cercano(matriz, inicio=0)
    t1 = time.time()
    tiempo_nn = t1 - t0
    print("\nVecino más cercano: ruta (índices) =", ruta_nn)
    print("Vecino más cercano: distancia =", dist_nn)
    print(f"Tiempo NN: {tiempo_nn:.4f} s")

    # Gap / comparación
    if dist_ex is not None and dist_ex > 0:
        gap = (dist_nn - dist_ex) / dist_ex * 100
        print(f"\nGap (NN vs óptimo) = {gap:.2f} %")
    else:
        print("\nNo se pudo calcular gap (división por cero o falta de óptimo).")

    # Mostrar grafico final: grafo completo con ambas rutas superpuestas
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    fig, ax = plt.subplots(figsize=(8,8))
    fig.canvas.manager.set_window_title("Grafo Completo con Rutas")
    dibujar_grafo_completo(ax, ciudades)
    resaltar_ruta(ax, ruta_ex, color='red', ancho=3, etiqueta=f"Óptimo ({dist_ex:.4f})")
    resaltar_ruta(ax, ruta_nn, color='green', ancho=2, etiqueta=f"NN ({dist_nn:.4f})")
    ax.legend(loc='upper right')
    ax.set_xlabel("Longitud (lon)")
    ax.set_ylabel("Latitud (lat)")
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.show()

    # Animaciones paso a paso (primero NN, luego exhaustivo records)
    input("\nPresiona ENTER para ver la animación del Vecino Más Cercano...")
    animar_historial(hist_nn, "Vecino Más Cercano (construcción paso a paso)", velocidad=0.8, es_exhaustivo=False)

    input("Presiona ENTER para ver la animación del Exhaustivo (records encontrados)...")
    animar_historial(hist_ex, "Exhaustivo (records encontrados durante la búsqueda)", velocidad=0.6, es_exhaustivo=True)

if __name__ == "__main__":
    main()  
