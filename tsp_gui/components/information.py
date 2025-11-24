from components.content import InfoBox, AlertBox, MetricCard

# ===== INFO BOXES =====

def info_calculo_distancias():
    return InfoBox(
        "📐 Cálculo de Distancias",
        "Las distancias entre ciudades se calculan mediante la <strong>fórmula euclidiana</strong> usando latitud/longitud como coordenadas.",
        color="#32d5c9"
    )

def info_instrucciones_comparacion():
    return InfoBox(
        "📝 Instrucciones",
        """
        <ul style='margin:0 0 0 1rem; padding:0; line-height:1.6;'>
            <li>Presiona <strong>Ejecutar Búsqueda Exhaustiva</strong></li>
            <li>Luego presiona <strong>Ejecutar Vecino Más Cercano</strong></li>
            <li>Vuelve a la sección de comparación para ver resultados</li>
        </ul>
        """,
        color="#4b5563"
    )

# ===== ALERT BOXES =====

def alert_ejecutar_exhaustiva():
    return AlertBox(
        "Ejecuta <strong>Búsqueda Exhaustiva</strong> para ver la animación del proceso.",
        alert_type="info"
    )

def alert_ejecutar_vecino():
    return AlertBox(
        "Ejecuta <strong>Vecino Más Cercano</strong> para ver su recorrido animado.",
        alert_type="info"
    )

def alert_ejecutar_ambos():
    return AlertBox(
        "Para habilitar la comparación completa, ejecuta <strong>ambos</strong> métodos.",
        alert_type="warning"
    )

def alert_analisis_gap_bueno(gap):
    return AlertBox(
        f"✨ Heurístico cercano a óptimo — gap: <strong>{gap:.2f}%</strong>.",
        alert_type="success"
    )

def alert_analisis_gap_alto(gap):
    return AlertBox(
        f"⚠️ Heurístico más rápido pero gap alto: <strong>{gap:.2f}%</strong>.",
        alert_type="warning"
    )

# ===== METRIC CARDS =====
# retornan HTML para st.markdown(..., unsafe_allow_html=True)

def metric_distancia_exhaustiva(dist_ex):
    return MetricCard("Distancia (Exhaustiva)", f"{dist_ex:.2f}", "km", color="#ff7b7b")

def metric_tiempo_exhaustiva(tiempo_ex):
    return MetricCard("Tiempo (Exhaustiva)", f"{tiempo_ex:.6f}", "s", color="#b983ff")

def metric_distancia_vecino(dist_nn):
    return MetricCard("Distancia (Vecino)", f"{dist_nn:.2f}", "km", color="#60f0d6")

def metric_tiempo_vecino(tiempo_nn):
    return MetricCard("Tiempo (Vecino)", f"{tiempo_nn:.6f}", "s", color="#4fc3f7")

def metric_gap_optimalidad(gap):
    return MetricCard("Gap de Optimalidad", f"{gap:.2f}", "%", color="#ffd36b")

def metric_factor_velocidad(factor_velocidad):
    return MetricCard("Factor de Velocidad", f"{factor_velocidad:.1f}", "x", color="#7bd389")

# ===== CONCLUSIONES =====

def conclusiones_detalladas(tiempo_ex, dist_ex, tiempo_nn, dist_nn, gap):
    recomendacion = (
        "El heurístico ofrece excelente balance entre velocidad y calidad."
        if gap is not None and gap < 10
        else "Considerar heurísticas avanzadas o metaheurísticos para mejorar calidad."
    )

    return f"""<div style="color:#9aa7bf; line-height:1.8; padding:10px;">
<p style="margin:0 0 10px 0;">
<strong style="color:#e6eef8;">Búsqueda Exhaustiva</strong><br>
- Tiempo: <strong>{tiempo_ex:.6f} s</strong><br>
- Distancia: <strong>{dist_ex:.4f} km</strong><br>
- Complejidad: <code>O(n!)</code>
</p>

<p style="margin:10px 0;">
<strong style="color:#e6eef8;">Vecino Más Cercano</strong><br>
- Tiempo: <strong>{tiempo_nn:.6f} s</strong><br>
- Distancia: <strong>{dist_nn:.4f} km</strong><br>
- Gap: <strong>{gap:.2f}%</strong>
</p>

<p style="margin:10px 0 0 0;">
<strong style="color:#e6eef8;">Recomendación:</strong><br>
{recomendacion}
</p>
</div>"""