-- Habilitar extensión vector para embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear usuario no-root
DO $$
BEGIN
   CREATE USER n8n_user WITH PASSWORD 'n8n_User456!';
EXCEPTION WHEN duplicate_object THEN
   RAISE NOTICE 'Usuario ya existe';
END
$$;

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n_user;

-- Conectarse a la base de datos n8n
\c n8n;

-- Dar permisos en el schema public
GRANT ALL PRIVILEGES ON SCHEMA public TO n8n_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO n8n_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO n8n_user;

-- Crear tabla para entregas (guardará los TPs de los alumnos)
CREATE TABLE IF NOT EXISTS entregas (
    id SERIAL PRIMARY KEY,
    alumno VARCHAR(100),
    archivo_nombre VARCHAR(255),
    texto_extraido TEXT,
    embedding vector(384),
    decision VARCHAR(50),
    puntuacion FLOAT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índice para búsqueda rápida de similitud
CREATE INDEX IF NOT EXISTS idx_embedding ON entregas USING ivfflat (embedding vector_cosine_ops);
