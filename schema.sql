-- Coach Nutriólogo Pro - Base de Datos Relacional
-- Ejecutar en PostgreSQL con: psql -U postgres -d coach_nutriologo -f schema.sql

-- ========== CREAR TABLAS ==========

-- Tabla de usuarios (para futuro multi-usuario)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    peso_actual DECIMAL(5,2),
    altura DECIMAL(3,2),
    edad INT,
    nivel_experiencia VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de registros de nutrición
CREATE TABLE IF NOT EXISTS pesos_diarios (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    fecha DATE NOT NULL UNIQUE,
    peso DECIMAL(5,2) NOT NULL,
    hora TIME DEFAULT CURRENT_TIME,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS registros_nutricion (
    id SERIAL PRIMARY KEY,
    usuario_id INT DEFAULT 1,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    comida VARCHAR(50) NOT NULL,
    dieta VARCHAR(50) NOT NULL,
    alimento_recomendado VARCHAR(100) NOT NULL,
    alimento_consumido VARCHAR(100) NOT NULL,
    alternativa VARCHAR(2) NOT NULL DEFAULT 'No',
    gramos_recomendado DECIMAL(6,2) NOT NULL,
    gramos_consumido DECIMAL(6,2) NOT NULL,
    porcentaje_cumplimiento DECIMAL(5,2),
    kcal DECIMAL(8,2),
    proteina_g DECIMAL(6,2),
    carbos_g DECIMAL(6,2),
    grasas_g DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de registros de entrenamiento
CREATE TABLE IF NOT EXISTS registros_entrenamiento (
    id SERIAL PRIMARY KEY,
    usuario_id INT DEFAULT 1,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    tren VARCHAR(100) NOT NULL,
    lugar VARCHAR(50) NOT NULL,
    duracion INT,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de progreso de entrenamiento
CREATE TABLE IF NOT EXISTS progreso_entrenamiento (
    id SERIAL PRIMARY KEY,
    usuario_id INT DEFAULT 1,
    fecha DATE NOT NULL,
    ejercicio VARCHAR(100) NOT NULL,
    series INT NOT NULL,
    reps VARCHAR(50) NOT NULL,
    peso DECIMAL(6,2),
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- ========== CREAR ÍNDICES ==========

CREATE INDEX IF NOT EXISTS idx_registros_nutricion_fecha ON registros_nutricion(fecha);
CREATE INDEX IF NOT EXISTS idx_registros_nutricion_usuario ON registros_nutricion(usuario_id);
CREATE INDEX IF NOT EXISTS idx_registros_entrenamiento_fecha ON registros_entrenamiento(fecha);
CREATE INDEX IF NOT EXISTS idx_registros_entrenamiento_usuario ON registros_entrenamiento(usuario_id);
CREATE INDEX IF NOT EXISTS idx_progreso_fecha ON progreso_entrenamiento(fecha);
CREATE INDEX IF NOT EXISTS idx_progreso_usuario ON progreso_entrenamiento(usuario_id);

-- ========== INSERTAR USUARIO POR DEFECTO ==========

INSERT INTO usuarios (nombre, email, peso_actual, altura, edad, nivel_experiencia)
VALUES ('Usuario Principal', 'usuario@coach.local', 71.4, 1.68, 26, 'Principiante')
ON CONFLICT DO NOTHING;
