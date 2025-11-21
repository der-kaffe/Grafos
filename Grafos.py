# tsp_grafo_combinado.py
import numpy as np
import itertools
import matplotlib.pyplot as plt
import time
import math

# ----------------------------
#  Datos (puedes cambiarlos)
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

# ---------------------------------------------------
#  Búsqueda exhaustiva (CON PRINTS DETALLADOS)
# ---------------------------------------------------
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
            a = ruta_actual[i]; b = ruta_actual[i + 1]
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

# ---------------------------------------------------
#  Heurística: Vecino Más Cercano (CON PRINTS DETALLADOS)
# ---------------------------------------------------
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

# ---------------------------------------------------
#  Visualización: grafo completo + resaltado de ruta
# ---------------------------------------------------
# Tamaños (Opción A)
TITULO_FS = 16
EJES_FS = 15
CIUDADES_FS = 16
LEYENDA_FS = 12

def dibujar_grafo_completo(ax, ciudades, color_arista='#cccccc'):
    """Dibuja todas las aristas, nodos y etiquetas una sola vez."""
    lats = [c[0] for c in ciudades]
    lons = [c[1] for c in ciudades]

    # dibujar todas las aristas (i,j) con i<j
    for i in range(len(ciudades)):
        for j in range(i + 1, len(ciudades)):
            ax.plot([lons[i], lons[j]], [lats[i], lats[j]], color=color_arista,
                    linewidth=0.8, zorder=1)

    # nodos y etiquetas
    ax.scatter(lons, lats, c='blue', s=80, zorder=3)
    for idx, name in enumerate(nombres_ciudades):
        ax.annotate(name, (lons[idx], lats[idx]), xytext=(5, 5),
                    textcoords='offset points', fontsize=CIUDADES_FS, zorder=4)

    # etiquetas de los ejes (solo una vez)
    ax.set_xlabel("Longitud (lon)", fontsize=EJES_FS)
    ax.set_ylabel("Latitud (lat)", fontsize=EJES_FS)

def resaltar_ruta(ax, ruta_idxs, color='red', ancho=3, etiqueta=None):
    """Dibuja la ruta (lista de índices) sobre ax."""
    lats_r = [coordenadas[nombres_ciudades[i]][0] for i in ruta_idxs]
    lons_r = [coordenadas[nombres_ciudades[i]][1] for i in ruta_idxs]
    ax.plot(lons_r, lats_r, color=color, linewidth=ancho, zorder=5, label=etiqueta)

# ---------------------------------------------------
#  Animación simple (paso a paso)
# ---------------------------------------------------
def animar_historial(historial, titulo, velocidad=0.8, es_exhaustivo=False):
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    # intentar poner título de ventana, fallará silenciosamente si no aplica
    try:
        fig.canvas.manager.set_window_title(titulo)
    except Exception:
        pass

    for i, paso in enumerate(historial):
        ax.clear()
        ax.set_title(f"{titulo}  (Paso {i+1}/{len(historial)})", fontsize=TITULO_FS)
        ax.set_xlabel("Longitud (lon)", fontsize=EJES_FS)
        ax.set_ylabel("Latitud (lat)", fontsize=EJES_FS)

        # dibujar grafo completo en gris
        dibujar_grafo_completo(ax, ciudades)

        # dependiendo del tipo, extraemos la ruta
        if es_exhaustivo:
            ruta_idxs, dist = paso
            etiqueta = f"Record actual: {dist:.4f}"
            resaltar_ruta(ax, ruta_idxs, color='red', ancho=3, etiqueta=etiqueta)
            ax.legend(loc='upper right', fontsize=LEYENDA_FS)
        else:
            ruta_idxs = paso
            etiqueta = f"Construcción NN (paso {i+1})"
            resaltar_ruta(ax, ruta_idxs, color='green', ancho=3, etiqueta=etiqueta)
            ax.legend(loc='upper right', fontsize=LEYENDA_FS)

        ax.grid(True, linestyle='--', alpha=0.4)
        plt.draw()
        plt.pause(velocidad)

    plt.ioff()
    plt.show()

# ---------------------------------------------------
#  Gráfico simple de solo puntos (sin conexiones)
# ---------------------------------------------------
def grafico_solo_puntos():
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    lats = [c[0] for c in ciudades]
    lons = [c[1] for c in ciudades]

    plt.figure(figsize=(8, 8))
    plt.scatter(lons, lats, c='blue', s=100)

    for idx, name in enumerate(nombres_ciudades):
        plt.annotate(name, (lons[idx], lats[idx]), xytext=(5, 5),
                     textcoords='offset points', fontsize=CIUDADES_FS)

    plt.title("Mapa de ciudades (sin conexiones)", fontsize=TITULO_FS)
    plt.xlabel("Longitud", fontsize=EJES_FS)
    plt.ylabel("Latitud", fontsize=EJES_FS)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.show()

# ---------------------------------------------------
#  Ejecución principal
# ---------------------------------------------------
def main():
    print("\nMostrando gráfico de puntos (sin conexiones)...")
    grafico_solo_puntos()

    matriz = construir_matriz_distancias()

    # Mostrar matriz bonita
    mostrar_matriz_bonita(matriz)

    # 1) Exhaustivo (medición de tiempo)
    t0 = time.time()
    ruta_ex, dist_ex, hist_ex = busqueda_exhaustiva(matriz)
    t1 = time.time()
    tiempo_ex = t1 - t0

    # 2) Vecino más cercano (medición de tiempo)
    t0 = time.time()
    ruta_nn, dist_nn, hist_nn = vecino_mas_cercano(matriz, inicio=0)
    t1 = time.time()
    tiempo_nn = t1 - t0

    # ----------------------------
    #  TABLA COMPARATIVA FINAL
    # ----------------------------
    print("\n" + "█" * 80)
    print(f"{' RESUMEN DE RENDIMIENTO ':^80}")
    print("█" * 80)
    print(f"{'Método':<30} | {'Tiempo (seg)':<15} | {'Distancia Total':<15}")
    print("-" * 80)
    print(f"{'Exhaustivo (Óptimo)':<30} | {tiempo_ex:<15.6f} | {dist_ex:<15.4f}")
    print(f"{'Vecino Más Cercano':<30} | {tiempo_nn:<15.6f} | {dist_nn:<15.4f}")
    print("-" * 80)

    # Gap / comparación
    if dist_ex is not None and dist_ex > 0:
        gap = (dist_nn - dist_ex) / dist_ex * 100
        print(f" CONCLUSIÓN: El vecino más cercano se desvió un {gap:.2f}% del óptimo.")
    else:
        print("\nNo se pudo calcular gap.")

    # Mostrar grafico final: grafo completo con ambas rutas superpuestas
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    fig, ax = plt.subplots(figsize=(8, 8))
    try:
        fig.canvas.manager.set_window_title("Comparativa Final: Greedy vs Óptimo")
    except Exception:
        pass

    dibujar_grafo_completo(ax, ciudades)
    resaltar_ruta(ax, ruta_ex, color='red', ancho=3, etiqueta=f"Óptimo ({dist_ex:.4f})")
    resaltar_ruta(ax, ruta_nn, color='green', ancho=2, etiqueta=f"NN ({dist_nn:.4f})")
    ax.legend(loc='upper right', fontsize=LEYENDA_FS)
    ax.set_xlabel("Longitud (lon)", fontsize=EJES_FS)
    ax.set_ylabel("Latitud (lat)", fontsize=EJES_FS)
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.show()

    # Animaciones
    print("\n--- ANIMACIONES ---")
    input("Presiona ENTER para ver la animación del Vecino Más Cercano...")
    animar_historial(hist_nn, "Vecino Más Cercano (construcción paso a paso)", velocidad=0.8, es_exhaustivo=False)

    input("Presiona ENTER para ver la animación del Exhaustivo (records)...")
    animar_historial(hist_ex, "Exhaustivo (records encontrados)", velocidad=0.6, es_exhaustivo=True)

if __name__ == "__main__":
    main()
