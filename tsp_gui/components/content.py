GLOBAL_CSS = """
<style>
/* ===== Contenedor general ===== */
.block-container {
    padding-top: 1.5rem !important;
    color: #e6eef8;
    background: #0b1220;
}

/* ===== Tarjetas oscuras ===== */
.card {
    background: #0f1724;
    border: 1px solid rgba(255,255,255,0.04);
    padding: 1.2rem 1.4rem;
    border-radius: 12px;
    margin: 0.9rem 0;
    box-shadow: 0 6px 18px rgba(2,6,23,0.6);
}

/* ===== Tarjeta destacada (header/sections) ===== */
.card-hero {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.03);
    padding: 1.6rem 1.8rem;
    border-radius: 14px;
    margin: 0.8rem 0 1.6rem 0;
}

/* ===== Tipografía / títulos ===== */
.h1 {
    color: #e6eef8;
    font-weight: 800;
    margin: 0;
}
.h2 {
    color: #e6eef8;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
}
.lead {
    color: #97a6bf;
    margin: 0;
    font-size: 0.98rem;
}

/* ===== Info box ===== */
.infobox {
    background: #08101b;
    border-left: 5px solid var(--infobox-color);
    padding: 0.9rem 1rem;
    border-radius: 10px;
    margin: 0.8rem 0;
}
.infobox .title {
    color: var(--infobox-color);
    font-weight: 700;
    margin: 0 0 0.3rem 0;
}
.infobox .text {
    color: #9aa7bf;
    font-size: 0.95rem;
    margin: 0;
}

/* ===== Alert box ===== */
.alertbox {
    background: rgba(255,255,255,0.01);
    border-left: 5px solid var(--alert-color);
    padding: 0.9rem 1rem;
    border-radius: 10px;
    margin: 0.8rem 0;
    color: #dbe9ff;
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
}
.alertbox .msg {
    color: #dbe9ff;
    margin: 0;
    font-weight: 600;
}

/* ===== Metric card ===== */
.metric {
    background: #0b1220;
    border: 1px solid rgba(255,255,255,0.03);
    padding: 0.9rem;
    border-radius: 10px;
    text-align: center;
    width: 100%;
}
.metric .label {
    color: #9aa7bf;
    font-size: 0.78rem;
    margin: 0 0 0.35rem 0;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.metric .value {
    color: var(--metric-color);
    font-weight: 800;
    font-size: 1.6rem;
    margin: 0;
}

/* ===== Divider ligero ===== */
.light-divider {
    height: 1px;
    background: rgba(255,255,255,0.03);
    margin: 1.2rem 0;
    border-radius: 1px;
}

/* ===== Footer ===== */
.tsp-footer {
    text-align: center;
    color: #8f9bb1;
    font-size: 0.92rem;
    margin-top: 1.2rem;
    padding-top: 1rem;
}
</style>
"""

def inject_global_styles():
    return GLOBAL_CSS


# ----------------------
# HEADER & SECCIONES
# ----------------------

def Header():
    return """
    <div class="card-hero">
        <h1 class="h1" style="font-size:2rem;text-align:center;"> Problema del Viajante (TSP)</h1>
        <p class="lead" style="text-align:center;margin-top:0.45rem;">
            Visualización y comparación entre algoritmo exhaustivo y heurístico (Vecino Más Cercano).
        </p>
    </div>
    """

def SectionCities():
    return """
    <div class="card">
        <h2 class="h2"> Ciudades y Coordenadas</h2>
        <p class="lead">Tabla con las coordenadas geográficas usadas en el análisis.</p>
    </div>
    """

def SectionDistanceMatrix():
    return """
    <div class="card">
        <h2 class="h2"> Matriz de Distancias</h2>
        <p class="lead">Matriz euclidiana de distancias entre las ciudades.</p>
    </div>
    """

def SectionExhaustiveSolution():
    return """
    <div class="card">
        <h2 class="h2"> Solución Óptima (Búsqueda Exhaustiva)</h2>
        <p class="lead">Explora todas las permutaciones para encontrar la ruta mínima (no escalable).</p>
    </div>
    """

def SectionNNSolution():
    return """
    <div class="card">
        <h2 class="h2"> Vecino Más Cercano (Heurístico)</h2>
        <p class="lead">Construye una ruta rápida seleccionando el siguiente punto más cercano.</p>
    </div>
    """

def SectionComparison():
    return """
    <div class="card">
        <h2 class="h2"> Comparación y Análisis</h2>
        <p class="lead">Comparación de distancia, tiempo y gap entre ambos métodos.</p>
    </div>
    """

# ----------------------
# COMPONENTES (InfoBox, AlertBox, MetricCard)
# ----------------------

def InfoBox(title, content, color="#32d5c9"):
    """
    color = color hex para el borde / título (ej: '#32d5c9')
    content puede contener HTML (listas, <strong>, etc.)
    """
    safe_color = color
    return f"""
    <div class="infobox" style="--infobox-color:{safe_color};">
        <div class="title">{title}</div>
        <div class="text">{content}</div>
    </div>
    """

def AlertBox(message, alert_type="info"):
    """
    alert_type in {'info','success','warning','error'}
    """
    mapping = {
        "info":  ("#3b82f6"),
        "success":("#10b981"),
        "warning":("#f59e0b"),
        "error": ("#ef4444")
    }
    color = mapping.get(alert_type, "#3b82f6")
    icon = {
        "info":"ℹ️",
        "success":"✅",
        "warning":"⚠️",
        "error":"❌"
    }.get(alert_type, "ℹ️")

    return f"""
    <div class="alertbox" style="--alert-color:{color}; border-left-color:{color};">
        <div style="font-size:1.05rem;">{icon}</div>
        <div class="msg">{message}</div>
    </div>
    """

def MetricCard(label, value, unit="", color="#60a5fa"):
    """
    label: texto pequeño de la métrica
    value: valor formateado (string)
    unit: sufijo a mostrar
    color: color principal de la tarjeta
    """
    safe_color = color
    return f"""
    <div class="metric" style="--metric-color:{safe_color};">
        <div class="label">{label}</div>
        <div class="value">{value} <span style="font-size:0.9rem;font-weight:600;color:#9aa7bf;">{unit}</span></div>
    </div>
    """

def footer():
    return """
    <div class="tsp-footer">
        <hr style="opacity:0.06;margin-bottom:0.8rem;">
        <div> <strong>Visualización del Problema del Viajante (TSP)</strong></div>
        <div style="margin-top:0.35rem;">Desarrollado con Streamlit — Algoritmos y visualización</div>
    </div>
    """
