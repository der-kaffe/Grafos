import streamlit as st
import plotly.graph_objects as go
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
from logic.data import coordenadas, nombres_ciudades
from logic.graphics import dibujar_grafo_completo, resaltar_ruta
from core.state import  (
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
        
        # Agregar imagen debajo de la tabla
        st.image(
            "../apoyo_visual/mapa9.png",  # Cambia por la ruta de tu imagen
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
    st.latex(r"d = \sqrt{(lat2 - lat1)^2 + (lon2 - lon1)^2}")

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

        # Botón que ejecuta CON animación
        ejecutar_ex = st.button(
            "▶ Ejecutar Búsqueda Exhaustiva",
            use_container_width=True,
            type="primary",
            key="btn_ejecutar_ex"
        )

        if ejecutar_ex:
            clear_logs_ex()
            with st.spinner("Ejecutando búsqueda exhaustiva..."):
                ruta_ex, dist_ex, tiempo_ex, hist_ex = ejecutar_busqueda_exhaustiva(
                    matriz,
                    logger=append_log_ex
                )
                set_resultado_ex(ruta_ex, dist_ex, tiempo_ex, hist_ex)
            st.success(" Ejecutado: Búsqueda Exhaustiva")

        # Mostrar resultados numéricos si ya existen
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
        # Un solo placeholder que se usará para animación y quedará con el último frame
        placeholder_ex = st.empty()

        if resultado_ex is not None and ejecutar_ex:
            # Solo animar inmediatamente después de pulsar el botón
            _, _, _, hist_ex = resultado_ex
            animar_historial(
                hist_ex,
                "Búsqueda Exhaustiva",
                placeholder=placeholder_ex,
                sleep=1.0,
                es_exhaustivo=True,
                logger=append_log_ex
            )
        elif resultado_ex is not None:
            # Ya hay resultado pero NO se acaba de pulsar el botón → NO animar de nuevo
            # Simplemente mostramos el último estado (ruta óptima) en el placeholder
            ruta_ex, dist_ex, _, _ = resultado_ex

            ciudades = [coordenadas[name] for name in nombres_ciudades]
            fig_final = go.Figure()
            dibujar_grafo_completo(fig_final, ciudades)
            resaltar_ruta(fig_final, ruta_ex, color='red', ancho=4, etiqueta=f"Óptimo ({dist_ex:.4f})")

            lats = [c[0] for c in ciudades]
            lons = [c[1] for c in ciudades]
            margin = 2

            fig_final.update_layout(
                title=dict(text="Ruta Óptima Encontrada", font=dict(size=16)),
                xaxis=dict(
                    title=dict(text="Longitud (lon)", font=dict(size=14)),
                    showgrid=False,
                    range=[min(lons) - margin, max(lons) + margin]
                ),
                yaxis=dict(
                    title=dict(text="Latitud (lat)", font=dict(size=14)),
                    showgrid=False,
                    range=[min(lats) - margin, max(lats) + margin]
                ),
                width=1000,
                height=700,
                hovermode='closest',
                showlegend=True
            )

            placeholder_ex.plotly_chart(fig_final, use_container_width=False)
        else:
            placeholder_ex.markdown(alert_ejecutar_exhaustiva(), unsafe_allow_html=True)

    # Logs detallados
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

        # Botón que ejecuta CON animación
        ejecutar_nn = st.button(
            "▶ Ejecutar Vecino Más Cercano",
            use_container_width=True,
            type="primary",
            key="btn_ejecutar_nn"
        )

        if ejecutar_nn:
            clear_logs_nn()
            with st.spinner("Ejecutando vecino más cercano..."):
                ruta_nn, dist_nn, tiempo_nn, hist_nn = ejecutar_vecino_mas_cercano(
                    matriz,
                    inicio=0,
                    logger=append_log_nn
                )
                set_resultado_nn(ruta_nn, dist_nn, tiempo_nn, hist_nn)
            st.success("Ejecutado: Vecino Más Cercano")

        # Mostrar resultados numéricos si ya existen
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
        # Un solo placeholder que se usará para animación y quedará con el último frame
        placeholder_nn = st.empty()

        if resultado_nn is not None and ejecutar_nn:
            # Solo animar justo después de ejecutar
            _, _, _, hist_nn = resultado_nn
            animar_historial(
                hist_nn,
                "Vecino Más Cercano",
                placeholder=placeholder_nn,
                sleep=1.0,
                es_exhaustivo=False,
                logger=append_log_nn
            )
        elif resultado_nn is not None:
            # Mostrar solo el último estado sin animación
            ruta_nn, dist_nn, _, _ = resultado_nn

            ciudades = [coordenadas[name] for name in nombres_ciudades]
            fig_final = go.Figure()
            dibujar_grafo_completo(fig_final, ciudades)
            resaltar_ruta(fig_final, ruta_nn, color='green', ancho=4, etiqueta=f"NN ({dist_nn:.4f})")

            lats = [c[0] for c in ciudades]
            lons = [c[1] for c in ciudades]
            margin = 2

            fig_final.update_layout(
                title=dict(text="Ruta Heurística Encontrada", font=dict(size=16)),
                xaxis=dict(
                    title=dict(text="Longitud (lon)", font=dict(size=14)),
                    showgrid=False,
                    range=[min(lons) - margin, max(lons) + margin]
                ),
                yaxis=dict(
                    title=dict(text="Latitud (lat)", font=dict(size=14)),
                    showgrid=False,
                    range=[min(lats) - margin, max(lats) + margin]
                ),
                width=1000,
                height=700,
                hovermode='closest',
                showlegend=True
            )

            placeholder_nn.plotly_chart(fig_final, use_container_width=False)
        else:
            placeholder_nn.markdown(alert_ejecutar_vecino(), unsafe_allow_html=True)

    # Logs detallados
    resultado_nn = get_resultado_nn()
    if resultado_nn is not None:
        with st.expander(" Ver logs detallados"):
            st.code("\n".join(get_logs_nn()) or "Sin logs", language="text")


# ------------------------------------------------------
# SECCIÓN 5: COMPARACIÓN Y ANÁLISIS
# ------------------------------------------------------

def render_seccion_comparacion(matriz):
    st.markdown(SectionComparison(), unsafe_allow_html=True)

    # Obtener resultados actuales
    resultado_ex = get_resultado_ex()
    resultado_nn = get_resultado_nn()

    # versiones actuales
    ver_ex = st.session_state.get('resultado_ex_version', 0)
    ver_nn = st.session_state.get('resultado_nn_version', 0)
    ultima_comp = st.session_state.get('ultima_version_comparacion', (0, 0))

    # Botón para mostrar la comparación (sigue existiendo)
    comparar_clicked = st.button("▶ Mostrar Comparación", type="primary", use_container_width=False)

    # Si falta alguno y se hizo click, mostrar advertencia
    if resultado_ex is None or resultado_nn is None:
        if comparar_clicked:
            st.warning(
                "⚠️ **Para comparar necesitas haber ejecutado antes:**\n\n"
                "- La **Búsqueda Exhaustiva**\n"
                "- El **Vecino Más Cercano** \n\n"
                "Por favor, ejecuta ambos algoritmos primero."
            )
        else:
            st.markdown(info_instrucciones_comparacion(), unsafe_allow_html=True)
        return

    # Decidir si debemos mostrar/actualizar la comparación:
    # - si el usuario presionó el botón OR
    # - si las versiones han cambiado desde la última comparación mostrada
    versiones_actuales = (ver_ex, ver_nn)
    should_show = comparar_clicked or (versiones_actuales != ultima_comp)

    if should_show:
        ruta_ex, dist_ex, tiempo_ex, _ = resultado_ex
        ruta_nn, dist_nn, tiempo_nn, _ = resultado_nn

        col_tabla, col_metricas = st.columns([2, 1])

        with col_tabla:
            st.subheader(" 📊 Tabla Comparativa")
            df_resumen = crear_dataframe_comparativo(tiempo_ex, dist_ex, tiempo_nn, dist_nn)
            st.dataframe(df_resumen, use_container_width=True)

        with col_metricas:
            st.subheader(" 📈 Métricas Clave")
            gap = calcular_gap(dist_ex, dist_nn)
            if gap is not None:
                st.markdown(metric_gap_optimalidad(gap), unsafe_allow_html=True)

            factor_velocidad = (tiempo_ex / tiempo_nn) if (tiempo_nn and tiempo_nn > 0) else 0
            st.markdown(metric_factor_velocidad(factor_velocidad), unsafe_allow_html=True)

        st.subheader(" 🔍 Análisis de Resultados")

        gap = calcular_gap(dist_ex, dist_nn)
        if gap is not None:
            if gap < 10:
                st.markdown(alert_analisis_gap_bueno(gap), unsafe_allow_html=True)
            else:
                st.markdown(alert_analisis_gap_alto(gap), unsafe_allow_html=True)

        st.subheader(" 🗺️ Comparación Visual de Rutas")
        fig_comp = get_grafico_comparativo(ruta_ex, dist_ex, ruta_nn, dist_nn)
        st.plotly_chart(fig_comp, use_container_width=False)

        with st.expander(" 📝 Ver conclusiones detalladas"):
            st.markdown(
                conclusiones_detalladas(tiempo_ex, dist_ex, tiempo_nn, dist_nn, gap),
                unsafe_allow_html=True
            )

        # Actualizar la versión de la última comparación mostrada
        st.session_state['ultima_version_comparacion'] = versiones_actuales
    else:
        # Si ya está actualizada y no se pidió mostrar, avisamos
        st.info("✅ La comparación ya está actualizada. Si quieres verla, presiona '▶ Mostrar Comparación'.")