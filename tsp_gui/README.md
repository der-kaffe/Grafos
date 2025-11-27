# TSP GUI - Interfaz Gráfica Interactiva

Aplicación web interactiva construida con Streamlit y Plotly para visualizar y comparar algoritmos de solución del Problema del Viajante (TSP).

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Arquitectura](#-arquitectura)
- [Componentes Principales](#-componentes-principales)
- [Flujo de Datos](#-flujo-de-datos)
- [Personalización](#-personalización)
- [Troubleshooting](#-troubleshooting)

## 🎯 Descripción General

Esta interfaz gráfica permite explorar de forma interactiva el Problema del Viajante (TSP) mediante:

- **Visualización de datos**: Tabla de ciudades, coordenadas y matriz de distancias.
- **Ejecución de algoritmos**: Búsqueda exhaustiva (óptima) y Vecino Más Cercano (heurística).
- **Animaciones paso a paso**: Observa cómo cada algoritmo construye su ruta.
- **Comparación visual**: Gráficos superpuestos, métricas de rendimiento y análisis de gap.

La aplicación está diseñada con un tema oscuro moderno y una arquitectura modular que separa lógica, presentación y estado.

## ✨ Características

### 1. Sección de Ciudades y Coordenadas

- Tabla interactiva con las coordenadas geográficas (latitud/longitud).
- Mapa visual de puntos sin conexiones.

### 2. Matriz de Distancias

- Cálculo automático de distancias euclidianas.
- Visualización en formato tabular (DataFrame).

### 3. Búsqueda Exhaustiva (Óptima)

- Explora todas las permutaciones posibles.
- Muestra logs detallados de cada nuevo récord encontrado.
- **Animación solo al ejecutar**: La animación se muestra únicamente al presionar el botón de ejecución.
- **Gráfico estático en reruns**: En navegaciones posteriores, se muestra solo el resultado final sin volver a animar.
- Métricas: distancia óptima y tiempo de ejecución.

### 4. Vecino Más Cercano (Heurística)

- Construcción greedy de la ruta.
- Logs paso a paso de las decisiones tomadas.
- **Animación solo al ejecutar**: La animación se muestra únicamente al presionar el botón de ejecución.
- **Gráfico estático en reruns**: En navegaciones posteriores, se muestra solo el resultado final sin volver a animar.
- Métricas: distancia heurística y tiempo de ejecución.

### 5. Comparación y Análisis

- **Sin animaciones**: Utiliza solo los resultados ya calculados.
- Tabla comparativa de ambos métodos.
- Cálculo del gap de optimalidad (% de desviación).
- Factor de velocidad (cuántas veces más rápido es el heurístico).
- Gráfico superpuesto con ambas rutas (estático).
- Análisis automático con recomendaciones.

## 📁 Estructura del Proyecto

```
tsp_gui/
│
├── main.py                      # Punto de entrada de la aplicación
│
├── core/                        # Núcleo de la aplicación
│   ├── __init__.py
│   ├── state.py                 # Gestión del estado (session_state)
│   └── processing.py            # Procesamiento y orquestación de algoritmos
│
├── logic/                       # Lógica de negocio (algoritmos TSP)
│   ├── __init__.py
│   ├── data.py                  # Datos de ciudades y coordenadas
│   ├── distance.py              # Cálculo de distancias y matriz
│   ├── exhaustive.py            # Búsqueda exhaustiva
│   ├── nearest_neighbor.py      # Heurística de Vecino Más Cercano
│   ├── graphics.py              # Generación de gráficos con Plotly
│   └── animation.py             # Animaciones paso a paso
│
├── components/                  # Capa de presentación
│   ├── __init__.py
│   ├── content.py               # Estilos CSS y componentes HTML
│   ├── information.py           # Cajas de info, alertas y métricas
│   └── app.py                   # Renderizado de secciones de la app
│
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

### Descripción de Carpetas

#### `core/`

Contiene la lógica central de la aplicación:

- **`state.py`**: Maneja el estado de la aplicación usando `st.session_state`. Incluye funciones para:

  - Inicializar el estado.
  - Guardar y recuperar resultados de algoritmos.
  - Gestionar logs de ejecución.

- **`processing.py`**: Orquesta la ejecución de algoritmos y prepara datos para visualización:
  - Ejecuta búsqueda exhaustiva y vecino más cercano.
  - Genera DataFrames para tablas.
  - Crea gráficos comparativos.
  - Calcula métricas (gap, factor de velocidad).

#### `logic/`

Implementa los algoritmos del TSP:

- **`data.py`**: Define las ciudades y sus coordenadas.
- **`distance.py`**: Calcula distancias euclidianas y construye la matriz.
- **`exhaustive.py`**: Implementa la búsqueda exhaustiva (fuerza bruta).
- **`nearest_neighbor.py`**: Implementa la heurística greedy.
- **`graphics.py`**: Genera gráficos interactivos con Plotly.
- **`animation.py`**: Maneja las animaciones paso a paso.

#### `components/`

Capa de presentación y diseño:

- **`content.py`**: Define estilos CSS globales y componentes HTML reutilizables:

  - `inject_global_styles()`: CSS del tema oscuro.
  - `Header()`, `SectionCities()`, etc.: Secciones HTML.
  - `InfoBox()`, `AlertBox()`, `MetricCard()`: Componentes visuales.

- **`information.py`**: Wrapper de componentes para información contextual:

  - Cajas de información (info boxes).
  - Alertas (success, warning, error).
  - Tarjetas de métricas.

- **`app.py`**: Renderiza cada sección de la aplicación:
  - `render_seccion_ciudades()`
  - `render_seccion_matriz()`
  - `render_seccion_exhaustiva()`
  - `render_seccion_vecino()`
  - `render_seccion_comparacion()`

## 🔧 Requisitos

### Software

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias

Las dependencias se encuentran en `requirements.txt`:

```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
```

## 📦 Instalación

### 1. Clonar el repositorio (o navegar a la carpeta)

```bash
cd tsp_gui
```

### ejecucion rapida

```bash
 streamlit run main.py
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
streamlit run main.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado (por defecto en `http://localhost:8501`).

### Flujo de Uso Recomendado

1. **Explorar Ciudades**: Revisa la tabla de coordenadas y el mapa de puntos.

2. **Ver Matriz de Distancias**: Observa las distancias calculadas entre todas las ciudades.

3. **Ejecutar Búsqueda Exhaustiva**:

   - Presiona el botón "▶ Ejecutar Búsqueda Exhaustiva".
   - Observa la animación del proceso (se muestra solo una vez).
   - Revisa los logs detallados y las métricas.
   - En navegaciones posteriores, verás solo el gráfico final sin animación.

4. **Ejecutar Vecino Más Cercano**:

   - Presiona el botón "▶ Ejecutar Vecino Más Cercano".
   - Observa cómo se construye la ruta paso a paso (animación única).
   - Revisa los logs y métricas.
   - En navegaciones posteriores, verás solo el gráfico final sin animación.

5. **Comparar Resultados**:
   - Ve a la sección de "Comparación y Análisis".
   - Presiona "▶ Mostrar Comparación".
   - Si falta ejecutar algún algoritmo, se te notificará.
   - Analiza la tabla comparativa, métricas y gráfico superpuesto (sin animaciones).
   - Lee las conclusiones y recomendaciones.

## 🏗️ Arquitectura

La aplicación sigue una arquitectura de tres capas:

```
┌─────────────────────────────────────────┐
│         PRESENTACIÓN (UI)               │
│  components/app.py                      │
│  components/content.py                  │
│  components/information.py              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         LÓGICA DE APLICACIÓN            │
│  core/processing.py                     │
│  core/state.py                          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         LÓGICA DE NEGOCIO               │
│  logic/exhaustive.py                    │
│  logic/nearest_neighbor.py              │
│  logic/graphics.py                      │
│  logic/animation.py                     │
│  logic/distance.py                      │
│  logic/data.py                          │
└─────────────────────────────────────────┘
```

### Principios de Diseño

- **Separación de Responsabilidades**: Cada módulo tiene una función clara y específica.
- **Reutilización**: Los componentes visuales (InfoBox, AlertBox, etc.) son reutilizables.
- **Estado Centralizado**: Todo el estado de la aplicación se maneja en `core/state.py`.
- **Modularidad**: Fácil agregar nuevos algoritmos o secciones sin modificar código existente.

## 🧩 Componentes Principales

### 1. main.py

Punto de entrada de la aplicación. Orquesta el flujo principal:

```python
# Configuración de página
st.set_page_config(...)

# Inicializar estado
init_state()

# Inyectar estilos
st.markdown(inject_global_styles(), unsafe_allow_html=True)

# Renderizar secciones
render_seccion_ciudades()
render_seccion_matriz()
render_seccion_exhaustiva(matriz)
render_seccion_vecino(matriz)
render_seccion_comparacion(matriz)
```

### 2. core/state.py

Gestiona el estado de la aplicación:

```python
# Inicializar estado
def init_state()

# Logs
def append_log_ex(msg)
def clear_logs_ex()
def get_logs_ex()

# Resultados
def set_resultado_ex(ruta, dist, tiempo, historial)
def get_resultado_ex()
```

### 3. core/processing.py

Funciones de alto nivel para procesamiento:

```python
# Obtener datos
def get_coordenadas_dataframe()
def get_matriz_distancias()
def get_mapa_puntos()

# Ejecutar algoritmos
def ejecutar_busqueda_exhaustiva(matriz, logger)
def ejecutar_vecino_mas_cercano(matriz, inicio, logger)

# Análisis
def crear_dataframe_comparativo(...)
def calcular_gap(dist_ex, dist_nn)
def get_grafico_comparativo(...)
```

### 4. logic/exhaustive.py

Implementación de la búsqueda exhaustiva:

```python
def busqueda_exhaustiva(matriz_dist, logger=None):
    """
    Explora todas las permutaciones posibles.

    Args:
        matriz_dist: Matriz de distancias (numpy array)
        logger: Función opcional para logging

    Returns:
        tuple: (mejor_ruta, mejor_dist, historial)
    """
    # Implementación...
```

### 5. logic/nearest_neighbor.py

Implementación del vecino más cercano:

```python
def vecino_mas_cercano(matriz_dist, inicio=0, logger=None):
    """
    Construye ruta greedy seleccionando el vecino más cercano.

    Args:
        matriz_dist: Matriz de distancias
        inicio: Índice de ciudad inicial
        logger: Función opcional para logging

    Returns:
        tuple: (ruta, dist_total, historial)
    """
    # Implementación...
```

### 6. logic/graphics.py

Generación de gráficos con Plotly:

```python
# Constantes de estilo
GRAPH_WIDTH = 1150
GRAPH_HEIGHT = 700
TITULO_FS = 16
EJES_FS = 14
CIUDADES_FS = 14
LEYENDA_FS = 12

# Funciones principales
def dibujar_grafo_completo(fig, ciudades, color_arista='#cccccc')
def resaltar_ruta(fig, ruta_idxs, color='red', ancho=3, etiqueta=None)
def grafico_solo_puntos_fig()
def comparativa_fig(ruta_ex, dist_ex, ruta_nn, dist_nn)
```

### 7. logic/animation.py

Animaciones paso a paso:

```python
def animar_historial(
    historial,
    titulo,
    placeholder=None,
    sleep=0.8,
    es_exhaustivo=False,
    logger=None
):
    """
    Anima el proceso de construcción de ruta.

    Args:
        historial: Lista de pasos (rutas parciales o records)
        titulo: Título de la animación
        placeholder: st.empty() para actualizar
        sleep: Tiempo entre frames (segundos)
        es_exhaustivo: True si es búsqueda exhaustiva
        logger: Función opcional para logging
    """
    # Implementación...
```

### 8. components/content.py

Componentes visuales reutilizables:

```python
# Estilos globales
def inject_global_styles() -> str

# Secciones
def Header() -> str
def SectionCities() -> str
def SectionDistanceMatrix() -> str
def SectionExhaustiveSolution() -> str
def SectionNNSolution() -> str
def SectionComparison() -> str

# Componentes
def InfoBox(title, content, color="#32d5c9") -> str
def AlertBox(message, alert_type="info") -> str
def MetricCard(label, value, unit="", color="#60a5fa") -> str
def footer() -> str
```

### 9. components/app.py

Renderizado de secciones completas:

```python
def render_seccion_ciudades():
    """Renderiza tabla de coordenadas y mapa de puntos."""

def render_seccion_matriz():
    """Renderiza matriz de distancias."""

def render_seccion_exhaustiva(matriz):
    """Renderiza controles, resultados y animación de búsqueda exhaustiva."""

def render_seccion_vecino(matriz):
    """Renderiza controles, resultados y animación de vecino más cercano."""

def render_seccion_comparacion(matriz):
    """Renderiza comparación completa con métricas y análisis."""
```

## 🔄 Flujo de Datos

### 1. Inicialización

```
main.py
  ├─> init_state()                    # Inicializa session_state
  ├─> inject_global_styles()          # Inyecta CSS
  └─> Header()                        # Renderiza header
```

### 2. Ejecución de Algoritmo (Ejemplo: Exhaustiva)

```
Usuario presiona botón (ejecutar_ex = True)
│
├─> clear_logs_ex() # Limpia logs anteriores
│
├─> ejecutar_busqueda_exhaustiva()
│ ├─> construir_matriz_distancias()
│ ├─> busqueda_exhaustiva()
│ │ └─> append_log_ex() # Logs en tiempo real
│ └─> return (ruta, dist, tiempo, historial)
│
├─> set_resultado_ex() # Guarda en session_state
│
├─> st.success() # Notifica al usuario
│
└─> animar_historial() # Animación SOLO en esta ejecución
└─> placeholder_ex.plotly_chart()

En reruns posteriores (ejecutar_ex = False):
│
├─> get_resultado_ex() # Recupera resultados guardados
│
└─> Mostrar gráfico estático final
├─> crear figura Plotly
├─> dibujar_grafo_completo()
├─> resaltar_ruta()
└─> placeholder_ex.plotly_chart() # Sin animación
```

### 3. Animación (Solo al Ejecutar)

```
render_seccion_exhaustiva()
│
├─> placeholder_ex = st.empty() # Un solo contenedor
│
├─> get_resultado_ex() # Recupera resultados
│
├─> if resultado_ex AND ejecutar_ex:
│ └─> animar_historial() # Animar SOLO al presionar botón
│ ├─> for paso in historial:
│ │ ├─> crear figura Plotly
│ │ ├─> dibujar_grafo_completo()
│ │ ├─> resaltar_ruta()
│ │ ├─> placeholder_ex.plotly_chart()
│ │ └─> time.sleep()
│ └─> Último frame queda visible
│
└─> elif resultado_ex: # Reruns posteriores
└─> Mostrar gráfico estático final
└─> placeholder_ex.plotly_chart() # Sin animación
```

### 4. Comparación (Sin Animaciones)

```
render_seccion_comparacion()
│
├─> get_resultado_ex() # Recupera resultados guardados
├─> get_resultado_nn() # Recupera resultados guardados
│
├─> Si falta alguno:
│ └─> Mostrar advertencia (NO ejecuta automáticamente)
│
├─> Si ambos existen y se presiona botón:
│ ├─> crear_dataframe_comparativo()
│ ├─> calcular_gap()
│ ├─> get_grafico_comparativo() # Gráfico estático
│ │
│ └─> Renderizar:
│ ├─> Tabla comparativa
│ ├─> Métricas (gap, factor velocidad)
│ ├─> Gráfico superpuesto (SIN animación)
│ └─> Conclusiones
│
└─> Nota: NUNCA llama a animar_historial()
```

## 🎨 Personalización

### Cambiar Ciudades

Edita `logic/data.py`:

```python
coordenadas = {
    "Nueva York": (40.670, -73.940),
    "Los Ángeles": (34.110, -118.410),
    "Chicago": (41.840, -87.680),
    "Houston": (29.7407, -95.4636),
    "Phoenix": (33.540, -112.070),
    "Filadelfia": (40.010, -75.130),
    "San Antonio": (29.460, -98.510),
    # "San Diego": (32.715, -117.161),
    # "Dallas": (32.779, -96.808)
}
```

### Ajustar Tamaños de Gráficos

Edita `logic/graphics.py`:

```python
GRAPH_WIDTH = 1150   # Ancho en píxeles
GRAPH_HEIGHT = 700   # Alto en píxeles
```

### Modificar Tamaños de Fuente

Edita `logic/graphics.py`:

```python
TITULO_FS = 16      # Título del gráfico
EJES_FS = 14        # Etiquetas de ejes
CIUDADES_FS = 14    # Nombres de ciudades
LEYENDA_FS = 12     # Texto de leyenda
```

### Cambiar Colores del Tema

Edita `components/content.py` en la sección `GLOBAL_CSS`:

```css
/* Colores principales */
background: #0b1220; /* Fondo general */
color: #e6eef8; /* Texto principal */
border: rgba(255, 255, 255, 0.04); /* Bordes */
```

### Velocidad de Animaciones

Al llamar `animar_historial()`, ajusta el parámetro `sleep`:

```python
animar_historial(
    historial,
    titulo,
    placeholder=placeholder,
    sleep=0.5,  # Más rápido (0.5s entre frames)
    es_exhaustivo=True
)
```

### Agregar Nuevos Algoritmos

1. **Crear módulo en `logic/`:**

```python
# logic/mi_algoritmo.py
def mi_algoritmo(matriz_dist, logger=None):
    # Implementación
    return ruta, distancia, historial
```

2. **Agregar función en `core/processing.py`:**

```python
def ejecutar_mi_algoritmo(matriz, logger):
    t0 = time.perf_counter()
    ruta, dist, hist = mi_algoritmo(matriz, logger=logger)
    t1 = time.perf_counter()
    return ruta, dist, t1-t0, hist
```

3. **Crear sección en `components/app.py`:**

```python
def render_seccion_mi_algoritmo(matriz):
    # Similar a render_seccion_exhaustiva()
    pass
```

4. **Agregar en `main.py`:**

```python
render_seccion_mi_algoritmo(matriz)
```

## 🐛 Troubleshooting

### La aplicación no inicia

**Problema:** Error al ejecutar `streamlit run main.py`

**Solución:**

- Verifica que el entorno virtual esté activado.
- Reinstala dependencias: `pip install -r requirements.txt`
- Verifica la versión de Python: `python --version` (debe ser 3.8+)

### Los gráficos no se muestran correctamente

**Problema:** Gráficos cortados o con tamaño incorrecto

**Solución:**

- Asegúrate de usar `use_container_width=False` en `st.plotly_chart()`.
- Verifica que `GRAPH_WIDTH` y `GRAPH_HEIGHT` estén definidos en `logic/graphics.py`.
- Añade `autosize=False` en `fig.update_layout()`.

### Las animaciones son muy lentas/rápidas

**Problema:** Velocidad de animación no adecuada

**Solución:**
Ajusta el parámetro `sleep` en las llamadas a `animar_historial()`:

- Más lento: `sleep=1.5`
- Más rápido: `sleep=0.3`

### Los logs no se muestran

**Problema:** Los logs de ejecución están vacíos

**Solución:**

- Verifica que estés pasando el logger a las funciones:

```python
busqueda_exhaustiva(matriz, logger=append_log_ex)
```

- Asegúrate de que `init_state()` se llame al inicio de `main.py`.

### Error: "module not found"

**Problema:** Python no encuentra los módulos

**Solución:**

- Asegúrate de estar en la carpeta `tsp_gui/` al ejecutar.
- Verifica que existan archivos `__init__.py` en `core/`, `logic/` y `components/`.
- Si persiste, añade al inicio de `main.py`:

```python
import sys
sys.path.insert(0, '.')
```

### La comparación no muestra resultados

**Problema:** La sección de comparación está vacía

**Solución:**

- Ejecuta primero "Búsqueda Exhaustiva" y "Vecino Más Cercano".
- O presiona "▶ Ejecutar Comparación" que ejecutará automáticamente lo que falte.

### Problemas de rendimiento con muchas ciudades

**Problema:** La búsqueda exhaustiva tarda demasiado

**Solución:**

- La búsqueda exhaustiva tiene complejidad O(n!), no es escalable.
- Para más de 10 ciudades, considera solo usar el heurístico.
- O implementa algoritmos más avanzados (2-opt, Simulated Annealing, Genetic Algorithms).

## 📚 Referencias

### Documentación de Librerías

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/docs/)
- [NumPy](https://numpy.org/doc/)

### Problema del Viajante (TSP)

- [Wikipedia - TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- [Nearest Neighbor Algorithm](https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm)

## 📝 Notas Adicionales

### Complejidad de Algoritmos

- **Búsqueda Exhaustiva**: O(n!) - No escalable, solo para demostración con pocas ciudades.
- **Vecino Más Cercano**: O(n²) - Rápido pero no garantiza solución óptima.

### Mejoras Futuras

- [ ] Agregar más algoritmos (2-opt, Simulated Annealing, Genetic Algorithm).
- [ ] Permitir carga de ciudades desde archivo CSV.
- [ ] Exportar resultados a PDF/Excel.
- [ ] Modo de comparación múltiple (más de 2 algoritmos).
- [ ] Visualización 3D con altitud.
- [ ] Soporte para distancias reales (usando APIs de mapas).

### Contribuciones

Si deseas contribuir:

- Mantén la estructura modular.
- Documenta todas las funciones con docstrings.
- Sigue el estilo de código existente.
- Prueba exhaustivamente antes de integrar.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

Desarrollado como proyecto educativo para visualización de algoritmos del TSP.

## 🙏 Agradecimientos

- **Streamlit** por su excelente framework de aplicaciones web.
- **Plotly** por sus gráficos interactivos.
- La comunidad de **Python** por las herramientas de ciencia de datos.
