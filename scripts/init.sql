-- Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear tabla principal
CREATE TABLE IF NOT EXISTS entregas (
    id SERIAL PRIMARY KEY,
    alumno_nombre VARCHAR(255),
    alumno_email VARCHAR(255),
    archivo_nombre VARCHAR(500),
    texto_original TEXT,
    embedding vector(384),
    similitud_consigna FLOAT,
    max_similitud_previa FLOAT,
    decision VARCHAR(50),
    fecha_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_procesamiento TIMESTAMP
);

-- Crear índice para búsqueda de similitud
CREATE INDEX IF NOT EXISTS idx_embedding ON entregas USING ivfflat (embedding vector_cosine_ops);

-- Tabla para almacenar respuestas modelo
CREATE TABLE IF NOT EXISTS respuestas_modelo (
    id SERIAL PRIMARY KEY,
    consigna TEXT,
    embedding vector(384),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar consigna por defecto
INSERT INTO respuestas_modelo (consigna) 
VALUES ('Explicar qué es un algoritmo y dar un ejemplo.')
ON CONFLICT DO NOTHING;

-- Crear usuario para n8n (si es necesario)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'n8n_user') THEN
      CREATE USER n8n_user WITH PASSWORD 'n8n_pass';
      GRANT CONNECT ON DATABASE sice_db TO n8n_user;
      GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO n8n_user;
   END IF;
END
$do$;
