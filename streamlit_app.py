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
    .stat-value { font-size: 2rem; font-weight: 700; }
    .profile-item { background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; display: flex; justify-content: space-between; }
    .status-alto { color: #FBBC04; }
    .status-perfecto { color: #34A853; }
    .status-saludable { color: #34A853; }
    .stButton > button { background-color: #1F1F1F; color: #FFFFFF; width: 100%; border-radius: 8px; }
    .meal-item { background: #FFFFFF; border-left: 3px solid #1F1F1F; padding: 1rem; border-radius: 8px; margin: 0.8rem 0; }
    .alternativa { background-color: #F0F0F0 !important; }
</style>
""", unsafe_allow_html=True)

# ========== BASE DE DATOS DE ALIMENTOS CON ALTERNATIVAS ==========
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
    "Papa": {"kcal": 77, "p": 1.7, "c": 40, "g": 0.2},
    "Atún": {"kcal": 132, "p": 29, "c": 0, "g": 1.3},
    "Aguacate": {"kcal": 160, "p": 2, "c": 9, "g": 15},
    "Carne magra": {"kcal": 250, "p": 26, "c": 0, "g": 15},
    "Salmon": {"kcal": 208, "p": 20, "c": 0, "g": 13},
    "Pan integral": {"kcal": 265, "p": 9, "c": 49, "g": 3.3},
    "Pasta integral": {"kcal": 124, "p": 5.3, "c": 25, "g": 1.1},
    "Tofu": {"kcal": 76, "p": 8, "c": 1.9, "g": 4.8},
    "Garbanzos": {"kcal": 119, "p": 7, "c": 20, "g": 2.4},
    "Claras de huevo": {"kcal": 52, "p": 11, "c": 0.7, "g": 0},
    "Manzana": {"kcal": 52, "p": 0.3, "c": 14, "g": 0.2},
    "Leche deslactosada": {"kcal": 64, "p": 3.2, "c": 4.8, "g": 3.6},
}

# ========== DIETAS CON ALTERNATIVAS ==========
DIETAS = {
    "Pollo": {
        "desayuno": {
            "nombre": "Avena + Huevos + Fruta",
            "principales": [("Avena", 60), ("Huevo", 100), ("Leche entera", 200), ("Plátano", 120)],
            "alternativas": {
                "Plátano": ["Manzana", "Papa"],
                "Leche entera": ["Leche deslactosada"],
                "Huevo": ["Claras de huevo"]
            }
        },
        "comida": {
            "nombre": "Arroz + Pollo + Verduras",
            "principales": [("Arroz integral", 150), ("Pechuga pollo", 200), ("Brócoli", 150)],
            "alternativas": {
                "Pechuga pollo": ["Carne magra", "Atún"],
                "Arroz integral": ["Pasta integral"]
            }
        },
        "cena": {
            "nombre": "Carne + Tubérculo",
            "principales": [("Carne magra", 200), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
                "Carne magra": ["Pechuga pollo", "Salmon"]
            }
        }
    },
    "Carnes Rojas": {
        "desayuno": {
            "nombre": "Pan + Huevo + Fruta",
            "principales": [("Pan integral", 80), ("Huevo", 100), ("Manzana", 150)],
            "alternativas": {
                "Manzana": ["Plátano"],
                "Huevo": ["Claras de huevo"]
            }
        },
        "comida": {
            "nombre": "Arroz + Carne + Verduras",
            "principales": [("Arroz integral", 150), ("Carne magra", 220), ("Brócoli", 150)],
            "alternativas": {
                "Carne magra": ["Pechuga pollo"],
                "Arroz integral": ["Pasta integral"]
            }
        },
        "cena": {
            "nombre": "Lomo + Tubérculo",
            "principales": [("Carne magra", 220), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
                "Carne magra": ["Salmon"]
            }
        }
    }
}

# ========== ENTRENAMIENTOS ==========
ENTRENAMIENTOS = {
    "Tren Inferior A": {
        "enfoque": "Cuádriceps + Glúteos",
        "duracion": 70,
        "musculos": "Cuádriceps, Glúteos",
        "ejercicios": [
            ("Sentadilla Barra", "4x8-10", "Movimiento compuesto fundamental"),
            ("Prensa de Pierna", "4x10-12", "Volumen de trabajo en cuádriceps"),
            ("Empuje de Cadera", "4x12-15", "Desarrollo específico de glúteos"),
        ]
    },
    "Tren Superior A": {
        "enfoque": "Pecho + Hombros",
        "duracion": 55,
        "musculos": "Pecho, Hombros, Tríceps",
        "ejercicios": [
            ("Press Banca", "4x8-10", "Desarrollo de pecho"),
            ("Prensa Militar", "3x10-12", "Hombros y estabilidad"),
        ]
    },
    "Tren Inferior B": {
        "enfoque": "Isquiotibiales + Glúteos",
        "duracion": 70,
        "musculos": "Isquiotibiales, Glúteos",
        "ejercicios": [
            ("Peso Muerto Rumano", "4x8-10", "Cadena posterior"),
            ("Curl Femoral", "3x12-15", "Aislamiento de isquios"),
        ]
    },
    "Tren Superior B": {
        "enfoque": "Espalda + Bíceps",
        "duracion": 55,
        "musculos": "Espalda, Bíceps",
        "ejercicios": [
            ("Remo Barra", "4x8-10", "Espalda gruesa"),
            ("Jalón al Pecho", "3x10-12", "Amplitud dorsal"),
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
    """Calcular macros de un alimento"""
    info = ALIMENTOS.get(alimento, {"kcal": 0, "p": 0, "c": 0, "g": 0})
    return {
        "kcal": round((info["kcal"] * gramos) / 100, 1),
        "p": round((info["p"] * gramos) / 100, 1),
        "c": round((info["c"] * gramos) / 100, 1),
        "g": round((info["g"] * gramos) / 100, 1),
    }

def calcular_composicion_corporal(peso, altura):
    """Calcular composición corporal"""
    bmi = peso / (altura ** 2)
    grasa_porcentaje = 22.4
    peso_grasa = (peso * grasa_porcentaje) / 100
    peso_muscular = peso - peso_grasa
    
    return {
        "Peso (kg)": (peso, "Alto" if peso > 70 else "Normal"),
        "BMI": (round(bmi, 1), "Alto" if bmi > 25 else "Normal"),
        "Grasa (%)": (grasa_porcentaje, "Alto" if grasa_porcentaje > 25 else "Perfecto"),
        "Peso muscular (kg)": (round(peso_muscular, 1), "Perfecto" if peso_muscular > 29 else "Bueno"),
    }

# ========== HEADER ==========
st.markdown("# Coach Nutriólogo Pro")
st.markdown("Sistema avanzado de entrenamiento y nutrición")
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
        st.markdown(f'<div class="stat-box"><div class="stat-value">{st.session_state.altura}</div><div class="stat-label">m</div></div>', unsafe_allow_html=True)

# ========== PÁGINA: INICIO ==========
if pagina == "Inicio":
    col1, col2 = st.columns([0.65, 0.35])
    
    with col1:
        st.markdown("## Tu Composición Corporal")
        composicion = calcular_composicion_corporal(st.session_state.peso_actual, st.session_state.altura)
        
        for metrica, (valor, estado) in composicion.items():
            if estado == "Alto":
                color = '<span class="status-alto">Alto</span>'
            else:
                color = '<span class="status-perfecto">Perfecto</span>'
            st.markdown(f'<div class="profile-item"><strong>{metrica}</strong><span class="stat-value">{valor}</span> {color}</div>', unsafe_allow_html=True)
    
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
        
        tabla = []
        total_macros = {"kcal": 0, "p": 0, "c": 0, "g": 0}
        
        # Alimentos principales
        for alimento, gramos in comida_info['principales']:
            macros = calcular_macros(alimento, gramos)
            tabla.append({
                "Alimento": alimento,
                "Gramos": gramos,
                "kcal": macros["kcal"],
                "Proteína (g)": macros["p"],
                "Carbos (g)": macros["c"],
                "Grasas (g)": macros["g"],
                "Tipo": "Principal"
            })
            for key in total_macros:
                total_macros[key] += macros[key]
        
        # Alimentos alternativos
        for alimento_original, alternativas in comida_info['alternativas'].items():
            for alternativa in alternativas:
                macros = calcular_macros(alternativa, 150)  # Usar 150g como referencia
                tabla.append({
                    "Alimento": f"⚙️ {alternativa} (alt. de {alimento_original})",
                    "Gramos": "150",
                    "kcal": macros["kcal"],
                    "Proteína (g)": macros["p"],
                    "Carbos (g)": macros["c"],
                    "Grasas (g)": macros["g"],
                    "Tipo": "Alternativa"
                })
        
        df = pd.DataFrame(tabla)
        
        # Mostrar tabla con colores
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("kcal Total", round(total_macros["kcal"]))
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
                st.markdown(f"**Enfoque**: {detalles['enfoque']}")
                st.markdown(f"**Duración**: {detalles['duracion']} min")
                st.markdown(f"**Músculos**: {detalles['musculos']}")
                
                st.markdown("#### Ejercicios")
                for i, (ejercicio, series, desc) in enumerate(detalles["ejercicios"], 1):
                    st.markdown(f"**{i}. {ejercicio}**")
                    st.write(f"Series: {series} | {desc}")

# ========== PÁGINA: REGISTROS ==========
elif pagina == "Registros":
    st.markdown("## Registro de Seguimiento")
    
    tab_nut, tab_ent = st.tabs(["📋 Nutrición", "🏋️ Entrenamiento"])
    
    # ========== TAB: NUTRICIÓN ==========
    with tab_nut:
        st.markdown("### Registrar Consumo Nutricional")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha = st.date_input("Fecha", datetime.today(), key="fecha_nut")
        with col2:
            hora = st.time_input("Hora", datetime.now().time(), key="hora_nut")
        with col3:
            comida_tipo = st.selectbox("Comida", ["Desayuno", "Media Mañana", "Comida", "Merienda", "Cena", "Pre-dormir"], key="comida_tipo")
        
        st.markdown("#### Alimentos Consumidos")
        
        # Obtener alimentos de la dieta actual
        dieta_actual = DIETAS.get(st.session_state.dieta, {})
        alimentos_dieta = []
        
        for comida_key, comida_info in dieta_actual.items():
            for alimento, _ in comida_info['principales']:
                if alimento not in alimentos_dieta:
                    alimentos_dieta.append(alimento)
        
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            st.write("**Recomendado** vs **Consumido**")
            
            items_registro = []
            for alimento in alimentos_dieta[:5]:  # Mostrar primeros 5
                col_a, col_b = st.columns(2)
                with col_a:
                    gramos_recomendado = st.number_input(f"{alimento} (rec.)", value=100, key=f"rec_{alimento}", disabled=True)
                with col_b:
                    gramos_consumido = st.number_input(f"{alimento} (cons.)", value=100, key=f"cons_{alimento}")
                
                items_registro.append({
                    "alimento": alimento,
                    "recomendado": gramos_recomendado,
                    "consumido": gramos_consumido,
                    "porcentaje": round((gramos_consumido / gramos_recomendado * 100), 1) if gramos_recomendado > 0 else 0
                })
        
        if st.button("💾 Guardar Registro Nutrición", use_container_width=True):
            # Crear registro
            nuevo_registro = {
                "fecha": str(fecha),
                "hora": str(hora),
                "comida": comida_tipo,
                "items": items_registro,
                "timestamp": datetime.now().isoformat()
            }
            
            # Guardar en session_state
            st.session_state.registros_nutricion.append(nuevo_registro)
            st.success("✅ Registro guardado correctamente")
        
        st.divider()
        
        # Mostrar histórico
        st.markdown("### Histórico de Registros")
        
        if st.session_state.registros_nutricion:
            # Crear tabla de monitoreo como en la imagen
            registros_hoy = [r for r in st.session_state.registros_nutricion if r["fecha"] == str(fecha)]
            
            if registros_hoy:
                for registro in registros_hoy:
                    st.markdown(f"**{registro['comida']}** - {registro['hora']}")
                    
                    tabla_monitoreo = []
                    promedio_cumplimiento = 0
                    
                    for item in registro['items']:
                        tabla_monitoreo.append({
                            "Alimento": item['alimento'],
                            "Gramaje recomendado": item['recomendado'],
                            "Gramaje consumido": item['consumido'],
                            "% Cumplimiento": f"{item['porcentaje']}%"
                        })
                        promedio_cumplimiento += item['porcentaje']
                    
                    if tabla_monitoreo:
                        df_monitoreo = pd.DataFrame(tabla_monitoreo)
                        st.dataframe(df_monitoreo, use_container_width=True, hide_index=True)
                        
                        promedio = round(promedio_cumplimiento / len(tabla_monitoreo), 1)
                        st.metric("Porcentaje de cumplimiento promedio", f"{promedio}%")
                    
                    st.divider()
            else:
                st.info("No hay registros para esta fecha")
        else:
            st.info("📝 No hay registros aún. ¡Comienza a registrar tu consumo!")
    
    # ========== TAB: ENTRENAMIENTO ==========
    with tab_ent:
        st.markdown("### Registrar Entrenamiento")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_ent = st.date_input("Fecha", datetime.today(), key="fecha_ent")
        with col2:
            hora_ent = st.time_input("Hora", datetime.now().time(), key="hora_ent")
        with col3:
            lugar = st.radio("Lugar", ["Gimnasio", "Casa"], horizontal=True, key="lugar")
        
        tren = st.selectbox("Tren a entrenar", list(ENTRENAMIENTOS.keys()), key="tren")
        
        duracion = st.number_input("Duración (minutos)", value=60, key="duracion_ent")
        notas = st.text_area("Notas del entrenamiento", key="notas_ent")
        
        if st.button("💾 Guardar Registro Entrenamiento", use_container_width=True):
            nuevo_registro_ent = {
                "fecha": str(fecha_ent),
                "hora": str(hora_ent),
                "lugar": lugar,
                "tren": tren,
                "duracion": duracion,
                "notas": notas,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.registros_entrenamiento.append(nuevo_registro_ent)
            st.success("✅ Entrenamiento registrado correctamente")
        
        st.divider()
        
        # Mostrar histórico de entrenamientos
        st.markdown("### Histórico de Entrenamientos")
        
        if st.session_state.registros_entrenamiento:
            registros_ent_df = pd.DataFrame(st.session_state.registros_entrenamiento)
            
            # Mostrar solo columnas importantes
            columnas_mostrar = ["fecha", "hora", "tren", "lugar", "duracion"]
            df_mostrar = registros_ent_df[columnas_mostrar].copy()
            df_mostrar.columns = ["Fecha", "Hora", "Tren", "Lugar", "Duración (min)"]
            
            st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
        else:
            st.info("📝 No hay entrenamientos registrados aún")

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
        st.selectbox("Nivel", ["Principiante", "Intermedio", "Avanzado"])
    
    if st.button("Guardar Configuración"):
        st.success("✓ Guardado")

st.divider()
st.caption("Coach Nutriólogo Pro © 2024")
