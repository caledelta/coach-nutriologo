import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

st.set_page_config(page_title="Coach Nutriólogo Pro", page_icon="💪", layout="wide", initial_sidebar_state="expanded")

# ========== ESTILOS MINIMALISTAS ==========
st.markdown("""
<style>
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    body { background-color: #FAFAFA; color: #1F1F1F; }
    .main { background-color: #FAFAFA; }
    .stSidebar { background-color: #FFFFFF; border-right: 1px solid #E8E8E8; }
    h1 { color: #1F1F1F; font-size: 2.2rem; font-weight: 600; }
    h2 { color: #1F1F1F; font-size: 1.5rem; font-weight: 600; margin: 1.5rem 0 1rem 0; }
    h3 { color: #424242; font-size: 1.1rem; font-weight: 500; }
    .stat-box { background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 12px; padding: 1.2rem; text-align: center; }
    .stat-value { font-size: 2rem; font-weight: 700; color: #1F1F1F; }
    .stat-label { font-size: 0.85rem; color: #757575; text-transform: uppercase; }
    .stButton > button { background-color: #1F1F1F; color: #FFFFFF; width: 100%; border-radius: 8px; }
    .stButton > button:hover { background-color: #424242; }
    .meal-item { background: #FFFFFF; border-left: 3px solid #1F1F1F; padding: 1rem; border-radius: 8px; margin: 0.8rem 0; }
    .exercise-item { background: #FFFFFF; border: 1px solid #E8E8E8; padding: 1.2rem; border-radius: 12px; margin: 1rem 0; }
    .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.5rem; margin: 1rem 0; }
    .calendar-day { background: #FFFFFF; border: 1px solid #E8E8E8; padding: 0.8rem; border-radius: 8px; text-align: center; font-size: 0.8rem; }
    .calendar-day.active { background: #1F1F1F; color: white; }
    .calendar-day.partial { background: #E8E8E8; }
</style>
""", unsafe_allow_html=True)

# ========== BASE DE DATOS DE ALIMENTOS (GRAMOS/100g) ==========
ALIMENTOS = {
    "Avena": {"kcal": 389, "p": 17, "c": 66, "g": 7},
    "Huevo": {"kcal": 155, "p": 13, "c": 1.1, "g": 11},
    "Plátano": {"kcal": 89, "p": 1.1, "c": 23, "g": 0.3},
    "Leche entera": {"kcal": 64, "p": 3.2, "c": 4.8, "g": 3.6},
    "Yogur griego": {"kcal": 59, "p": 10, "c": 3.3, "g": 0.4},
    "Pechuga pollo": {"kcal": 165, "p": 31, "c": 0, "g": 3.6},
    "Arroz integral": {"kcal": 112, "p": 2.6, "c": 24, "g": 0.9},
    "Brócoli": {"kcal": 34, "p": 2.8, "c": 7, "g": 0.4},
    "Camote": {"kcal": 86, "p": 1.6, "c": 20, "g": 0.1},
    "Atún": {"kcal": 132, "p": 29, "c": 0, "g": 1.3},
    "Aguacate": {"kcal": 160, "p": 2, "c": 9, "g": 15},
    "Carne magra": {"kcal": 250, "p": 26, "c": 0, "g": 15},
    "Salmon": {"kcal": 208, "p": 20, "c": 0, "g": 13},
    "Lentejas": {"kcal": 116, "p": 9, "c": 20, "g": 0.4},
    "Pan integral": {"kcal": 265, "p": 9, "c": 49, "g": 3.3},
}

DIETAS = {
    "Pollo": {
        "desayuno": {"nombre": "Avena + Huevos + Plátano", "alimentos": [("Avena", 60), ("Huevo", 100), ("Leche entera", 200), ("Plátano", 120)]},
        "media_mañana": {"nombre": "Yogur + Frutos", "alimentos": [("Yogur griego", 200), ("Plátano", 100)]},
        "comida": {"nombre": "Arroz + Pollo + Brócoli", "alimentos": [("Arroz integral", 150), ("Pechuga pollo", 200), ("Brócoli", 150)]},
        "merienda": {"nombre": "Pan + Atún", "alimentos": [("Pan integral", 60), ("Atún", 150), ("Aguacate", 50)]},
        "cena": {"nombre": "Carne + Camote", "alimentos": [("Carne magra", 200), ("Camote", 150)]},
        "pre_dormir": {"nombre": "Leche", "alimentos": [("Leche entera", 250)]}
    }
}

ENTRENAMIENTOS = {
    "Tren Inferior A": {"musculos": ["Cuádriceps", "Glúteos"], "duracion": 70, "ejercicios": [
        ("Sentadilla Barra", "Cuádriceps", 4, "8-10"),
        ("Prensa Pierna", "Cuádriceps", 4, "10-12"),
        ("Empuje Cadera", "Glúteos", 4, "12-15"),
        ("Extensiones", "Cuádriceps", 3, "12-15"),
    ]},
    "Tren Superior A": {"musculos": ["Pecho", "Hombros"], "duracion": 55, "ejercicios": [
        ("Press Banca", "Pecho", 4, "8-10"),
        ("Prensa Militar", "Hombros", 3, "10-12"),
        ("Aperturas", "Pecho", 3, "12-15"),
    ]},
    "Tren Inferior B": {"musculos": ["Isquiotibiales", "Glúteos"], "duracion": 70, "ejercicios": [
        ("Peso Muerto Rumano", "Isquiotibiales", 4, "8-10"),
        ("Zancadas", "Glúteos", 3, "12-15"),
        ("Curl Femoral", "Isquiotibiales", 3, "12-15"),
    ]},
    "Tren Superior B": {"musculos": ["Espalda", "Bíceps"], "duracion": 55, "ejercicios": [
        ("Remo Barra", "Espalda", 4, "8-10"),
        ("Jalón", "Espalda", 3, "10-12"),
        ("Barra Rizada", "Bíceps", 3, "10-12"),
    ]}
}

# ========== INICIALIZAR SESSION ==========
if "registros_nutricion" not in st.session_state:
    st.session_state.registros_nutricion = []
if "registros_entrenamiento" not in st.session_state:
    st.session_state.registros_entrenamiento = []
if "peso_actual" not in st.session_state:
    st.session_state.peso_actual = 70.0
if "dieta" not in st.session_state:
    st.session_state.dieta = "Pollo"

# ========== FUNCIONES AUXILIARES ==========
def calcular_macros(alimento, gramos):
    """Calcular macros basado en gramos"""
    info = ALIMENTOS[alimento]
    return {
        "kcal": round((info["kcal"] * gramos) / 100, 1),
        "p": round((info["p"] * gramos) / 100, 1),
        "c": round((info["c"] * gramos) / 100, 1),
        "g": round((info["g"] * gramos) / 100, 1),
    }

def crear_cuerpo_humano(musculos_activos):
    """Crear SVG del cuerpo humano"""
    hombros_color = "#1F1F1F" if "Hombros" in musculos_activos else "#E8E8E8"
    pecho_color = "#1F1F1F" if "Pecho" in musculos_activos else "#E8E8E8"
    espalda_color = "#1F1F1F" if "Espalda" in musculos_activos else "#E8E8E8"
    core_color = "#1F1F1F" if "Core" in musculos_activos else "#E8E8E8"
    cuads_color = "#1F1F1F" if "Cuádriceps" in musculos_activos else "#E8E8E8"
    gluteos_color = "#1F1F1F" if "Glúteos" in musculos_activos else "#E8E8E8"
    biceps_color = "#1F1F1F" if "Bíceps" in musculos_activos else "#E8E8E8"
    isquios_color = "#1F1F1F" if "Isquiotibiales" in musculos_activos else "#E8E8E8"
    
    svg = f"""
    <svg viewBox="0 0 200 400" style="width:100%; max-width:200px; margin:0 auto;">
        <circle cx="100" cy="40" r="20" fill="#E8E8E8" stroke="#1F1F1F" stroke-width="2"/>
        <ellipse cx="100" cy="70" rx="45" ry="15" fill="{hombros_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="75" y="85" width="50" height="40" rx="5" fill="{pecho_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="75" y="130" width="50" height="30" rx="5" fill="{espalda_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="80" y="165" width="40" height="40" rx="3" fill="{core_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="70" y="215" width="25" height="80" rx="5" fill="{cuads_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="105" y="215" width="25" height="80" rx="5" fill="{cuads_color}" stroke="#1F1F1F" stroke-width="2"/>
        <ellipse cx="87" cy="210" rx="18" ry="22" fill="{gluteos_color}" stroke="#1F1F1F" stroke-width="2"/>
        <ellipse cx="113" cy="210" rx="18" ry="22" fill="{gluteos_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="45" y="90" width="20" height="60" rx="5" fill="{biceps_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="135" y="90" width="20" height="60" rx="5" fill="{biceps_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="70" y="280" width="25" height="20" rx="3" fill="{isquios_color}" stroke="#1F1F1F" stroke-width="2"/>
        <rect x="105" y="280" width="25" height="20" rx="3" fill="{isquios_color}" stroke="#1F1F1F" stroke-width="2"/>
    </svg>
    """
    return svg

# ========== HEADER ==========
st.markdown("# Coach Nutriólogo Pro")
st.markdown("Sistema avanzado de entrenamiento y nutrición basado en registro detallado")
st.divider()

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("## Navegación")
    pagina = st.radio("", ["Inicio", "Nutrición", "Entrenamientos", "Registros", "Configuración"], label_visibility="collapsed")
    
    st.divider()
    
    st.markdown("### Tu Perfil")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{st.session_state.peso_actual:.1f}</div><div class="stat-label">kg</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><div class="stat-value">1.68</div><div class="stat-label">m</div></div>', unsafe_allow_html=True)

# ========== PÁGINA: INICIO ==========
if pagina == "Inicio":
    col1, col2 = st.columns([0.65, 0.35])
    
    with col1:
        st.markdown("## Tu Meta de Hoy")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a: st.markdown('<div class="stat-box"><div class="stat-value">2760</div><div class="stat-label">kcal</div></div>', unsafe_allow_html=True)
        with col_b: st.markdown('<div class="stat-box"><div class="stat-value">145g</div><div class="stat-label">Proteína</div></div>', unsafe_allow_html=True)
        with col_c: st.markdown('<div class="stat-box"><div class="stat-value">360g</div><div class="stat-label">Carbos</div></div>', unsafe_allow_html=True)
        with col_d: st.markdown('<div class="stat-box"><div class="stat-value">80g</div><div class="stat-label">Grasas</div></div>', unsafe_allow_html=True)
        
        st.markdown("## Calendario de Cumplimiento")
        
        # Crear calendario
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        
        st.markdown("**Nutrición (Verde=Cumplido, Amarillo=Parcial, Gris=Incumplido)**")
        
        dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
        
        # Registros del mes actual
        registros_hoy = [r for r in st.session_state.registros_nutricion if r["fecha"].startswith(hoy.strftime("%Y-%m"))]
        fechas_registradas = set(r["fecha"] for r in registros_hoy)
        
        fecha_actual = inicio_mes
        cal_html = '<div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:8px; margin:1rem 0;">'
        
        # Headers
        for dia in dias_semana:
            cal_html += f'<div style="text-align:center; font-weight:600; font-size:0.8rem; color:#757575;">{dia}</div>'
        
        # Días
        dias_mostrar = (inicio_mes.weekday()) % 7
        for _ in range(dias_mostrar):
            cal_html += '<div></div>'
        
        while fecha_actual.month == hoy.month:
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            
            if fecha_str in fechas_registradas:
                color = "#1F1F1F"
            else:
                color = "#E8E8E8"
            
            cal_html += f'<div style="background:{color}; padding:0.8rem; border-radius:8px; text-align:center; font-size:0.8rem; color:white; font-weight:600;">{fecha_actual.day}</div>'
            
            fecha_actual += timedelta(days=1)
        
        cal_html += '</div>'
        st.markdown(cal_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("## Próximo Entrenamiento")
        st.markdown("**Lunes** — Tren Inferior A (70 min)")
        
        # Cuerpo humano
        st.markdown("### Musculos a Entrenar")
        st.markdown(crear_cuerpo_humano(["Cuádriceps", "Glúteos"]), unsafe_allow_html=True)

# ========== PÁGINA: NUTRICIÓN ==========
elif pagina == "Nutrición":
    st.markdown("## Plan Nutricional Detallado")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        st.session_state.dieta = st.selectbox("Elige tu dieta", list(DIETAS.keys()), label_visibility="collapsed")
    
    st.divider()
    
    dieta = DIETAS[st.session_state.dieta]
    
    for comida_key, comida_info in dieta.items():
        with st.container():
            st.markdown(f"### {comida_key.upper()}")
            st.markdown(f"*{comida_info['nombre']}*")
            
            total_macros = {"kcal": 0, "p": 0, "c": 0, "g": 0}
            
            st.markdown("#### Desglose de Alimentos")
            
            tabla_alimentos = []
            
            for alimento, gramos in comida_info["alimentos"]:
                macros = calcular_macros(alimento, gramos)
                
                tabla_alimentos.append({
                    "Alimento": alimento,
                    "Gramos": gramos,
                    "kcal": macros["kcal"],
                    "Proteína (g)": macros["p"],
                    "Carbos (g)": macros["c"],
                    "Grasas (g)": macros["g"]
                })
                
                for key in total_macros:
                    total_macros[key] += macros[key]
            
            df = pd.DataFrame(tabla_alimentos)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Total kcal", round(total_macros["kcal"]))
            with col2: st.metric("Proteína", f"{round(total_macros['p'])}g")
            with col3: st.metric("Carbos", f"{round(total_macros['c'])}g")
            with col4: st.metric("Grasas", f"{round(total_macros['g'])}g")
            
            st.divider()

# ========== PÁGINA: ENTRENAMIENTOS ==========
elif pagina == "Entrenamientos":
    st.markdown("## Programa de Entrenamientos")
    
    tabs = st.tabs(list(ENTRENAMIENTOS.keys()))
    
    for tab, (nombre, detalles) in zip(tabs, ENTRENAMIENTOS.items()):
        with tab:
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                st.markdown(f"### {nombre}")
                st.markdown(f"**Duración**: {detalles['duracion']} min")
                st.markdown("#### Ejercicios")
                
                for i, (ejercicio, musculo, series, reps) in enumerate(detalles["ejercicios"], 1):
                    st.markdown(f'<div class="exercise-item"><h4>{i}. {ejercicio}</h4><div class="exercise-meta">{series}x{reps} | {musculo}</div></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### Músculos Trabajados")
                st.markdown(crear_cuerpo_humano(detalles["musculos"]), unsafe_allow_html=True)
                
                st.markdown(f"**Grupos principales**:")
                for musculo in detalles["musculos"]:
                    st.write(f"🔹 {musculo}")

# ========== PÁGINA: REGISTROS ==========
elif pagina == "Registros":
    st.markdown("## Registro de Seguimiento")
    
    tab1, tab2, tab3 = st.tabs(["Registrar Nutrición", "Registrar Entrenamiento", "Ver Registros"])
    
    with tab1:
        st.markdown("### Registrar Consumo Nutricional")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_nut = st.date_input("Fecha", key="fecha_nut")
        with col2:
            hora_nut = st.time_input("Hora", key="hora_nut")
        with col3:
            comida = st.selectbox("Comida", ["Desayuno", "Media Mañana", "Comida", "Merienda", "Cena", "Pre-dormir"])
        
        dieta_actual = DIETAS[st.session_state.dieta]
        comida_key = list(dieta_actual.keys())[["Desayuno", "Media Mañana", "Comida", "Merienda", "Cena", "Pre-dormir"].index(comida)]
        comida_info = dieta_actual[comida_key]
        
        st.markdown("#### Alimentos Consumidos")
        
        kcal_total = 0
        p_total = 0
        c_total = 0
        g_total = 0
        
        consumo_alimentos = {}
        
        for alimento, gramos_recomendados in comida_info["alimentos"]:
            gramos_consumidos = st.number_input(f"{alimento} (g)", value=gramos_recomendados, key=f"gramos_{alimento}")
            macros = calcular_macros(alimento, gramos_consumidos)
            consumo_alimentos[alimento] = {"gramos": gramos_consumidos, "macros": macros}
            
            kcal_total += macros["kcal"]
            p_total += macros["p"]
            c_total += macros["c"]
            g_total += macros["g"]
        
        st.markdown("#### Totales")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("kcal", round(kcal_total))
        with col2: st.metric("Proteína (g)", round(p_total, 1))
        with col3: st.metric("Carbos (g)", round(c_total, 1))
        with col4: st.metric("Grasas (g)", round(g_total, 1))
        
        if st.button("Guardar Registro Nutrición"):
            st.session_state.registros_nutricion.append({
                "fecha": str(fecha_nut),
                "hora": str(hora_nut),
                "comida": comida,
                "kcal": round(kcal_total, 1),
                "proteina": round(p_total, 1),
                "carbos": round(c_total, 1),
                "grasas": round(g_total, 1),
                "alimentos": consumo_alimentos
            })
            st.success("✓ Registro guardado")
    
    with tab2:
        st.markdown("### Registrar Entrenamiento")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_ent = st.date_input("Fecha", key="fecha_ent")
        with col2:
            hora_ent = st.time_input("Hora", key="hora_ent")
        
        tipo_entrenamiento = st.selectbox("Tipo de Entrenamiento", list(ENTRENAMIENTOS.keys()))
        detalles_ent = ENTRENAMIENTOS[tipo_entrenamiento]
        
        st.markdown("#### Registros de Ejercicios")
        
        registros_ejercicios = []
        
        for i, (ejercicio, musculo, series_default, reps_default) in enumerate(detalles_ent["ejercicios"]):
            with st.expander(f"**{i+1}. {ejercicio}**"):
                col1, col2, col3 = st.columns(3)
                
                # Extraer número de series del formato "4x8-10"
                series_num = int(series_default.split("x")[0]) if "x" in series_default else 4
                
                with col1:
                    series_realizadas = st.number_input(
                        f"Series", 
                        value=series_num, 
                        min_value=1,
                        key=f"series_{i}"
                    )
                with col2:
                    reps_realizadas = st.text_input(
                        f"Reps (ej: 8-10)", 
                        value=reps_default, 
                        key=f"reps_{i}"
                    )
                with col3:
                    peso_usado = st.number_input(
                        f"Peso (kg)", 
                        value=0.0, 
                        step=2.5, 
                        key=f"peso_{i}"
                    )
                
                registros_ejercicios.append({
                    "ejercicio": ejercicio,
                    "musculo": musculo,
                    "series": int(series_realizadas),
                    "reps": reps_realizadas,
                    "peso": peso_usado
                })
        
        lugar = st.radio("Lugar de Entrenamiento", ["Gimnasio", "Casa"])
        notas = st.text_area("Notas")
        
        if st.button("Guardar Registro Entrenamiento"):
            st.session_state.registros_entrenamiento.append({
                "fecha": str(fecha_ent),
                "hora": str(hora_ent),
                "tipo": tipo_entrenamiento,
                "lugar": lugar,
                "ejercicios": registros_ejercicios,
                "notas": notas
            })
            st.success("✓ Registro guardado")
    
    with tab3:
        st.markdown("### Historial de Registros")
        
        if st.session_state.registros_nutricion:
            st.markdown("#### Nutrición")
            df_nut = pd.DataFrame(st.session_state.registros_nutricion)
            st.dataframe(df_nut[["fecha", "hora", "comida", "kcal", "proteina", "carbos", "grasas"]], use_container_width=True, hide_index=True)
        
        if st.session_state.registros_entrenamiento:
            st.markdown("#### Entrenamiento")
            df_ent = pd.DataFrame(st.session_state.registros_entrenamiento)
            st.dataframe(df_ent[["fecha", "hora", "tipo", "lugar"]], use_container_width=True, hide_index=True)

# ========== PÁGINA: CONFIGURACIÓN ==========
elif pagina == "Configuración":
    st.markdown("## Configuración")
    
    col1, col2 = st.columns(2)
    with col1:
        nuevo_peso = st.number_input("Peso actual (kg)", value=st.session_state.peso_actual, step=0.1)
        st.session_state.peso_actual = nuevo_peso
    with col2:
        st.number_input("Altura (m)", value=1.68, step=0.01)
    
    st.divider()
    
    st.markdown("### Integración con OKOK Internacional")
    st.markdown("Para sincronizar datos de tu báscula electrónica:")
    st.info("""
    1. En la app OKOK Internacional, ve a Configuración
    2. Busca "Sincronizar" o "Export"
    3. Descarga los datos en CSV o JSON
    4. Carga el archivo aquí
    """)
    
    archivo_okok = st.file_uploader("Cargar archivo OKOK", type=["csv", "json"])
    
    if archivo_okok:
        if archivo_okok.type == "application/json":
            datos_okok = json.loads(archivo_okok.getvalue())
            st.success(f"✓ Datos importados: {len(datos_okok)} registros")
        else:
            df_okok = pd.read_csv(archivo_okok)
            st.dataframe(df_okok)
            st.success("✓ Archivo OKOK cargado")

st.divider()
st.caption("Coach Nutriólogo Pro © 2024 | Registro avanzado de progreso")
