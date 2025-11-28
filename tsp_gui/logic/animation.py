import time
import plotly.graph_objects as go
import streamlit as st
from .graphics import dibujar_grafo_completo, resaltar_ruta, GRAPH_WIDTH, GRAPH_HEIGHT, EJES_FS
from .data import coordenadas, nombres_ciudades

def animar_historial(
    historial,
    titulo,
    placeholder=None,
    sleep=0.5,
    es_exhaustivo=False,
    logger=None
):
    """
    Muestra la animación actualizando `placeholder` (que debe ser st.empty()).
    - historial:
        * NN: lista de rutas parciales [ [0,3], [0,3,1], ... ]
        * Exhaustivo: lista de (ruta, dist) cuando hay nuevo record
    - sleep: tiempo entre pasos (segundos).
    - es_exhaustivo: True si cada paso es (ruta, dist)
    - logger: callable opcional para anotar logs
    """
    if placeholder is None:
        placeholder = st.empty()

    ciudades = [coordenadas[name] for name in nombres_ciudades]

    # Precalcular límites para que no cambien entre frames
    lats = [c[0] for c in ciudades]
    lons = [c[1] for c in ciudades]
    margin = 2  # Margen más grande para mejor visualización
    x_min, x_max = min(lons) - margin, max(lons) + margin
    y_min, y_max = min(lats) - margin, max(lats) + margin

    for i, paso in enumerate(historial):
        # permitir detener la animación desde la UI
        if st.session_state.get('animation_stop', False):
            if logger:
                logger("Animación detenida por el usuario.")
            break

        # Crear figura de Plotly nueva en cada iteración
        fig = go.Figure()

        # Dibujar grafo completo (todas las aristas y nodos)
        dibujar_grafo_completo(fig, ciudades)

        # Añadir ruta del paso actual
        if es_exhaustivo:
            ruta, dist = paso
            etiqueta = f"Record {dist:.4f}"
            color = "red"
        else:
            ruta = paso
            etiqueta = f"Construcción NN (paso {i+1})"
            color = "green"

        # Para que se note aún más el cambio, línea gruesa y marcadores grandes
        resaltar_ruta(fig, ruta, color=color, ancho=5, etiqueta=etiqueta)

        # Fijar siempre el mismo rango y tamaño para evitar "saltos" de zoom
        fig.update_layout(
            title=dict(
                text=f"{titulo} (Paso {i+1}/{len(historial)})",
                font=dict(size=16)
            ),
            xaxis=dict(
                title=dict(text="Longitud (lon)", font=dict(size=EJES_FS)),
                showgrid=False,
                range=[x_min, x_max],
                fixedrange=True  # Evita que el usuario haga zoom
            ),
            yaxis=dict(
                title=dict(text="Latitud (lat)", font=dict(size=EJES_FS)),
                showgrid=False,
                range=[y_min, y_max],
                fixedrange=True  # Evita que el usuario haga zoom
            ),
            width=GRAPH_WIDTH,
            height=GRAPH_HEIGHT,
            hovermode='closest',
            showlegend=True,
            autosize=False  # Importante: desactiva el autosize
        )

        # Muy importante: use_container_width=False para respetar width/height
        placeholder.plotly_chart(fig, use_container_width=False)

        time.sleep(sleep)

    # limpiar flag de stop para futuras ejecuciones
    st.session_state['animation_stop'] = False