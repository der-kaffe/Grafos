import plotly.graph_objects as go
from .data import coordenadas, nombres_ciudades

# Constantes de estilo (ajustables)
TITULO_FS = 16      # Tamaño de la fuente del TÍTULO de la gráfica
EJES_FS = 14        # Tamaño de la fuente de las ETIQUETAS de los EJES (x / y)
CIUDADES_FS = 14    # Tamaño de la fuente de los NOMBRES de las CIUDADES en el mapa
LEYENDA_FS = 12     # Tamaño de la fuente del TEXTO de la LEYENDA

# Constantes de tamaño de gráficos (ajusta estos valores para cambiar el tamaño)
GRAPH_WIDTH = 1000   # Ancho de los gráficos en píxeles
GRAPH_HEIGHT = 700  # Alto de los gráficos en píxeles

def dibujar_grafo_completo(fig, ciudades, color_arista='#cccccc'):
    """Dibuja todas las conexiones entre ciudades en el grafo."""
    lats = [c[0] for c in ciudades]
    lons = [c[1] for c in ciudades]

    # Dibujar todas las aristas
    for i in range(len(ciudades)):
        for j in range(i + 1, len(ciudades)):
            fig.add_trace(go.Scatter(
                x=[lons[i], lons[j]],
                y=[lats[i], lats[j]],
                mode='lines',
                line=dict(color=color_arista, width=1),
                showlegend=False,
                hoverinfo='skip'
            ))

    # Dibujar puntos de ciudades
    fig.add_trace(go.Scatter(
        x=lons,
        y=lats,
        mode='markers+text',
        marker=dict(color='blue', size=15),
        text=nombres_ciudades,
        textposition='top right',
        textfont=dict(size=CIUDADES_FS),
        showlegend=False,
        hoverinfo='text',
        hovertext=nombres_ciudades
    ))

def resaltar_ruta(fig, ruta_idxs, color='red', ancho=3, etiqueta=None):
    """Resalta una ruta específica en el grafo."""
    lats_r = [coordenadas[nombres_ciudades[i]][0] for i in ruta_idxs]
    lons_r = [coordenadas[nombres_ciudades[i]][1] for i in ruta_idxs]
    
    fig.add_trace(go.Scatter(
        x=lons_r,
        y=lats_r,
        mode='lines+markers',
        line=dict(color=color, width=ancho),
        marker=dict(color=color, size=8),
        name=etiqueta if etiqueta else 'Ruta',
        showlegend=True if etiqueta else False
    ))

def grafico_solo_puntos_fig():
    """Crea un gráfico con solo los puntos de las ciudades."""
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    lats = [c[0] for c in ciudades]
    lons = [c[1] for c in ciudades]

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=lons,
        y=lats,
        mode='markers+text',
        marker=dict(color='blue', size=15),
        text=nombres_ciudades,
        textposition='top right',
        textfont=dict(size=CIUDADES_FS),
        showlegend=False,
        hoverinfo='text',
        hovertext=nombres_ciudades
    ))
    
    fig.update_layout(
        title=dict(text="Mapa de ciudades (sin conexiones)", font=dict(size=TITULO_FS)),
        xaxis=dict(
            title=dict(text="Longitud", font=dict(size=EJES_FS)),
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title=dict(text="Latitud", font=dict(size=EJES_FS)),
            showgrid=True,
            gridcolor='lightgray'
        ),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
        autosize=False,
        hovermode='closest'
    )
    
    return fig

def comparativa_fig(ruta_ex, dist_ex, ruta_nn, dist_nn):
    """Crea un gráfico comparativo con ambas rutas superpuestas."""
    ciudades = [coordenadas[name] for name in nombres_ciudades]
    
    fig = go.Figure()
    
    # Dibujar grafo completo
    dibujar_grafo_completo(fig, ciudades)
    
    # Resaltar ruta exhaustiva
    if ruta_ex is not None:
        resaltar_ruta(fig, ruta_ex, color='red', ancho=3, etiqueta=f"Óptimo ({dist_ex:.4f})")
    
    # Resaltar ruta vecino más cercano
    if ruta_nn is not None:
        resaltar_ruta(fig, ruta_nn, color='green', ancho=2, etiqueta=f"NN ({dist_nn:.4f})")
    
    fig.update_layout(
        xaxis=dict(
            title=dict(text="Longitud (lon)", font=dict(size=EJES_FS)),
            showgrid=False,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title=dict(text="Latitud (lat)", font=dict(size=EJES_FS)),
            showgrid=False,
            gridcolor='lightgray'
        ),
        legend=dict(font=dict(size=LEYENDA_FS), x=1, y=1, xanchor='right', yanchor='top'),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
        autosize=False,
        margin=dict(l=80, r=40, t=80, b=80),
        hovermode='closest'
    )
    
    return fig