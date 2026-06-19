import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import streamlit as st

# ========== CONFIGURACIÓN DE CONEXIÓN (Lee Secrets de Streamlit Cloud) ==========

def get_db_config():
    """Obtener configuración de BD desde connection string de Neon"""
    try:
        conn_str = st.secrets["database"]["connection_string"]
        return conn_str
    except:
        return "postgresql://postgres:Terracota00@localhost/coach_nutriologo"

DB_CONFIG = get_db_config()

def get_connection():
    """Obtener nueva conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        st.error(f"Error de conexión a BD: {e}")
        return None

# ========== REGISTROS DE NUTRICIÓN ==========

def guardar_registro_nutricion(fecha, hora, comida, dieta, items_con_recomendado, calcular_macros_fn):
    """Guardar registro de nutrición en BD con dieta, alternativa y macronutrientes"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        with conn.cursor() as cur:
            for item in items_con_recomendado:
                # Calcular % cumplimiento
                gramos_recomendado = item['recomendado']
                gramos_consumido = item['consumido']
                porcentaje = round((gramos_consumido / gramos_recomendado * 100), 1) if gramos_recomendado > 0 else 0
                
                # Determinar si es alternativa
                es_alternativa = "Sí" if item['alimento'] != item['consumido_nombre'] else "No"
                
                # Calcular macronutrientes del alimento consumido
                macros = calcular_macros_fn(item['consumido_nombre'], gramos_consumido)
                
                cur.execute("""
                    INSERT INTO registros_nutricion 
                    (usuario_id, fecha, hora, comida, dieta, alimento_recomendado, alimento_consumido, 
                     alternativa, gramos_recomendado, gramos_consumido, porcentaje_cumplimiento,
                     kcal, proteina_g, carbos_g, grasas_g)
                    VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (fecha, hora, comida, dieta, item['alimento'], item['consumido_nombre'], 
                      es_alternativa, gramos_recomendado, gramos_consumido, porcentaje,
                      macros['kcal'], macros['p'], macros['c'], macros['g']))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al guardar: {e}")
        if conn:
            conn.close()
        return False

def obtener_registros_nutricion(fecha=None):
    """Obtener registros de nutrición agrupados por comida"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if fecha:
                cur.execute("""
                    SELECT id, fecha, hora, comida, dieta, alimento_recomendado, alimento_consumido, 
                           alternativa, gramos_recomendado, gramos_consumido, porcentaje_cumplimiento,
                           kcal, proteina_g, carbos_g, grasas_g
                    FROM registros_nutricion 
                    WHERE usuario_id = 1 AND fecha = %s
                    ORDER BY hora DESC, comida
                """, (fecha,))
            else:
                cur.execute("""
                    SELECT id, fecha, hora, comida, dieta, alimento_recomendado, alimento_consumido, 
                           alternativa, gramos_recomendado, gramos_consumido, porcentaje_cumplimiento,
                           kcal, proteina_g, carbos_g, grasas_g
                    FROM registros_nutricion 
                    WHERE usuario_id = 1
                    ORDER BY fecha DESC, hora DESC
                    LIMIT 100
                """)
            
            resultados = cur.fetchall()
        
        conn.close()
        return resultados
    except psycopg2.Error as e:
        st.error(f"Error al obtener registros: {e}")
        if conn:
            conn.close()
        return []

# ========== REGISTROS DE ENTRENAMIENTO ==========

def guardar_registro_entrenamiento(fecha, hora, lugar, tren, duracion, notas=""):
    """Guardar registro de entrenamiento en BD"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO registros_entrenamiento 
                (usuario_id, fecha, hora, tren, lugar, duracion, notas)
                VALUES (1, %s, %s, %s, %s, %s, %s)
            """, (fecha, hora, tren, lugar, duracion, notas))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al guardar: {e}")
        if conn:
            conn.close()
        return False

def obtener_registros_entrenamiento(fecha=None):
    """Obtener registros de entrenamiento de BD"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if fecha:
                cur.execute("""
                    SELECT * FROM registros_entrenamiento 
                    WHERE usuario_id = 1 AND fecha = %s
                    ORDER BY hora DESC
                """, (fecha,))
            else:
                cur.execute("""
                    SELECT * FROM registros_entrenamiento 
                    WHERE usuario_id = 1
                    ORDER BY fecha DESC, hora DESC
                    LIMIT 100
                """)
            
            resultados = cur.fetchall()
        
        conn.close()
        return resultados
    except psycopg2.Error as e:
        st.error(f"Error al obtener registros: {e}")
        if conn:
            conn.close()
        return []

# ========== PROGRESO DE ENTRENAMIENTO ==========

def guardar_progreso_entrenamiento(fecha, ejercicio, series, reps, peso):
    """Guardar progreso de entrenamiento en BD"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO progreso_entrenamiento 
                (usuario_id, fecha, ejercicio, series, reps, peso)
                VALUES (1, %s, %s, %s, %s, %s)
            """, (fecha, ejercicio, series, reps, peso))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al guardar: {e}")
        if conn:
            conn.close()
        return False

def obtener_progreso_entrenamiento():
    """Obtener historial de progreso de BD"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM progreso_entrenamiento 
                WHERE usuario_id = 1
                ORDER BY fecha DESC, ejercicio
                LIMIT 100
            """)
            
            resultados = cur.fetchall()
        
        conn.close()
        return resultados
    except psycopg2.Error as e:
        st.error(f"Error al obtener registros: {e}")
        if conn:
            conn.close()
        return []


def obtener_totales_nutricion_dia(fecha):
    """Obtener totales de macronutrientes por día"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    SUM(kcal) as total_kcal,
                    SUM(proteina_g) as total_proteina,
                    SUM(carbos_g) as total_carbos,
                    SUM(grasas_g) as total_grasas
                FROM registros_nutricion
                WHERE usuario_id = 1 AND fecha = %s
            """, (fecha,))
            
            resultado = cur.fetchone()
        
        conn.close()
        return resultado
    except psycopg2.Error:
        if conn:
            conn.close()
        return None

def guardar_configuracion(peso, altura):
    """Guardar peso y altura del usuario en BD"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE usuarios 
                SET peso_actual = %s, altura = %s, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (peso, altura))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al guardar: {e}")
        if conn:
            conn.close()
        return False

def actualizar_registro_nutricion(registro_id, gramos_consumido, calcular_macros_fn):
    """Actualizar registro de nutrición existente"""
    conn = get_connection()
    if not conn:
        st.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Obtener datos del registro
            cur.execute("SELECT alimento_consumido, gramos_recomendado, dieta FROM registros_nutricion WHERE id = %s", (registro_id,))
            registro = cur.fetchone()
            
            if not registro:
                st.error("Registro no encontrado")
                return False
            
            # Calcular nuevo porcentaje y macros
            gramos_recomendado = registro['gramos_recomendado']
            porcentaje = round((gramos_consumido / gramos_recomendado * 100), 1) if gramos_recomendado > 0 else 0
            
            macros = calcular_macros_fn(registro['alimento_consumido'], gramos_consumido)
            
            # Actualizar registro
            cur.execute("""
                UPDATE registros_nutricion 
                SET gramos_consumido = %s, porcentaje_cumplimiento = %s,
                    kcal = %s, proteina_g = %s, carbos_g = %s, grasas_g = %s
                WHERE id = %s
            """, (gramos_consumido, porcentaje, macros['kcal'], macros['p'], 
                  macros['c'], macros['g'], registro_id))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al actualizar: {e}")
        if conn:
            conn.close()
        return False

def eliminar_registro_nutricion(registro_id):
    """Eliminar un registro de nutrición"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM registros_nutricion WHERE id = %s", (registro_id,))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al eliminar: {e}")
        if conn:
            conn.close()
        return False

def obtener_progreso_por_ejercicio(ejercicio):
    """Obtener progreso de un ejercicio específico"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM progreso_entrenamiento 
                WHERE usuario_id = 1 AND ejercicio = %s
                ORDER BY fecha DESC
            """, (ejercicio,))
            
            resultados = cur.fetchall()
        
        conn.close()
        return resultados
    except psycopg2.Error:
        if conn:
            conn.close()
        return []

def guardar_peso_diario(fecha, peso, notas=""):
    """Guardar peso diario (mañana, en ayunas)"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO pesos_diarios (usuario_id, fecha, peso, notas)
                VALUES (1, %s, %s, %s)
                ON CONFLICT (fecha) DO UPDATE 
                SET peso = EXCLUDED.peso, notas = EXCLUDED.notas
            """, (fecha, peso, notas))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error as e:
        st.error(f"Error al guardar peso: {e}")
        if conn:
            conn.close()
        return False

def obtener_pesos_diarios():
    """Obtener todos los pesos registrados"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT fecha, peso, notas FROM pesos_diarios
                WHERE usuario_id = 1
                ORDER BY fecha DESC
                LIMIT 30
            """)
            
            resultados = cur.fetchall()
        
        conn.close()
        return resultados
    except psycopg2.Error:
        if conn:
            conn.close()
        return []

def eliminar_peso_diario(fecha):
    """Eliminar registro de peso de una fecha"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM pesos_diarios WHERE usuario_id = 1 AND fecha = %s", (fecha,))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error:
        if conn:
            conn.close()
        return False

def actualizar_registro_entrenamiento(registro_id, duracion):
    """Actualizar duración de un registro de entrenamiento"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE registros_entrenamiento 
                SET duracion = %s
                WHERE id = %s
            """, (duracion, registro_id))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error:
        if conn:
            conn.close()
        return False

def eliminar_registro_entrenamiento(registro_id):
    """Eliminar un registro de entrenamiento"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM registros_entrenamiento WHERE id = %s", (registro_id,))
        
        conn.commit()
        conn.close()
        return True
    except psycopg2.Error:
        if conn:
            conn.close()
        return False

def obtener_configuracion():
    """Obtener peso y altura del usuario desde BD"""
    conn = get_connection()
    if not conn:
        return {"peso_actual": 71.4, "altura": 1.68}
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT peso_actual, altura FROM usuarios WHERE id = 1
            """)
            
            resultado = cur.fetchone()
        
        conn.close()
        if resultado:
            return {"peso_actual": float(resultado['peso_actual']), "altura": float(resultado['altura'])}
        return {"peso_actual": 71.4, "altura": 1.68}
    except psycopg2.Error:
        if conn:
            conn.close()
        return {"peso_actual": 71.4, "altura": 1.68}

def validar_cumplimiento_dia(fecha, limites_dieta):
    """Validar si el día cumple con el 85% de macronutrientes"""
    conn = get_connection()
    if not conn:
        return False, {}
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Obtener registros del día
            cur.execute("""
                SELECT porcentaje_cumplimiento
                FROM registros_nutricion
                WHERE usuario_id = 1 AND fecha = %s AND porcentaje_cumplimiento > 0
                ORDER BY porcentaje_cumplimiento
            """, (fecha,))
            
            registros = cur.fetchall()
        
        conn.close()
        
        # Si no hay registros, no cumple
        if not registros:
            return False, {"error": "Sin registros"}
        
        # Calcular promedio de porcentajes
        porcentajes = [r['porcentaje_cumplimiento'] for r in registros if r['porcentaje_cumplimiento']]
        
        if porcentajes:
            promedio = sum(porcentajes) / len(porcentajes)
            # Cumple si el promedio es >= 85%
            return promedio >= 85, {"promedio": round(promedio, 1), "registros": len(registros)}
        
        return False, {"error": "Sin datos válidos"}
    except psycopg2.Error:
        if conn:
            conn.close()
        return False, {}
