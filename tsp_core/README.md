# TSP Core – Algoritmos y Visualización en Consola

Este módulo contiene la implementación **"código bruto"** del Problema del Viajante (TSP), con:

- Algoritmos de **búsqueda exhaustiva** (óptima) y **Vecino Más Cercano** (heurístico).
- Cálculo de matriz de distancias.
- Gráficos y animaciones con **Matplotlib**.
- Resumen comparativo en consola.

Es la base algorítmica sobre la que se apoya la interfaz gráfica (`tsp_gui`), pero puede ejecutarse de forma independiente desde la terminal.

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Módulos y Funciones](#-módulos-y-funciones)
- [Flujo de Ejecución](#-flujo-de-ejecución)
- [Personalización](#-personalización)
- [Troubleshooting](#-troubleshooting)
- [Notas sobre Complejidad](#-notas-sobre-complejidad)
- [Mejoras Futuras](#-mejoras-futuras)

---

## 🎯 Descripción General

`tsp_core` implementa el Problema del Viajante en una versión **orientada a consola y gráficos con Matplotlib**, sin interfaz web.

El flujo principal:

1. Muestra un **mapa de ciudades** (solo puntos).
2. Construye y muestra la **matriz de distancias**.
3. Ejecuta:
   - **Búsqueda exhaustiva** para encontrar la ruta óptima.
   - **Vecino Más Cercano** como heurística rápida.
4. Imprime un **resumen comparativo** (tiempo y distancia) en la consola.
5. Permite ver **animaciones paso a paso** de ambos algoritmos.
6. Muestra un **gráfico final comparativo** con ambas rutas superpuestas.

---

## ✨ Características

- Cálculo de distancias euclidianas entre ciudades.
- Matriz de distancias legible en consola.
- Algoritmo de fuerza bruta (exhaustivo) con logs de récords.
- Algoritmo heurístico (Vecino Más Cercano) con trazas detalladas.
- Gráficos con Matplotlib:
  - Mapa de puntos.
  - Animación paso a paso.
  - Comparación final de rutas.
- Código modular y documentado.

---

## 📁 Estructura del Proyecto

```
tsp_core/
│
├── tsp_grafo_combinado.py   # Programa principal (main)
├── data.py                  # Datos de ciudades y coordenadas
├── distance.py              # Cálculo de distancias y matriz
├── exhaustive.py            # Búsqueda exhaustiva (óptima)
├── nearest_neighbor.py      # Heurística Vecino Más Cercano
├── graphics.py              # Gráficos con Matplotlib
└── animation.py             # Animaciones paso a paso
```

### Resumen de módulos

#### `tsp_grafo_combinado.py`

Orquesta el flujo completo: gráficos iniciales, ejecución de algoritmos, resumen y animaciones.

#### `data.py`

Define las ciudades y sus coordenadas.

#### `distance.py`

Calcula distancias y construye la matriz de distancias.

#### `exhaustive.py`

Implementa el algoritmo de búsqueda exhaustiva para encontrar la ruta óptima.

#### `nearest_neighbor.py`

Implementa la heurística greedy de vecino más cercano.

#### `graphics.py`

Maneja la visualización de grafos y rutas con Matplotlib.

#### `animation.py`

Implementa animaciones paso a paso usando Matplotlib interactivo.

---

## 🔧 Requisitos

### Software

- Python 3.8 o superior

### Dependencias principales

En tu `requirements.txt` (o instala manualmente):

```
matplotlib>=3.7.0
numpy>=1.24.0
```

---

## 📦 Instalación

Desde la carpeta raíz del proyecto:

```bash
cd tsp_core
```

### (Opcional pero recomendado) Crear entorno virtual

```bash
python -m venv venv
```

**Activar:**

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

(o bien instalar solo matplotlib y numpy si lo prefieres)

---

## 🚀 Uso

Ejecutar el programa principal:

```bash
python tsp_grafo_combinado.py
```

### Flujo de ejecución:

1. Se abre una ventana con el **mapa de puntos** (ciudades sin conexiones).
2. En consola se muestra la **matriz de distancias**.
3. Se ejecuta:
   - **Búsqueda Exhaustiva** (se imprime progreso y récords).
   - **Vecino Más Cercano** (se imprime paso a paso).
4. Se imprime una **tabla comparativa** de tiempos y distancias.
5. En la terminal:
   - Se te pedirá: `Presiona ENTER para ver la animación del Vecino Más Cercano...`
   - Luego: `Presiona ENTER para ver la animación del Exhaustivo (records)...`
6. Finalmente se muestra el **gráfico comparativo** con ambas rutas.

---

## 🧩 Módulos y Funciones

### `data.py`

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

nombres_ciudades = list(coordenadas.keys())
n = len(nombres_ciudades)
```

**Variables:**

- `coordenadas`: diccionario `{nombre: (lat, lon)}`.
- `nombres_ciudades`: lista ordenada de nombres.
- `n`: cantidad de ciudades.

---

### `distance.py`

```python
def distancia_euclidiana(c1_idx, c2_idx):
    """Distancia euclidiana entre las ciudades con índices c1_idx y c2_idx."""
    ...

def construir_matriz_distancias():
    """Construye y retorna la matriz simétrica n x n de distancias."""
    ...

def mostrar_matriz_bonita(matriz):
    """Imprime la matriz de distancias en formato tabular legible."""
    ...
```

**Responsabilidades:**

- Calcular distancia entre dos ciudades por índice.
- Construir matriz de distancias como `numpy.ndarray`.
- Imprimir la matriz con encabezados alineados y valores formateados.

---

### `exhaustive.py`

```python
def busqueda_exhaustiva(matriz_dist):
    """
    Búsqueda exhaustiva de la mejor ruta TSP.

    Recorre todas las permutaciones posibles (fuerza bruta),
    imprime cada vez que encuentra un nuevo récord y
    guarda el historial de récords.

    Args:
        matriz_dist: matriz de distancias (numpy.ndarray)

    Returns:
        tuple: (mejor_ruta, mejor_dist, historial)
            - mejor_ruta: lista de índices (incluye retorno al inicio)
            - mejor_dist: distancia total de esa ruta
            - historial: lista de pares (ruta, dist) cuando hay nuevo récord
    """
    ...
```

**Características:**

- Complejidad factorial O((n-1)!).
- Imprime:
  - Número total de rutas a evaluar.
  - Cada nuevo récord con su distancia y ruta.
- Devuelve:
  - Ruta óptima.
  - Distancia mínima.
  - Historial de récords (para animación).

---

### `nearest_neighbor.py`

```python
def vecino_mas_cercano(matriz_dist, inicio=0):
    """
    Heurística del Vecino Más Cercano.

    Args:
        matriz_dist: matriz de distancias
        inicio: índice de ciudad inicial (por defecto 0)

    Returns:
        tuple: (ruta, dist_total, historial)
            - ruta: lista de índices con ciudad inicial al final
            - dist_total: distancia total recorrida
            - historial: lista de rutas parciales para animación
    """
    ...
```

**Características:**

- Selecciona iterativamente el vecino no visitado más cercano.
- Imprime en consola:
  - Ciudad actual.
  - Distancia a cada candidato.
  - Decisión final en cada paso.
- Devuelve:
  - Ruta heurística (incluyendo retorno al inicio).
  - Distancia total.
  - Historial de rutas parciales.

---

### `graphics.py`

```python
# Constantes de estilo
TITULO_FS = 16
EJES_FS = 15
CIUDADES_FS = 16
LEYENDA_FS = 12

def dibujar_grafo_completo(ax, ciudades, color_arista='#cccccc'):
    """Dibuja todas las aristas, nodos y etiquetas en el eje ax."""
    ...

def resaltar_ruta(ax, ruta_idxs, color='red', ancho=3, etiqueta=None):
    """Dibuja una ruta específica sobre el eje ax."""
    ...

def grafico_solo_puntos():
    """Muestra un gráfico con únicamente los puntos (ciudades)."""
    ...
```

**Responsabilidades:**

- Dibujar grafo completo (todas las aristas) en gris.
- Dibujar nodos (ciudades) y sus etiquetas.
- Resaltar rutas con color y ancho configurables.
- Mostrar mapa simple de puntos.

---

### `animation.py`

```python
def animar_historial(historial, titulo, velocidad=0.8, es_exhaustivo=False):
    """
    Anima el historial de rutas paso a paso con Matplotlib interactivo.

    Args:
        historial:
            - Exhaustivo: lista de (ruta, dist)
            - NN: lista de rutas parciales
        titulo: título de la ventana/figura
        velocidad: pausa entre pasos (segundos)
        es_exhaustivo: True si historial es de récords exhaustivos
    """
    ...
```

**Comportamiento:**

- Usa `plt.ion()` para modo interactivo.
- En cada frame:
  - Limpia el eje.
  - Dibuja el grafo completo.
  - Resalta la ruta parcial o récord actual.
  - Actualiza título con el número de paso.
- Al final, desactiva modo interactivo y muestra la figura.

---

### `tsp_grafo_combinado.py` (main)

```python
def main():
    print("\nMostrando gráfico de puntos (sin conexiones)...")
    grafico_solo_puntos()

    matriz = construir_matriz_distancias()
    mostrar_matriz_bonita(matriz)

    # 1) Exhaustivo
    ruta_ex, dist_ex, hist_ex, tiempo_ex = ...

    # 2) Vecino Más Cercano
    ruta_nn, dist_nn, hist_nn, tiempo_nn = ...

    # Resumen en consola
    ...

    # Animaciones (con input para avanzar)
    ...

    # Gráfico final comparativo
    ...
```

**Responsable de:**

- Coordinar todo el flujo.
- Medir tiempos de ejecución (`time.time()`).
- Mostrar resumen comparativo:
  - Método
  - Tiempo (s)
  - Distancia total
- Calcular y mostrar el gap de optimalidad.
- Lanzar animaciones y gráfico final.

---

## 🔄 Flujo de Ejecución

```
main()
 ├─ grafico_solo_puntos()
 ├─ matriz = construir_matriz_distancias()
 ├─ mostrar_matriz_bonita(matriz)
 ├─ (ruta_ex, dist_ex, hist_ex) = busqueda_exhaustiva(matriz)
 ├─ (ruta_nn, dist_nn, hist_nn) = vecino_mas_cercano(matriz)
 ├─ imprimir tabla comparativa en consola
 ├─ input() → animar_historial(hist_nn, ...)
 ├─ input() → animar_historial(hist_ex, ...)
 └─ gráfico final con dibujar_grafo_completo() + resaltar_ruta()
```

---

## 🎨 Personalización

### Cambiar ciudades

Edita `data.py`:

```python
coordenadas = {
    "Ciudad A": (lat, lon),
    "Ciudad B": (lat, lon),
    # ...
}
```

Los nombres se usarán en:

- Encabezados de matriz.
- Etiquetas de nodos y rutas.
- Impresiones en consola.

### Ajustar velocidad de animación

En `animation.py` o al llamar a `animar_historial`:

```python
animar_historial(hist_nn, "Vecino Más Cercano", velocidad=0.5)
animar_historial(hist_ex, "Exhaustivo", velocidad=1.0, es_exhaustivo=True)
```

- Valores más pequeños → animación más rápida.
- Valores mayores → animación más lenta.

### Cambiar tamaños de fuente y figuras

En `graphics.py`:

```python
TITULO_FS = 16
EJES_FS = 15
CIUDADES_FS = 16
LEYENDA_FS = 12
```

En `tsp_grafo_combinado.py` y `animation.py`, ajusta:

```python
fig, ax = plt.subplots(figsize=(8, 8))
```

---

## 🛠 Troubleshooting

### No se muestra ninguna ventana de Matplotlib

**Problema:** Las ventanas de gráficos no aparecen.

**Solución:**

- Asegúrate de no estar ejecutando en un entorno sin soporte gráfico (por ejemplo, WSL sin X, servidor remoto sin display).
- Prueba en un IDE local (VS Code, PyCharm) o ejecutando desde tu sistema operativo directamente.
- Añade al inicio:

```python
  import matplotlib
  print(matplotlib.get_backend())
```

para verificar el backend gráfico.

### El programa se "queda detenido" después de imprimir "Presiona ENTER..."

**Problema:** El programa parece bloqueado.

**Solución:**

- Eso es normal: el programa está esperando que presiones ENTER en la terminal para continuar con la siguiente animación.
- Si estás en un IDE, asegúrate de que el foco esté en la consola y no en la ventana del gráfico.

### La búsqueda exhaustiva tarda mucho

**Problema:** El algoritmo exhaustivo no termina o tarda excesivamente.

**Solución:**

- Recuerda que su complejidad es O((n-1)!).
- Con muchas ciudades el tiempo crece explosivamente.
- Para propósitos educativos, se recomienda usar 7–10 ciudades máximo.

---

## 📈 Notas sobre Complejidad

### Búsqueda Exhaustiva: O((n-1)!)

- Explora todas las rutas posibles (fuerza bruta).
- Óptima pero totalmente no escalable.

### Vecino Más Cercano: O(n²)

- Mucho más rápido, pero no garantiza solución óptima.
- Ideal para comparación con el resultado exhaustivo.

---

## 📚 Referencias

### Documentación de Librerías

- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [NumPy Documentation](https://numpy.org/doc/)

### Problema del Viajante (TSP)

- [Wikipedia - Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- [Nearest Neighbor Algorithm](https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm)

---
