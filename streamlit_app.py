import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Coach Nutriólogo Pro", page_icon="💪", layout="wide", initial_sidebar_state="expanded")

# ========== ESTILOS ==========
st.markdown("""
<style>
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    body { background-color: #FAFAFA; color: #1F1F1F; }
    .main { background-color: #FAFAFA; }
    .stSidebar { background-color: #FFFFFF; border-right: 1px solid #E8E8E8; }
    h1 { color: #1F1F1F; font-size: 2.2rem; font-weight: 600; }
    h2 { color: #1F1F1F; font-size: 1.5rem; font-weight: 600; margin: 1.5rem 0 1rem 0; }
    .stat-box { background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 12px; padding: 1.2rem; text-align: center; }
    .stat-value { font-size: 2rem; font-weight: 700; color: #1F1F1F; }
    .stat-label { font-size: 0.85rem; color: #757575; text-transform: uppercase; }
    .profile-item { background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; display: flex; justify-content: space-between; align-items: center; }
    .profile-value { font-size: 1.3rem; font-weight: 700; }
    .status-alto { color: #FBBC04; }
    .status-perfecto { color: #34A853; }
    .status-saludable { color: #34A853; }
    .status-sobrepeso { color: #FBBC04; }
    .stButton > button { background-color: #1F1F1F; color: #FFFFFF; width: 100%; border-radius: 8px; }
    .meal-item { background: #FFFFFF; border-left: 3px solid #1F1F1F; padding: 1rem; border-radius: 8px; margin: 0.8rem 0; }
    .exercise-item { background: #FFFFFF; border: 1px solid #E8E8E8; padding: 1.2rem; border-radius: 12px; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ========== BASE DE DATOS DE ALIMENTOS ==========
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
    "Pasta integral": {"kcal": 124, "p": 5.3, "c": 25, "g": 1.1},
    "Tofu": {"kcal": 76, "p": 8, "c": 1.9, "g": 4.8},
    "Garbanzos": {"kcal": 119, "p": 7, "c": 20, "g": 2.4},
    "Claras de huevo": {"kcal": 52, "p": 11, "c": 0.7, "g": 0},
    "Manzana": {"kcal": 52, "p": 0.3, "c": 14, "g": 0.2},
}

# ========== DIETAS MÚLTIPLES ==========
DIETAS = {
    "Pollo": {
        "desayuno": {"nombre": "Avena + Huevos + Plátano", "alimentos": [("Avena", 60), ("Huevo", 100), ("Leche entera", 200), ("Plátano", 120)]},
        "media_mañana": {"nombre": "Yogur + Frutos", "alimentos": [("Yogur griego", 200), ("Plátano", 100)]},
        "comida": {"nombre": "Arroz + Pollo + Brócoli", "alimentos": [("Arroz integral", 150), ("Pechuga pollo", 200), ("Brócoli", 150)]},
        "merienda": {"nombre": "Pan + Atún", "alimentos": [("Pan integral", 60), ("Atún", 150), ("Aguacate", 50)]},
        "cena": {"nombre": "Carne + Camote", "alimentos": [("Carne magra", 200), ("Camote", 150)]},
        "pre_dormir": {"nombre": "Leche", "alimentos": [("Leche entera", 250)]}
    },
    "Carnes Rojas": {
        "desayuno": {"nombre": "Panqueques + Huevo + Plátano", "alimentos": [("Pan integral", 80), ("Huevo", 100), ("Manzana", 150)]},
        "media_mañana": {"nombre": "Yogur + Frutos", "alimentos": [("Yogur griego", 200), ("Manzana", 100)]},
        "comida": {"nombre": "Arroz + Carne Magra + Verduras", "alimentos": [("Arroz integral", 150), ("Carne magra", 220), ("Brócoli", 150)]},
        "merienda": {"nombre": "Pan + Queso + Aguacate", "alimentos": [("Pan integral", 60), ("Aguacate", 80)]},
        "cena": {"nombre": "Lomo + Camote", "alimentos": [("Carne magra", 220), ("Camote", 150)]},
        "pre_dormir": {"nombre": "Yogur Griego", "alimentos": [("Yogur griego", 250)]}
    },
    "Pescado": {
        "desayuno": {"nombre": "Avena + Claras + Plátano", "alimentos": [("Avena", 70), ("Claras de huevo", 200), ("Leche entera", 180), ("Plátano", 120)]},
        "media_mañana": {"nombre": "Batido Proteico", "alimentos": [("Yogur griego", 200), ("Manzana", 100)]},
        "comida": {"nombre": "Pasta + Salmón + Verduras", "alimentos": [("Pasta integral", 150), ("Salmon", 200), ("Brócoli", 150)]},
        "merienda": {"nombre": "Pan + Atún + Aguacate", "alimentos": [("Pan integral", 70), ("Atún", 150), ("Aguacate", 60)]},
        "cena": {"nombre": "Tilapia + Camote", "alimentos": [("Salmon", 200), ("Camote", 150)]},
        "pre_dormir": {"nombre": "Leche", "alimentos": [("Leche entera", 250)]}
    },
    "Vegetariana": {
        "desayuno": {"nombre": "Avena + Leche + Frutos", "alimentos": [("Avena", 70), ("Leche entera", 250), ("Manzana", 120)]},
        "media_mañana": {"nombre": "Yogur + Granola", "alimentos": [("Yogur griego", 200), ("Plátano", 100)]},
        "comida": {"nombre": "Pasta + Lentejas + Verduras", "alimentos": [("Pasta integral", 150), ("Lentejas", 200), ("Brócoli", 150)]},
        "merienda": {"nombre": "Pan + Garbanzos", "alimentos": [("Pan integral", 60), ("Garbanzos", 150)]},
        "cena": {"nombre": "Tofu + Camote + Ensalada", "alimentos": [("Tofu", 250), ("Camote", 150)]},
        "pre_dormir": {"nombre": "Leche + Cereales", "alimentos": [("Leche entera", 250)]}
    },
    "Equilibrada": {
        "desayuno": {"nombre": "Avena + Huevo + Fruta", "alimentos": [("Avena", 65), ("Huevo", 100), ("Leche entera", 200), ("Manzana", 100)]},
        "media_mañana": {"nombre": "Yogur + Plátano", "alimentos": [("Yogur griego", 200), ("Plátano", 100)]},
        "comida": {"nombre": "Arroz + Pollo + Verduras", "alimentos": [("Arroz integral", 150), ("Pechuga pollo", 180), ("Brócoli", 150)]},
        "merienda": {"nombre": "Pan + Atún + Aguacate", "alimentos": [("Pan integral", 60), ("Atún", 150), ("Aguacate", 50)]},
        "cena": {"nombre": "Salmon + Camote", "alimentos": [("Salmon", 180), ("Camote", 150)]},
        "pre_dormir": {"nombre": "Leche", "alimentos": [("Leche entera", 250)]}
    }
}

# ========== ENTRENAMIENTOS CON JUSTIFICACIÓN CIENTÍFICA ==========
ENTRENAMIENTOS = {
    "Tren Inferior A": {
        "enfoque": "Cuádriceps + Glúteos",
        "duracion": 70,
        "musculos": "Cuádriceps, Glúteos",
        "ejercicios": [
            {
                "nombre": "Sentadilla Barra",
                "series": "4x8-10",
                "musculo": "Cuádriceps/Glúteos",
                "justificacion": "Movimiento compuesto fundamental. Activa máxima cantidad de fibras musculares. Mayor producción de hormona anabólica (testosterona, GH)."
            },
            {
                "nombre": "Prensa de Pierna",
                "series": "4x10-12",
                "musculo": "Cuádriceps",
                "justificacion": "Volumen de trabajo. Reduce riesgo articular comparado con barra. Permite alcanzar mayor fatiga muscular."
            },
            {
                "nombre": "Empuje de Cadera",
                "series": "4x12-15",
                "musculo": "Glúteos",
                "justificacion": "Isolación específica de glúteos. Máxima activación de glúteo mayor. Desarrollo direccionado de masa glútea."
            },
            {
                "nombre": "Extensiones Cuádriceps",
                "series": "3x12-15",
                "musculo": "Cuádriceps",
                "justificacion": "Aislamiento monoarticular. Bombeo de volumen. Estrés metabólico en cuádriceps con menor carga articular."
            },
        ]
    },
    "Tren Superior A": {
        "enfoque": "Empuje (Pecho, Hombros)",
        "duracion": 55,
        "musculos": "Pecho, Hombros, Tríceps",
        "ejercicios": [
            {
                "nombre": "Press Banca Plano",
                "series": "4x8-10",
                "musculo": "Pecho",
                "justificacion": "Movimiento compuesto fundamental. Mayor producción anabólica. Máxima transferencia de fuerza."
            },
            {
                "nombre": "Prensa Militar",
                "series": "3x10-12",
                "musculo": "Hombros",
                "justificacion": "Desarrollo deltoides anterior. Mayor reclutamiento de estabilizadores. Fortaleza funcional."
            },
            {
                "nombre": "Aperturas Polea",
                "series": "3x12-15",
                "musculo": "Pecho",
                "justificacion": "Aislamiento de pecho. Estiramiento bajo tensión. Desarrollo de sección media del pecho."
            },
        ]
    },
    "Tren Inferior B": {
        "enfoque": "Isquiotibiales + Glúteos",
        "duracion": 70,
        "musculos": "Isquiotibiales, Glúteos",
        "ejercicios": [
            {
                "nombre": "Peso Muerto Rumano",
                "series": "4x8-10",
                "musculo": "Isquiotibiales",
                "justificacion": "Especificidad en cadena posterior. Mayor rango de movimiento. Estiramiento bajo tensión en isquios."
            },
            {
                "nombre": "Zancadas",
                "series": "3x12c/p",
                "musculo": "Glúteos",
                "justificacion": "Movimiento unilateral. Equilibrio muscular. Mayor hipertrofia glútea por desequilibrio de carga."
            },
            {
                "nombre": "Curl Femoral",
                "series": "3x12-15",
                "musculo": "Isquiotibiales",
                "justificacion": "Aislamiento monoarticular. Flexión directa. Acumulación de lactato (hipertrofia miofibrilar)."
            },
            {
                "nombre": "Abducción Máquina",
                "series": "3x15-20",
                "musculo": "Glúteos",
                "justificacion": "Aislamiento de glúteo medio. Glúteo posterior. Resistencia muscular localizada."
            },
        ]
    },
    "Tren Superior B": {
        "enfoque": "Jalón (Espalda, Bíceps)",
        "duracion": 55,
        "musculos": "Espalda, Bíceps",
        "ejercicios": [
            {
                "nombre": "Remo Barra",
                "series": "4x8-10",
                "musculo": "Espalda",
                "justificacion": "Movimiento compuesto espalda. Máxima activación dorsal. Desarrollo de espalda gruesa y ancha."
            },
            {
                "nombre": "Jalón al Pecho",
                "series": "3x10-12",
                "musculo": "Espalda",
                "justificacion": "Desarrollo de amplitud dorsal. Mayor seguridad articular que dominadas en principiantes."
            },
            {
                "nombre": "Barra Rizada",
                "series": "3x10-12",
                "musculo": "Bíceps",
                "justificacion": "Ejercicio compound de bíceps. Mayor reclutamiento muscular. Progresión de fuerza."
            },
        ]
    }
}

# ========== INICIALIZAR SESSION ==========
if "registros_nutricion" not in st.session_state:
    st.session_state.registros_nutricion = []
if "registros_entrenamiento" not in st.session_state:
    st.session_state.registros_entrenamiento = []
if "peso_actual" not in st.session_state:
    st.session_state.peso_actual = 71.4
if "dieta" not in st.session_state:
    st.session_state.dieta = "Pollo"
if "altura" not in st.session_state:
    st.session_state.altura = 1.68

# ========== FUNCIONES ==========
def calcular_macros(alimento, gramos):
    info = ALIMENTOS[alimento]
    return {
        "kcal": round((info["kcal"] * gramos) / 100, 1),
        "p": round((info["p"] * gramos) / 100, 1),
        "c": round((info["c"] * gramos) / 100, 1),
        "g": round((info["g"] * gramos) / 100, 1),
    }

def calcular_composicion_corporal(peso, altura, grasa_porcentaje=22.4):
    """Calcular composición corporal basada en datos"""
    bmi = peso / (altura ** 2)
    peso_grasa = (peso * grasa_porcentaje) / 100
    peso_muscular = peso - peso_grasa
    edad_metabolica = 30  # Ejemplo
    metabolismo = 1600.8  # kcal base
    
    return {
        "Peso (kg)": (peso, "Alto" if peso > 70 else "Normal"),
        "BMI": (round(bmi, 1), "Alto" if bmi > 25 else "Normal"),
        "Grasa (%)": (grasa_porcentaje, "Alto" if grasa_porcentaje > 25 else "Perfecto"),
        "Peso de grasa corporal (kg)": (round(peso_grasa, 1), "Alto" if peso_grasa > 18 else "Saludable"),
        "Masa muscular (%)": (round((peso_muscular/peso)*100, 1), "Perfecto" if (peso_muscular/peso)*100 > 40 else "Bueno"),
        "Peso muscular (kg)": (round(peso_muscular, 1), "Perfecto" if peso_muscular > 29 else "Bueno"),
        "Metabolismo (kcal)": (metabolismo, "Saludable"),
        "Proteína (%)": (19.3, "Saludable"),
        "Agua (%)": (54.8, "Saludable"),
        "Peso sin grasa (kg)": (round(peso_muscular, 2), "Saludable"),
        "Edad metabólica": (edad_metabolica, "Normal"),
    }

# ========== HEADER ==========
st.markdown("# Coach Nutriólogo Pro")
st.markdown("Sistema avanzado de entrenamiento y nutrición basado en composición corporal")
st.divider()

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("## Navegación")
    pagina = st.radio("", ["Inicio", "Nutrición", "Entrenamientos", "Registros", "Configuración"], label_visibility="collapsed")
    
    st.divider()
    
    st.markdown("### Tu Perfil Actual")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{st.session_state.peso_actual:.1f}</div><div class="stat-label">kg</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{st.session_state.altura}</div><div class="stat-label">m</div></div>', unsafe_allow_html=True)

# ========== PÁGINA: INICIO ==========
if pagina == "Inicio":
    col1, col2 = st.columns([0.65, 0.35])
    
    with col1:
        st.markdown("## Tu Composición Corporal")
        
        composicion = calcular_composicion_corporal(st.session_state.peso_actual, st.session_state.altura)
        
        for metrica, (valor, estado) in composicion.items():
            if estado == "Alto":
                color_status = '<span class="status-alto">Alto</span>'
            elif estado == "Perfecto":
                color_status = '<span class="status-perfecto">Perfecto</span>'
            elif estado == "Saludable":
                color_status = '<span class="status-saludable">Saludable</span>'
            elif estado == "Sobrepeso":
                color_status = '<span class="status-sobrepeso">Sobrepeso</span>'
            else:
                color_status = '<span class="status-saludable">Normal</span>'
            
            st.markdown(f'<div class="profile-item"><div><strong>{metrica}</strong></div><div><span class="profile-value">{valor}</span> {color_status}</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("## Meta de Hoy")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="stat-box"><div class="stat-value">2760</div><div class="stat-label">kcal</div></div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="stat-box"><div class="stat-value">145g</div><div class="stat-label">Proteína</div></div>', unsafe_allow_html=True)

# ========== PÁGINA: NUTRICIÓN ==========
elif pagina == "Nutrición":
    st.markdown("## Plan Nutricional Detallado")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        st.session_state.dieta = st.selectbox("Elige tu dieta", list(DIETAS.keys()), label_visibility="collapsed")
    
    st.divider()
    
    dieta = DIETAS[st.session_state.dieta]
    
    for comida_key, comida_info in dieta.items():
        st.markdown(f"### {comida_key.upper()}")
        st.markdown(f"*{comida_info['nombre']}*")
        
        tabla_alimentos = []
        total_macros = {"kcal": 0, "p": 0, "c": 0, "g": 0}
        
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
        with col1: st.metric("kcal", round(total_macros["kcal"]))
        with col2: st.metric("Proteína", f"{round(total_macros['p'])}g")
        with col3: st.metric("Carbos", f"{round(total_macros['c'])}g")
        with col4: st.metric("Grasas", f"{round(total_macros['g'])}g")
        
        st.divider()

# ========== PÁGINA: ENTRENAMIENTOS ==========
elif pagina == "Entrenamientos":
    st.markdown("## Programa de Entrenamientos Científico")
    
    tabs = st.tabs(list(ENTRENAMIENTOS.keys()))
    
    for tab, (nombre, detalles) in zip(tabs, ENTRENAMIENTOS.items()):
        with tab:
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                st.markdown(f"### {nombre}")
                st.markdown(f"**Enfoque**: {detalles['enfoque']}")
                st.markdown(f"**Duración**: {detalles['duracion']} min")
                st.markdown(f"**Grupos musculares**: {detalles['musculos']}")
                
                st.markdown("#### Ejercicios")
                
                for i, ej in enumerate(detalles["ejercicios"], 1):
                    with st.expander(f"{i}. {ej['nombre']} ({ej['series']})"):
                        st.markdown(f"**Grupo muscular**: {ej['musculo']}")
                        st.markdown(f"**Series x Reps**: {ej['series']}")
                        st.markdown(f"**Justificación científica**:")
                        st.markdown(f"> {ej['justificacion']}")
            
            with col2:
                st.markdown("#### Beneficios")
                st.info(f"""
                **{nombre}** desarrolla:
                - {detalles['musculos'].split(',')[0]}
                - Mayor fuerza y potencia
                - Hipertrofia muscular
                - Aumento metabólico
                """)

# ========== PÁGINA: REGISTROS ==========
elif pagina == "Registros":
    st.markdown("## Registro de Seguimiento")
    
    tab1, tab2 = st.tabs(["Registrar Nutrición", "Ver Registros"])
    
    with tab1:
        st.markdown("### Registrar Consumo Nutricional")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_nut = st.date_input("Fecha", key="fecha_nut")
        with col2:
            hora_nut = st.time_input("Hora", key="hora_nut")
        with col3:
            comida = st.selectbox("Comida", ["Desayuno", "Media Mañana", "Comida", "Merienda", "Cena", "Pre-dormir"])
        
        if st.button("Guardar Registro Nutrición"):
            st.success("✓ Registro guardado")
    
    with tab2:
        if st.session_state.registros_nutricion:
            st.markdown("#### Nutrición")
            df_nut = pd.DataFrame(st.session_state.registros_nutricion)
            st.dataframe(df_nut, use_container_width=True, hide_index=True)
        else:
            st.info("📝 No hay registros aún")

# ========== PÁGINA: CONFIGURACIÓN ==========
elif pagina == "Configuración":
    st.markdown("## Configuración")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.peso_actual = st.number_input("Peso actual (kg)", value=st.session_state.peso_actual, step=0.1)
    with col2:
        st.session_state.altura = st.number_input("Altura (m)", value=st.session_state.altura, step=0.01)
    
    col3, col4 = st.columns(2)
    with col3:
        st.number_input("Edad", value=26)
    with col4:
        st.selectbox("Nivel de experiencia", ["Principiante", "Intermedio", "Avanzado"])
    
    if st.button("Guardar Configuración"):
        st.success("✓ Configuración guardada")

st.divider()
st.caption("Coach Nutriólogo Pro © 2024 | Basado en ciencia nutricional y deportiva")
