import numpy as np
import itertools
import matplotlib.pyplot as plt
import time

# =============================================================================
# 1. DATOS
# =============================================================================

'''
Datos de google maps sobre las plazas de armas de cada sitio
coordenadas = {
    "Temuco": (-38.73924804905055, -72.59037442500298),
    "Villarrica": (-39.277930266287626, -72.22750273186602),
    "Pucón": (-39.272975881908295, -71.97773335885098),
    "Angol": (-37.79859525844711, -72.7095697866449),
    "Victoria": (-38.1756178907116, -72.3358133749394),
    "Lautaro": (-38.53371314846101, -72.43532045597144),
    "Nueva Imperial": (-38.744786477975666, -72.95210789444599)
'''

coordenadas = {
    "Nueva York": (40.7128, -74.0060),
    "Los Ángeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "Phoenix": (33.4484, -112.0740)
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

def mostrar_matriz(matriz, nombres):
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

def busqueda_exhaustiva(matriz_dist):
    print("\n" + "="*60)
    print("INICIANDO: ALGORITMO DE BUSQUEDA EXHAUSTIVA")
    print("="*60)
    
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
            print(f"[Intento #{contador}] ¡RECORD ENCONTRADO!")
            print(f"   Ruta: {ruta_nombres}")
            print(f"   Distancia: {mejor_dist:.4f}")
            print("-" * 20)
            
    print(f"Total de rutas evaluadas: {contador}")
    return mejor_ruta, mejor_dist, historial

def vecino_mas_cercano(matriz_dist, inicio=0):
    print("\n" + "="*60)
    print("INICIANDO: ALGORITMO DE VECINO MAS CERCANO")
    print("="*60)
    
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
    plt.rcParams.update({'font.size': 18})  
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title(titulo_ventana)
    
    for i, paso in enumerate(historial):
        ax.clear()
        
        ax.set_title(f"{titulo_ventana}\nEstado: {i+1}/{len(historial)}", fontsize=18)
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        
        lats = [coordenadas[c][0] for c in nombres_ciudades]
        lons = [coordenadas[c][1] for c in nombres_ciudades]
        ax.scatter(lons, lats, c='blue', s=100, zorder=5)
        
        for idx, txt in enumerate(nombres_ciudades):
            ax.annotate(txt, (lons[idx], lats[idx]), xytext=(5, 5), 
                        textcoords='offset points', fontsize=18)
        
        if es_optimo:
            ruta_idxs, dist = paso
            color = 'red'
            info = f"Record Actual: {dist:.4f}"
        else:
            ruta_idxs = paso
            color = 'green'
            info = "Explorando..."
            
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

matriz = construir_matriz_distancias()
mostrar_matriz(matriz, nombres_ciudades)

# --- MEDICION ALGORITMO DE BUSQUEDA EXHAUSTIVA ---
t_inicio_ex = time.time()
ruta_ex, dist_ex, hist_ex = busqueda_exhaustiva(matriz)
t_fin_ex = time.time()
tiempo_ex = t_fin_ex - t_inicio_ex

# --- MEDICION ALGORITMO DE VECINO MAS CERCANO ---
t_inicio_nn = time.time()
ruta_nn, dist_nn, hist_nn = vecino_mas_cercano(matriz)
t_fin_nn = time.time()
tiempo_nn = t_fin_nn - t_inicio_nn

# --- TABLA COMPARATIVA  ---
# Ajustamos el ancho de la primera columna a 35 caracteres
ancho_nombre = 35
ancho_tabla = ancho_nombre + 15 + 15 + 6 # +6 por los separadores ' | '

print("\n" + "="*ancho_tabla)
print(f"{'COMPARATIVA DE RENDIMIENTO':^{ancho_tabla}}")
print("="*ancho_tabla)
print(f"{'Nombre del Algoritmo':<{ancho_nombre}} | {'Tiempo (seg)':<15} | {'Distancia Total':<15}")
print("-" * ancho_tabla)

print(f"{'Algoritmo de Busqueda Exhaustiva':<{ancho_nombre}} | {tiempo_ex:<15.6f} | {dist_ex:<15.4f}")
print(f"{'Algoritmo de Vecino Mas Cercano':<{ancho_nombre}} | {tiempo_nn:<15.6f} | {dist_nn:<15.4f}")
print("-" * ancho_tabla)

# --- ANALISIS ---
if dist_nn == dist_ex:
    conclusion = "CONCLUSION: Empate!"
else:
    diff = ((dist_nn - dist_ex) / dist_ex) * 100
    conclusion = f"CONCLUSION: El Vecino Mas Cercano fue un {diff:.2f}% menos eficiente."

print(conclusion)
print("="*ancho_tabla)

# --- GRAFICOS ---
print("\n--- MODO VISUALIZACION EN VIVO ---")
input("Presiona ENTER para ver: Algoritmo de Vecino Mas Cercano...")
reproducir_en_vivo(hist_nn, "Algoritmo de Vecino Mas Cercano", es_optimo=False, velocidad=0.8)

print("\nLa ventana anterior mostro el resultado.")
input("Cierra la ventana y presiona ENTER para ver: Algoritmo de Busqueda Exhaustiva...")
reproducir_en_vivo(hist_ex, "Algoritmo de Busqueda Exhaustiva", es_optimo=True, velocidad=0.5)

print("\nFIN")