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
    .metric-row { background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; display: flex; justify-content: space-between; align-items: center; }
    .metric-label { display: flex; align-items: center; gap: 0.8rem; flex: 1; }
    .metric-icon { font-size: 1.5rem; }
    .metric-info { font-weight: 500; }
    .metric-value-text { font-size: 1.5rem; font-weight: 700; margin-right: 1rem; }
    .status-alto { color: #FBBC04; font-weight: 600; }
    .status-perfecto { color: #34A853; font-weight: 600; }
    .status-saludable { color: #34A853; font-weight: 600; }
    .status-sobrepeso { color: #FBBC04; font-weight: 600; }
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
    "Papa": {"kcal": 77, "p": 1.7, "c": 40, "g": 0.2},
    "Atún": {"kcal": 132, "p": 29, "c": 0, "g": 1.3},
    "Aguacate": {"kcal": 160, "p": 2, "c": 9, "g": 15},
    "Carne magra": {"kcal": 250, "p": 26, "c": 0, "g": 15},
    "Salmon": {"kcal": 208, "p": 20, "c": 0, "g": 13},
}

# ========== DIETAS CON ALTERNATIVAS ==========
DIETAS = {
    "Pollo": {
        "desayuno": {
            "nombre": "Avena + Huevos + Fruta",
            "principales": [("Avena", 60), ("Huevo", 100), ("Leche entera", 200), ("Plátano", 120)],
            "alternativas": {
                "Plátano": ["Manzana"],
                "Leche entera": ["Leche entera"],
            }
        },
        "media_mañana": {
            "nombre": "Yogur Griego + Frutos",
            "principales": [("Yogur griego", 200), ("Plátano", 100)],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Arroz + Pollo + Verduras",
            "principales": [("Arroz integral", 150), ("Pechuga pollo", 200), ("Brócoli", 150)],
            "alternativas": {
                "Pechuga pollo": ["Carne magra", "Atún"],
            }
        },
        "merienda": {
            "nombre": "Pan + Atún + Aguacate",
            "principales": [("Pan integral", 60), ("Atún", 150), ("Aguacate", 50)],
            "alternativas": {}
        },
        "cena": {
            "nombre": "Carne + Tubérculo",
            "principales": [("Carne magra", 200), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
                "Carne magra": ["Salmon"],
            }
        },
        "pre_dormir": {
            "nombre": "Leche Entera",
            "principales": [("Leche entera", 250)],
            "alternativas": {}
        }
    },
    "Carnes Rojas": {
        "desayuno": {
            "nombre": "Pan + Huevo + Fruta",
            "principales": [("Pan integral", 80), ("Huevo", 100), ("Manzana", 150)],
            "alternativas": {
                "Manzana": ["Plátano"],
            }
        },
        "media_mañana": {
            "nombre": "Yogur + Frutos",
            "principales": [("Yogur griego", 200), ("Plátano", 100)],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Arroz + Carne + Verduras",
            "principales": [("Arroz integral", 150), ("Carne magra", 220), ("Brócoli", 150)],
            "alternativas": {
                "Carne magra": ["Pechuga pollo"],
            }
        },
        "merienda": {
            "nombre": "Pan + Queso + Aguacate",
            "principales": [("Pan integral", 60), ("Aguacate", 80)],
            "alternativas": {}
        },
        "cena": {
            "nombre": "Lomo + Tubérculo",
            "principales": [("Carne magra", 220), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
            }
        },
        "pre_dormir": {
            "nombre": "Yogur Griego",
            "principales": [("Yogur griego", 250)],
            "alternativas": {}
        }
    },
    "Pescado": {
        "desayuno": {
            "nombre": "Avena + Claras + Fruta",
            "principales": [("Avena", 70), ("Claras de huevo", 200), ("Leche entera", 180), ("Plátano", 120)],
            "alternativas": {}
        },
        "media_mañana": {
            "nombre": "Yogur + Frutos",
            "principales": [("Yogur griego", 200), ("Manzana", 100)],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Pasta + Salmón + Verduras",
            "principales": [("Pasta integral", 150), ("Salmon", 200), ("Brócoli", 150)],
            "alternativas": {}
        },
        "merienda": {
            "nombre": "Pan + Atún + Aguacate",
            "principales": [("Pan integral", 70), ("Atún", 150), ("Aguacate", 60)],
            "alternativas": {}
        },
        "cena": {
            "nombre": "Tilapia + Tubérculo",
            "principales": [("Salmon", 200), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
            }
        },
        "pre_dormir": {
            "nombre": "Leche Entera",
            "principales": [("Leche entera", 250)],
            "alternativas": {}
        }
    },
    "Vegetariana": {
        "desayuno": {
            "nombre": "Avena + Leche + Frutos",
            "principales": [("Avena", 70), ("Leche entera", 250), ("Manzana", 120)],
            "alternativas": {}
        },
        "media_mañana": {
            "nombre": "Yogur + Plátano",
            "principales": [("Yogur griego", 200), ("Plátano", 100)],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Pasta + Lentejas + Verduras",
            "principales": [("Pasta integral", 150), ("Lentejas", 200), ("Brócoli", 150)],
            "alternativas": {}
        },
        "merienda": {
            "nombre": "Pan + Garbanzos",
            "principales": [("Pan integral", 60), ("Garbanzos", 150)],
            "alternativas": {}
        },
        "cena": {
            "nombre": "Tofu + Tubérculo + Ensalada",
            "principales": [("Tofu", 250), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
            }
        },
        "pre_dormir": {
            "nombre": "Leche + Cereales",
            "principales": [("Leche entera", 250)],
            "alternativas": {}
        }
    },
    "Equilibrada": {
        "desayuno": {
            "nombre": "Avena + Huevo + Fruta",
            "principales": [("Avena", 65), ("Huevo", 100), ("Leche entera", 200), ("Manzana", 100)],
            "alternativas": {
                "Manzana": ["Plátano"],
            }
        },
        "media_mañana": {
            "nombre": "Yogur + Plátano",
            "principales": [("Yogur griego", 200), ("Plátano", 100)],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Arroz + Pollo + Verduras",
            "principales": [("Arroz integral", 150), ("Pechuga pollo", 180), ("Brócoli", 150)],
            "alternativas": {
                "Pechuga pollo": ["Salmon"],
            }
        },
        "merienda": {
            "nombre": "Pan + Atún + Aguacate",
            "principales": [("Pan integral", 60), ("Atún", 150), ("Aguacate", 50)],
            "alternativas": {}
        },
        "cena": {
            "nombre": "Salmón + Tubérculo",
            "principales": [("Salmon", 180), ("Camote", 150)],
            "alternativas": {
                "Camote": ["Papa"],
            }
        },
        "pre_dormir": {
            "nombre": "Leche Entera",
            "principales": [("Leche entera", 250)],
            "alternativas": {}
        }
    }
}

# ========== ENTRENAMIENTOS DETALLADOS ==========
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
                "nombre": "Curl Femoral",
                "series": "3x12-15",
                "musculo": "Isquiotibiales",
                "justificacion": "Aislamiento monoarticular. Flexión directa. Acumulación de lactato (hipertrofia)."
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
                "justificacion": "Desarrollo de amplitud dorsal. Mayor seguridad articular."
            },
        ]
    }
}

# ========== INICIALIZAR SESSION ==========
if "registros_nutricion" not in st.session_state:
    st.session_state.registros_nutricion = []
if "registros_entrenamiento" not in st.session_state:
    st.session_state.registros_entrenamiento = []
if "progreso_entrenamiento" not in st.session_state:
    st.session_state.progreso_entrenamiento = []
if "peso_actual" not in st.session_state:
    st.session_state.peso_actual = 71.4
if "dieta" not in st.session_state:
    st.session_state.dieta = "Pollo"
if "altura" not in st.session_state:
    st.session_state.altura = 1.68

# ========== FUNCIONES ==========
def calcular_macros(alimento, gramos):
    info = ALIMENTOS.get(alimento, {"kcal": 0, "p": 0, "c": 0, "g": 0})
    return {
        "kcal": round((info["kcal"] * gramos) / 100, 1),
        "p": round((info["p"] * gramos) / 100, 1),
        "c": round((info["c"] * gramos) / 100, 1),
        "g": round((info["g"] * gramos) / 100, 1),
    }

def calcular_composicion(peso, altura):
    """Calcular composición corporal detallada"""
    bmi = peso / (altura ** 2)
    grasa_pct = 22.4
    peso_grasa = (peso * grasa_pct) / 100
    peso_muscular = peso - peso_grasa
    
    return {
        ("⚖️ Peso (kg)", peso): "Alto" if peso > 70 else "Normal",
        ("📊 BMI", round(bmi, 1)): "Alto" if bmi > 25 else "Normal",
        ("💪 Grasa (%)", grasa_pct): "Alto" if grasa_pct > 25 else "Perfecto",
        ("🔥 Peso de grasa corporal (kg)", round(peso_grasa, 1)): "Alto" if peso_grasa > 18 else "Saludable",
        ("💯 Porcentaje de masa muscular esquelética (%)", round((peso_muscular/peso)*100, 1)): "Perfecto" if (peso_muscular/peso)*100 > 40 else "Bueno",
        ("🏋️ Peso de la masa muscular esquelética (kg)", round(peso_muscular, 1)): "Perfecto" if peso_muscular > 29 else "Bueno",
        ("🔥 Músculos (%)", 74.2): "Perfecto",
        ("⚡ Peso muscular (kg)", 53.0): "Perfecto",
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
        
        composicion = calcular_composicion(st.session_state.peso_actual, st.session_state.altura)
        
        for (icono_label, valor), estado in composicion.items():
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
            
            st.markdown(f'<div class="metric-row"><div class="metric-label"><span class="metric-icon">{icono_label.split()[0]}</span><span class="metric-info">{icono_label.split(" ", 1)[1]}</span></div><div style="display: flex; align-items: center;"><span class="metric-value-text">{valor}</span>{color_status}</div></div>', unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("## Calendario de Cumplimiento")
        
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        
        st.markdown("**Seguimiento de Entrenamientos (Verde=Completado)**")
        
        dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
        
        registros_mes = [r for r in st.session_state.registros_entrenamiento if r["fecha"].startswith(hoy.strftime("%Y-%m"))]
        fechas_entrenadas = set(r["fecha"] for r in registros_mes)
        
        fecha_actual = inicio_mes
        cal_html = '<div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:8px; margin:1rem 0;">'
        
        for dia in dias_semana:
            cal_html += f'<div style="text-align:center; font-weight:600; font-size:0.8rem; color:#757575;">{dia}</div>'
        
        dias_iniciales = (inicio_mes.weekday()) % 7
        for _ in range(dias_iniciales):
            cal_html += '<div></div>'
        
        while fecha_actual.month == hoy.month:
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            color = "#1F1F1F" if fecha_str in fechas_entrenadas else "#E8E8E8"
            text_color = "white" if fecha_str in fechas_entrenadas else "#1F1F1F"
            
            cal_html += f'<div style="background:{color}; padding:0.8rem; border-radius:8px; text-align:center; font-size:0.8rem; color:{text_color}; font-weight:600;">{fecha_actual.day}</div>'
            fecha_actual += timedelta(days=1)
        
        cal_html += '</div>'
        st.markdown(cal_html, unsafe_allow_html=True)
    
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
        
        for alimento, gramos in comida_info['principales']:
            macros = calcular_macros(alimento, gramos)
            tabla.append({
                "Alimento": alimento,
                "Gramos": gramos,
                "kcal": macros["kcal"],
                "Proteína (g)": macros["p"],
                "Carbos (g)": macros["c"],
                "Grasas (g)": macros["g"],
            })
            for key in total_macros:
                total_macros[key] += macros[key]
        
        for alimento_original, alternativas in comida_info['alternativas'].items():
            for alternativa in alternativas:
                macros = calcular_macros(alternativa, 150)
                tabla.append({
                    "Alimento": f"⚙️ {alternativa} (alt.)",
                    "Gramos": "150",
                    "kcal": macros["kcal"],
                    "Proteína (g)": macros["p"],
                    "Carbos (g)": macros["c"],
                    "Grasas (g)": macros["g"],
                })
        
        df = pd.DataFrame(tabla)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("kcal", round(total_macros["kcal"]))
        with col2: st.metric("Proteína", f"{round(total_macros['p'])}g")
        with col3: st.metric("Carbos", f"{round(total_macros['c'])}g")
        with col4: st.metric("Grasas", f"{round(total_macros['g'])}g")
        
        st.divider()

# ========== PÁGINA: ENTRENAMIENTOS ==========
elif pagina == "Entrenamientos":
    tab_rutinas, tab_progreso = st.tabs(["📋 Rutinas", "📈 Progreso"])
    
    with tab_rutinas:
        st.markdown("## Programa de Entrenamientos")
        
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
                            st.markdown(f"**Justificación científica**:")
                            st.markdown(f"> {ej['justificacion']}")
                
                with col2:
                    st.markdown("#### Beneficios")
                    st.info(f"""
                    **{nombre}** desarrolla:
                    - {detalles['musculos'].split(',')[0]}
                    - Mayor fuerza y potencia
                    - Hipertrofia muscular
                    """)
    
    with tab_progreso:
        st.markdown("### Progreso y Periodicidad de Aumento")
        
        col1, col2 = st.columns([0.5, 0.5])
        
        with col1:
            st.markdown("#### Registrar Progreso")
            
            fecha_prog = st.date_input("Fecha", datetime.today(), key="fecha_prog")
            ejercicio_prog = st.selectbox("Ejercicio", ["Sentadilla Barra", "Press Banca", "Remo Barra", "Peso Muerto Rumano"])
            
            col_a, col_b = st.columns(2)
            with col_a:
                series_realizadas = st.number_input("Series realizadas", value=4, min_value=1)
            with col_b:
                reps_realizadas = st.text_input("Reps realizadas (ej: 8-10)", value="8-10")
            
            peso_usado = st.number_input("Peso usado (kg)", value=0.0, step=2.5)
            
            if st.button("💾 Guardar Progreso"):
                nuevo_progreso = {
                    "fecha": str(fecha_prog),
                    "ejercicio": ejercicio_prog,
                    "series": series_realizadas,
                    "reps": reps_realizadas,
                    "peso": peso_usado
                }
                st.session_state.progreso_entrenamiento.append(nuevo_progreso)
                st.success("✓ Progreso guardado")
        
        with col2:
            st.markdown("#### Periodicidad de Aumento")
            st.info("""
            **Semana 1-2**: Aprende la forma correcta
            
            **Semana 3+**: Aumenta +2.5kg por semana
            
            **Alternativa**: Si no puedes subir peso, +1 repetición por semana
            
            **Meta**: Progresión continua cada entrenamiento
            """)
        
        st.divider()
        
        st.markdown("### Histórico de Progreso")
        
        if st.session_state.progreso_entrenamiento:
            df_progreso = pd.DataFrame(st.session_state.progreso_entrenamiento)
            st.dataframe(df_progreso, use_container_width=True, hide_index=True)
        else:
            st.info("📝 No hay registros de progreso aún")

# ========== PÁGINA: REGISTROS ==========
elif pagina == "Registros":
    st.markdown("## Registro de Seguimiento")
    
    tab_nut, tab_ent = st.tabs(["📋 Nutrición", "🏋️ Entrenamiento"])
    
    with tab_nut:
        st.markdown("### Registrar Consumo Nutricional")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha = st.date_input("Fecha", datetime.today(), key="fecha_nut")
        with col2:
            hora = st.time_input("Hora", datetime.now().time(), key="hora_nut")
        with col3:
            comida_tipo = st.selectbox("Comida", ["Desayuno", "Comida", "Cena"])
        
        items_registro = []
        for alimento in ["Avena", "Huevo", "Leche entera", "Plátano"][:4]:
            col_a, col_b = st.columns(2)
            with col_a:
                st.number_input(f"{alimento} (rec.)", value=100, disabled=True, key=f"rec_{alimento}")
            with col_b:
                consumido = st.number_input(f"{alimento} (cons.)", value=100, key=f"cons_{alimento}")
            
            items_registro.append({"alimento": alimento, "consumido": consumido})
        
        if st.button("💾 Guardar Registro Nutrición"):
            st.session_state.registros_nutricion.append({
                "fecha": str(fecha),
                "hora": str(hora),
                "comida": comida_tipo,
                "items": items_registro
            })
            st.success("✓ Registro guardado")
    
    with tab_ent:
        st.markdown("### Registrar Entrenamiento")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_ent = st.date_input("Fecha", datetime.today(), key="fecha_ent")
        with col2:
            hora_ent = st.time_input("Hora", datetime.now().time(), key="hora_ent")
        with col3:
            lugar = st.radio("Lugar", ["Gimnasio", "Casa"], horizontal=True)
        
        tren = st.selectbox("Tren", list(ENTRENAMIENTOS.keys()))
        duracion = st.number_input("Duración (min)", value=60)
        
        if st.button("💾 Guardar Entrenamiento"):
            st.session_state.registros_entrenamiento.append({
                "fecha": str(fecha_ent),
                "hora": str(hora_ent),
                "lugar": lugar,
                "tren": tren,
                "duracion": duracion
            })
            st.success("✓ Entrenamiento guardado")
        
        st.divider()
        
        if st.session_state.registros_entrenamiento:
            df_ent = pd.DataFrame(st.session_state.registros_entrenamiento)
            st.dataframe(df_ent[["fecha", "hora", "tren", "lugar"]], use_container_width=True, hide_index=True)

# ========== PÁGINA: CONFIGURACIÓN ==========
elif pagina == "Configuración":
    st.markdown("## Configuración")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.peso_actual = st.number_input("Peso (kg)", value=st.session_state.peso_actual, step=0.1)
    with col2:
        st.session_state.altura = st.number_input("Altura (m)", value=st.session_state.altura, step=0.01)
    
    if st.button("Guardar"):
        st.success("✓ Guardado")

st.divider()
st.caption("Coach Nutriólogo Pro © 2024")
