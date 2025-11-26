import streamlit as st
from components.content import (
    SectionCities, SectionDistanceMatrix,
    SectionExhaustiveSolution, SectionNNSolution,
    SectionComparison
)
from components.information import (
    info_calculo_distancias,
    info_instrucciones_comparacion,
    alert_ejecutar_exhaustiva,
    alert_ejecutar_vecino,
    alert_ejecutar_ambos,
    alert_analisis_gap_bueno,
    alert_analisis_gap_alto,
    metric_distancia_exhaustiva,
    metric_tiempo_exhaustiva,
    metric_distancia_vecino,
    metric_tiempo_vecino,
    metric_gap_optimalidad,
    metric_factor_velocidad,
    conclusiones_detalladas,
)
from logic.animation import animar_historial
from core.state import (
    append_log_ex, clear_logs_ex, get_logs_ex,
    get_resultado_ex, set_resultado_ex,
    append_log_nn, clear_logs_nn, get_logs_nn,
    get_resultado_nn, set_resultado_nn
)
from core.processing import (
    get_coordenadas_dataframe,
    get_matriz_distancias,
    get_matriz_distancias_numpy,
    get_mapa_puntos,
    ejecutar_busqueda_exhaustiva,
    ejecutar_vecino_mas_cercano,
    convertir_ruta_a_nombres,
    crear_dataframe_comparativo,
    calcular_gap,
    get_grafico_comparativo
)

# ------------------------------------------------------
# SECCIÓN 1: CIUDADES Y COORDENADAS
# ------------------------------------------------------

def render_seccion_ciudades():
    st.markdown(SectionCities(), unsafe_allow_html=True)

    col_coord1, col_coord2 = st.columns([1, 2])

    with col_coord1:
        st.subheader(" Tabla de Coordenadas")
        df_coordenadas = get_coordenadas_dataframe()
        st.dataframe(df_coordenadas, use_container_width=True)
        
        # ← AQUÍ: Agregar imagen debajo de la tabla
        st.image(
            "../apoyo_visual/mapa(ciudades).png",  # Cambia por la ruta de tu imagen
            use_container_width=True  # Para que ocupe todo el ancho de la columna
        )

    with col_coord2:
        st.subheader(" Visualización del Mapa")
        fig_puntos = get_mapa_puntos()
        st.plotly_chart(fig_puntos, use_container_width=False)


# ------------------------------------------------------
# SECCIÓN 2: MATRIZ DE DISTANCIAS
# ------------------------------------------------------

def render_seccion_matriz():
    st.markdown(SectionDistanceMatrix(), unsafe_allow_html=True)
    st.markdown(info_calculo_distancias(), unsafe_allow_html=True)

    # Mostrar matriz con nombres de ciudades
    df_matriz = get_matriz_distancias()
    st.dataframe(df_matriz, use_container_width=True)

    # Retornar matriz numpy para los algoritmos
    matriz = get_matriz_distancias_numpy()
    return matriz  # importante: se usa en otras secciones


# ------------------------------------------------------
# SECCIÓN 3: BÚSQUEDA EXHAUSTIVA
# ------------------------------------------------------
def render_seccion_exhaustiva(matriz):
    st.markdown(SectionExhaustiveSolution(), unsafe_allow_html=True)

    col_ex_control, col_ex_visual = st.columns([1, 2])

    with col_ex_control:
        st.subheader(" Control de Ejecución")

        if st.button("▶ Ejecutar Búsqueda Exhaustiva", use_container_width=True, type="primary"):
            clear_logs_ex()
            with st.spinner("Ejecutando búsqueda exhaustiva..."):
                ruta_ex, dist_ex, tiempo_ex, hist_ex = ejecutar_busqueda_exhaustiva(
                    matriz,
                    logger=append_log_ex
                )
                set_resultado_ex(ruta_ex, dist_ex, tiempo_ex, hist_ex)
            st.success("Ejecutado: Búsqueda Exhaustiva")

        resultado_ex = get_resultado_ex()
        if resultado_ex is not None:
            ruta_ex, dist_ex, tiempo_ex, hist_ex = resultado_ex
            ruta_ex_nombres = convertir_ruta_a_nombres(ruta_ex)

            st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)
            st.subheader(" Resultados")

            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.markdown(metric_distancia_exhaustiva(dist_ex), unsafe_allow_html=True)
            with metric_col2:
                st.markdown(metric_tiempo_exhaustiva(tiempo_ex), unsafe_allow_html=True)

            st.markdown("** Ruta Óptima:**")
            st.info(" → ".join(ruta_ex_nombres))

    with col_ex_visual:
        st.subheader(" Visualización del Proceso")

        resultado_ex = get_resultado_ex()
        if resultado_ex is not None:
            _, _, _, hist_ex = resultado_ex
            placeholder_ex = st.empty()
            animar_historial(
                hist_ex,
                "Búsqueda Exhaustiva",
                placeholder=placeholder_ex,
                sleep=1.0,
                es_exhaustivo=True,
                logger=append_log_ex
            )
        else:
            st.markdown(alert_ejecutar_exhaustiva(), unsafe_allow_html=True)

    # ← AQUÍ: Fuera de las columnas, logs detallados ocupan todo el ancho
    resultado_ex = get_resultado_ex()
    if resultado_ex is not None:
        with st.expander(" Ver logs detallados"):
            st.code("\n".join(get_logs_ex()) or "Sin logs", language="text")


# ------------------------------------------------------
# SECCIÓN 4: VECINO MÁS CERCANO
# ------------------------------------------------------
def render_seccion_vecino(matriz):
    st.markdown(SectionNNSolution(), unsafe_allow_html=True)

    col_nn_control, col_nn_visual = st.columns([1, 2])

    with col_nn_control:
        st.subheader(" Control de Ejecución")

        if st.button("▶ Ejecutar Vecino Más Cercano", use_container_width=True, type="primary"):
            clear_logs_nn()
            with st.spinner("Ejecutando vecino más cercano..."):
                ruta_nn, dist_nn, tiempo_nn, hist_nn = ejecutar_vecino_mas_cercano(
                    matriz,
                    inicio=0,
                    logger=append_log_nn
                )
                set_resultado_nn(ruta_nn, dist_nn, tiempo_nn, hist_nn)
            st.success("Ejecutado: Vecino Más Cercano")

        resultado_nn = get_resultado_nn()
        if resultado_nn is not None:
            ruta_nn, dist_nn, tiempo_nn, hist_nn = resultado_nn
            ruta_nn_nombres = convertir_ruta_a_nombres(ruta_nn)

            st.markdown("<div class='light-divider'></div>", unsafe_allow_html=True)
            st.subheader(" Resultados")

            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.markdown(metric_distancia_vecino(dist_nn), unsafe_allow_html=True)
            with metric_col2:
                st.markdown(metric_tiempo_vecino(tiempo_nn), unsafe_allow_html=True)

            st.markdown("** Ruta Heurística:**")
            st.info(" → ".join(ruta_nn_nombres))

    with col_nn_visual:
        st.subheader(" Visualización del Proceso")

        resultado_nn = get_resultado_nn()
        if resultado_nn is not None:
            _, _, _, hist_nn = resultado_nn
            placeholder_nn = st.empty()
            animar_historial(
                hist_nn,
                "Vecino Más Cercano",
                placeholder=placeholder_nn,
                sleep=1.0,
                es_exhaustivo=False,
                logger=append_log_nn
            )
        else:
            st.markdown(alert_ejecutar_vecino(), unsafe_allow_html=True)

    # ← AQUÍ: Fuera de las columnas, logs detallados ocupan todo el ancho
    resultado_nn = get_resultado_nn()
    if resultado_nn is not None:
        with st.expander(" Ver logs detallados"):
            st.code("\n".join(get_logs_nn()) or "Sin logs", language="text")


# ------------------------------------------------------
# SECCIÓN 5: COMPARACIÓN Y ANÁLISIS
# ------------------------------------------------------

def render_seccion_comparacion(matriz):
    st.markdown(SectionComparison(), unsafe_allow_html=True)

    # Botón para ejecutar la comparación (ejecuta lo que falte automáticamente)
    if st.button("▶ Ejecutar Comparación", type="primary", use_container_width=False):
        resultado_ex = get_resultado_ex()
        resultado_nn = get_resultado_nn()

        # Ejecutar exhaustiva si no existe
        if resultado_ex is None:
            clear_logs_ex()
            with st.spinner("Ejecutando búsqueda exhaustiva..."):
                ruta_ex, dist_ex, tiempo_ex, hist_ex = ejecutar_busqueda_exhaustiva(
                    matriz,
                    logger=append_log_ex
                )
                set_resultado_ex(ruta_ex, dist_ex, tiempo_ex, hist_ex)
            st.success(" Búsqueda Exhaustiva completada")

        # Ejecutar vecino más cercano si no existe
        if resultado_nn is None:
            clear_logs_nn()
            with st.spinner("Ejecutando vecino más cercano..."):
                ruta_nn, dist_nn, tiempo_nn, hist_nn = ejecutar_vecino_mas_cercano(
                    matriz,
                    inicio=0,
                    logger=append_log_nn
                )
                set_resultado_nn(ruta_nn, dist_nn, tiempo_nn, hist_nn)
            st.success(" Vecino Más Cercano completado")

        st.success(" Comparación lista")
        # Forzar rerun para mostrar los resultados
        st.rerun()

    # Obtener resultados actuales
    resultado_ex = get_resultado_ex()
    resultado_nn = get_resultado_nn()

    # Si no hay resultados, mostrar instrucciones
    if resultado_ex is None or resultado_nn is None:
        st.markdown(info_instrucciones_comparacion(), unsafe_allow_html=True)
        return

    # Si hay resultados, mostrar la comparación
    ruta_ex, dist_ex, tiempo_ex, _ = resultado_ex
    ruta_nn, dist_nn, tiempo_nn, _ = resultado_nn

    col_tabla, col_metricas = st.columns([2, 1])

    with col_tabla:
        st.subheader(" Tabla Comparativa")
        df_resumen = crear_dataframe_comparativo(tiempo_ex, dist_ex, tiempo_nn, dist_nn)
        st.dataframe(df_resumen, use_container_width=True)

    with col_metricas:
        st.subheader(" Métricas Clave")
        gap = calcular_gap(dist_ex, dist_nn)
        if gap is not None:
            st.markdown(metric_gap_optimalidad(gap), unsafe_allow_html=True)

        factor_velocidad = (tiempo_ex / tiempo_nn) if (tiempo_nn and tiempo_nn > 0) else 0
        st.markdown(metric_factor_velocidad(factor_velocidad), unsafe_allow_html=True)

    st.subheader(" Análisis de Resultados")

    gap = calcular_gap(dist_ex, dist_nn)
    if gap is not None:
        if gap < 10:
            st.markdown(alert_analisis_gap_bueno(gap), unsafe_allow_html=True)
        else:
            st.markdown(alert_analisis_gap_alto(gap), unsafe_allow_html=True)

    st.subheader(" Comparación Visual de Rutas")
    fig_comp = get_grafico_comparativo(ruta_ex, dist_ex, ruta_nn, dist_nn)
    st.plotly_chart(fig_comp, use_container_width=False)

    with st.expander(" Ver conclusiones detalladas"):
        st.markdown(
            conclusiones_detalladas(tiempo_ex, dist_ex, tiempo_nn, dist_nn, gap),
            unsafe_allow_html=True
        )