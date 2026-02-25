# Usar imagen oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Expone el puerto 5000 (el de Flask)
EXPOSE 5000

# Comando para ejecutar la API
CMD ["python", "app.py"]