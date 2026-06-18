import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Coach Nutriólogo Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== PALETA MINIMALISTA PROFESIONAL ==========
st.markdown("""
<style>
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    body { background-color: #FAFAFA; color: #1F1F1F; }
    .main { background-color: #FAFAFA; }
    .stSidebar { background-color: #FFFFFF; border-right: 1px solid #E8E8E8; }
    h1 { color: #1F1F1F; font-size: 2.2rem; font-weight: 600; margin-bottom: 0.5rem; }
    h2 { color: #1F1F1F; font-size: 1.5rem; font-weight: 600; margin: 1.5rem 0 1rem 0; }
    h3 { color: #424242; font-size: 1.1rem; font-weight: 500; }
    
    .stat-box {
        background: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.2s;
    }
    
    .stat-box:hover { border-color: #1F1F1F; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .stat-value { font-size: 2rem; font-weight: 700; color: #1F1F1F; margin: 0.5rem 0; }
    .stat-label { font-size: 0.85rem; color: #757575; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .stButton > button {
        background-color: #1F1F1F;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { background-color: #424242; }
    
    .meal-item {
        background: #FFFFFF;
        border-left: 3px solid #1F1F1F;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    .exercise-item {
        background: #FFFFFF;
        border: 1px solid #E8E8E8;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .exercise-item h4 { color: #1F1F1F; margin: 0 0 0.5rem 0; }
    .exercise-meta { color: #757575; font-size: 0.9rem; }
    
    .progress-box {
        background: linear-gradient(135deg, #1F1F1F 0%, #424242 100%);
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .progress-value { font-size: 3rem; font-weight: 700; }
    .progress-label { font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; }
    
    .tab-label { font-weight: 500; color: #424242; }
    [aria-selected="true"] .tab-label { color: #1F1F1F; border-bottom: 2px solid #1F1F1F; }
</style>
""", unsafe_allow_html=True)

# ========== DIETAS ==========
DIETAS = {
    "Pollo": {
        "desayuno": {"comida": "Avena + Huevos + Plátano", "kcal": 520, "p": 25, "c": 65, "g": 18},
        "media_mañana": {"comida": "Yogur Griego + Granola", "kcal": 320, "p": 22, "c": 35, "g": 12},
        "comida": {"comida": "Arroz + Pechuga + Brócoli", "kcal": 720, "p": 50, "c": 75, "g": 18},
        "merienda": {"comida": "Pan Integral + Atún", "kcal": 380, "p": 30, "c": 35, "g": 15},
        "cena": {"comida": "Pechuga + Camote + Ensalada", "kcal": 520, "p": 45, "c": 60, "g": 12},
        "pre_dormir": {"comida": "Leche + Cereal", "kcal": 300, "p": 30, "c": 20, "g": 10}
    },
    "Carnes Rojas": {
        "desayuno": {"comida": "Panqueques Avena + Huevo", "kcal": 530, "p": 28, "c": 68, "g": 12},
        "media_mañana": {"comida": "Manzana + Almendras", "kcal": 320, "p": 20, "c": 38, "g": 14},
        "comida": {"comida": "Carne Magra + Papas", "kcal": 720, "p": 48, "c": 76, "g": 20},
        "merienda": {"comida": "Sándwich Jamón + Queso", "kcal": 380, "p": 32, "c": 34, "g": 16},
        "cena": {"comida": "Lomo + Batata + Ensalada", "kcal": 520, "p": 46, "c": 58, "g": 14},
        "pre_dormir": {"comida": "Yogur Griego + Granola", "kcal": 300, "p": 28, "c": 22, "g": 10}
    },
    "Pescado": {
        "desayuno": {"comida": "Tortillas + Huevo + Aguacate", "kcal": 520, "p": 26, "c": 62, "g": 19},
        "media_mañana": {"comida": "Batido Plátano + Proteína", "kcal": 320, "p": 28, "c": 36, "g": 8},
        "comida": {"comida": "Salmón + Arroz Integral", "kcal": 730, "p": 46, "c": 74, "g": 22},
        "merienda": {"comida": "Galletas Integrales + PB", "kcal": 370, "p": 26, "c": 42, "g": 14},
        "cena": {"comida": "Tilapia + Papas + Espinacas", "kcal": 520, "p": 42, "c": 62, "g": 13},
        "pre_dormir": {"comida": "Leche + Caseína", "kcal": 300, "p": 32, "c": 18, "g": 10}
    }
}

# ========== ENTRENAMIENTOS CON PRIORIDAD TREN INFERIOR ==========
ENTRENAMIENTOS = {
    "Tren Inferior A": {
        "enfoque": "Cuádriceps + Glúteos",
        "duracion": 70,
        "ejercicios": [
            {"nombre": "Sentadilla Barra", "series": "4x8-10", "notas": "Ejercicio principal", "musculo": "Cuádriceps/Glúteos"},
            {"nombre": "Prensa de Pierna", "series": "4x10-12", "notas": "Volumen", "musculo": "Cuádriceps"},
            {"nombre": "Leg Press Inclinado", "series": "3x12-15", "notas": "Glúteos énfasis", "musculo": "Glúteos"},
            {"nombre": "Extensiones Cuádriceps", "series": "3x12-15", "notas": "Aislamiento", "musculo": "Cuádriceps"},
            {"nombre": "Pantorrillas", "series": "4x15-20", "notas": "Gemelos", "musculo": "Pantorrillas"},
        ]
    },
    "Tren Superior A": {
        "enfoque": "Empuje (Pecho, Hombros, Tríceps)",
        "duracion": 55,
        "ejercicios": [
            {"nombre": "Press Banca Plano", "series": "4x8-10", "notas": "Principal", "musculo": "Pecho"},
            {"nombre": "Prensa Militar", "series": "3x10-12", "notas": "Hombros", "musculo": "Hombros"},
            {"nombre": "Aperturas Polea", "series": "3x12-15", "notas": "Aislamiento", "musculo": "Pecho"},
            {"nombre": "Elevaciones Laterales", "series": "3x12-15", "notas": "Deltoides", "musculo": "Hombros"},
            {"nombre": "Barra Rizada", "series": "3x10-12", "notas": "Bíceps", "musculo": "Bíceps"},
        ]
    },
    "Tren Inferior B": {
        "enfoque": "Isquiotibiales + Glúteos",
        "duracion": 70,
        "ejercicios": [
            {"nombre": "Peso Muerto Rumano", "series": "4x8-10", "notas": "Principal isquios", "musculo": "Isquiotibiales"},
            {"nombre": "Zancadas Mancuernas", "series": "3x12c/p", "notas": "Unilateral", "musculo": "Glúteos/Isquios"},
            {"nombre": "Empuje de Cadera", "series": "4x12-15", "notas": "Glúteos máximo", "musculo": "Glúteos"},
            {"nombre": "Curl Femoral Tumbado", "series": "3x12-15", "notas": "Aislamiento", "musculo": "Isquiotibiales"},
            {"nombre": "Abducción Máquina", "series": "3x15-20", "notas": "Glúteo medio", "musculo": "Glúteos"},
        ]
    },
    "Tren Superior B": {
        "enfoque": "Jalón (Espalda, Tríceps, Bíceps)",
        "duracion": 55,
        "ejercicios": [
            {"nombre": "Remo Barra", "series": "4x8-10", "notas": "Principal espalda", "musculo": "Espalda"},
            {"nombre": "Jalón al Pecho", "series": "3x10-12", "notas": "Lats", "musculo": "Espalda"},
            {"nombre": "Remo Polea Baja", "series": "3x12-15", "notas": "Espalda media", "musculo": "Espalda"},
            {"nombre": "Press Banca Inclinado", "series": "3x10-12", "notas": "Pecho/Tríceps", "musculo": "Pecho"},
            {"nombre": "Extensión Tríceps", "series": "3x12-15", "notas": "Aislamiento", "musculo": "Tríceps"},
        ]
    }
}

# ========== INICIALIZAR SESSION ==========
if "dieta" not in st.session_state:
    st.session_state.dieta = "Pollo"
if "progreso" not in st.session_state:
    st.session_state.progreso = []
if "dias_entreno" not in st.session_state:
    st.session_state.dias_entreno = {"lunes": True, "martes": True, "miercoles": False, "jueves": True, "viernes": True, "sabado": False, "domingo": False}

# ========== HEADER MINIMALISTA ==========
st.markdown("# Coach Nutriólogo Pro")
st.markdown("Sistema de entrenamiento y nutrición basado en resultados")
st.divider()

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("## Navegación")
    pagina = st.radio("", ["Inicio", "Nutrición", "Entrenamientos", "Progreso", "Configuración"], label_visibility="collapsed")
    
    st.divider()
    
    st.markdown("### Tu Perfil")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stat-box"><div class="stat-value">70</div><div class="stat-label">kg</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><div class="stat-value">1.68</div><div class="stat-label">m</div></div>', unsafe_allow_html=True)
    
    st.markdown("### Meta Diaria")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stat-box"><div class="stat-value">2760</div><div class="stat-label">kcal</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><div class="stat-value">145g</div><div class="stat-label">proteína</div></div>', unsafe_allow_html=True)

# ========== PÁGINA: INICIO ==========
if pagina == "Inicio":
    col1, col2 = st.columns([0.65, 0.35])
    
    with col1:
        st.markdown("## Tu Meta de Hoy")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.markdown('<div class="stat-box"><div class="stat-value">2760</div><div class="stat-label">Calorías</div></div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="stat-box"><div class="stat-value">145g</div><div class="stat-label">Proteína</div></div>', unsafe_allow_html=True)
        with col_c:
            st.markdown('<div class="stat-box"><div class="stat-value">360g</div><div class="stat-label">Carbos</div></div>', unsafe_allow_html=True)
        with col_d:
            st.markdown('<div class="stat-box"><div class="stat-value">80g</div><div class="stat-label">Grasas</div></div>', unsafe_allow_html=True)
        
        st.markdown("## Tracking de Hoy")
        
        tab1, tab2 = st.tabs(["Consumo Real", "Análisis"])
        
        with tab1:
            dieta = DIETAS[st.session_state.dieta]
            
            for comida, info in dieta.items():
                with st.container():
                    col1, col2 = st.columns([0.6, 0.4])
                    with col1:
                        st.markdown(f'<div class="meal-item"><strong>{comida.upper()}</strong><br>{info["comida"]}</div>', unsafe_allow_html=True)
                    with col2:
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.caption(f'{info["kcal"]}kcal')
                        with c2:
                            st.caption(f'P:{info["p"]}g')
                        with c3:
                            st.caption(f'C:{info["c"]}g')
                        with c4:
                            st.caption(f'G:{info["g"]}g')
        
        with tab2:
            st.markdown("### Distribución de Macros")
            
            fig = go.Figure(data=[go.Pie(
                labels=["Proteína (145g)", "Carbohidratos (360g)", "Grasas (80g)"],
                values=[580, 1440, 740],
                marker=dict(colors=["#1F1F1F", "#424242", "#757575"])
            )])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("## Progreso Esta Semana")
        
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        cumpl = [85, 92, 0, 88, 0, 0, 0]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dias, y=cumpl,
            marker_color=["#1F1F1F" if x > 0 else "#E8E8E8" for x in cumpl]
        ))
        fig.update_layout(height=300, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("## Próximo Entrenamiento")
        st.markdown("**Lunes** — Tren Inferior A (70 min)")
        st.markdown("Cuádriceps + Glúteos | Intensidad Máxima")

# ========== PÁGINA: NUTRICIÓN ==========
elif pagina == "Nutrición":
    st.markdown("## Plan Nutricional")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        st.session_state.dieta = st.selectbox("Elige tu dieta", list(DIETAS.keys()), label_visibility="collapsed")
    
    st.divider()
    
    dieta = DIETAS[st.session_state.dieta]
    
    for comida, info in dieta.items():
        st.markdown(f'<div class="meal-item"><strong>{comida.upper()}</strong><br>{info["comida"]}</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Calorías", info["kcal"])
        with col2:
            st.metric("Proteína", f"{info['p']}g")
        with col3:
            st.metric("Carbos", f"{info['c']}g")
        with col4:
            st.metric("Grasas", f"{info['g']}g")
        
        st.divider()

# ========== PÁGINA: ENTRENAMIENTOS ==========
elif pagina == "Entrenamientos":
    st.markdown("## Programa de Entrenamientos")
    
    st.info("Enfoque: Máximo desarrollo de tren inferior (piernas y glúteos)")
    
    st.divider()
    
    tabs = st.tabs([nombre for nombre in ENTRENAMIENTOS.keys()])
    
    for tab, (nombre, detalles) in zip(tabs, ENTRENAMIENTOS.items()):
        with tab:
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                st.markdown(f"### {nombre}")
                st.markdown(f"**Enfoque**: {detalles['enfoque']}")
                st.markdown(f"**Duración**: {detalles['duracion']} min")
                
                st.markdown("#### Ejercicios")
                
                for i, ej in enumerate(detalles['ejercicios'], 1):
                    st.markdown(f'<div class="exercise-item"><h4>{i}. {ej["nombre"]}</h4><div class="exercise-meta">{ej["series"]} | {ej["musculo"]}</div><div style="color: #757575; font-size: 0.85rem; margin-top: 0.5rem;">{ej["notas"]}</div></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Grupos Musculares")
                
                musculos = {}
                for ej in detalles['ejercicios']:
                    for m in ej['musculo'].split('/'):
                        musculos[m.strip()] = musculos.get(m.strip(), 0) + 1
                
                fig = go.Figure(data=[
                    go.Bar(x=list(musculos.keys()), y=list(musculos.values()), marker_color="#1F1F1F")
                ])
                fig.update_layout(height=300, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)

# ========== PÁGINA: PROGRESO ==========
elif pagina == "Progreso":
    st.markdown("## Tu Progreso")
    
    tab1, tab2 = st.tabs(["Registrar", "Historial"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha = st.date_input("Fecha")
        with col2:
            peso = st.number_input("Peso (kg)", value=70.0, step=0.1)
        with col3:
            brazo = st.number_input("Brazo (cm)", value=32.0, step=0.5)
        
        col4, col5 = st.columns(2)
        with col4:
            pecho = st.number_input("Pecho (cm)", value=95.0, step=0.5)
        with col5:
            cadera = st.number_input("Cadera (cm)", value=95.0, step=0.5)
        
        st.markdown("### Periodicidad de Aumento")
        st.info("Semana 1-2: Aprende forma | Semana 3+: +2.5kg/semana en ejercicios principales")
        
        if st.button("Guardar Medición"):
            st.session_state.progreso.append({
                "fecha": str(fecha),
                "peso": peso,
                "brazo": brazo,
                "pecho": pecho,
                "cadera": cadera
            })
            st.success("✓ Guardado")
    
    with tab2:
        if st.session_state.progreso:
            df = pd.DataFrame(st.session_state.progreso)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Registra tu primera medición")

# ========== PÁGINA: CONFIGURACIÓN ==========
elif pagina == "Configuración":
    st.markdown("## Configuración")
    
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Peso (kg)", value=70)
    with col2:
        st.number_input("Altura (m)", value=1.68, step=0.01)
    
    col3, col4 = st.columns(2)
    with col3:
        st.number_input("Edad", value=25)
    with col4:
        st.selectbox("Nivel", ["Principiante", "Intermedio", "Avanzado"])
    
    st.divider()
    
    st.markdown("### Días de Entrenamiento")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_keys = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    for dia, key in zip(dias, dias_keys):
        st.session_state.dias_entreno[key] = st.checkbox(dia, value=st.session_state.dias_entreno[key])
    
    if st.button("Guardar Configuración"):
        st.success("✓ Guardado")

st.divider()
st.caption("Coach Nutriólogo Pro © 2024")
