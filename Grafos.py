
import numpy as np
import itertools
import matplotlib.pyplot as plt

# =============================================================================
# 1. DATOS
# =============================================================================
coordenadas = {
    "Temuco": (-38.7392, -72.5904),
    "Villarrica": (-39.2779, -72.2274),
    "Pucon": (-39.2667, -71.9667),
    "Angol": (-37.7986, -72.7096),
    "Victoria": (-38.2167, -72.3333),
    "Lautaro": (-38.5337, -72.4353),
    "Nueva Imperial": (-38.7448, -72.9521)
}

nombres_ciudades = list(coordenadas.keys())
n = len(nombres_ciudades)

# =============================================================================
# 2. LOGICA MATEMATICA 
# =============================================================================
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

# --- FUNCIÓN CORREGIDA PARA NOMBRES LARGOS ---
def mostrar_matriz(matriz, nombres):
    ancho_col = 16
    ancho_nombre_fila = 16
    # Calculamos el ancho total 
    ancho_total = ancho_nombre_fila + (ancho_col * len(nombres))
    print("\n" + "="*ancho_total)
    print(f"{'MATRIZ DE DISTANCIAS (Grados Euclidianos)':^{ancho_total}}")
    print("="*ancho_total)

    # 1. Imprimir Encabezado
    header = f"{'':<{ancho_nombre_fila}}" + "".join([f"{nombre:>{ancho_col}}" for nombre in nombres])
    print(header)
    print("-" * len(header))
    # 2. Imprimir Filas
    for i, fila in enumerate(matriz):
        # Nombre de la ciudad a la izquierda
        linea = f"{nombres[i]:<{ancho_nombre_fila}}"
        for val in fila:
            if val == 0:
                # Poner un guion en la diagonal (distancia 0)
                linea += f"{'-':>{ancho_col}}"
            else:
                # Formatear a 4 decimales y usar el ancho correcto
                linea += f"{val:{ancho_col}.4f}"
        print(linea)
    print("-" * len(header))
    print(f"{'* Los valores representan distancia euclidiana plana.':^{ancho_total}}\n")

def busqueda_exhaustiva(matriz_dist):
    print("\n" + "="*40)
    print("INICIANDO BUSQUEDA EXHAUSTIVA")
    print("="*40)
    
    indices = list(range(n))
    inicio = 0
    otros = indices[1:]
    mejor_dist = float('inf')
    mejor_ruta = []
    historial = []
    
    contador = 0

    for perm in itertools.permutations(otros):
        contador += 1
        ruta_actual = [inicio] + list(perm) + [inicio]
        
        dist_actual = 0
        for i in range(len(ruta_actual) - 1):
            dist_actual += matriz_dist[ruta_actual[i], ruta_actual[i+1]]
            
        if dist_actual < mejor_dist:
            mejor_dist = dist_actual
            mejor_ruta = ruta_actual
            historial.append((list(mejor_ruta), mejor_dist))
            
            ruta_nombres = " -> ".join([nombres_ciudades[idx] for idx in mejor_ruta])
            print(f"[Intento #{contador}] NUEVO RECORD ENCONTRADO!")
            print(f"   Ruta: {ruta_nombres}")
            print(f"   Distancia: {mejor_dist:.4f}")
            print("-" * 20)
            
    print(f"Total de rutas evaluadas: {contador}")
    return mejor_ruta, mejor_dist, historial

def vecino_mas_cercano(matriz_dist, inicio=0):
    print("\n" + "="*40)
    print("INICIANDO HEURISTICA VECINO MAS CERCANO")
    print("="*40)
    
    ruta = [inicio]
    visitadas = {inicio}
    actual = inicio
    dist_total = 0
    historial = [list(ruta)]
    
    print(f"Inicio en: {nombres_ciudades[inicio]}")
    
    while len(visitadas) < n:
        mejor_dist_local = float('inf')
        siguiente = -1
        
        print(f"\nEstoy en {nombres_ciudades[actual]}, mirando vecinos:")
        
        for vecino in range(n):
            if vecino not in visitadas:
                d = matriz_dist[actual, vecino]
                print(f"   -> Candidato: {nombres_ciudades[vecino]} (Distancia: {d:.4f})")
                
                if d < mejor_dist_local:
                    mejor_dist_local = d
                    siguiente = vecino
        
        print(f"   >>> DECISION: El mas cercano es {nombres_ciudades[siguiente]} ({mejor_dist_local:.4f})")
        
        dist_total += mejor_dist_local
        actual = siguiente
        ruta.append(actual)
        visitadas.add(actual)
        historial.append(list(ruta))
    
    dist_retorno = matriz_dist[actual, inicio]
    print(f"\nTodas las ciudades visitadas. Regresando a {nombres_ciudades[inicio]} (Distancia: {dist_retorno:.4f})")
    
    dist_total += dist_retorno
    ruta.append(inicio)
    historial.append(list(ruta))
    
    return ruta, dist_total, historial

# =============================================================================
# 3. VISUALIZACION EN VIVO
# =============================================================================

def reproducir_en_vivo(historial, titulo_ventana, es_optimo=False, velocidad=0.5):
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title(titulo_ventana)
    
    for i, paso in enumerate(historial):
        ax.clear()
        
        ax.set_title(f"{titulo_ventana}\nEstado: {i+1}/{len(historial)}", fontsize=12)
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        
        lats = [coordenadas[c][0] for c in nombres_ciudades]
        lons = [coordenadas[c][1] for c in nombres_ciudades]
        ax.scatter(lons, lats, c='blue', s=100, zorder=5)
        
        for idx, txt in enumerate(nombres_ciudades):
            ax.annotate(txt, (lons[idx], lats[idx]), xytext=(5, 5), 
                        textcoords='offset points', fontsize=9)
        
        if es_optimo:
            ruta_idxs, dist = paso
            color = 'red'
            info = f"Distancia Record: {dist:.4f}"
        else:
            ruta_idxs = paso
            color = 'green'
            info = "Buscando siguiente ciudad..."
            
        r_lats = [coordenadas[nombres_ciudades[idx]][0] for idx in ruta_idxs]
        r_lons = [coordenadas[nombres_ciudades[idx]][1] for idx in ruta_idxs]
        
        ax.plot(r_lons, r_lats, c=color, linewidth=2, label=info)
        ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.5)
        
        plt.draw()
        plt.pause(velocidad)
        
    plt.ioff()
    plt.show()

# =============================================================================
# 4. EJECUCION
# =============================================================================
if __name__ == "__main__":
    matriz = construir_matriz_distancias()
    
    # Printear matriz completa sin recortes
    mostrar_matriz(matriz, nombres_ciudades)
    
    ruta_ex, dist_ex, hist_ex = busqueda_exhaustiva(matriz)
    ruta_nn, dist_nn, hist_nn = vecino_mas_cercano(matriz)
    
    print("\n" + "="*40)
    print("CALCULOS FINALIZADOS. INICIANDO GRAFICOS...")
    print("="*40)
    
    print("\n--- MODO VISUALIZACION EN VIVO ---")
    input("Presiona ENTER para ver la animacion de Heuristica (Vecino Mas Cercano)...")
    reproducir_en_vivo(hist_nn, "Heuristica Vecino Mas Cercano", es_optimo=False, velocidad=0.8)
    
    print("\nLa ventana anterior mostro el resultado final.")
    input("Cierra la ventana del grafico y presiona ENTER para ver la animacion de Busqueda Exhaustiva...")
    reproducir_en_vivo(hist_ex, "Busqueda Exhaustiva (Mejorando Rutas)", es_optimo=True, velocidad=0.5)
    
    print("\n¡Demostracion finalizada!")