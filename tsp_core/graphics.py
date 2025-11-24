"""Funciones para visualización de grafos y rutas."""
import matplotlib.pyplot as plt
from data import coordenadas, nombres_ciudades

# Tamaños de fuente
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


def grafico_solo_puntos():
    """Gráfico simple de solo puntos (sin conexiones)."""
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