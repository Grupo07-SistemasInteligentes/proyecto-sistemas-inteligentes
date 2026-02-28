# Importamos las librerías necesarias
from flask import Flask, request, jsonify   # Flask para crear la API
from sentence_transformers import SentenceTransformer  # Modelo para generar embeddings
from sklearn.metrics.pairwise import cosine_similarity  # Para medir similitud
import PyPDF2  # Para leer PDFs

# Creamos la aplicación Flask
app = Flask(__name__)

# -------------------------------
# 1️⃣ Cargar modelo de embeddings
# -------------------------------
# Este modelo convierte texto en vectores de 384 dimensiones
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# -------------------------------
# 2️⃣ Definir consigna (pregunta)
# -------------------------------
CONSIGNA = "Explicar qué es un algoritmo y dar un ejemplo."

# Generamos el embedding de la consigna una sola vez
embedding_consigna = modelo.encode(CONSIGNA)

# -------------------------------
# 3️⃣ Respuestas previas (mock)
# -------------------------------
# Simulamos respuestas anteriores almacenadas
respuestas_previas = [
    "Un algoritmo es una secuencia ordenada de pasos para resolver un problema.",
    "Un algoritmo es un conjunto de instrucciones definidas."
]

# Convertimos esas respuestas en embeddings
embeddings_previos = [modelo.encode(r) for r in respuestas_previas]

# -------------------------------
# 4️⃣ Umbrales de decisión
# -------------------------------
UMBRAL_COPIA = 0.85   # Si supera este valor → posible copia
UMBRAL_TEMA = 0.40    # Si es menor que esto → fuera de tema

# -------------------------------
# 5️⃣ Función para extraer texto del PDF
# -------------------------------
def extraer_texto_pdf(file_stream):
    """
    Recibe un archivo PDF y devuelve todo su texto concatenado.
    """
    reader = PyPDF2.PdfReader(file_stream)
    texto = ""

    # Recorremos cada página del PDF
    for page in reader.pages:
        texto += page.extract_text()

    return texto


# -------------------------------
# 6️⃣ Endpoint /analizar
# -------------------------------
@app.route("/analizar", methods=["POST"])
def analizar():

    # Verificamos que se haya enviado un archivo
    if "file" not in request.files:
        return jsonify({"error": "Debe enviar un archivo PDF"}), 400

    archivo = request.files["file"]

    # Extraemos texto del PDF
    texto = extraer_texto_pdf(archivo)

    # Validamos que se haya podido extraer texto
    if not texto.strip():
        return jsonify({"error": "No se pudo extraer texto del PDF"}), 400

    # -------------------------------
    # 7️⃣ Generar embedding del alumno
    # -------------------------------
    embedding_texto = modelo.encode(texto)

    # -------------------------------
    # 8️⃣ Comparar con consigna
    # -------------------------------
    similitud_consigna = cosine_similarity(
        [embedding_texto],
        [embedding_consigna]
    )[0][0]

    # -------------------------------
    # 9️⃣ Comparar con respuestas previas
    # -------------------------------
    similitudes_previas = [
        cosine_similarity([embedding_texto], [emb])[0][0]
        for emb in embeddings_previos
    ]

    max_similitud_previa = max(similitudes_previas)

    # -------------------------------
    # 🔟 Lógica de decisión
    # -------------------------------
    if max_similitud_previa > UMBRAL_COPIA:
        decision = "Posible copia"
    elif similitud_consigna < UMBRAL_TEMA:
        decision = "Fuera de tema"
    else:
        decision = "Entrega válida"

    # -------------------------------
    # 1️⃣1️⃣ Respuesta final en JSON
    # -------------------------------
    return jsonify({
        "similitud_consigna": float(similitud_consigna),
        "max_similitud_previa": float(max_similitud_previa),
        "decision": decision
    })

# Endpoint de health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "model": "loaded"}), 200
# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)