# animation.py
"""Funciones para animación de algoritmos TSP."""
import matplotlib.pyplot as plt
from data import coordenadas, nombres_ciudades
from graphics import dibujar_grafo_completo, resaltar_ruta, TITULO_FS, EJES_FS, LEYENDA_FS


def animar_historial(historial, titulo, velocidad=0.8, es_exhaustivo=False):
    """Animación simple (paso a paso)."""
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