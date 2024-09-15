FROM python:3.9-slim

WORKDIR /workspace

# Actualiza pip y asegura que tengas las herramientas necesarias
RUN pip install --upgrade pip

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

CMD ["python", "app.py"]
