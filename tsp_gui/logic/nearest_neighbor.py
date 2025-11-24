from .data import n, nombres_ciudades

def vecino_mas_cercano(matriz_dist, inicio=0, logger=None):
    """
    Vecino más cercano. Retorna ruta, dist_total, historial (lista de rutas parciales).
    Muestra todas las decisiones paso a paso.
    """
    if logger:
        logger("=" * 80)
        logger(f"{' INICIANDO VECINO MÁS CERCANO (GREEDY) ':^80}")
        logger("=" * 80)
        logger(f"Comenzamos en: {nombres_ciudades[inicio].upper()}")

    ruta = [inicio]
    visitadas = {inicio}
    actual = inicio
    dist_total = 0.0
    historial = [list(ruta)]

    while len(visitadas) < n:
        if logger:
            logger("")  # Línea en blanco
            logger(f"Estoy en {nombres_ciudades[actual]}... buscando destino más cercano:")
        
        mejor_dist_local = float('inf')
        siguiente = None
        
        # Buscar el vecino no visitado más cercano
        for vecino in range(n):
            if vecino in visitadas:
                continue
            
            d = matriz_dist[actual, vecino]
            
            if logger:
                if d < mejor_dist_local:
                    logger(f"   - ¿Ir a {nombres_ciudades[vecino]}? Distancia: {d:.2f} (¡Candidato actual!)")
                    mejor_dist_local = d
                    siguiente = vecino
                else:
                    logger(f"   - ¿Ir a {nombres_ciudades[vecino]}? Distancia: {d:.2f}")
            else:
                # Sin logger, solo calcular
                if d < mejor_dist_local:
                    mejor_dist_local = d
                    siguiente = vecino
        
        if siguiente is None:
            # Esto no debería ocurrir si el grafo está conectado y n > 0
            if logger:
                logger(f"Error: No se encontró un vecino para {nombres_ciudades[actual]}.")
            break

        # Mover al siguiente
        if logger:
            logger(f" >>> DECISIÓN: Viajo a {nombres_ciudades[siguiente]} (Dist: {mejor_dist_local:.2f})")
        
        dist_total += mejor_dist_local
        actual = siguiente
        ruta.append(actual)
        visitadas.add(actual)
        historial.append(list(ruta))

    # Volver al inicio
    dist_retorno = matriz_dist[actual, inicio]
    if logger:
        logger("")  # Línea en blanco
        logger(f"Todas visitadas. Regresando al inicio ({nombres_ciudades[inicio]})...")
        logger(f" >>> Retorno: {dist_retorno:.2f}")
        logger("")  # Línea en blanco
        logger("-" * 80)
        logger(f"FIN VECINO MÁS CERCANO. Ruta final: {' → '.join([nombres_ciudades[i] for i in ruta])}")
        logger(f"Distancia total: {dist_total:.4f}")
        logger("-" * 80)

    dist_total += dist_retorno
    ruta.append(inicio)
    historial.append(list(ruta))

    return ruta, dist_total, historial