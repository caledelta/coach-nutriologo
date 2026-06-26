import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
from db import (
    guardar_registro_nutricion, obtener_registros_nutricion,
    guardar_registro_entrenamiento, obtener_registros_entrenamiento,
    guardar_progreso_entrenamiento, obtener_progreso_entrenamiento,
    obtener_progreso_por_ejercicio, validar_cumplimiento_dia,
    guardar_configuracion, obtener_configuracion,
    actualizar_registro_nutricion, eliminar_registro_nutricion,
    guardar_peso_diario, obtener_pesos_diarios, eliminar_peso_diario,
    actualizar_registro_entrenamiento, eliminar_registro_entrenamiento
)

st.set_page_config(page_title="Coach Nutriólogo Pro", layout="wide", initial_sidebar_state="expanded")

# ========== ESTILOS ==========
st.markdown("""
<style>
    /* ========== TIPOGRAFÍA Y BASE ========== */
    * { 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
        font-feature-settings: "kern" 1;
    }
    
    /* ========== FONDOS Y ESTRUCTURA ========== */
    body, .stApp { 
        background-color: #F8F9FA !important; 
        color: #1F1F1F !important;
    }
    
    .main { 
        background-color: #F8F9FA !important;
        padding: 2rem 1rem !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background-color: #F8F9FA !important;
    }
    
    .stSidebar {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E0E0E0 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
    }
    
    /* ========== TIPOGRAFÍA ========== */
    h1 { 
        color: #1F1F1F !important; 
        font-size: 2.2rem !important; 
        font-weight: 600 !important;
        letter-spacing: -0.5px !important;
    }
    
    h2 { 
        color: #1F1F1F !important; 
        font-size: 1.5rem !important; 
        font-weight: 600 !important; 
        margin: 1.5rem 0 1rem 0 !important;
        letter-spacing: -0.3px !important;
    }
    
    h3 {
        color: #1F1F1F !important;
        font-weight: 600 !important;
        letter-spacing: -0.2px !important;
    }
    
    p, span, label {
        color: #1F1F1F !important;
    }
    
    /* ========== CAJAS Y CONTENEDORES ========== */
    .stat-box { 
        background: #FFFFFF !important; 
        border: 1px solid #EBEBEB !important; 
        border-radius: 12px !important; 
        padding: 1.2rem !important; 
        text-align: center !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stat-box:hover {
        border-color: #D0D0D0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stat-value { 
        font-size: 2rem !important; 
        font-weight: 700 !important;
        color: #1F1F1F !important;
    }
    
    .metric-row { 
        background: #FFFFFF !important; 
        border: 1px solid #EBEBEB !important; 
        border-radius: 12px !important; 
        padding: 1rem !important; 
        margin: 0.5rem 0 !important; 
        display: flex !important; 
        justify-content: space-between !important; 
        align-items: center !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .metric-row:hover {
        border-color: #D0D0D0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }
    
    .metric-label { 
        display: flex !important; 
        align-items: center !important; 
        gap: 0.8rem !important; 
        flex: 1 !important;
    }
    
    .metric-icon { 
        font-size: 1.5rem !important;
        flex-shrink: 0 !important;
    }
    
    .metric-info { 
        font-weight: 500 !important;
        color: #1F1F1F !important;
    }
    
    .metric-value-text { 
        font-size: 1.5rem !important; 
        font-weight: 700 !important;
        color: #1F1F1F !important;
        margin-right: 1rem !important; 
    }
    
    /* ========== ESTADOS Y COLORES (Verde Oliva Pastel Claro) ========== */
    .status-alto { 
        color: #FBBC04 !important; 
        font-weight: 600 !important;
    }
    
    .status-perfecto { 
        color: #A8B894 !important; 
        font-weight: 600 !important;
    }
    
    .status-saludable { 
        color: #A8B894 !important; 
        font-weight: 600 !important;
    }
    
    .status-sobrepeso { 
        color: #FBBC04 !important; 
        font-weight: 600 !important;
    }
    
    /* ========== BOTONES (Verde Oliva Pastel Claro) ========== */
    .stButton > button {
        background-color: #A8B894 !important;
        color: #FFFFFF !important;
        width: 100% !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1.2rem !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 4px rgba(168, 184, 148, 0.25) !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background-color: #96A882 !important;
        box-shadow: 0 4px 8px rgba(168, 184, 148, 0.35) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        background-color: #A8B894 !important;
        transform: translateY(0) !important;
        box-shadow: 0 2px 4px rgba(168, 184, 148, 0.25) !important;
    }
    
    /* ========== SELECTBOX Y COMBOBOX ========== */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
    }
    
    [data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #EBEBEB !important;
        border-radius: 8px !important;
    }
    
    [data-baseweb="select"] > div:hover {
        border-color: #D0D0D0 !important;
    }
    
    [data-baseweb="select"] > div:focus-within {
        border-color: #1F1F1F !important;
        box-shadow: 0 0 0 3px rgba(31, 31, 31, 0.05) !important;
    }
    
    /* ========== INPUTS Y TEXTAREAS ========== */
    input, textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #EBEBEB !important;
        border-radius: 8px !important;
        color: #1F1F1F !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    input:hover, textarea:hover {
        border-color: #D0D0D0 !important;
    }
    
    input:focus, textarea:focus {
        border-color: #1F1F1F !important;
        box-shadow: 0 0 0 3px rgba(31, 31, 31, 0.05) !important;
        outline: none !important;
    }
    
    /* ========== CHECKBOXES ========== */
    [data-testid="stCheckbox"] {
        color: #1F1F1F !important;
    }
    
    [data-testid="stCheckbox"] label {
        color: #1F1F1F !important;
    }
    
    /* ========== ELEMENTOS ESPECÍFICOS ========== */
    .meal-item { 
        background: #FFFFFF !important; 
        border-left: 3px solid #1F1F1F !important; 
        padding: 1rem !important; 
        border-radius: 8px !important; 
        margin: 0.8rem 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    .exercise-item { 
        background: #FFFFFF !important; 
        border: 1px solid #EBEBEB !important; 
        padding: 1.2rem !important; 
        border-radius: 12px !important; 
        margin: 1rem 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .exercise-item:hover {
        border-color: #D0D0D0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== BASE DE DATOS DE ALIMENTOS ==========
ALIMENTOS = {
    "Avena": {"kcal": 389, "p": 17, "c": 66, "g": 7},
    "Huevo": {"kcal": 155, "p": 13, "c": 1.1, "g": 11},
    "Plátano": {"kcal": 89, "p": 1.1, "c": 23, "g": 0.3},
    "Leche entera": {"kcal": 64, "p": 3.2, "c": 4.8, "g": 3.6},
    "Leche Lala 100": {"kcal": 60, "p": 5.0, "c": 4.8, "g": 1.0},
    "Leche de coco": {"kcal": 230, "p": 2.3, "c": 5.5, "g": 24},
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
    "Manzana": {"kcal": 52, "p": 0.3, "c": 14, "g": 0.2},
    "Mantequilla de maní": {"kcal": 588, "p": 25, "c": 20, "g": 50},
    "Claras de huevo": {"kcal": 52, "p": 11, "c": 0.7, "g": 0},
    "Pasta integral": {"kcal": 124, "p": 5.3, "c": 25, "g": 1.1},
    "Filete de tilapia": {"kcal": 96, "p": 20, "c": 0, "g": 1.2},
    "Agua": {"kcal": 0, "p": 0, "c": 0, "g": 0},
    "Creatina monohidratada": {"kcal": 0, "p": 0, "c": 0, "g": 0},
}

# ========== DIETAS CON ALTERNATIVAS Y UNIDADES ==========
DIETAS = {
    "Pollo": {
        "desayuno": {
            "nombre": "Avena + Huevos + Fruta + Agua + Creatina",
            "principales": [
                ("Avena", 60, "g"),
                ("Huevo", 100, "g"),
                ("Leche Lala 100", 200, "mL"),
                ("Plátano", 120, "g"),
                ("Creatina monohidratada", 5, "g"),
                ("Agua", 500, "mL")
            ],
            "alternativas": {
                "Plátano": ["Manzana (alt. a Plátano)"],
                "Leche Lala 100": ["Leche de coco (alt. a Leche Lala 100)"],
            }
        },
        "media_mañana": {
            "nombre": "Yogur Griego + Frutos + Agua",
            "principales": [
                ("Yogur griego", 200, "g"),
                ("Plátano", 100, "g"),
                ("Agua", 400, "mL")
            ],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Arroz + Pollo + Verduras + Agua",
            "principales": [
                ("Arroz integral", 180, "g"),
                ("Pechuga pollo", 200, "g"),
                ("Brócoli", 150, "g"),
                ("Agua", 600, "mL")
            ],
            "alternativas": {
                "Pechuga pollo": ["Carne magra (alt. a Pollo)", "Atún (alt. a Pollo)"],
            }
        },
        "merienda": {
            "nombre": "Pan + Atún + Mantequilla de Maní + Agua",
            "principales": [
                ("Pan integral", 60, "g"),
                ("Atún", 150, "g"),
                ("Mantequilla de maní", 32, "g"),
                ("Agua", 400, "mL")
            ],
            "alternativas": {
                "Atún": ["Pechuga pollo (alt. a Atún)"],
            }
        },
        "cena": {
            "nombre": "Carne + Tubérculo + Agua",
            "principales": [
                ("Carne magra", 200, "g"),
                ("Papa", 150, "g"),
                ("Agua", 500, "mL")
            ],
            "alternativas": {
                "Papa": ["Plátano (alt. a Papa)"],
                "Carne magra": ["Atún (alt. a Carne magra)"],
            }
        },
        "pre_dormir": {
            "nombre": "Yogur Griego",
            "principales": [
                ("Yogur griego", 250, "g")
            ],
            "alternativas": {}
        }
    },
    "Carnes Rojas": {
        "desayuno": {
            "nombre": "Pan + Huevo + Fruta + Mantequilla de Maní + Agua + Creatina",
            "principales": [
                ("Pan integral", 100, "g"),
                ("Huevo", 100, "g"),
                ("Manzana", 150, "g"),
                ("Mantequilla de maní", 20, "g"),
                ("Creatina monohidratada", 5, "g"),
                ("Agua", 500, "mL")
            ],
            "alternativas": {
                "Manzana": ["Plátano (alt. a Manzana)"],
            }
        },
        "media_mañana": {
            "nombre": "Yogur + Frutos + Agua",
            "principales": [
                ("Yogur griego", 200, "g"),
                ("Plátano", 100, "g"),
                ("Agua", 400, "mL")
            ],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Arroz + Carne + Verduras + Agua",
            "principales": [
                ("Arroz integral", 180, "g"),
                ("Carne magra", 220, "g"),
                ("Brócoli", 150, "g"),
                ("Agua", 600, "mL")
            ],
            "alternativas": {
                "Carne magra": ["Pechuga pollo (alt. a Carne)"],
            }
        },
        "merienda": {
            "nombre": "Pan + Mantequilla de Maní + Fruta + Agua",
            "principales": [
                ("Pan integral", 60, "g"),
                ("Mantequilla de maní", 32, "g"),
                ("Manzana", 100, "g"),
                ("Agua", 400, "mL")
            ],
            "alternativas": {
                "Manzana": ["Plátano (alt. a Manzana)"],
            }
        },
        "cena": {
            "nombre": "Lomo + Tubérculo + Agua",
            "principales": [
                ("Carne magra", 220, "g"),
                ("Camote", 150, "g"),
                ("Agua", 500, "mL")
            ],
            "alternativas": {
                "Camote": ["Papa (alt. a Camote)"],
            }
        },
        "pre_dormir": {
            "nombre": "Yogur Griego",
            "principales": [
                ("Yogur griego", 250, "g")
            ],
            "alternativas": {}
        }
    },
    "Pescado": {
        "desayuno": {
            "nombre": "Avena + Claras + Fruta + Agua + Creatina",
            "principales": [
                ("Avena", 70, "g"),
                ("Claras de huevo", 200, "mL"),
                ("Leche Lala 100", 180, "mL"),
                ("Plátano", 120, "g"),
                ("Creatina monohidratada", 5, "g"),
                ("Agua", 500, "mL")
            ],
            "alternativas": {}
        },
        "media_mañana": {
            "nombre": "Yogur + Frutos + Agua",
            "principales": [
                ("Yogur griego", 200, "g"),
                ("Manzana", 100, "g"),
                ("Agua", 400, "mL")
            ],
            "alternativas": {}
        },
        "comida": {
            "nombre": "Pasta + Tilapia + Verduras + Agua",
            "principales": [
                ("Pasta integral", 180, "g"),
                ("Filete de tilapia", 200, "g"),
                ("Brócoli", 150, "g"),
                ("Agua", 600, "mL")
            ],
            "alternativas": {}
        },
        "merienda": {
            "nombre": "Pan + Mantequilla de Maní + Aguacate + Agua",
            "principales": [
                ("Pan integral", 70, "g"),
                ("Mantequilla de maní", 32, "g"),
                ("Aguacate", 40, "g"),
                ("Agua", 400, "mL")
            ],
            "alternativas": {}
        },
        "cena": {
            "nombre": "Tilapia + Tubérculo + Agua",
            "principales": [
                ("Filete de tilapia", 200, "g"),
                ("Papa", 150, "g"),
                ("Agua", 500, "mL")
            ],
            "alternativas": {
                "Papa": ["Plátano (alt. a Papa)"],
            }
        },
        "pre_dormir": {
            "nombre": "Yogur Griego",
            "principales": [
                ("Yogur griego", 250, "g")
            ],
            "alternativas": {}
        }
    }
}

# ========== ENTRENAMIENTOS DETALLADOS ==========
ENTRENAMIENTOS = {
    "Tren Inferior A": {
        "enfoque": "Cuádriceps + Glúteos",
        "duracion": 90,
        "musculos": "Cuádriceps, Glúteos",
        "ejercicios": [
            {
                "nombre": "Sentadilla Barra",
                "series": "4x6-8",
                "musculo": "Cuádriceps/Glúteos",
                "justificacion": "Movimiento compuesto fundamental. Máxima activación de fibras Type II (hipertrofia). Producción anabólica (testosterona, GH). Patrón de movimiento natural. Base de cualquier programa de ganancia muscular (Schoenfeld et al., 2016)."
            },
            {
                "nombre": "Prensa de Pierna",
                "series": "3x8-10",
                "musculo": "Cuádriceps",
                "justificacion": "Volumen de trabajo adicional. Reduce riesgo articular vs barra. Mayor aislamiento de cuádriceps. Permite alcanzar mayor fatiga muscular en rangos hipertróficos (8-10 reps). Complementa el patrón de sentadilla (Schoenfeld, 2010)."
            },
            {
                "nombre": "Extensión de Cuádriceps",
                "series": "3x12-15",
                "musculo": "Cuádriceps",
                "justificacion": "Aislamiento monoarticular. Máxima contracción del cuádriceps. Acumulación de metabolitos (lactato, fosfato). Hipertrofia miofibrilar sin fatiga articular (Contreras et al., 2015). Complementa movimientos compuestos."
            },
            {
                "nombre": "Empuje de Cadera",
                "series": "3x10-12",
                "musculo": "Glúteos",
                "justificacion": "Especificidad para glúteo mayor (mayor reclutamiento). Patrón de extensión de cadera aislado. Desarrollo direccionado de masa glútea. Menor fatiga del SNC que sentadilla (Contreras et al., 2016)."
            },
        ]
    },
    "Tren Superior A": {
        "enfoque": "Empuje (Pecho, Hombros, Tríceps)",
        "duracion": 90,
        "musculos": "Pecho, Hombros, Tríceps",
        "ejercicios": [
            {
                "nombre": "Press Banca Plano",
                "series": "4x6-8",
                "musculo": "Pecho",
                "justificacion": "Movimiento compuesto fundamental. Mayor producción anabólica. Máxima transferencia de fuerza. Reclutamiento de pecho, hombros y tríceps (Schoenfeld et al., 2016). Base de desarrollo de pecho."
            },
            {
                "nombre": "Press Inclinado Mancuernas",
                "series": "3x8-10",
                "musculo": "Pecho superior",
                "justificacion": "Énfasis en porción superior de pecho. Mayor rango de movimiento vs barra. Activación adicional de deltoides anterior. Volumen complementario para equilibrio muscular (Schoenfeld, 2010)."
            },
            {
                "nombre": "Aperturas en Pecho",
                "series": "3x12-15",
                "musculo": "Pecho",
                "justificacion": "Aislamiento de pecho. Mayor elongación bajo tensión (estiramiento miofibrilar). Acumulación de metabolitos. Complementa movimientos de empuje sin fatiga articular (Contreras et al., 2016)."
            },
            {
                "nombre": "Prensa Militar",
                "series": "3x8-10",
                "musculo": "Hombros/Tríceps",
                "justificacion": "Desarrollo deltoides anterior. Estabilizadores rotatores del hombro. Patrón de empuje vertical esencial. Mayor reclutamiento de estabilizadores vs press plano (Schoenfeld, 2010)."
            },
        ]
    },
    "Tren Inferior B": {
        "enfoque": "Isquiotibiales + Glúteos (Cadena Posterior)",
        "duracion": 90,
        "musculos": "Isquiotibiales, Glúteos",
        "ejercicios": [
            {
                "nombre": "Peso Muerto Rumano",
                "series": "4x6-8",
                "musculo": "Isquiotibiales",
                "justificacion": "Especificidad en cadena posterior. Mayor rango de movimiento que convencional. Estiramiento bajo tensión en isquios (hipertrofia del sarcómero). Menor fatiga del SNC vs convencional (Contreras et al., 2015)."
            },
            {
                "nombre": "Curl Femoral",
                "series": "3x10-12",
                "musculo": "Isquiotibiales",
                "justificacion": "Aislamiento monoarticular. Flexión de rodilla sin extensión de cadera. Acumulación de lactato (hipertrofia miometabólica). Complementa el patrón de extensión de cadera del RDL (Schoenfeld, 2010)."
            },
            {
                "nombre": "Nordic Curl",
                "series": "3x6-8",
                "musculo": "Isquiotibiales",
                "justificacion": "Contracción excéntrica extrema. Máxima tensión mecánica en excéntrica (potente estímulo hipertrófico). Mayor activación de isquios vs curl tradicional. Prevención de lesiones (Contreras et al., 2016)."
            },
            {
                "nombre": "Hip Thrust con Barra",
                "series": "3x8-10",
                "musculo": "Glúteos",
                "justificacion": "Máxima activación de glúteo mayor en extensión de cadera. Volumen adicional para cadena posterior. Patrón complementario a RDL. Mayor especificidad que empuje de cadera (Contreras et al., 2016)."
            },
        ]
    },
    "Tren Superior B": {
        "enfoque": "Jalón (Espalda, Bíceps)",
        "duracion": 90,
        "musculos": "Espalda, Bíceps, Trapecio",
        "ejercicios": [
            {
                "nombre": "Remo Barra",
                "series": "4x6-8",
                "musculo": "Espalda",
                "justificacion": "Movimiento compuesto espalda. Máxima activación dorsal. Desarrollo de espalda gruesa (ancho + grosor). Mayor producción anabólica. Equilibra press banca (Schoenfeld et al., 2016)."
            },
            {
                "nombre": "Jalón al Pecho",
                "series": "3x8-10",
                "musculo": "Espalda",
                "justificacion": "Desarrollo de amplitud dorsal (dorsal ancho). Mayor seguridad articular vs remo en posición inclinada. Volumen complementario. Diferentes ángulos de tracción para estimulación óptima (Schoenfeld, 2010)."
            },
            {
                "nombre": "Remo Mancuerna",
                "series": "3x10-12",
                "musculo": "Espalda",
                "justificacion": "Mayor rango de movimiento vs barra. Reclutamiento asimétrico evita compesaciones. Flexibilidad para mayor amplitud. Complementa patrón de remo convencional (Contreras et al., 2015)."
            },
            {
                "nombre": "Curl de Bíceps",
                "series": "3x10-12",
                "musculo": "Bíceps",
                "justificacion": "Aislamiento monoarticular de bíceps. Flexión de codo sin movimiento de espalda. Hipertrofia directa de bíceps. Complementa movimientos de tracción compuestos (Schoenfeld, 2010)."
            },
        ]
    }
}

# ========== CATÁLOGO COMPLETO DE EJERCICIOS ==========
def obtener_todos_ejercicios():
    """Retorna lista de todos los ejercicios principales y alternativos"""
    ejercicios = set()
    
    # Agregar ejercicios principales de todas las rutinas
    for rutina, detalles in ENTRENAMIENTOS.items():
        for ejercicio in detalles["ejercicios"]:
            ejercicios.add(ejercicio["nombre"])
            
            # Agregar ejercicios alternativos si existen
            if ejercicio["nombre"] in ALTERNATIVAS_EJERCICIOS:
                for alt in ALTERNATIVAS_EJERCICIOS[ejercicio["nombre"]]:
                    ejercicios.add(alt["nombre"])
    
    return sorted(list(ejercicios))

def obtener_ejercicios_completos_por_tren(nombre_tren):
    """Retorna ejercicios principales + alternativos de un tren específico"""
    if nombre_tren not in ENTRENAMIENTOS:
        return []
    
    rutina = ENTRENAMIENTOS[nombre_tren]
    ejercicios_completos = []
    
    # Agregar ejercicios principales
    for ejercicio in rutina["ejercicios"]:
        nombre = ejercicio["nombre"]
        ejercicios_completos.append(nombre)
        
        # Agregar alternativos si existen
        if nombre in ALTERNATIVAS_EJERCICIOS:
            for alt in ALTERNATIVAS_EJERCICIOS[nombre]:
                ejercicios_completos.append(alt["nombre"])
    
    return sorted(list(set(ejercicios_completos)))

# ========== ALTERNATIVAS DE EJERCICIOS ==========
ALTERNATIVAS_EJERCICIOS = {
    "Sentadilla Barra": [
        {"nombre": "Sentadilla Búlgara", "series": "3x8-10 (por pierna)"},
        {"nombre": "Sentadilla Goblet", "series": "3x10-12"},
        {"nombre": "Sentadilla Smith", "series": "3x10-12"},
    ],
    "Prensa de Pierna": [
        {"nombre": "Sentadilla Hack", "series": "3x10-12"},
        {"nombre": "Leg Press V", "series": "3x10-12"},
        {"nombre": "Prensa Horizontal", "series": "3x10-12"},
    ],
    "Extensión de Cuádriceps": [
        {"nombre": "Leg Extension Máquina", "series": "3x12-15"},
        {"nombre": "Sissy Squat", "series": "3x10-12"},
    ],
    "Empuje de Cadera": [
        {"nombre": "Puente de Glúteos (sin peso)", "series": "3x15-20"},
        {"nombre": "Máquina Abductora", "series": "3x12-15"},
        {"nombre": "Elevación de Cadera Máquina", "series": "3x10-12"},
    ],
    "Press Banca Plano": [
        {"nombre": "Press Mancuerna Plano", "series": "4x8-10"},
        {"nombre": "Press en Máquina", "series": "4x8-10"},
        {"nombre": "Push-ups", "series": "3x8-12"},
    ],
    "Press Inclinado Mancuernas": [
        {"nombre": "Press Banca Inclinado", "series": "3x8-10"},
        {"nombre": "Press Inclinado Máquina", "series": "3x8-10"},
        {"nombre": "Aperturas Inclinadas", "series": "3x10-12"},
    ],
    "Aperturas en Pecho": [
        {"nombre": "Aperturas Mancuerna Pecho", "series": "3x12-15"},
        {"nombre": "Pec Deck Máquina", "series": "3x12-15"},
    ],
    "Prensa Militar": [
        {"nombre": "Press Mancuerna Sentado", "series": "3x8-10"},
        {"nombre": "Press Pike (cuerpo completo)", "series": "3x8-10"},
        {"nombre": "Elevación Frontal", "series": "3x10-12"},
    ],
    "Peso Muerto Rumano": [
        {"nombre": "Peso Muerto Convencional", "series": "4x6-8"},
        {"nombre": "Stiff Leg Deadlift", "series": "4x8-10"},
        {"nombre": "Trap Bar Deadlift", "series": "4x6-8"},
    ],
    "Curl Femoral": [
        {"nombre": "Curl Nórdico", "series": "3x5-8"},
        {"nombre": "Curl Acostado Máquina", "series": "3x10-12"},
        {"nombre": "Curl Femoral Sentado", "series": "3x10-12"},
    ],
    "Nordic Curl": [
        {"nombre": "Curl Femoral Máquina", "series": "3x10-12"},
        {"nombre": "Nordic Curl Asistido", "series": "3x8-10"},
    ],
    "Hip Thrust con Barra": [
        {"nombre": "Hip Thrust Mancuerna", "series": "3x10-12"},
        {"nombre": "Hip Thrust Máquina", "series": "3x10-12"},
    ],
    "Remo Barra": [
        {"nombre": "Remo Mancuerna", "series": "3x8-10"},
        {"nombre": "Remo T-Bar", "series": "3x8-10"},
        {"nombre": "Remo en Máquina", "series": "3x10-12"},
    ],
    "Jalón al Pecho": [
        {"nombre": "Jalón Inverso", "series": "3x8-10"},
        {"nombre": "Jalón Máquina", "series": "3x10-12"},
        {"nombre": "Remo Vertical", "series": "3x10-12"},
    ],
    "Remo Mancuerna": [
        {"nombre": "Remo Máquina", "series": "3x10-12"},
        {"nombre": "Remo con Cable", "series": "3x10-12"},
    ],
    "Curl de Bíceps": [
        {"nombre": "Curl Mancuerna", "series": "3x10-12"},
        {"nombre": "Curl en Máquina", "series": "3x10-12"},
        {"nombre": "Curl en Cable", "series": "3x10-12"},
    ],
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
if "config_loaded" not in st.session_state:
    st.session_state.config_loaded = False

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

def calcular_superavit_calorico(peso, altura, edad=26):
    """
    Calcular calorías sugeridas para ganancia muscular
    Usa fórmula Harris-Benedict + factor de actividad + superávit
    """
    # Harris-Benedict para hombres (kcal/día)
    tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    
    # Factor de actividad (entrenamiento 5-6 veces/semana)
    tdee = tmb * 1.55
    
    # Superávit calórico para ganancia muscular (350 kcal/día)
    kcal_sugeridas = tdee + 350
    
    return round(kcal_sugeridas)

# ========== HEADER ==========
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <h1 style="color: #A8B894; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif; font-weight: 700; letter-spacing: -0.5px; margin: 0.5rem 0;">Coach Nutriólogo Pro</h1>
    <p style="color: #1F1F1F; font-size: 0.95rem; font-weight: 400; margin: 0.5rem 0;">Sistema avanzado de entrenamiento y nutrición</p>
</div>
""", unsafe_allow_html=True)
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
    
    st.markdown("### Tus Metas (85% cumplimiento)")
    
    # Metas a 2, 4, 6, 8 meses con 85% cumplimiento
    peso_inicial = 71.4
    musculo_inicial = 40.6
    grasa_inicial = 22.4
    
    ganancia_musculo_mes = 1.5
    ganancia_peso_mes = 2.0
    reduccion_grasa_mes = 0.5
    
    meses_meta = [
        {"mes": "2 meses", "num": 2},
        {"mes": "4 meses", "num": 4},
        {"mes": "6 meses", "num": 6},
        {"mes": "8 meses", "num": 8},
    ]
    
    col_m1, col_m2 = st.columns(2)
    
    for idx, meta in enumerate(meses_meta):
        mes_num = meta["num"]
        
        # 85% cumplimiento (70% de ganancias)
        peso_85 = peso_inicial + (ganancia_peso_mes * mes_num * 0.70)
        musculo_85 = musculo_inicial + (ganancia_musculo_mes * mes_num * 0.70)
        grasa_85 = max(grasa_inicial - (reduccion_grasa_mes * mes_num * 0.70), 12)
        
        col = col_m1 if idx % 2 == 0 else col_m2
        
        with col:
            st.markdown(f"""
            <div class="stat-box" style="font-size: 0.9rem; padding: 12px;">
                <div style="font-weight: 600; color: #1F1F1F; margin-bottom: 8px;">{meta['mes']}</div>
                <div style="font-size: 0.85rem; line-height: 1.6;">
                    <strong>{peso_85:.1f}kg</strong><br>
                    {musculo_85:.1f}% musc.<br>
                    {grasa_85:.1f}% grasa
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========== PÁGINA: INICIO ==========
if pagina == "Inicio":
    # Cargar configuración desde BD solo una vez
    if not st.session_state.config_loaded:
        config = obtener_configuracion()
        st.session_state.peso_actual = config["peso_actual"]
        st.session_state.altura = config["altura"]
        st.session_state.config_loaded = True
    
    st.markdown("## Carlos, esta es tu Composición Corporal")
    
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
    
    # ========== METAS MENSUALES ==========
    st.markdown("## Metas Mensuales")
    
    # Proyecciones mensuales (considerando ganancia de peso y masa muscular)
    meses = ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"]
    
    # Datos iniciales (reales actuales del usuario)
    peso_inicial = st.session_state.peso_actual  # 69 kg (actual)
    altura_cm = st.session_state.altura * 100  # Convertir a cm
    edad = 26  # Dato conocido de Carlos
    
    # Composición inicial (basada en 22.4% grasa)
    grasa_pct_inicial = 22.4
    peso_grasa_inicial = (peso_inicial * grasa_pct_inicial) / 100
    musculo_inicial = peso_inicial - peso_grasa_inicial
    
    # Ganancia esperada por mes (kg)
    ganancia_musculo_mes = 1.5
    ganancia_peso_mes = 2.0
    reduccion_grasa_mes = 0.5
    
    datos_metas = []
    
    # AGREGAR MES 0 (INICIO)
    kcal_mes_0 = calcular_superavit_calorico(peso_inicial, altura_cm, edad)
    datos_metas.append({
        "Mes": "Mes 0 (Inicio)",
        "Superávit": f"{kcal_mes_0} cal.",
        "100%": f"{peso_inicial:.1f}kg | {(musculo_inicial/peso_inicial)*100:.1f}% | {grasa_pct_inicial:.1f}%",
        "90%": "—",
        "85%": "—"
    })
    
    # MESES 1-6
    for i, mes in enumerate(meses):
        mes_num = i + 1
        
        # Peso proyectado a 100% cumplimiento
        peso_100 = peso_inicial + (ganancia_peso_mes * mes_num)
        
        # Proyecciones para 100% cumplimiento
        musculo_100_kg = musculo_inicial + (ganancia_musculo_mes * mes_num)
        musculo_100_pct = (musculo_100_kg / peso_100) * 100
        grasa_100_kg = peso_100 - musculo_100_kg
        grasa_100_pct = (grasa_100_kg / peso_100) * 100
        
        # 90% cumplimiento (85% de ganancias)
        peso_90 = peso_inicial + (ganancia_peso_mes * mes_num * 0.85)
        musculo_90_kg = musculo_inicial + (ganancia_musculo_mes * mes_num * 0.85)
        musculo_90_pct = (musculo_90_kg / peso_90) * 100
        grasa_90_kg = peso_90 - musculo_90_kg
        grasa_90_pct = (grasa_90_kg / peso_90) * 100
        
        # 85% cumplimiento (70% de ganancias)
        peso_85 = peso_inicial + (ganancia_peso_mes * mes_num * 0.70)
        musculo_85_kg = musculo_inicial + (ganancia_musculo_mes * mes_num * 0.70)
        musculo_85_pct = (musculo_85_kg / peso_85) * 100
        grasa_85_kg = peso_85 - musculo_85_kg
        grasa_85_pct = (grasa_85_kg / peso_85) * 100
        
        # Calcular calorías según peso proyectado a 100%
        kcal_mes = calcular_superavit_calorico(peso_100, altura_cm, edad)
        
        datos_metas.append({
            "Mes": mes,
            "Superávit": f"{kcal_mes} cal.",
            "100%": f"{peso_100:.1f}kg | {musculo_100_pct:.1f}% | {grasa_100_pct:.1f}%",
            "90%": f"{peso_90:.1f}kg | {musculo_90_pct:.1f}% | {grasa_90_pct:.1f}%",
            "85%": f"{peso_85:.1f}kg | {musculo_85_pct:.1f}% | {grasa_85_pct:.1f}%"
        })
    
    df_metas = pd.DataFrame(datos_metas)
    
    st.caption("Peso | % Masa Muscular | % Grasa Corporal")
    st.dataframe(
        df_metas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mes": st.column_config.TextColumn(width="small"),
            "Superávit": st.column_config.TextColumn(label="Superávit", width="small"),
            "100%": st.column_config.TextColumn(label="100% Cumplimiento", width="medium"),
            "90%": st.column_config.TextColumn(label="90% Cumplimiento", width="medium"),
            "85%": st.column_config.TextColumn(label="85% Cumplimiento", width="medium"),
        }
    )
    
    st.divider()
    
    # ========== CALENDARIO DE CUMPLIMIENTO ==========
    st.markdown("## Calendario de Cumplimiento Nutricional")
    
    hoy = datetime.now()
    inicio_mes = hoy.replace(day=1)
    
    # Nombre del mes centrado
    nombre_mes = inicio_mes.strftime("%B %Y").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")
    st.markdown(f"<h3 style='text-align: center; color: #1F1F1F;'>{nombre_mes}</h3>", unsafe_allow_html=True)
    
    st.markdown("**Seguimiento: Verde = Cumple 85% | Amarillo = Incumplimiento | Gris = Sin registros**")
    
    dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
    
    fecha_actual = inicio_mes
    cal_html = '<div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:8px; margin:1rem 0;">'
    
    for dia in dias_semana:
        cal_html += f'<div style="text-align:center; font-weight:600; font-size:0.8rem; color:#757575;">{dia}</div>'
    
    dias_iniciales = (inicio_mes.weekday()) % 7
    for _ in range(dias_iniciales):
        cal_html += '<div></div>'
    
    while fecha_actual.month == hoy.month:
        fecha_str = fecha_actual.strftime("%Y-%m-%d")
        
        # Validar cumplimiento del día
        cumple_85, detalles = validar_cumplimiento_dia(fecha_str, {})
        
        # Determinar color basado en estado
        if not detalles or detalles.get("error") == "Sin registros":
            # Gris: Sin registros o error
            color = "#E8E8E8"
            text_color = "#1F1F1F"
            titulo = "Sin registros"
        elif cumple_85:
            # Verde oliva pastel claro: Cumple 85%
            color = "#A8B894"
            text_color = "#1F1F1F"
            titulo = f"✓ {detalles.get('promedio', 0)}%"
        else:
            # Amarillo pastel: No cumple
            color = "#F5E6D3"
            text_color = "#1F1F1F"
            titulo = f"⚠ {detalles.get('promedio', 0)}%"
        
        cal_html += f'<div style="background:{color}; padding:0.8rem; border-radius:8px; text-align:center; font-size:0.8rem; color:{text_color}; font-weight:600; cursor:pointer;" title="{titulo}">{fecha_actual.day}</div>'
        fecha_actual += timedelta(days=1)
    
    cal_html += '</div>'
    st.markdown(cal_html, unsafe_allow_html=True)

# ========== PÁGINA: NUTRICIÓN ==========
elif pagina == "Nutrición":
    st.markdown("## Plan Nutricional Detallado")
    
    # Primero: Selectbox de dieta (para saber cuál dieta calcular)
    col_temp1, col_temp2 = st.columns([3, 1], gap="small")
    
    with col_temp2:
        dieta_seleccionada = st.selectbox(
            "Dieta",
            list(DIETAS.keys()),
            index=list(DIETAS.keys()).index(st.session_state.dieta),
            key="dieta_nutricion",
            label_visibility="collapsed"
        )
        st.session_state.dieta = dieta_seleccionada
    
    # Segundo: Calcular totales por dieta
    dieta_actual = DIETAS[st.session_state.dieta]
    total_kcal = 0
    total_p = 0
    total_c = 0
    total_g = 0
    
    for comida_key in ["desayuno", "media_mañana", "comida", "merienda", "cena", "pre_dormir"]:
        if comida_key in dieta_actual:
            comida_info = dieta_actual[comida_key]
            for alimento_data in comida_info['principales']:
                if len(alimento_data) == 3:
                    alimento, cantidad, unidad = alimento_data
                else:
                    alimento, cantidad = alimento_data
                
                if alimento.lower() not in ["agua", "creatina monohidratada"]:
                    macros = calcular_macros(alimento, cantidad)
                    total_kcal += macros["kcal"]
                    total_p += macros["p"]
                    total_c += macros["c"]
                    total_g += macros["g"]
    
    # Tercero: Mostrar barra de resumen compacta UNIFICADA
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #A8B894 0%, #96A882 100%); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-around; flex: 3; gap: 10px;">
            <div style="text-align: center; flex: 1;">
                <div style="color: white; font-size: 26px; font-weight: bold; line-height: 1;">{round(total_kcal)}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 11px; margin-top: 2px;">kcal</div>
            </div>
            <div style="text-align: center; flex: 1;">
                <div style="color: white; font-size: 26px; font-weight: bold; line-height: 1;">{round(total_p)}g</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 11px; margin-top: 2px;">Proteína</div>
            </div>
            <div style="text-align: center; flex: 1;">
                <div style="color: white; font-size: 26px; font-weight: bold; line-height: 1;">{round(total_c)}g</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 11px; margin-top: 2px;">Carbos</div>
            </div>
            <div style="text-align: center; flex: 1;">
                <div style="color: white; font-size: 26px; font-weight: bold; line-height: 1;">{round(total_g)}g</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 11px; margin-top: 2px;">Grasas</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recomendaciones adicionales
    with st.expander("💡 Recomendaciones Nutricionales y Suplementos"):
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("#### 💧 Hidratación")
            st.markdown("""
            - **Ingesta diaria:** 3-4 litros de agua
            - **Distribución:** 500ml cada hora durante el día
            - **Post-entrenamiento:** 500-750ml adicionales
            - **Referencia científica:** Estudios de Performance hidratación (ISSN)
            """)
            
            st.markdown("#### 🧴 Suplementos Recomendados")
            st.markdown("""
            - **Creatina Monohidrato:** 5g/día (aumento de fuerza y volumen muscular)
            - **Proteína Whey:** 30-40g post-entreno (recuperación)
            - **Omega-3:** 2-3g/día (inflamación, salud cardiovascular)
            - **Multivitamínico:** 1/día (cobertura micronutrientes)
            """)
        
        with col_rec2:
            st.markdown("#### ⚠️ Restricciones y Límites")
            st.markdown("""
            - **Refrescos azucarados:** Máximo 1 vaso/semana (picos de glucosa)
            - **Alcohol:** Máximo 1 vez cada 20 días (inhibe síntesis proteica)
            - **Azúcares refinados:** <20g/día fuera de comidas (estabilidad glucémica)
            - **Alimentos ultraprocesados:** Evitar en lo posible
            """)
            
            st.markdown("#### 📚 Base Científica")
            st.markdown("""
            - ISSN (International Society of Sports Nutrition)
            - Schoenfeld et al. (Nutrición para hipertrofia)
            - ACSM (American College of Sports Medicine)
            """)
        
        # Segunda fila de recomendaciones
        st.markdown("---")
        
        col_rec3, col_rec4, col_rec5 = st.columns(3)
        
        with col_rec3:
            st.markdown("#### 😴 Sueño y Descanso")
            st.markdown("""
            - **Duración:** 7-9 horas diarias (óptimo para recuperación)
            - **Horario:** Dormir mismo horario todos los días
            - **Pre-sueño:** Evitar pantallas 1 hora antes
            - **Temperatura:** 16-19°C ambiente (favorece sueño profundo)
            - **Impacto:** El 80% del crecimiento muscular ocurre durante el sueño
            """)
        
        with col_rec4:
            st.markdown("#### ⏱️ Descanso entre Series")
            st.markdown("""
            - **Movimientos compuestos:** 2-3 minutos
            - **Ejercicios secundarios:** 60-90 segundos
            - **Superseries:** 0-30 segundos entre pares
            - **Circuit training:** 30-60 segundos máximo
            - **Propósito:** Recuperación del ATP/PCr para siguiente serie
            - **Referencia:** Schoenfeld et al. (Rest-Pause Training)
            """)
        
        with col_rec5:
            st.markdown("#### 🔥 Calentamiento Pre-Entrenamiento")
            st.markdown("""
            - **Duración total:** 10-15 minutos
            - **Cardiovascular:** 3-5 min ligero (trotar, bicicleta)
            - **Movilidad:** 3-5 min (rotaciones articulares)
            - **Activación:** 2-3 min (ejercicios del tren a trabajar)
            - **Series de prueba:** 1-2 series al 50-70% de peso
            - **Beneficios:** Aumento de temperatura, activación neural, prevención de lesiones
            """)
    
    dieta = DIETAS[st.session_state.dieta]
    
    for comida_key, comida_info in dieta.items():
        # Formatear título: "media_mañana" -> "Media Mañana"
        titulo_formateado = comida_key.replace("_", " ").title()
        st.markdown(f"### {titulo_formateado}")
        st.markdown(f"*{comida_info['nombre']}*")
        
        tabla = []
        total_macros = {"kcal": 0, "p": 0, "c": 0, "g": 0}
        
        for alimento_data in comida_info['principales']:
            # Soportar tanto tuplas de 2 elementos (legacy) como de 3 (nuevo con unidades)
            if len(alimento_data) == 3:
                alimento, cantidad, unidad = alimento_data
                cantidad_display = f"{cantidad} {unidad}"
            else:
                alimento, cantidad = alimento_data
                unidad = "g"
                cantidad_display = f"{cantidad} {unidad}"
            
            # No calcular macros para agua pura
            if alimento.lower() == "agua":
                tabla.append({
                    "Alimento": alimento,
                    "Cantidad": cantidad_display,
                    "kcal": 0,
                    "Proteína (g)": 0,
                    "Carbos (g)": 0,
                    "Grasas (g)": 0,
                })
            else:
                # Usar cantidad en gramos para calcular macros (asumiendo bebidas en mL tienen equivalente)
                macros = calcular_macros(alimento, cantidad)
                tabla.append({
                    "Alimento": alimento,
                    "Cantidad": cantidad_display,
                    "kcal": macros["kcal"],
                    "Proteína (g)": macros["p"],
                    "Carbos (g)": macros["c"],
                    "Grasas (g)": macros["g"],
                })
                for key in total_macros:
                    total_macros[key] += macros[key]
        
        # Alternativas con formato claro: "Manzana (alt. a Plátano)"
        for alimento_original, alternativas in comida_info['alternativas'].items():
            for alternativa in alternativas:
                # Extraer nombre de alternativa si tiene el formato "(alt. a ...)"
                if "(alt. a" in alternativa:
                    alt_nombre = alternativa.split(" (alt. a")[0]
                else:
                    alt_nombre = alternativa
                    alternativa = f"{alternativa} (alt. a {alimento_original})"
                
                macros = calcular_macros(alt_nombre, 150)
                tabla.append({
                    "Alimento": f"↔️ {alternativa}",
                    "Cantidad": "150 g",
                    "kcal": macros["kcal"],
                    "Proteína (g)": macros["p"],
                    "Carbos (g)": macros["c"],
                    "Grasas (g)": macros["g"],
                })
        
        df = pd.DataFrame(tabla)
        
        # Configurar ancho de columnas
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Alimento": st.column_config.TextColumn(width="medium"),
                "Cantidad": st.column_config.TextColumn(width="small"),
                "kcal": st.column_config.NumberColumn(width="small"),
            }
        )
        
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
                            
                            # Mostrar alternativas si existen
                            if ej['nombre'] in ALTERNATIVAS_EJERCICIOS:
                                st.divider()
                                st.markdown("**🔄 Ejercicios Alternativos:**")
                                alternativas = ALTERNATIVAS_EJERCICIOS[ej['nombre']]
                                for alt in alternativas:
                                    st.caption(f"• {alt['nombre']} — {alt['series']}")
                
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
            ejercicio_prog = st.selectbox("Ejercicio", obtener_todos_ejercicios())
            
            col_a, col_b = st.columns(2)
            with col_a:
                series_realizadas = st.number_input("Series realizadas", value=4, min_value=1)
            with col_b:
                reps_realizadas = st.text_input("Reps realizadas (ej: 8-10)", value="8-10")
            
            peso_usado = st.number_input("Peso usado (kg)", value=0.0, step=2.5)
            
            if st.button("Guardar Progreso"):
                if guardar_progreso_entrenamiento(fecha_prog, ejercicio_prog, series_realizadas, reps_realizadas, peso_usado):
                    st.success("✓ Progreso guardado en BD")
                else:
                    st.error("Error al guardar")
        
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
        
        progreso_db = obtener_progreso_entrenamiento()
        
        if progreso_db:
            progreso_lista = []
            for prog in progreso_db:
                progreso_lista.append({
                    "Fecha": prog['fecha'],
                    "Ejercicio": prog['ejercicio'],
                    "Series": prog['series'],
                    "Reps": prog['reps'],
                    "Peso (kg)": prog['peso']
                })
            
            df_progreso = pd.DataFrame(progreso_lista)
            st.dataframe(df_progreso, use_container_width=True, hide_index=True)
        else:
            st.info("📝 No hay registros de progreso aún")

# ========== PÁGINA: REGISTROS ==========
elif pagina == "Registros":
    st.markdown("## Registro de Seguimiento")
    
    tab_nut, tab_ent = st.tabs(["📋 Nutrición", "🏋️ Entrenamiento"])
    
    with tab_nut:
        st.markdown("### Registrar Consumo Nutricional")
        st.markdown("<p style='color: #A8B894; font-size: 0.9rem; margin: 5px 0 15px 0;'>Selecciona el alimento consumido (principal u alternativa) y registra la cantidad</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # Restricción: solo hoy y hasta 30 días atrás
            from datetime import date as date_class
            hoy = date_class.today()
            fecha_min = hoy - timedelta(days=30)
            fecha = st.date_input(
                "Fecha", 
                hoy, 
                min_value=fecha_min,
                max_value=hoy,
                key="fecha_nut"
            )
        with col2:
            comida_tipo = st.selectbox("Comida", ["Desayuno", "Media mañana", "Comida", "Merienda", "Cena", "Pre-dormir"])
        with col3:
            # Horas recomendadas por platillo
            horas_platillo = {
                "Desayuno": list(range(5, 11)),  # 5:00 a 10:59
                "Media mañana": list(range(9, 13)),  # 9:00 a 12:59
                "Comida": list(range(12, 16)),  # 12:00 a 15:59
                "Merienda": list(range(15, 19)),  # 15:00 a 18:59
                "Cena": list(range(18, 22)),  # 18:00 a 21:59
                "Pre-dormir": list(range(21, 24)),  # 21:00 a 23:59
            }
            
            horas_disponibles = horas_platillo.get(comida_tipo, list(range(5, 24)))
            hora_seleccionada = st.selectbox(
                "Hora", 
                [f"{h:02d}:00" for h in horas_disponibles],
                key="hora_nut"
            )
            hora = datetime.strptime(hora_seleccionada, "%H:%M").time()
        
        # Mostrar alimentos de la dieta actual
        dieta_actual = DIETAS[st.session_state.dieta]
        # Convertir comida_tipo a clave de dieta (reemplazar guiones y espacios por guiones bajos)
        comida_key = comida_tipo.lower().replace(" ", "_").replace("-", "_")
        
        items_registro = []
        
        if comida_key in dieta_actual:
            comida_info = dieta_actual[comida_key]
            st.markdown(f"*{comida_info['nombre']}*")
            
            for alimento_data in comida_info['principales']:
                # Manejar tuplas de 2 o 3 elementos
                if len(alimento_data) == 3:
                    alimento, cantidad, unidad = alimento_data
                else:
                    alimento, cantidad = alimento_data
                    unidad = "g"
                
                col_a, col_b, col_c = st.columns([1.5, 1, 1.2])
                
                # Obtener alternativas si existen
                alternativas_disp = comida_info.get('alternativas', {}).get(alimento, [])
                
                # Extraer nombres limpios de alternativas
                alts_limpias = [alt.split(" (alt. a")[0] if "(alt. a" in alt else alt for alt in alternativas_disp]
                opciones_completas = [alimento] + alts_limpias
                
                with col_a:
                    st.markdown(f"**{alimento}**")
                    
                    # Radio buttons: principal + alternativas - VISIBLE Y SELECCIONABLE
                    if alts_limpias:
                        # Si hay alternativas, mostrar como radio buttons
                        consumido_nombre = st.radio(
                            f"Consumido (de {alimento})",
                            options=opciones_completas,
                            index=0,
                            key=f"radio_{comida_key}_{alimento}",
                            label_visibility="collapsed",
                            horizontal=True
                        )
                    else:
                        # Si no hay alternativas, simple selectbox
                        consumido_nombre = st.selectbox(
                            f"Consumido (de {alimento})",
                            [alimento],
                            key=f"sel_{comida_key}_{alimento}",
                            label_visibility="collapsed"
                        )
                
                with col_b:
                    st.text(f"{cantidad} {unidad}")
                
                with col_c:
                    consumido = st.number_input(
                        f"Consumo", 
                        value=cantidad, 
                        key=f"cons_{alimento}", 
                        label_visibility="collapsed"
                    )
                
                # Limpiar nombre para guardar en BD
                consumido_nombre_limpio = consumido_nombre
                
                items_registro.append({
                    "alimento": alimento,
                    "recomendado": cantidad,
                    "consumido": consumido,
                    "consumido_nombre": consumido_nombre_limpio
                })
        
        if st.button("Guardar Registro"):
            from datetime import date as date_class
            hoy = date_class.today()
            
            # Validar que fecha no sea futura
            if fecha > hoy:
                st.error(f"❌ No puedes registrar una fecha futura. Hoy es {hoy}")
            elif items_registro:
                # Convertir comida_tipo a formato de BD (minúsculas, espacios a guiones bajos)
                comida_tipo_bd = comida_tipo.lower().replace(" ", "_").replace("-", "_")
                
                if guardar_registro_nutricion(fecha, hora, comida_tipo_bd, st.session_state.dieta, items_registro, calcular_macros):
                    st.success("✓ Registro guardado exitosamente en la base de datos")
                else:
                    st.error("❌ Error al guardar. Verifica la conexión a la BD")
            else:
                st.warning("⚠️ Selecciona una comida válida para registrar")
        
        st.divider()
        
        st.markdown("### Histórico de Registros")
        
        registros_db = obtener_registros_nutricion(fecha)
        
        if registros_db:
            # Agrupar por fecha y hora de comida
            registros_por_fecha = {}
            for reg in registros_db:
                fecha_reg = str(reg['fecha'])
                if fecha_reg not in registros_por_fecha:
                    registros_por_fecha[fecha_reg] = {}
                
                clave_comida = (str(reg['hora']), reg['comida'])
                if clave_comida not in registros_por_fecha[fecha_reg]:
                    registros_por_fecha[fecha_reg][clave_comida] = []
                
                registros_por_fecha[fecha_reg][clave_comida].append(reg)
            
            # Mostrar por fecha
            for fecha_mostrar in sorted(registros_por_fecha.keys(), reverse=True):
                comidas_dia = registros_por_fecha[fecha_mostrar]
                
                # Calcular totales del día
                total_kcal = 0
                total_proteina = 0
                total_carbos = 0
                total_grasas = 0
                
                st.markdown(f"**📅 {fecha_mostrar}**")
                
                # Mostrar cada comida del día
                for (hora_comida, nombre_comida), registros in sorted(comidas_dia.items(), reverse=True):
                    st.markdown(f"*{nombre_comida}* - {hora_comida}")
                    
                    tabla_monitoreo = []
                    cumplimientos = []
                    
                    for reg in registros:
                        tabla_monitoreo.append({
                            "Alimento": reg['alimento_recomendado'],
                            "Gramaje": reg['gramos_recomendado'],
                            "Alimento consumido": reg['alimento_consumido'],
                            "Gramaje consumido": reg['gramos_consumido'],
                            "Alternativa": reg['alternativa'],
                            "% cumplimiento": f"{reg['porcentaje_cumplimiento']}%",
                            "ID": reg['id']
                        })
                        # Solo agregar porcentajes > 0 al cálculo de promedio
                        if reg['porcentaje_cumplimiento'] > 0:
                            cumplimientos.append(reg['porcentaje_cumplimiento'])
                        
                        # Acumular macronutrientes
                        if reg['kcal']:
                            total_kcal += reg['kcal']
                        if reg['proteina_g']:
                            total_proteina += reg['proteina_g']
                        if reg['carbos_g']:
                            total_carbos += reg['carbos_g']
                        if reg['grasas_g']:
                            total_grasas += reg['grasas_g']
                    
                    if tabla_monitoreo:
                        df_monitoreo = pd.DataFrame([{k: v for k, v in d.items() if k != 'ID'} for d in tabla_monitoreo])
                        st.dataframe(df_monitoreo, use_container_width=True, hide_index=True)
                        
                        # Sección de edición
                        with st.expander("✏️ Editar o eliminar registros"):
                            st.markdown("**✏️ Editar alimentos individuales:**")
                            
                            for i, reg in enumerate(registros):
                                col_e1, col_e2, col_e3 = st.columns([0.5, 0.25, 0.25])
                                with col_e1:
                                    nuevo_gramaje = st.number_input(
                                        f"Gramaje: {reg['alimento_consumido']}",
                                        value=float(reg['gramos_consumido']),
                                        step=1.0,
                                        key=f"gramaje_{reg['id']}"
                                    )
                                with col_e2:
                                    if st.button("Actualizar", key=f"actualizar_{reg['id']}"):
                                        if actualizar_registro_nutricion(reg['id'], nuevo_gramaje, calcular_macros):
                                            st.success(f"✓ Actualizado")
                                            st.rerun()
                                with col_e3:
                                    if st.button("Eliminar", key=f"eliminar_{reg['id']}"):
                                        if eliminar_registro_nutricion(reg['id']):
                                            st.success(f"✓ Eliminado")
                                            st.rerun()
                        
                        if cumplimientos:
                            promedio = round(sum(cumplimientos) / len(cumplimientos), 1)
                            st.markdown(f"*Porcentaje de cumplimiento promedio: **{promedio}%***")
                
                # Mostrar expander con totales del día
                with st.expander(f"Resumen del Día - kcal: {round(total_kcal)}, Proteína: {round(total_proteina)}g, Carbos: {round(total_carbos)}g, Grasas: {round(total_grasas)}g"):
                    col_k, col_p, col_c, col_g = st.columns(4)
                    with col_k:
                        st.metric("Total kcal", round(total_kcal))
                    with col_p:
                        st.metric("Proteína (g)", round(total_proteina, 1))
                    with col_c:
                        st.metric("Carbohidratos (g)", round(total_carbos, 1))
                    with col_g:
                        st.metric("Grasas (g)", round(total_grasas, 1))
                
                st.divider()
        else:
            st.info("No hay registros para esta fecha")
        
        # Gráfica de cumplimiento últimos 7 días
        st.markdown("### Cumplimiento Nutricional (Últimos 7 días)")
        
        from datetime import timedelta
        
        # Diccionario de meses en español
        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        
        datos_grafica = []
        meses_involucrados = set()
        
        for i in range(7, 0, -1):  # Últimos 7 días
            fecha_grafica = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
            cumple, detalles = validar_cumplimiento_dia(fecha_grafica, {})
            
            fecha_obj = datetime.today() - timedelta(days=i)
            promedio_dia = detalles.get("promedio", 0) if detalles else 0
            
            meses_involucrados.add(fecha_obj.month)
            
            datos_grafica.append({
                "Día": fecha_obj.strftime("%d"),
                "Cumplimiento %": float(promedio_dia) if promedio_dia else 0
            })
        
        df_grafica = pd.DataFrame(datos_grafica)
        
        if df_grafica["Cumplimiento %"].sum() > 0:
            fig = go.Figure(data=[
                go.Bar(
                    x=df_grafica["Día"],
                    y=df_grafica["Cumplimiento %"],
                    width=0.5,
                    marker=dict(
                        color=df_grafica["Cumplimiento %"],
                        colorscale=[[0, '#F5E6D3'], [0.85, '#D4E0C9'], [0.86, '#A8B894'], [1, '#A8B894']],
                        showscale=False,
                        line=dict(width=0)
                    ),
                    text=df_grafica["Cumplimiento %"].round(0).astype(str) + "%",
                    textposition="inside",
                    textfont=dict(size=14, color="white"),
                    hovertemplate="Día %{x}<br>Cumplimiento: %{y:.1f}%<extra></extra>"
                )
            ])
            
            # Determinar título del mes
            año = datetime.today().year
            if len(meses_involucrados) == 1:
                # Un solo mes
                mes_numero = list(meses_involucrados)[0]
                mes_titulo = f"{meses_es[mes_numero]} {año}"
            else:
                # Dos meses consecutivos
                meses_sorted = sorted(meses_involucrados)
                mes1 = meses_es[meses_sorted[0]]
                mes2 = meses_es[meses_sorted[1]]
                mes_titulo = f"{mes1} - {mes2} {año}"
            
            fig.update_layout(
                title=dict(
                    text=f"<i style='font-size:16px; color:#666; font-weight:normal'>{mes_titulo}</i>",
                    x=0.5,
                    xanchor="center",
                    y=0.98,
                    yanchor="top"
                ),
                xaxis_title=None,
                yaxis_title=None,
                height=180,
                showlegend=False,
                hovermode="x unified",
                margin=dict(l=30, r=20, t=40, b=25),
                template="plotly_white"
            )
            fig.update_yaxes(
                range=[0, 100], 
                showticklabels=False, 
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(200, 200, 200, 0.2)",
                showline=True,
                linewidth=1,
                linecolor="rgba(150, 150, 150, 0.3)",
                zeroline=False
            )
            fig.update_xaxes(
                showgrid=False, 
                showline=True,
                linewidth=1,
                linecolor="rgba(150, 150, 150, 0.3)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos de cumplimiento en los últimos 7 días")
    
    with tab_ent:
        st.markdown("### Registrar Entrenamiento")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_ent = st.date_input("Fecha", datetime.today(), key="fecha_ent")
        with col2:
            hora_ent = st.time_input("Hora", datetime.now().time(), key="hora_ent")
        with col3:
            lugar = st.selectbox("Lugar", ["Gimnasio", "Casa"])
        
        tren = st.selectbox("Tren", list(ENTRENAMIENTOS.keys()))
        
        # Checklist de ejercicios del tren seleccionado (principales + alternativos)
        st.markdown("**Ejercicios realizados:**")
        ejercicios_tren = obtener_ejercicios_completos_por_tren(tren)
        
        cols_ejercicios = st.columns(3)
        ejercicios_realizados = []
        
        for idx, ejercicio in enumerate(ejercicios_tren):
            col = cols_ejercicios[idx % 3]
            with col:
                if st.checkbox(ejercicio, key=f"check_ent_{ejercicio}_{tren}"):
                    ejercicios_realizados.append(ejercicio)
        
        duracion = st.number_input("Duración (min)", value=60)
        
        if st.button("Guardar Entrenamiento"):
            if guardar_registro_entrenamiento(fecha_ent, hora_ent, lugar, tren, duracion):
                st.success("✓ Entrenamiento guardado en BD")
            else:
                st.error("Error al guardar el registro")
        
        st.divider()
        
        registros_db_ent = obtener_registros_entrenamiento()
        
        if registros_db_ent:
            # Convertir a DataFrame para mostrar
            registros_lista = []
            for reg in registros_db_ent:
                registros_lista.append({
                    "Fecha": reg['fecha'],
                    "Hora": reg['hora'],
                    "Tren": reg['tren'],
                    "Lugar": reg['lugar'],
                    "Duración (min)": reg['duracion'],
                    "ID": reg['id']
                })
            
            df_ent = pd.DataFrame([{k: v for k, v in d.items() if k != 'ID'} for d in registros_lista])
            st.dataframe(df_ent, use_container_width=True, hide_index=True)
            
            # Sección de editar/eliminar
            with st.expander("✏️ Editar o eliminar entrenamientos"):
                for i, reg in enumerate(registros_db_ent):
                    col_e1, col_e2, col_e3 = st.columns([0.5, 0.25, 0.25])
                    with col_e1:
                        duracion_edit = st.number_input(
                            f"Duración (min) - {reg['fecha']} {reg['tren']}",
                            value=int(reg['duracion']),
                            min_value=5,
                            step=5,
                            key=f"dur_ent_{reg['id']}"
                        )
                    with col_e2:
                        if st.button("Actualizar", key=f"upd_ent_{reg['id']}"):
                            if actualizar_registro_entrenamiento(reg['id'], duracion_edit):
                                st.success("✓ Actualizado")
                                st.rerun()
                    with col_e3:
                        if st.button("Eliminar", key=f"del_ent_{reg['id']}"):
                            if eliminar_registro_entrenamiento(reg['id']):
                                st.success("✓ Eliminado")
                                st.rerun()
        else:
            st.info("📝 No hay entrenamientos registrados")

# ========== PÁGINA: CONFIGURACIÓN ==========
elif pagina == "Configuración":
    st.markdown("## Configuración")
    
    st.markdown("### Datos Personales")
    col1, col2 = st.columns(2)
    with col1:
        nuevo_peso = st.number_input("Peso (kg)", value=st.session_state.peso_actual, step=0.1)
    with col2:
        nueva_altura = st.number_input("Altura (m)", value=st.session_state.altura, step=0.01)
    
    if st.button("Guardar Cambios"):
        if guardar_configuracion(nuevo_peso, nueva_altura):
            st.session_state.peso_actual = nuevo_peso
            st.session_state.altura = nueva_altura
            st.success("✓ Datos guardados correctamente en BD")
            st.rerun()
        else:
            st.error("Error al guardar los datos")
    
    st.divider()
    
    st.markdown("### Registro de Peso Diario (En ayunas)")
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_peso = st.date_input("Fecha del registro", datetime.today(), key="fecha_peso")
    with col2:
        peso_diario = st.number_input("Peso (kg)", value=st.session_state.peso_actual, step=0.1, key="peso_diario")
    
    notas = st.text_input("Notas (opcional)", placeholder="Ej: Pesado por la tarde, hidratación alta")
    
    col_a, col_b = st.columns([0.7, 0.3])
    with col_a:
        if st.button("Registrar Peso", use_container_width=True):
            if guardar_peso_diario(fecha_peso, peso_diario, notas):
                st.success(f"✓ Peso registrado: {peso_diario}kg en {fecha_peso}")
                st.rerun()
    
    with col_b:
        st.write("")  # Espaciador
    
    # Histórico de pesos
    st.markdown("#### Histórico (últimos 30 días)")
    pesos = obtener_pesos_diarios()
    
    if pesos:
        df_pesos = pd.DataFrame(pesos)
        df_pesos['Cambio'] = df_pesos['peso'].diff().round(2)
        
        # Mostrar tabla
        st.dataframe(
            df_pesos[['fecha', 'peso', 'Cambio', 'notas']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "fecha": st.column_config.DateColumn("Fecha"),
                "peso": st.column_config.NumberColumn("Peso (kg)", format="%.2f kg"),
                "Cambio": st.column_config.NumberColumn("Cambio (kg)", format="%.2f kg"),
                "notas": st.column_config.TextColumn("Notas"),
            }
        )
        
        # Botones de editar/eliminar
        with st.expander("✏️ Editar o eliminar registros"):
            for idx, registro in enumerate(pesos):
                col_d1, col_d2, col_d3 = st.columns([0.5, 0.25, 0.25])
                with col_d1:
                    nuevo_peso_edit = st.number_input(
                        f"Peso {registro['fecha']}", 
                        value=float(registro['peso']),
                        step=0.1,
                        key=f"peso_edit_{idx}"
                    )
                with col_d2:
                    if st.button("Actualizar", key=f"save_peso_{idx}", help="Actualizar"):
                        if guardar_peso_diario(registro['fecha'], nuevo_peso_edit, registro['notas']):
                            st.success("✓ Actualizado")
                            st.rerun()
                with col_d3:
                    if st.button("🗑️", key=f"del_peso_{idx}", help="Eliminar"):
                        if eliminar_peso_diario(registro['fecha']):
                            st.success("✓ Eliminado")
                            st.rerun()
    else:
        st.info("No hay registros de peso aún. ¡Comienza a registrar!")

st.divider()
ahora = datetime.now()
fecha_hora = ahora.strftime("%A, %d de %B de %Y | %H:%M:%S").replace("Monday", "Lunes").replace("Tuesday", "Martes").replace("Wednesday", "Miércoles").replace("Thursday", "Jueves").replace("Friday", "Viernes").replace("Saturday", "Sábado").replace("Sunday", "Domingo").replace("January", "Enero").replace("February", "Febrero").replace("March", "Marzo").replace("April", "Abril").replace("May", "Mayo").replace("June", "Junio").replace("July", "Julio").replace("August", "Agosto").replace("September", "Septiembre").replace("October", "Octubre").replace("November", "Noviembre").replace("December", "Diciembre")
st.caption(f"⏰ {fecha_hora} | Coach Nutriólogo Pro © 2024")
