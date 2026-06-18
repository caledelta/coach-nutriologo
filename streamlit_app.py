import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Coach Nutriólogo Pro",
    page_icon="💪",
    layout="wide"
)

st.markdown("""
<style>
body { background-color: #0F0F0F; color: #E8E8E8; }
.main { background-color: #0F0F0F; }
.stSidebar { background-color: #0D1B2A; }
h1, h2, h3 { color: #E8E8E8; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

PROGRAMA = {
    "perfil": {"peso": 70, "altura": 1.68, "nivel": "Principiante"},
    "macros": {"proteina": 145, "carbs": 360, "grasas": 80, "total_kcal": 2760},
    "nutricion": {
        "desayuno": {"nombre": "Avena + Huevos + Plátano", "kcal": 520, "p": 25, "c": 65, "g": 18},
        "media_mañana": {"nombre": "Yogur + Frutos Secos", "kcal": 320, "p": 22, "c": 35, "g": 12},
        "comida": {"nombre": "Arroz + Pechuga", "kcal": 720, "p": 45, "c": 75, "g": 20},
        "merienda": {"nombre": "Pan + Proteína", "kcal": 380, "p": 28, "c": 35, "g": 15},
        "cena": {"nombre": "Carne + Camote", "kcal": 520, "p": 40, "c": 60, "g": 12},
        "pre_dormir": {"nombre": "Leche + Proteína", "kcal": 300, "p": 30, "c": 20, "g": 10}
    }
}

if "progreso" not in st.session_state:
    st.session_state.progreso = []

st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1>💪 Coach Nutriólogo Pro</h1>
    <p style='color: #FFB703; font-size: 1.1rem;'>Tu Sistema de Ganancia Muscular</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📍 NAVEGACIÓN")
    pagina = st.radio("", ["🏠 Dashboard", "🍽️ Nutrición", "🏋️ Entrenamientos", "📊 Progreso", "⚙️ Configuración"], label_visibility="collapsed")
    st.divider()
    st.metric("Peso", "70 kg")
    st.metric("Altura", "1.68 m")

if pagina == "🏠 Dashboard":
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Meta Diaria", "2760 kcal")
    with col2: st.metric("Proteína", "145g")
    with col3: st.metric("Carbohidratos", "360g")
    with col4: st.metric("Grasas", "80g")
    
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Hoy", "🏋️ Semana", "🎯 Objetivos"])
    
    with tab1:
        st.subheader("Macros de Hoy")
        col1, col2 = st.columns(2)
        with col1:
            labels = ["Proteína", "Carbos", "Grasas"]
            sizes = [580, 1440, 740]
            colors = ["#FF6B35", "#FFB703", "#06A77D"]
            fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker=dict(colors=colors))])
            fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#E8E8E8"))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.info("✅ **Superávit Controlado**: +360 kcal sobre mantenimiento (2400 kcal)")
    
    with tab2:
        st.markdown("### Plan Semanal")
        cols = st.columns(7)
        dias = ["Lunes\nUPPER A", "Martes\nLOWER A", "Miércoles\nDescanso", "Jueves\nUPPER B", "Viernes\nLOWER B", "Sábado\nDescanso", "Domingo\nDescanso"]
        for col, dia in zip(cols, dias):
            with col: st.info(dia)
    
    with tab3:
        df = pd.DataFrame({
            "Período": ["4-6 semanas", "2-3 meses", "6 meses", "1 año"],
            "Cambio": ["+2-4 kg", "+4-8 kg", "+8-12 kg", "+12-16 kg"]
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

elif pagina == "🍽️ Nutrición":
    st.subheader("🍽️ Plan Nutricional (2760 kcal)")
    
    tab1, tab2 = st.tabs(["📋 Plan Diario", "📊 Macros"])
    
    with tab1:
        for nombre, datos in PROGRAMA["nutricion"].items():
            st.write(f"**{nombre.upper()}** - {datos['nombre']} ({datos['kcal']} kcal)")
            st.caption(f"P: {datos['p']}g | C: {datos['c']}g | G: {datos['g']}g")
            st.divider()
    
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Proteína", "145g (21%)")
        with col2: st.metric("Carbohidratos", "360g (52%)")
        with col3: st.metric("Grasas", "80g (27%)")
        
        st.info("✅ Proteína distribuida en 6 comidas para máxima síntesis proteica")

elif pagina == "🏋️ Entrenamientos":
    st.subheader("🏋️ Rutina Upper/Lower 4 Días")
    
    entrenamientos = {
        "LUNES - UPPER A (Empuje)": [
            ("Press Banca Plano", "4x8-10", "2 min"),
            ("Prensa Militar", "3x10-12", "90 seg"),
            ("Aperturas Polea", "3x12-15", "60 seg"),
            ("Elevaciones Laterales", "3x12-15", "60 seg"),
            ("Barra Rizada", "3x10-12", "60 seg"),
        ],
        "MARTES - LOWER A (Cuádriceps)": [
            ("Sentadilla Barra", "4x8-10", "2-3 min"),
            ("Prensa Pierna", "3x10-12", "2 min"),
            ("Extensiones Cuádriceps", "3x12-15", "60 seg"),
            ("Pantorrillas", "4x15-20", "60 seg"),
            ("Plancha Abdominal", "3x45s", "45 seg"),
        ],
        "JUEVES - UPPER B (Jalón)": [
            ("Remo Barra", "4x8-10", "2 min"),
            ("Jalón Pecho", "3x10-12", "90 seg"),
            ("Remo Polea Baja", "3x12-15", "60 seg"),
            ("Press Banca Inclinado", "3x10-12", "90 seg"),
            ("Extensión Tríceps", "3x12-15", "60 seg"),
        ],
        "VIERNES - LOWER B (Isquios)": [
            ("Peso Muerto Rumano", "4x8-10", "2-3 min"),
            ("Zancadas Mancuernas", "3x10-12", "90 seg"),
            ("Curl Femoral", "3x12-15", "60 seg"),
            ("Empuje Cadera", "3x12-15", "90 seg"),
            ("Crunch Polea", "3x15", "60 seg"),
        ]
    }
    
    for dia, ejercicios in entrenamientos.items():
        with st.expander(f"**{dia}**"):
            for i, (nombre, series, descanso) in enumerate(ejercicios, 1):
                st.write(f"{i}. **{nombre}** → {series} | Descanso: {descanso}")

elif pagina == "📊 Progreso":
    st.subheader("📊 Monitoreo de Progreso")
    
    tab1, tab2 = st.tabs(["📝 Registrar", "📈 Historial"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1: fecha = st.date_input("Fecha")
        with col2: peso = st.number_input("Peso (kg)", value=70.0, step=0.1)
        
        if st.button("💾 Guardar Medición"):
            st.session_state.progreso.append({"fecha": str(fecha), "peso": peso})
            st.success("✅ Medición guardada")
    
    with tab2:
        if st.session_state.progreso:
            df = pd.DataFrame(st.session_state.progreso)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if len(st.session_state.progreso) > 1:
                fechas = [p["fecha"] for p in st.session_state.progreso]
                pesos = [p["peso"] for p in st.session_state.progreso]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=fechas, y=pesos, mode='lines+markers', name='Peso',
                                        line=dict(color='#FF6B35', width=3),
                                        marker=dict(size=8, color='#FFB703')))
                fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,15,15,0.5)", font=dict(color="#E8E8E8"))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📝 No hay mediciones registradas")

elif pagina == "⚙️ Configuración":
    st.subheader("⚙️ Configuración")
    
    col1, col2 = st.columns(2)
    with col1: st.number_input("Peso (kg)", value=70, step=1)
    with col2: st.number_input("Altura (m)", value=1.68, step=0.01)
    
    if st.button("💾 Guardar"):
        st.success("✅ Configuración guardada")

st.markdown("---")
st.caption("© 2024 Coach Nutriólogo Pro | Hecho con ciencia 💪")
