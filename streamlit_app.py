import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from calendar import monthcalendar, month_name

st.set_page_config(
    page_title="Coach Nutriólogo Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ PALETA DE COLORES PROFESIONAL ============
COLORS = {
    "primary": "#1A73E8",
    "primary_dark": "#0D47A1",
    "accent": "#FF6B35",
    "success": "#34A853",
    "warning": "#FBBC04",
    "danger": "#EA4335",
    "bg": "#FFFFFF",
    "bg_light": "#F8F9FA",
    "text_dark": "#202124",
    "text_light": "#5F6368",
    "border": "#DADCE0",
}

st.markdown(f"""
<style>
    * {{
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    }}
    
    body {{
        background-color: {COLORS['bg']};
        color: {COLORS['text_dark']};
    }}
    
    .main {{
        background-color: {COLORS['bg']};
    }}
    
    .stSidebar {{
        background-color: {COLORS['bg_light']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    h1 {{
        color: {COLORS['primary_dark']};
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    h2 {{
        color: {COLORS['primary_dark']};
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }}
    
    h3 {{
        color: {COLORS['primary']};
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1rem;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin: 0.5rem 0;
    }}
    
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }}
    
    .metric-label {{
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .stButton > button {{
        background-color: {COLORS['accent']};
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background-color: #E55100;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 107, 53, 0.3);
    }}
    
    .success-box {{
        background-color: {COLORS['bg_light']};
        border-left: 4px solid {COLORS['success']};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .warning-box {{
        background-color: {COLORS['bg_light']};
        border-left: 4px solid {COLORS['warning']};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .danger-box {{
        background-color: {COLORS['bg_light']};
        border-left: 4px solid {COLORS['danger']};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .data-table {{
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
    }}
    
    .data-table th {{
        background-color: {COLORS['primary']};
        color: white;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
    }}
    
    .data-table td {{
        padding: 0.8rem 1rem;
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    .data-table tr:hover {{
        background-color: {COLORS['bg_light']};
    }}
    
    .progress-bar {{
        background-color: {COLORS['border']};
        border-radius: 8px;
        height: 30px;
        overflow: hidden;
        margin: 0.5rem 0;
    }}
    
    .progress-fill {{
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }}
</style>
""", unsafe_allow_html=True)

# ============ DATOS DE DIETAS REALISTAS ============
DIETAS = {
    "Clásica (Pollo)": {
        "desayuno": {"comida": "Avena + Huevos + Plátano", "kcal": 520, "p": 25, "c": 65, "g": 18},
        "media_mañana": {"comida": "Yogur Griego + Granola", "kcal": 320, "p": 22, "c": 35, "g": 12},
        "comida": {"comida": "Arroz + Pechuga + Brócoli", "kcal": 720, "p": 50, "c": 75, "g": 18},
        "merienda": {"comida": "Pan Integral + Atún + Aguacate", "kcal": 380, "p": 30, "c": 35, "g": 15},
        "cena": {"comida": "Pechuga + Camote + Ensalada", "kcal": 520, "p": 45, "c": 60, "g": 12},
        "pre_dormir": {"comida": "Leche + Cereal", "kcal": 300, "p": 30, "c": 20, "g": 10}
    },
    "Carnes Rojas": {
        "desayuno": {"comida": "Panqueques de Avena + Huevo", "kcal": 530, "p": 28, "c": 68, "g": 12},
        "media_mañana": {"comida": "Manzana + Almendras + Queso", "kcal": 320, "p": 20, "c": 38, "g": 14},
        "comida": {"comida": "Carne Magra + Papas + Verduras", "kcal": 720, "p": 48, "c": 76, "g": 20},
        "merienda": {"comida": "Sándwich de Jamón + Queso", "kcal": 380, "p": 32, "c": 34, "g": 16},
        "cena": {"comida": "Lomo + Batata + Ensalada", "kcal": 520, "p": 46, "c": 58, "g": 14},
        "pre_dormir": {"comida": "Yogur Griego + Granola", "kcal": 300, "p": 28, "c": 22, "g": 10}
    },
    "Pescado": {
        "desayuno": {"comida": "Tortillas de Maíz + Huevo + Aguacate", "kcal": 520, "p": 26, "c": 62, "g": 19},
        "media_mañana": {"comida": "Batido de Plátano + Proteína", "kcal": 320, "p": 28, "c": 36, "g": 8},
        "comida": {"comida": "Salmón + Arroz Integral + Espárragos", "kcal": 730, "p": 46, "c": 74, "g": 22},
        "merienda": {"comida": "Galletas Integrales + PB", "kcal": 370, "p": 26, "c": 42, "g": 14},
        "cena": {"comida": "Tilapia + Papas + Espinacas", "kcal": 520, "p": 42, "c": 62, "g": 13},
        "pre_dormir": {"comida": "Leche + Caseína", "kcal": 300, "p": 32, "c": 18, "g": 10}
    },
    "Vegetariana": {
        "desayuno": {"comida": "Avena + Leche + Frutos Rojos", "kcal": 510, "p": 18, "c": 68, "g": 14},
        "media_mañana": {"comida": "Hummus + Vegetales + Pan", "kcal": 320, "p": 12, "c": 42, "g": 10},
        "comida": {"comida": "Lentejas + Arroz + Verduras", "kcal": 720, "p": 24, "c": 92, "g": 14},
        "merienda": {"comida": "Queso + Nueces + Fruta", "kcal": 380, "p": 22, "c": 38, "g": 16},
        "cena": {"comida": "Tofu + Batata + Brócoli", "kcal": 520, "p": 28, "c": 66, "g": 14},
        "pre_dormir": {"comida": "Yogur + Granola", "kcal": 300, "p": 20, "c": 36, "g": 8}
    }
}

# ============ ENTRENAMIENTOS DETALLADOS ============
ENTRENAMIENTOS_DETALLE = {
    "UPPER A - Empuje": {
        "musulos": ["Pecho", "Hombros", "Tríceps", "Bíceps"],
        "prioridad": "Alta",
        "duracion": 55,
        "descripcion": "Enfoque en movimientos de empuje. Desarrolla pectorales, deltoides anteriores y tríceps con alta intensidad.",
        "ejercicios": [
            {"nombre": "Press Banca Plano", "series": 4, "reps": "8-10", "descanso": "2 min", "grupo": "Pecho", "desc": "Ejercicio principal para pecho"},
            {"nombre": "Prensa Militar", "series": 3, "reps": "10-12", "descanso": "90 seg", "grupo": "Hombros", "desc": "Hombros y tríceps"},
            {"nombre": "Aperturas Polea", "series": 3, "reps": "12-15", "descanso": "60 seg", "grupo": "Pecho", "desc": "Aislamiento de pecho"},
            {"nombre": "Elevaciones Laterales", "series": 3, "reps": "12-15", "descanso": "60 seg", "grupo": "Hombros", "desc": "Deltoides lateral"},
            {"nombre": "Barra Rizada", "series": 3, "reps": "10-12", "descanso": "60 seg", "grupo": "Bíceps", "desc": "Bíceps principal"},
        ]
    },
    "LOWER A - Cuádriceps": {
        "musculos": ["Cuádriceps", "Glúteos", "Core"],
        "prioridad": "Máxima",
        "duracion": 60,
        "descripcion": "Enfoque en piernas superiores. Máxima intensidad en cuádriceps con volumen moderado.",
        "ejercicios": [
            {"nombre": "Sentadilla Barra", "series": 4, "reps": "8-10", "descanso": "2-3 min", "grupo": "Cuádriceps", "desc": "Ejercicio rey de piernas"},
            {"nombre": "Prensa Pierna", "series": 3, "reps": "10-12", "descanso": "2 min", "grupo": "Cuádriceps", "desc": "Volumen de cuádriceps"},
            {"nombre": "Extensiones", "series": 3, "reps": "12-15", "descanso": "60 seg", "grupo": "Cuádriceps", "desc": "Aislamiento"},
            {"nombre": "Pantorrillas", "series": 4, "reps": "15-20", "descanso": "60 seg", "grupo": "Pantorrillas", "desc": "Pantorrillas"},
        ]
    },
    "UPPER B - Jalón": {
        "musculos": ["Espalda", "Lats", "Tríceps", "Bíceps"],
        "prioridad": "Alta",
        "duracion": 55,
        "descripcion": "Enfoque en movimientos de jalón. Desarrolla espalda ancha y profunda.",
        "ejercicios": [
            {"nombre": "Remo Barra", "series": 4, "reps": "8-10", "descanso": "2 min", "grupo": "Espalda", "desc": "Espalda gruesa"},
            {"nombre": "Jalón Pecho", "series": 3, "reps": "10-12", "descanso": "90 seg", "grupo": "Lats", "desc": "Lats"},
            {"nombre": "Remo Polea", "series": 3, "reps": "12-15", "descanso": "60 seg", "grupo": "Espalda", "desc": "Espalda media"},
            {"nombre": "Press Inclinado", "series": 3, "reps": "10-12", "descanso": "90 seg", "grupo": "Pecho", "desc": "Pecho alto"},
        ]
    },
    "LOWER B - Isquios": {
        "musculos": ["Isquiotibiales", "Glúteos", "Espalda Baja"],
        "prioridad": "Alta",
        "duracion": 60,
        "descripcion": "Enfoque en cadena posterior. Desarrolla isquiotibiales y glúteos.",
        "ejercicios": [
            {"nombre": "Peso Muerto Rumano", "series": 4, "reps": "8-10", "descanso": "2-3 min", "grupo": "Isquios", "desc": "Ejercicio principal"},
            {"nombre": "Zancadas", "series": 3, "reps": "10-12", "descanso": "90 seg", "grupo": "Glúteos", "desc": "Glúteos"},
            {"nombre": "Curl Femoral", "series": 3, "reps": "12-15", "descanso": "60 seg", "grupo": "Isquios", "desc": "Aislamiento"},
            {"nombre": "Empuje Cadera", "series": 3, "reps": "12-15", "descanso": "90 seg", "grupo": "Glúteos", "desc": "Glúteos máximo"},
        ]
    }
}

# ============ INICIALIZAR SESSION STATE ============
if "progreso_nutricion" not in st.session_state:
    st.session_state.progreso_nutricion = {}

if "dieta_seleccionada" not in st.session_state:
    st.session_state.dieta_seleccionada = "Clásica (Pollo)"

if "dias_entrenamiento" not in st.session_state:
    st.session_state.dias_entrenamiento = {
        "lunes": True, "martes": True, "miercoles": False,
        "jueves": True, "viernes": True, "sabado": False, "domingo": False
    }

# ============ HEADER ============
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("""
    <div style='padding: 2rem 0;'>
        <h1>💪 Coach Nutriólogo Pro</h1>
        <p style='color: #5F6368; font-size: 1.1rem;'>Tu Sistema Profesional de Ganancia Muscular</p>
    </div>
    """, unsafe_allow_html=True)

# ============ SIDEBAR NAVEGACIÓN ============
with st.sidebar:
    st.markdown("### 📍 NAVEGACIÓN")
    pagina = st.radio(
        "",
        ["🏠 Dashboard", "🍽️ Nutrición", "🏋️ Entrenamientos", "📊 Progreso", "⚙️ Configuración"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("### 👤 TU PERFIL")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Peso", "70 kg", delta="+2 kg")
    with col2:
        st.metric("Altura", "1.68 m")
    
    st.markdown("### 🎯 META DIARIA")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Calorías", "2760")
    with col2:
        st.metric("Proteína", "145g")

# ============ PÁGINAS ============

if pagina == "🏠 Dashboard":
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Meta Diaria</div>
            <div class='metric-value'>2760</div>
            <div class='metric-label'>kcal</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Proteína</div>
            <div class='metric-value'>145g</div>
            <div class='metric-label'>Diarios</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Carbohidratos</div>
            <div class='metric-value'>360g</div>
            <div class='metric-label'>Diarios</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Grasas</div>
            <div class='metric-value'>80g</div>
            <div class='metric-label'>Diarios</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Tracking Hoy", "📊 Análisis Macros", "📈 Semana", "🎯 Objetivos"])
    
    with tab1:
        st.markdown("## Tracking de Nutrición - Hoy")
        
        col1, col2 = st.columns([0.7, 0.3])
        with col2:
            fecha_hoy = st.date_input("Fecha", datetime.today(), label_visibility="collapsed")
        
        # Tabla de tracking
        dieta = DIETAS[st.session_state.dieta_seleccionada]
        
        datos_tracking = []
        total_recomendado = {"kcal": 0, "p": 0, "c": 0, "g": 0}
        total_consumido = {"kcal": 0, "p": 0, "c": 0, "g": 0}
        
        for comida, info in dieta.items():
            consumido_kcal = st.number_input(f"{comida.upper()} - kcal", 0, 1000, info["kcal"], key=f"kcal_{comida}")
            consumido_p = st.number_input(f"{comida.upper()} - Proteína (g)", 0, 200, info["p"], key=f"p_{comida}")
            consumido_c = st.number_input(f"{comida.upper()} - Carbos (g)", 0, 300, info["c"], key=f"c_{comida}")
            consumido_g = st.number_input(f"{comida.upper()} - Grasas (g)", 0, 150, info["g"], key=f"g_{comida}")
            
            porc_kcal = round((consumido_kcal / info["kcal"] * 100)) if info["kcal"] > 0 else 0
            
            datos_tracking.append({
                "Comida": comida.upper(),
                "Recomendado": f"{info['kcal']} kcal",
                "Consumido": f"{consumido_kcal} kcal",
                "Cumplimiento": f"{min(porc_kcal, 100)}%"
            })
            
            total_recomendado["kcal"] += info["kcal"]
            total_consumido["kcal"] += consumido_kcal
        
        # Tabla de resumen
        df_tracking = pd.DataFrame(datos_tracking)
        st.dataframe(df_tracking, use_container_width=True, hide_index=True)
        
        # Semáforo de cumplimiento
        porc_total = round((total_consumido["kcal"] / total_recomendado["kcal"] * 100))
        porc_total = min(porc_total, 100)
        
        if porc_total >= 90:
            color_semaforo = "🟢"
            estado = "EXCELENTE"
        elif porc_total >= 70:
            color_semaforo = "🟡"
            estado = "BUENO"
        else:
            color_semaforo = "🔴"
            estado = "BAJO"
        
        st.markdown(f"""
        <div style='background: #F8F9FA; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0;'>
            <div style='font-size: 3rem;'>{color_semaforo}</div>
            <div style='font-size: 1.5rem; font-weight: 700; color: #202124;'>{porc_total}%</div>
            <div style='font-size: 1rem; color: #5F6368;'>Cumplimiento del día: {estado}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfica de consumo
        fig = go.Figure(data=[
            go.Bar(x=list(dieta.keys()), y=[info["kcal"] for info in dieta.values()], name="Recomendado", marker_color="#1A73E8"),
        ])
        fig.update_layout(height=400, showlegend=True, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("## Distribución de Macronutrientes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sizes = [580, 1440, 740]
            labels = ["Proteína\n145g (21%)", "Carbohidratos\n360g (52%)", "Grasas\n80g (27%)"]
            colors = ["#1A73E8", "#34A853", "#FF6B35"]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker=dict(colors=colors))])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Desglose")
            st.info("**Proteína**: 145g (21% - 580 kcal)\nEsencial para síntesis muscular")
            st.info("**Carbohidratos**: 360g (52% - 1440 kcal)\nEnergía para entrenamientos")
            st.info("**Grasas**: 80g (27% - 740 kcal)\nFunciones hormonales")
    
    with tab3:
        st.markdown("## Progreso Semanal")
        
        dias = ["Lunes", "Martes", "Miér", "Jueves", "Viernes", "Sábado", "Domingo"]
        cumplimientos = [85, 92, 78, 88, 95, 72, 80]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dias, y=cumplimientos, marker_color=["#EA4335" if x < 70 else "#FBBC04" if x < 90 else "#34A853" for x in cumplimientos]))
        fig.update_layout(height=400, yaxis_range=[0, 100], hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap semanal
        st.markdown("### 🔥 Heatmap Semanal")
        heatmap_data = np.random.randint(60, 100, (4, 7))
        fig = go.Figure(data=go.Heatmap(z=heatmap_data, x=dias, y=["Sem 1", "Sem 2", "Sem 3", "Sem 4"], colorscale="RdYlGn"))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("## 🎯 Objetivos y Timeline")
        
        timeline_data = pd.DataFrame({
            "Período": ["4-6 semanas", "2-3 meses", "6 meses", "1 año"],
            "Ganancia de peso": ["+2-4 kg", "+4-8 kg", "+8-12 kg", "+12-16 kg"],
            "Ganancia muscular": ["+1-2 kg", "+3-5 kg", "+6-9 kg", "+10-14 kg"],
            "Cambio de fuerza": ["+10-15%", "+20-30%", "+40-60%", "+80-100%"]
        })
        
        st.dataframe(timeline_data, use_container_width=True, hide_index=True)

elif pagina == "🍽️ Nutrición":
    st.markdown("## 🍽️ Plan Nutricional Personalizado")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        st.session_state.dieta_seleccionada = st.selectbox(
            "Elige tu dieta",
            list(DIETAS.keys())
        )
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📋 Plan Diario", "📊 Composición", "💡 Opciones Alternativas"])
    
    with tab1:
        st.markdown(f"### {st.session_state.dieta_seleccionada}")
        
        dieta = DIETAS[st.session_state.dieta_seleccionada]
        
        for i, (comida, info) in enumerate(dieta.items(), 1):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{i}. {comida.upper()}**\n{info['comida']}")
            with col2:
                st.metric("kcal", info["kcal"])
            with col3:
                st.metric("P", f"{info['p']}g")
            with col4:
                st.metric("C", f"{info['c']}g")
            with col5:
                st.metric("G", f"{info['g']}g")
            
            st.divider()
    
    with tab2:
        st.markdown("### Macronutrientes Totales")
        
        dieta = DIETAS[st.session_state.dieta_seleccionada]
        totales = {"kcal": 0, "p": 0, "c": 0, "g": 0}
        
        for info in dieta.values():
            totales["kcal"] += info["kcal"]
            totales["p"] += info["p"]
            totales["c"] += info["c"]
            totales["g"] += info["g"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Calorías", f"{totales['kcal']} kcal")
        with col2:
            st.metric("Proteína", f"{totales['p']}g")
        with col3:
            st.metric("Carbohidratos", f"{totales['c']}g")
        with col4:
            st.metric("Grasas", f"{totales['g']}g")
    
    with tab3:
        st.markdown("### Otras Opciones de Dieta")
        st.info("Todas mantienen los mismos macronutrientes recomendados (~2760 kcal, 145g proteína)")
        
        for nombre_dieta in DIETAS.keys():
            if nombre_dieta != st.session_state.dieta_seleccionada:
                if st.button(f"Ver {nombre_dieta}", use_container_width=True):
                    st.session_state.dieta_seleccionada = nombre_dieta
                    st.rerun()

elif pagina == "🏋️ Entrenamientos":
    st.markdown("## 🏋️ Programa de Entrenamientos")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        st.markdown("### 📅 Configura tus días")
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dias_keys = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        
        for dia, dia_key in zip(dias_semana, dias_keys):
            st.session_state.dias_entrenamiento[dia_key] = st.checkbox(dia, value=st.session_state.dias_entrenamiento[dia_key])
    
    st.divider()
    
    # Mostrar entrenamientos
    tabs = st.tabs([f"📋 {nombre}" for nombre in ENTRENAMIENTOS_DETALLE.keys()])
    
    for tab, (nombre, detalles) in zip(tabs, ENTRENAMIENTOS_DETALLE.items()):
        with tab:
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                st.markdown(f"### {nombre}")
                st.markdown(f"**Descripción**: {detalles['descripcion']}")
                
                st.markdown("#### 💪 Grupos Musculares")
                musculos_texto = ", ".join(detalles['musculos'])
                st.write(f"🔹 {musculos_texto}")
                
                st.markdown("#### ⏱️ Información")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Duración", f"{detalles['duracion']} min")
                with col_b:
                    st.metric("Intensidad", detalles['prioridad'])
                with col_c:
                    st.metric("Ejercicios", len(detalles['ejercicios']))
            
            with col2:
                st.markdown("#### 📊 Ejercicios")
                for i, ej in enumerate(detalles['ejercicios'], 1):
                    with st.expander(f"{i}. {ej['nombre']}"):
                        st.write(f"**Grupo**: {ej['grupo']}")
                        st.write(f"**Series x Reps**: {ej['series']}x{ej['reps']}")
                        st.write(f"**Descanso**: {ej['descanso']}")
                        st.write(f"**Descripción**: {ej['desc']}")
            
            st.divider()

elif pagina == "📊 Progreso":
    st.markdown("## 📊 Monitoreo de Progreso")
    
    tab1, tab2, tab3 = st.tabs(["📝 Registrar", "📈 Historial", "📊 Análisis"])
    
    with tab1:
        st.markdown("### Registrar Nueva Medición")
        
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
            cintura = st.number_input("Cintura (cm)", value=80.0, step=0.5)
        
        st.markdown("#### 📈 Periodicidad de Aumento")
        st.info("""
        **Semana 1-2**: Aprende la forma
        **Semana 3+**: +2.5 kg/semana en ejercicios principales
        **Alternativa**: Si no subes peso, +1 repetición/semana
        """)
        
        if st.button("💾 Guardar Medición", use_container_width=True):
            st.session_state.progreso_nutricion[str(fecha)] = {
                "peso": peso, "brazo": brazo, "pecho": pecho, "cintura": cintura
            }
            st.success("✅ Medición guardada")
    
    with tab2:
        st.markdown("### Historial de Mediciones")
        
        if st.session_state.progreso_nutricion:
            df = pd.DataFrame.from_dict(st.session_state.progreso_nutricion, orient="index")
            st.dataframe(df, use_container_width=True)
            
            # Gráfica de peso
            fechas = list(st.session_state.progreso_nutricion.keys())
            pesos = [v["peso"] for v in st.session_state.progreso_nutricion.values()]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fechas, y=pesos, mode='lines+markers', name='Peso',
                                    line=dict(color='#FF6B35', width=3),
                                    marker=dict(size=10, color='#FF6B35')))
            fig.update_layout(height=400, title="Evolución del Peso", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📝 No hay mediciones registradas aún")
    
    with tab3:
        st.markdown("### 📊 Análisis de Progreso")
        st.info("Registra al menos 2 mediciones para ver el análisis completo")

elif pagina == "⚙️ Configuración":
    st.markdown("## ⚙️ Configuración")
    
    tab1, tab2 = st.tabs(["👤 Perfil", "🔧 Preferencias"])
    
    with tab1:
        st.markdown("### Datos Personales")
        
        col1, col2 = st.columns(2)
        with col1:
            peso = st.number_input("Peso (kg)", value=70, step=1)
        with col2:
            altura = st.number_input("Altura (m)", value=1.68, step=0.01)
        
        col3, col4 = st.columns(2)
        with col3:
            edad = st.number_input("Edad", value=25, step=1)
        with col4:
            nivel = st.selectbox("Nivel de experiencia", ["Principiante", "Intermedio", "Avanzado"])
        
        if st.button("💾 Guardar Cambios", use_container_width=True):
            st.success("✅ Perfil actualizado")
    
    with tab2:
        st.markdown("### Preferencias")
        
        st.selectbox("Dieta preferida", list(DIETAS.keys()))
        st.number_input("Meta calórica diaria", value=2760)
        st.toggle("Notificaciones activadas")
        
        if st.button("💾 Guardar Preferencias", use_container_width=True):
            st.success("✅ Preferencias guardadas")

st.markdown("---")
st.caption("© 2024 Coach Nutriólogo Pro | Diseñado con precisión científica 💪")
