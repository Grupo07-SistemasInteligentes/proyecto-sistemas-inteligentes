import requests
import sys

# Configuración
API_URL = "http://localhost:5000/analizar"
PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else None

if not PDF_PATH:
    print("Uso: python test_api.py <ruta_al_pdf>")
    sys.exit(1)

# Enviar PDF a la API
with open(PDF_PATH, "rb") as f:
    files = {"file": f}
    response = requests.post(API_URL, files=files)

# Mostrar resultado
print("Status Code:", response.status_code)
print("Respuesta:", response.json())