# 🚀 DEPLOY EN STREAMLIT CLOUD CON POSTGRESQL

## ✅ Ya está en GitHub

Tu app está en: https://github.com/caledelta/coach-nutriologo

---

## 📋 PASOS PARA CONFIGURAR EN STREAMLIT CLOUD:

### PASO 1: Conecta tu repositorio (si no está hecho)
1. Ve a https://streamlit.io/cloud
2. Haz clic en "New app"
3. Selecciona `caledelta/coach-nutriologo`
4. Branch: `main`
5. File: `streamlit_app.py`
6. Haz clic en "Deploy"

### PASO 2: Configura tu Base de Datos PostgreSQL

**Opción A: Usar PostgreSQL Local (si tu BD está en la nube)**

En el dashboard de Streamlit Cloud:

1. Ve a tu app
2. Haz clic en los **3 puntos** (⋮) → **Settings**
3. Abre la sección **"Secrets"**
4. Agrega esto (reemplaza con TUS datos):

```toml
[database]
host = "localhost"
port = 5432
user = "postgres"
password = "Terracota00"
database = "coach_nutriologo"
```

**Opción B: Usar Neon (PostgreSQL Gratis en la Nube - RECOMENDADO)**

1. Ve a https://neon.tech
2. Regístrate gratis
3. Crea un proyecto "coach-nutriologo"
4. Copia la "Connection string"
5. En Secrets de Streamlit agrega:

```toml
[database]
host = "tu-neon-host.neon.tech"
port = 5432
user = "neon_user"
password = "tu_password"
database = "neon_db"
```

### PASO 3: Ejecuta el schema SQL

Conecta a tu BD (con pgAdmin o línea de comandos) y ejecuta:

```bash
psql -U postgres -d coach_nutriologo -f schema.sql
```

### PASO 4: La app se redesplegará automáticamente

La URL pública será:
```
https://coach-nutriologo-xxxxx.streamlit.app
```

---

## 🎯 Qué funciona:
✅ Nutrición con 3 dietas
✅ Entrenamientos con rutinas
✅ Registro de progreso
✅ Gráficas de cumplimiento
✅ Sincronización en BD

---

## 📱 Acceso desde celular:

```
https://coach-nutriologo-xxxxx.streamlit.app
```

(Funciona directamente en navegador del celular)

---

## 🆘 Si hay error "ModuleNotFoundError":

1. Espera 2-3 minutos (instalando dependencias)
2. Haz clic en "Rerun"
3. Verifica que requirements.txt está en GitHub

## 🆘 Si hay error de conexión a BD:

1. Verifica credenciales en Secrets
2. Asegúrate que la BD está online
3. Verifica que el schema.sql fue ejecutado completo

---

¡LISTA PARA PRODUCCIÓN! 💪

