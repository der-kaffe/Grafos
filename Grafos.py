import numpy as np
import itertools
import matplotlib.pyplot as plt
import time

# =============================================================================
# 1. CONFIGURACIÓN Y DATOS (CIUDADES DE LA ARAUCANÍA, CHILE)
# =============================================================================

coordenadas = {
    "Temuco": (-38.7392, -72.5903),
    "Villarrica": (-39.2779, -72.2275),
    "Pucón": (-39.2729, -71.9777),
    "Angol": (-37.7985, -72.7095),
    "Victoria": (-38.1756, -72.3358),
    "Lautaro": (-38.5337, -72.4353),
    "Nueva Imperial": (-38.7447, -72.9521)
}

nombres_ciudades = list(coordenadas.keys())
n = len(nombres_ciudades)

# =============================================================================
# 2. HERRAMIENTAS MATEMÁTICAS
# =============================================================================

def distancia_euclidiana(c1_idx, c2_idx):
    """Calcula la hipotenusa entre dos coordenadas (distancia recta)."""
    lat1, lon1 = coordenadas[nombres_ciudades[c1_idx]]
    lat2, lon2 = coordenadas[nombres_ciudades[c2_idx]]
    return np.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)

def construir_matriz_distancias():
    """Genera una tabla de distancias 'todos contra todos'."""
    matriz = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia_euclidiana(i, j)
            matriz[i, j] = d
            matriz[j, i] = d
    return matriz

def mostrar_matriz(matriz, nombres):
    print("\n" + "█"*80)
    print(f"{' 1. TABLA DE DISTANCIAS PRE-CALCULADAS ':^80}")
    print("█"*80)
    
    # Encabezados
    print(f"{'':<15}", end="")
    for nombre in nombres:
        print(f"{nombre[:10]:>10}", end="")
    print("\n" + "-"*85)

    # Filas
    for i, fila in enumerate(matriz):
        print(f"{nombres[i]:<15}", end="")
        for val in fila:
            if val == 0:
                print(f"{'-':>10}", end="")
            else:
                print(f"{val:>10.3f}", end="")
        print()
    print("-" * 85)

# =============================================================================
# 3. ALGORITMO: BÚSQUEDA EXHAUSTIVA (FUERZA BRUTA)
# =============================================================================

def busqueda_exhaustiva(matriz_dist):
    print("\n" + "█"*80)
    print(f"{' 2. EJECUTANDO BÚSQUEDA EXHAUSTIVA (La solución perfecta) ':^80}")
    print("█"*80)
    print("Descripción: Probando TODAS las combinaciones posibles de rutas...")
    
    indices = list(range(n))
    inicio = 0
    otros = indices[1:] # Todas las ciudades menos la de inicio
    
    mejor_dist = float('inf')
    mejor_ruta = []
    historial = []
    
    contador = 0
    total_permutaciones = 1  # Factorial de n-1
    for k in range(1, n): total_permutaciones *= k

    print(f" -> Total de rutas a evaluar: {total_permutaciones}")
    print("-" * 80)

    for perm in itertools.permutations(otros):
        contador += 1
        ruta_actual = [inicio] + list(perm) + [inicio]
        
        # Calcular distancia de esta ruta específica
        dist_actual = 0
        for i in range(len(ruta_actual) - 1):
            dist_actual += matriz_dist[ruta_actual[i], ruta_actual[i+1]]
            
        # Si encontramos un nuevo récord
        if dist_actual < mejor_dist:
            mejora = mejor_dist - dist_actual if mejor_dist != float('inf') else 0
            mejor_dist = dist_actual
            mejor_ruta = list(ruta_actual)
            historial.append((list(mejor_ruta), mejor_dist))
            
            ruta_txt = "→".join([nombres_ciudades[x][:3] for x in mejor_ruta])
            print(f" [{contador:^5}/{total_permutaciones}] ¡NUEVO RÉCORD! Dist: {mejor_dist:.4f} | Mejora: -{mejora:.4f}")
            print(f"           Ruta: {ruta_txt}")

    print("-" * 80)
    print(f"¡BÚSQUEDA FINALIZADA! La mejor ruta absoluta es de {mejor_dist:.4f}")
    return mejor_ruta, mejor_dist, historial

# =============================================================================
# 4. ALGORITMO: VECINO MÁS CERCANO (GREEDY / AVARO)
# =============================================================================

def vecino_mas_cercano(matriz_dist, inicio=0):
    print("\n" + "█"*80)
    print(f"{' 3. EJECUTANDO VECINO MÁS CERCANO (La solución rápida) ':^80}")
    print("█"*80)
    print(f"Estrategia: Desde {nombres_ciudades[inicio]}, ir siempre al más cercano disponible.")
    
    ruta = [inicio]
    visitadas = {inicio}
    actual = inicio
    dist_total = 0
    historial = [list(ruta)]
    
    paso = 1
    
    while len(visitadas) < n:
        print(f"\n[Paso {paso}] Estamos en: {nombres_ciudades[actual].upper()}")
        print(f"   Analizando distancias a ciudades no visitadas:")
        
        mejor_dist_local = float('inf')
        siguiente = -1
        
        # Evaluar candidatos
        for vecino in range(n):
            if vecino not in visitadas:
                d = matriz_dist[actual, vecino]
                # Lógica de visualización de comparación
                estado = " "
                if d < mejor_dist_local:
                    estado = "*" # Marcamos temporalmente el mejor
                
                print(f"    ├── {nombres_ciudades[vecino]:<15} : {d:.4f} {estado}")
                
                if d < mejor_dist_local:
                    mejor_dist_local = d
                    siguiente = vecino
        
        print(f"    └──> ¡DECISIÓN! Viajamos a {nombres_ciudades[siguiente]} (Es el más cercano)")
        
        dist_total += mejor_dist_local
        actual = siguiente
        ruta.append(actual)
        visitadas.add(actual)
        historial.append(list(ruta))
        paso += 1
    
    # Regreso al origen
    dist_retorno = matriz_dist[actual, inicio]
    print(f"\n[Final] Volviendo a casa ({nombres_ciudades[inicio]})")
    print(f"    └── Distancia de retorno: {dist_retorno:.4f}")
    
    dist_total += dist_retorno
    ruta.append(inicio)
    historial.append(list(ruta))
    
    return ruta, dist_total, historial

# =============================================================================
# 5. VISUALIZACIÓN GRÁFICA ANIMADA
# =============================================================================

def reproducir_en_vivo(historial, titulo_ventana, es_optimo=False, velocidad=0.5):
    plt.rcParams.update({'font.size': 10})  
    plt.ion() # Modo interactivo activado
    fig, ax = plt.subplots(figsize=(9, 7))
    fig.canvas.manager.set_window_title(titulo_ventana)
    
    lats = [coordenadas[c][0] for c in nombres_ciudades]
    lons = [coordenadas[c][1] for c in nombres_ciudades]
    
    for i, paso in enumerate(historial):
        ax.clear()
        
        # Configuración del mapa
        ax.set_title(f"{titulo_ventana}\nEstado: {i+1}/{len(historial)}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        
        # Dibujar puntos (Ciudades)
        ax.scatter(lons, lats, c='navy', s=150, zorder=5, edgecolors='white')
        
        # Etiquetas de ciudades
        for idx, txt in enumerate(nombres_ciudades):
            ax.annotate(txt, (lons[idx], lats[idx]), xytext=(8, 8), 
                        textcoords='offset points', fontsize=11, fontweight='bold')
        
        # Dibujar líneas (Rutas)
        if es_optimo:
            ruta_idxs, dist = paso
            color_linea = '#e74c3c' # Rojo
            estilo = '-'
            info_leyenda = f"Récord Actual: {dist:.4f}"
            alpha_line = 1.0
        else:
            ruta_idxs = paso
            color_linea = '#27ae60' # Verde
            estilo = '--'
            info_leyenda = "Explorando ruta..."
            alpha_line = 0.8
            
        r_lats = [coordenadas[nombres_ciudades[idx]][0] for idx in ruta_idxs]
        r_lons = [coordenadas[nombres_ciudades[idx]][1] for idx in ruta_idxs]
        
        # Dibujar el camino
        ax.plot(r_lons, r_lats, c=color_linea, linewidth=2.5, linestyle=estilo, label=info_leyenda, alpha=alpha_line, zorder=4)
        
        # Marcar inicio y fin actual
        if len(r_lons) > 0:
             ax.plot(r_lons[0], r_lats[0], 'go', markersize=10, alpha=0.3) # Inicio verde claro
             ax.plot(r_lons[-1], r_lats[-1], 'ro', markersize=5) # Cabeza actual roja
        
        ax.legend(loc='upper right')
        ax.grid(True, linestyle=':', alpha=0.6)
        
        plt.draw()
        plt.pause(velocidad)
        
    plt.ioff()
    print(f"\n[Gráfico] Animación de '{titulo_ventana}' finalizada.")
    plt.show()

# =============================================================================
# 6. EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    matriz = construir_matriz_distancias()
    mostrar_matriz(matriz, nombres_ciudades)

    # --- EJECUCIÓN VECINO MÁS CERCANO ---
    t0 = time.time()
    ruta_nn, dist_nn, hist_nn = vecino_mas_cercano(matriz)
    t1 = time.time()
    tiempo_nn = t1 - t0

    # --- EJECUCIÓN BÚSQUEDA EXHAUSTIVA ---
    t2 = time.time()
    ruta_ex, dist_ex, hist_ex = busqueda_exhaustiva(matriz)
    t3 = time.time()
    tiempo_ex = t3 - t2

    # --- RESUMEN FINAL ---
    ancho = 70
    print("\n" + "="*ancho)
    print(f"{' RESUMEN DE RESULTADOS ':^{ancho}}")
    print("="*ancho)
    
    print(f"{'Métrica':<25} | {'Vecino Más Cercano (Heurística)':<20} | {'Exhaustiva (Exacta)':<20}")
    print("-" * ancho)
    print(f"{'Tiempo de Cómputo':<25} | {tiempo_nn:<20.6f} | {tiempo_ex:<20.6f}")
    print(f"{'Distancia Total':<25} | {dist_nn:<20.4f} | {dist_ex:<20.4f}")
    
    error = ((dist_nn - dist_ex) / dist_ex) * 100
    print("-" * ancho)
    print(f"DIFERENCIA (GAP): El algoritmo rápido fue un {error:.2f}% peor que el óptimo.")
    
    ruta_nn_str = " -> ".join([nombres_ciudades[i][:3] for i in ruta_nn])
    ruta_ex_str = " -> ".join([nombres_ciudades[i][:3] for i in ruta_ex])
    
    print(f"\nRuta NN:  {ruta_nn_str}")
    print(f"Ruta Exh: {ruta_ex_str}")
    print("="*ancho)

    # --- ANIMACIONES ---
    print("\n--> Preparando visualización gráfica...")
    input("Presiona [ENTER] para ver la animación del: VECINO MÁS CERCANO...")
    reproducir_en_vivo(hist_nn, "Vecino Más Cercano (Construcción)", es_optimo=False, velocidad=0.8)

    print("\n")
    input("Presiona [ENTER] para ver la animación de la: BÚSQUEDA EXHAUSTIVA...")
    reproducir_en_vivo(hist_ex, "Búsqueda Exhaustiva (Mejores Records)", es_optimo=True, velocidad=0.6)