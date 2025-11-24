"""Programa principal para resolver TSP con diferentes algoritmos."""
import time
import matplotlib.pyplot as plt

from data import coordenadas, nombres_ciudades
from distance import construir_matriz_distancias, mostrar_matriz_bonita
from exhaustive import busqueda_exhaustiva
from nearest_neighbor import vecino_mas_cercano
from graphics import grafico_solo_puntos, dibujar_grafo_completo, resaltar_ruta, TITULO_FS, EJES_FS, LEYENDA_FS
from animation import animar_historial


def main():
    print("\nMostrando gráfico de puntos (sin conexiones)...")
    grafico_solo_puntos()

    matriz = construir_matriz_distancias()
    mostrar_matriz_bonita(matriz)

    # 1) Exhaustivo
    t0 = time.time()
    ruta_ex, dist_ex, hist_ex = busqueda_exhaustiva(matriz)
    t1 = time.time()
    tiempo_ex = t1 - t0

    # 2) Vecino más cercano
    t0 = time.time()
    ruta_nn, dist_nn, hist_nn = vecino_mas_cercano(matriz, inicio=0)
    t1 = time.time()
    tiempo_nn = t1 - t0

    # Tabla comparativa (prints en consola)
    print("\n" + "█" * 80)
    print(f"{' RESUMEN DE RENDIMIENTO ':^80}")
    print("█" * 80)
    print(f"{'Método':<30} | {'Tiempo (seg)':<15} | {'Distancia Total':<15}")
    print("-" * 80)
    print(f"{'Exhaustivo (Óptimo)':<30} | {tiempo_ex:<15.6f} | {dist_ex:<15.4f}")
    print(f"{'Vecino Más Cercano':<30} | {tiempo_nn:<15.6f} | {dist_nn:<15.4f}")
    print("-" * 80)

    if dist_ex is not None and dist_ex > 0:
        gap = (dist_nn - dist_ex) / dist_ex * 100
        print(f" CONCLUSIÓN: El vecino más cercano se desvió un {gap:.2f}% del óptimo.")
    else:
        print("\nNo se pudo calcular gap.")

    # --- ANIMACIONES ---
    print("\n--- ANIMACIONES ---")
    input("Presiona ENTER para ver la animación del Vecino Más Cercano...")
    animar_historial(hist_nn, "Vecino Más Cercano (construcción paso a paso)",
                     velocidad=0.8, es_exhaustivo=False)

    input("Presiona ENTER para ver la animación del Exhaustivo (records)...")
    animar_historial(hist_ex, "Exhaustivo (records encontrados)",
                     velocidad=0.6, es_exhaustivo=True)

    # --- GRÁFICO FINAL (lo ÚLTIMO en mostrarse) ---
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    fig, ax = plt.subplots(figsize=(8, 8))
    try:
        fig.canvas.manager.set_window_title("Comparativa Final: Greedy vs Óptimo")
    except Exception:
        pass

    dibujar_grafo_completo(ax, ciudades)
    resaltar_ruta(ax, ruta_ex, color='red', ancho=3,
                  etiqueta=f"Óptimo ({dist_ex:.4f})")
    resaltar_ruta(ax, ruta_nn, color='green', ancho=2,
                  etiqueta=f"NN ({dist_nn:.4f})")
    ax.legend(loc='upper right', fontsize=LEYENDA_FS)
    ax.set_xlabel("Longitud (lon)", fontsize=EJES_FS)
    ax.set_ylabel("Latitud (lat)", fontsize=EJES_FS)
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.show()   # <- este show se ejecuta al final de todo
if __name__ == "__main__":
    main()