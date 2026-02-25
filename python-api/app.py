from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import numpy as np
import time
import os

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Permitir que n8n se conecte

# Configurar timeout más largo para descarga
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '120'

# Cargar modelo UNA SOLA VEZ al iniciar
print("Cargando modelo de embeddings...")
print("(Esto puede tomar 2-3 minutos la primera vez)")
try:
    modelo = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2",
        device="cpu"
    )
    print("¡Modelo cargado correctamente!")
except Exception as e:
    print(f"Error en primera carga: {e}")
    print("Intentando con carpeta cache local...")
    os.makedirs("./modelo_cache", exist_ok=True)
    modelo = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2",
        device="cpu",
        cache_folder="./modelo_cache"
    )
    print("¡Modelo cargado con cache local!")

def generar_embedding(texto):
    """Convierte texto a embedding (vector numérico)"""
    embedding = modelo.encode(texto)
    return embedding.tolist()

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar que la API está viva"""
    return jsonify({
        "status": "ok",
        "modelo": "paraphrase-multilingual-MiniLM-L12-v2",
        "dimension": 384
    })

@app.route('/embed', methods=['POST'])
def embed():
    """
    Endpoint para generar embedding de UN texto
    Uso: POST con JSON {"texto": "tu texto aquí"}
    """
    try:
        data = request.get_json()
        
        if not data or 'texto' not in data:
            return jsonify({"error": "Se requiere campo 'texto'"}), 400
        
        texto = data['texto']
        
        if not texto or len(texto.strip()) == 0:
            return jsonify({"error": "El texto no puede estar vacío"}), 400
        
        # Medir tiempo
        inicio = time.time()
        embedding = generar_embedding(texto)
        fin = time.time()
        
        return jsonify({
            "texto": texto[:100] + "..." if len(texto) > 100 else texto,
            "embedding": embedding,
            "dimension": len(embedding),
            "tiempo_ms": round((fin - inicio) * 1000, 2)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/similitud', methods=['POST'])
def similitud():
    """
    Endpoint para calcular similitud entre DOS textos
    Uso: POST con JSON {"texto1": "hola", "texto2": "hola mundo"}
    """
    try:
        data = request.get_json()
        
        if not data or 'texto1' not in data or 'texto2' not in data:
            return jsonify({"error": "Se requieren campos 'texto1' y 'texto2'"}), 400
        
        # Asegurar codificación UTF-8
        texto1 = data['texto1'].encode('utf-8').decode('utf-8')
        texto2 = data['texto2'].encode('utf-8').decode('utf-8')
        
        emb1 = np.array(generar_embedding(texto1))
        emb2 = np.array(generar_embedding(texto2))
        
        # Calcular similitud de coseno
        cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        return jsonify({
            "texto1": texto1[:50],
            "texto2": texto2[:50],
            "similitud": float(cos_sim),
            "similitud_porcentaje": round(float(cos_sim) * 100, 2)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ejecutar en modo debug para pruebas
    app.run(host='0.0.0.0', port=5000, debug=True)