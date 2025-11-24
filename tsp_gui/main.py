import streamlit as st
from components.content import inject_global_styles, Header, footer
from core.app import (
    render_seccion_ciudades,
    render_seccion_matriz,
    render_seccion_exhaustiva,
    render_seccion_vecino,
    render_seccion_comparacion,
)
from core.state import init_state

# ------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ------------------------------------------------------
st.set_page_config(
    page_title="TSP - Problema del Viajante",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estado
init_state()

# Inyectar estilos (hacerlo una vez)
st.markdown(inject_global_styles(), unsafe_allow_html=True)

# Header
st.markdown(Header(), unsafe_allow_html=True)

# Contenedor principal
with st.container():
    # Sección 1
    render_seccion_ciudades()
    st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)

    # Sección 2
    matriz = render_seccion_matriz()
    st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)

    # Sección 3
    render_seccion_exhaustiva(matriz)
    st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)

    # Sección 4
    render_seccion_vecino(matriz)
    st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)

    # Sección 5
    render_seccion_comparacion(matriz)

# Footer
st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)
st.markdown(footer(), unsafe_allow_html=True)
