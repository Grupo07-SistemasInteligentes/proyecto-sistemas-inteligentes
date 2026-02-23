from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading

app = Flask(__name__)
CORS(app)

# Variable global para el modelo (se carga en segundo plano)
modelo = None
modelo_cargado = False

def cargar_modelo():
    global modelo, modelo_cargado
    print("🔄 Iniciando carga del modelo en segundo plano...")
    from sentence_transformers import SentenceTransformer
    modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    modelo_cargado = True
    print("✅ Modelo cargado exitosamente!")

# Iniciar carga en segundo plano
thread = threading.Thread(target=cargar_modelo)
thread.daemon = True
thread.start()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok", 
        "modelo_cargado": modelo_cargado,
        "mensaje": "API funcionando"
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "modelo_cargado": modelo_cargado,
        "tiempo_espera": "El modelo se carga en segundo plano, intenta en unos minutos"
    })

if __name__ == '__main__':
    print("🚀 API iniciando en puerto 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
