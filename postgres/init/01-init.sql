-- Habilitar extensión vector para embeddings (Tarea de Jeremy)
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear tabla para entregas
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

CREATE INDEX IF NOT EXISTS idx_embedding ON entregas USING ivfflat (embedding vector_cosine_ops);
