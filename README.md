# Problema del Viajante (TSP) – Algoritmos y Visualización

Este proyecto implementa el Problema del Viajante (TSP) de dos maneras:

1. **Código bruto de algoritmos** (sin interfaz gráfica):  
   Implementa el cálculo de distancias, la búsqueda exhaustiva (óptima) y la heurística de Vecino Más Cercano, además de utilidades para graficar y animar las rutas con Matplotlib.

2. **Interfaz gráfica interactiva con Streamlit**:  
   Una aplicación web que permite:
   - Ver la tabla de ciudades y sus coordenadas.
   - Generar y visualizar la **matriz de distancias**.
   - Ejecutar paso a paso la **búsqueda exhaustiva** y el **Vecino Más Cercano**, con animaciones usando Plotly.
   - Comparar tiempos, distancias, _gap_ de optimalidad y visualizar ambas rutas superpuestas en un solo mapa.

## Estructura del repositorio

- `tsp_core/`  
  Código “bruto” con la lógica principal del TSP:

  - `data.py`: definición de ciudades y coordenadas.
  - `distance.py`: construcción de la matriz de distancias.
  - `exhaustive.py`: búsqueda exhaustiva (solución óptima).
  - `nearest_neighbor.py`: heurística de Vecino Más Cercano.
  - `graphics.py`: gráficos y resaltado de rutas con Matplotlib.
  - `animation.py`: animaciones paso a paso.

  Más detalles en [`tsp_core/README.md`](tsp_core/README.md).

- `tsp_gui/`  
  Interfaz gráfica basada en Streamlit y Plotly:

  - `main.py`: punto de entrada de la app (`streamlit run main.py`).
  - `core/`: gestión de estado, procesamiento y orquestación de secciones.
    - `state.py`: manejo de `st.session_state` y resultados.
    - `processing.py`: ejecución de algoritmos, generación de DataFrames y gráficos.
  - `logic/`: lógica de TSP reutilizada para la interfaz.
    - `data.py`, `distance.py`, `exhaustive.py`, `nearest_neighbor.py`,
      `graphics.py`, `animation.py`.
  - `components/`: capa de presentación y estilos.
    - `content.py`: estilos globales y secciones visuales.
    - `information.py`: cajas de información, alertas y métricas.
    - `app.py`: layout de cada sección de la app (ciudades, matriz, exhaustiva, vecino, comparación).

  Más detalles en [`tsp_gui/README.md`](tsp_gui/README.md).

## Ejecución rápida

### 1. Entorno (en sus respectivas carpetas)

```bash
pip install -r requirements.txt
```

### 2. Ejecutar solo el código bruto (con gráficos Matplotlib)

cd tsp_core
python tsp_grafo_combinado.py

### 3. Ejecutar la interfaz gráfica (Streamlit)

cd tsp_gui
streamlit run main.py
