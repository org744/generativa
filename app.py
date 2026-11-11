"""
ArchGen AI - Generador y Validador de Arquitecturas de Software
==============================================================
Interfaz de usuario profesional en Streamlit para ingeniería DevOps,
diseño de sistemas distribuidos y auditoría arquitectónica (ADR).
"""

from __future__ import annotations

import base64
import html
from datetime import datetime
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

try:
    import pandas as pd
except ImportError:
    pd = None

from generator import (
    ArchitectureGenerator,
    ArchitecturePattern,
    ComponentType,
    GenerationResult,
    Layer,
    Pillar,
    Severity
)


# ==============================================================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN STREAMLIT
# ==============================================================================

st.set_page_config(
    page_title="ArchGen AI | Generador de Arquitecturas",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================================================================
# ESTILOS CSS PERSONALIZADOS (ESTILO CONSOLA DEVOPS & INGENIERÍA)
# ==============================================================================

DEVOPS_CUSTOM_CSS = """
<style>
    /* Estilos globales y paleta de ingeniería */
    :root {
        --bg-main: #0E131F;
        --card-bg: #161F30;
        --card-border: #24334C;
        --accent-cyan: #00D2FF;
        --accent-emerald: #10B981;
        --accent-purple: #8B5CF6;
        --text-muted: #94A3B8;
        --text-light: #F8FAFC;
    }

    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Contenedores de métricas custom */
    .metric-container {
        background: linear-gradient(145deg, #161F30, #111827);
        border: 1px solid #24334C;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-container:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.2;
    }
    .metric-subtitle {
        font-size: 0.78rem;
        color: #00D2FF;
        margin-top: 4px;
    }

    /* Badges de estado */
    .badge-pill {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        margin-right: 6px;
    }
    .badge-info {
        background-color: rgba(14, 165, 233, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(14, 165, 233, 0.4);
    }
    .badge-warning {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-success {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Tarjeta de componente */
    .component-card {
        background: #131B2B;
        border-left: 4px solid #38BDF8;
        border-top: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
        border-radius: 6px;
        padding: 14px;
        margin-bottom: 10px;
    }

    /* Estilo de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid #1E293B;
    }

    /* Header decorativo */
    .header-banner {
        background: linear-gradient(90deg, #1E1B4B 0%, #0F172A 100%);
        border: 1px solid #312E81;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
    }
</style>
"""

st.markdown(DEVOPS_CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# PRESETS Y PLANTILLAS DE EJEMPLO
# ==============================================================================

PRESETS = {
    "Personalizado (Escribe tu requerimiento)": "",
    "🛒 E-Commerce Distribuido (Alta Concurrencia + Saga)": (
        "Requiero diseñar una plataforma de comercio electrónico de alta concurrencia para soportar "
        "eventos de alta demanda (como Black Friday). El sistema debe incluir catálogo de productos con stock "
        "en tiempo real, carrito de compras distribuido, pasarela de pagos con tarjetas bancarias (cumpliendo PCI-DSS), "
        "gestión de órdenes y envíos, y un motor de notificaciones asíncronas para confirmaciones por correo y SMS. "
        "Es prioritario contar con caché agresiva para productos más vistos y desacoplamiento para picos de tráfico."
    ),
    "💳 Core Bancario & Motor de Pagos (Fintech + ACID + Ledger)": (
        "Sistema bancario y core financiero para procesamiento de transferencias interbancarias y pagos en tiempo real. "
        "Requiere un libro mayor contable (Ledger) inmutable con consistencia ACID estricta de doble partida, "
        "motor de evaluación de fraude con aprendizaje automático en menos de 50 milisegundos, servicio de autenticación "
        "robusta con OAuth2/mTLS, pistas de auditoría inmutables y base de datos con cifrado en reposo para cumplir "
        "normativas financieras internacionales."
    ),
    "⚡ Telemetría IoT & Streaming Masivo (MQTT + Kafka + TimeSeries)": (
        "Plataforma industrial para la ingesta de telemetría de más de 100,000 sensores de vehículos y flotas en tiempo real. "
        "Los dispositivos transmiten datos mediante el protocolo MQTT cada 2 segundos. Se requiere un bus de eventos "
        "de streaming de muy alta capacidad, procesamiento en streaming de métricas (cálculo de promedios, alertas de temperatura "
        "y colisión) y almacenamiento en base de datos especializada en series temporales con paneles Grafana."
    ),
    "🏥 Plataforma de Telemedicina y Salud Digital (HIPAA Compliance)": (
        "Sistema de salud y telemedicina para gestión integral de historias clínicas digitales (EHR) y consultas médicas remotas. "
        "Debe soportar agendamiento de citas, videollamadas seguras WebRTC, emisión de recetas electrónicas auditadas y "
        "almacenamiento cifrado de radiografías y expedientes confidenciales. Toda la solución debe cumplir estrictamente "
        "con los lineamientos de privacidad HIPAA y control de acceso basado en roles (RBAC)."
    ),
    "🏢 SaaS Multi-Tenant Empresarial B2B (Tenant Isolation + Facturación)": (
        "Plataforma SaaS B2B empresarial multitenant para gestión de inventarios y proyectos de empresas corporativas. "
        "Debe garantizar aislamiento estricto de datos entre clientes (inquilinos), soporte para subdominios personalizados, "
        "integración con Stripe para facturación recurrente mensual y roles de administración jerárquica con Single Sign-On (SSO)."
    ),
    "🚀 Monolito Modular Ágil (FastAPI + Clean Architecture)": (
        "Aplicación web de gestión interna ágil desarrollada bajo un patrón de Monolito Modular con FastAPI y Python 3.12. "
        "Estructurada en capas limpias con separación de dominios (Usuarios, Inventario, Facturación) pero desplegada "
        "en un único artefacto para simplificar operaciones DevOps en un equipo pequeño, apoyado con PostgreSQL, Redis "
        "y tareas en background con Celery."
    )
}


# ==============================================================================
# FUNCIONES AUXILIARES DE RENDERIZADO
# ==============================================================================

def render_mermaid_viewer(mermaid_code: str, height: int = 580) -> None:
    """
    Renderiza el diagrama Mermaid.js dinámicamente mediante iframe HTML seguro
    con soporte interactivo para zoom y temas oscuros.
    """
    escaped_code = html.escape(mermaid_code)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
      <style>
        * {{
          box-sizing: border-box;
        }}
        body {{
          background-color: #0B0F19;
          color: #F8FAFC;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
          margin: 0;
          padding: 16px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: flex-start;
          min-height: 100vh;
        }}
        .diagram-wrapper {{
          width: 100%;
          background: #111827;
          border: 1px solid #1F2937;
          border-radius: 8px;
          padding: 24px;
          overflow-x: auto;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: center;
        }}
        .mermaid {{
          display: flex;
          justify-content: center;
          width: 100%;
        }}
        .diagram-toolbar {{
          width: 100%;
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
          font-size: 0.85rem;
          color: #94A3B8;
        }}
        .status-dot {{
          height: 8px;
          width: 8px;
          background-color: #10B981;
          border-radius: 50%;
          display: inline-block;
          margin-right: 6px;
        }}
      </style>
    </head>
    <body>
      <div class="diagram-toolbar">
        <div><span class="status-dot"></span> Motor Mermaid.js v10.9 Activo</div>
        <div>Diagrama de Arquitectura de Capas</div>
      </div>
      <div class="diagram-wrapper">
        <pre class="mermaid">
{escaped_code}
        </pre>
      </div>
      <script>
        mermaid.initialize({{
          startOnLoad: true,
          theme: 'dark',
          securityLevel: 'loose',
          flowchart: {{
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis'
          }}
        }});
      </script>
    </body>
    </html>
    """
    components.html(html_content, height=height, scrolling=True)


def get_download_link(content: str, filename: str, label: str) -> str:
    """Genera un enlace o botón para descargar archivos generados."""
    b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="stDownloadButton">{label}</a>'


# ==============================================================================
# INICIALIZACIÓN DE ESTADO DE SESIÓN (SESSION STATE)
# ==============================================================================

if "generator" not in st.session_state:
    st.session_state.generator = ArchitectureGenerator()

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "preset_selected" not in st.session_state:
    st.session_state.preset_selected = "🛒 E-Commerce Distribuido (Alta Concurrencia + Saga)"


# ==============================================================================
# BARRA LATERAL (SIDEBAR DE CONTROL DEVOPS)
# ==============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Centro de Control DevOps")
    st.caption("Configuración de parámetros y restricciones de ingeniería")

    st.markdown("---")

    # Selector de Presets de Ejemplo
    preset_choice = st.selectbox(
        "📚 Plantillas y Casos de Estudio:",
        options=list(PRESETS.keys()),
        index=1,
        help="Selecciona un caso de estudio precargado para evaluar la aplicación al instante."
    )

    # Si cambia el preset, actualizamos el valor en session_state
    if preset_choice != st.session_state.preset_selected:
        st.session_state.preset_selected = preset_choice
        st.rerun()

    # Patrón de Arquitectura
    pattern_options = ["Auto-Detectar"] + [p.value for p in ArchitecturePattern]
    selected_pattern_pref = st.selectbox(
        "🏛️ Patrón Arquitectónico Deseado:",
        options=pattern_options,
        index=0,
        help="Elige un patrón específico o deja que el motor analice el texto."
    )

    # Perfil de Carga y Concurrencia
    load_profile = st.select_slider(
        "🚀 Perfil de Carga Estimado (RPS / RPM):",
        options=[
            "Baja (< 1k RPM)",
            "Media (1k - 10k RPM)",
            "Alta (10k - 100k RPM)",
            "Crítica (> 100k RPM / Streaming)"
        ],
        value="Alta (10k - 100k RPM)",
        help="Determina la necesidad de capas de caché, réplicas y buses de eventos."
    )

    # Marco de Cumplimiento Normativo
    compliance = st.selectbox(
        "🛡️ Cumplimiento y Gobernanza:",
        options=[
            "Estándar Empresarial",
            "Financiero / PCI-DSS / SOX",
            "Salud / HIPAA / Privacidad Médica",
            "GDPR / Cifrado Estricto"
        ],
        index=0
    )

    # Infraestructura Destino
    target_infra = st.selectbox(
        "🐳 Infraestructura de Despliegue:",
        options=[
            "Docker Local / Compose",
            "Kubernetes (K8s Cluster)",
            "Cloud Native Híbrido (AWS/GCP/Azure)"
        ],
        index=0
    )

    st.markdown("---")

    # Botón Principal de Generación
    generate_btn = st.button("⚡ GENERAR ARQUITECTURA", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.78rem; color: #94A3B8; text-align: center;">
            <b>ArchGen AI v2.4</b><br/>
            Motor Heurístico 100% Offline<br/>
            Optimizado para evaluación académica
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# ENCABEZADO Y PRESENTACIÓN DE LA APLICACIÓN
# ==============================================================================

st.markdown(
    """
    <div class="header-banner">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div>
                <h1 style="margin: 0; font-size: 2.1rem; color: #FFFFFF; font-weight: 800;">
                    🏗️ ArchGen AI
                </h1>
                <p style="margin: 6px 0 0 0; font-size: 1.05rem; color: #94A3B8;">
                    Generador y Validador Inteligente de Arquitecturas de Software & DevOps
                </p>
            </div>
            <div>
                <span class="badge-pill badge-info">⚡ Motor Local Offline</span>
                <span class="badge-pill badge-success">🐳 Docker Ready</span>
                <span class="badge-pill badge-warning">🛡️ Well-Architected</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==============================================================================
# ÁREA DE ENTRADA DE REQUERIMIENTOS
# ==============================================================================

st.markdown("#### 📝 Especificación de Requerimientos del Sistema")

# Cargar el texto del preset o permitir edición
default_input_text = PRESETS.get(st.session_state.preset_selected, "")

requirements_input = st.text_area(
    label="Ingresa las necesidades funcionales, no funcionales o la descripción de tu sistema en lenguaje natural:",
    value=default_input_text,
    height=125,
    placeholder="Ejemplo: Requiero un sistema de gestión logística para rastreo de flotas con base de datos ACID, notificaciones móviles y caché para alta concurrencia..."
)


# ==============================================================================
# LÓGICA DE EJECUCIÓN DEL MOTOR
# ==============================================================================

# Si se presionó el botón o no hay resultado en memoria, procesar
if generate_btn or (st.session_state.current_result is None and requirements_input.strip()):
    with st.spinner("🔍 Analizando requerimientos, sintetizando topología y generando especificaciones..."):
        result = st.session_state.generator.analyze_and_generate(
            requirements_text=requirements_input,
            preferred_pattern=selected_pattern_pref,
            load_profile=load_profile,
            compliance=compliance,
            target_infra=target_infra
        )
        st.session_state.current_result = result


# ==============================================================================
# RENDERIZADO DE RESULTADOS
# ==============================================================================

res: Optional[GenerationResult] = st.session_state.current_result

if res is not None:
    # --------------------------------------------------------------------------
    # TARJETAS DE MÉTRICAS CLAVE SUPERIORES
    # --------------------------------------------------------------------------
    st.markdown("<br/>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)

    total_services = sum(1 for c in res.components if c.component_type == ComponentType.SERVICE)
    total_dbs = sum(1 for c in res.components if c.component_type in [ComponentType.DATABASE, ComponentType.STORAGE])
    avg_score = int(sum(res.pillar_scores.values()) / max(1, len(res.pillar_scores)))

    with m1:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Patrón Arquitectónico</div>
                <div class="metric-value" style="font-size: 1.15rem; color: #38BDF8;">{res.pattern.value}</div>
                <div class="metric-subtitle">Validado con éxito</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Componentes Totales</div>
                <div class="metric-value">{len(res.components)} <span style="font-size: 0.9rem; color: #94A3B8;">nodos</span></div>
                <div class="metric-subtitle">{total_services} servicios | {total_dbs} DBs</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:
        score_color = "#34D399" if avg_score >= 80 else "#FBBF24"
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Índice Well-Architected</div>
                <div class="metric-value" style="color: {score_color};">{avg_score}/100</div>
                <div class="metric-subtitle">5 Pilares Evaluados</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Alertas & Validaciones</div>
                <div class="metric-value">{len(res.validations)} <span style="font-size: 0.9rem; color: #94A3B8;">items</span></div>
                <div class="metric-subtitle">Recomendaciones listas</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # PESTAÑAS PRINCIPALES DEL DASHBOARD
    # --------------------------------------------------------------------------
    tab_diagram, tab_components, tab_audit, tab_docker, tab_report = st.tabs([
        "🗺️ Diagrama Mermaid.js",
        "🧩 Desglose de Componentes",
        "🛡️ Auditoría Well-Architected",
        "🐳 Docker Compose DevOps",
        "📄 Reporte Técnico ADR (Markdown)"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: DIAGRAMA MERMAID.JS
    # --------------------------------------------------------------------------
    with tab_diagram:
        st.markdown("### 🗺️ Diagrama de Topología en Capas")
        st.caption("Visualización interactiva generada con sintaxis nativa de Mermaid.js. Agrupada por límites de red y capas lógicas.")

        # Renderizador interactivo
        render_mermaid_viewer(res.mermaid_diagram, height=580)

        col_d1, col_d2 = st.columns([3, 1])
        with col_d1:
            with st.expander("🔍 Ver y copiar código Mermaid.js en texto plano"):
                st.code(res.mermaid_diagram, language="mermaid")
        with col_d2:
            st.markdown(
                """
                <div style="padding: 10px; background: #161F30; border-radius: 8px; border: 1px solid #24334C; text-align: center;">
                    <span style="font-size: 0.85rem; color: #94A3B8;">¿Deseas editarlo en la nube?</span><br/>
                    <a href="https://mermaid.live" target="_blank" style="color: #38BDF8; font-weight: 600; text-decoration: none;">
                        Abrir Mermaid Live Editor ↗
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------------------------
    # TAB 2: DESGLOSE DE COMPONENTES
    # --------------------------------------------------------------------------
    with tab_components:
        st.markdown("### 🧩 Catálogo de Componentes e Infraestructura")
        st.caption("Estructura desagregada por capas lógicas, asignación de puertos y tecnologías recomendadas.")

        # Filtro de capa opcional
        layer_filter = st.selectbox(
            "Filtrar por Capa Arquitectónica:",
            options=["Todas las Capas"] + [lyr.value for lyr in Layer],
            index=0
        )

        filtered_comps = res.components
        if layer_filter != "Todas las Capas":
            filtered_comps = [c for c in res.components if c.layer.value == layer_filter]

        # Tabla Resumen
        if pd is not None:
            table_data = []
            for c in filtered_comps:
                table_data.append({
                    "ID": c.id,
                    "Nombre": c.name,
                    "Capa": c.layer.value,
                    "Tipo": c.component_type.value,
                    "Tecnología": c.technology,
                    "Puerto": c.port if c.port else "Interno"
                })
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            # Fallback limpio sin pandas
            for c in filtered_comps:
                st.markdown(f"- **{c.name}** (`{c.id}`): {c.technology} | Capa: *{c.layer.value}* | Puerto: `{c.port or 'Interno'}`")

        st.markdown("#### Fichas Técnicas de Componentes")
        for c in filtered_comps:
            with st.expander(f"🔹 {c.name} (`{c.id}`) - {c.layer.value}"):
                c_col1, c_col2 = st.columns([2, 1])
                with c_col1:
                    st.write(f"**Descripción:** {c.description}")
                    st.write(f"**Stack Tecnológico:** `{c.technology}`")
                    if c.depends_on:
                        st.write(f"**Depende de:** `{', '.join(c.depends_on)}`")
                with c_col2:
                    st.write(f"**Imagen Docker:** `{c.docker_image or 'Custom Build'}`")
                    st.write(f"**Puertos Mapeados:** `{c.port or 'Ninguno (Red Interna)'}`")
                    if c.healthcheck:
                        st.write(f"**Healthcheck:** `{c.healthcheck}`")

    # --------------------------------------------------------------------------
    # TAB 3: AUDITORÍA WELL-ARCHITECTED
    # --------------------------------------------------------------------------
    with tab_audit:
        st.markdown("### 🛡️ Auditoría de Calidad Arquitectónica")
        st.caption("Evaluación automática basada en los 5 pilares de ingeniería de sistemas de alto desempeño.")

        # Scores por pilar
        st.markdown("#### Puntuaciones de Conformidad Técnica")
        cols = st.columns(len(res.pillar_scores))
        for idx, (pillar_name, score) in enumerate(res.pillar_scores.items()):
            with cols[idx]:
                st.metric(label=pillar_name.split()[0], value=f"{score}%")
                st.progress(score / 100)

        st.markdown("---")
        st.markdown("#### Hallazgos y Diagnósticos del Sistema")

        for v in res.validations:
            severity_class = (
                "badge-info" if v.severity == Severity.INFO
                else ("badge-warning" if v.severity == Severity.WARNING else "badge-critical")
            )
            st.markdown(
                f"""
                <div class="component-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <h4 style="margin: 0; color: #F8FAFC;">{v.title}</h4>
                        <span class="badge-pill {severity_class}">{v.severity.value}</span>
                    </div>
                    <p style="margin: 4px 0; color: #94A3B8; font-size: 0.92rem;"><b>Diagnóstico:</b> {v.description}</p>
                    <p style="margin: 4px 0; color: #38BDF8; font-size: 0.92rem;"><b>Recomendación DevOps:</b> {v.recommendation}</p>
                    <span style="font-size: 0.78rem; color: #64748B;">Pilar: {v.pillar.value}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("#### ⚖️ Matriz de Compromisos Arquitectónicos (Trade-offs)")
        st.caption("Decisiones de compromiso fundamentales inherentes al patrón y perfil de concurrencia seleccionados:")

        for to in res.trade_offs:
            with st.expander(f"⚖️ {to.concept}"):
                t1, t2, t3 = st.columns(3)
                with t1:
                    st.markdown(f"**✅ Ventaja Estratégica:**\n\n{to.advantage}")
                with t2:
                    st.markdown(f"**⚠️ Desventaja o Sobrecarga:**\n\n{to.drawback}")
                with t3:
                    st.markdown(f"**🛠️ Mitigación Aplicada:**\n\n{to.mitigation}")

    # --------------------------------------------------------------------------
    # TAB 4: DOCKER COMPOSE DEVOPS
    # --------------------------------------------------------------------------
    with tab_docker:
        st.markdown("### 🐳 Especificación de Contenedores (`docker-compose.yml`)")
        st.caption("Archivo de orquestación local completamente funcional con redes aisladas, volúmenes y healthchecks.")

        st.download_button(
            label="📥 Descargar docker-compose.yml",
            data=res.docker_compose_yaml,
            file_name="docker-compose.yml",
            mime="text/yaml",
            type="primary"
        )

        st.code(res.docker_compose_yaml, language="yaml")

        st.markdown(
            """
            #### 🚀 Instrucciones de Despliegue en Servidor Local:
            ```powershell
            # 1. Iniciar la infraestructura completa en segundo plano
            docker compose up -d

            # 2. Monitorear el estado de salud de todos los servicios
            docker compose ps

            # 3. Inspeccionar logs agregados en tiempo real
            docker compose logs -f --tail=100

            # 4. Detener el entorno preservando los volúmenes de datos
            docker compose down
            ```
            """
        )

    # --------------------------------------------------------------------------
    # TAB 5: REPORTE TÉCNICO ADR (MARKDOWN)
    # --------------------------------------------------------------------------
    with tab_report:
        st.markdown("### 📄 Registro Formal de Decisiones de Arquitectura (ADR)")
        st.caption("Documento técnico exhaustivo listo para entrega profesional, auditoría o repositorio de código.")

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"ADR_Architecture_Report_{timestamp_str}.md"

        st.download_button(
            label="📥 Descargar Reporte Completo (.md)",
            data=res.markdown_report,
            file_name=report_filename,
            mime="text/markdown",
            type="primary"
        )

        st.markdown("---")
        st.markdown(res.markdown_report)

else:
    st.info("💡 Haz clic en '⚡ GENERAR ARQUITECTURA' en la barra lateral para procesar los requerimientos.")
