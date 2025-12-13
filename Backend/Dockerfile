FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero (mejor cache)
COPY requirements.txt .

# Actualizar pip e instalar dependencias
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del backend
COPY . .

ENV PORT=8000
EXPOSE 8000

# Ejecutar migraciones y levantar FastAPI
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
