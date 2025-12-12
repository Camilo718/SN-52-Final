# =============================
#      Imagen base
# =============================
FROM python:3.11-slim

# =============================
#      Variables de entorno
# =============================

# Directorio base del proyecto
ENV APP_HOME="/app"
ENV BACKEND_DIR="/app/BACKEND"

# Archivo de dependencias
ENV REQUIREMENTS_FILE="requirements.txt"

# Config de Uvicorn
ENV UVICORN_HOST="0.0.0.0"
ENV UVICORN_PORT="8000"

# Modo de ejecución (production | development)
ENV ENVIRONMENT="production"

# Comando de inicio
ENV START_CMD="alembic upgrade head && uvicorn main:app --host ${UVICORN_HOST} --port ${UVICORN_PORT}"

# =============================
#      Dependencias del sistema
# =============================

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc \
        pkg-config \
        libcairo2-dev \
        libfreetype6-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# =============================
#      Copiar proyecto
# =============================
WORKDIR ${APP_HOME}
COPY . ${APP_HOME}

# =============================
#      Instalar backend
# =============================
WORKDIR ${BACKEND_DIR}
RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

# =============================
#      Comando por defecto
# =============================
CMD ["sh", "-c", "${START_CMD}"]

# =============================
#      Exponer Puerto
# =============================
EXPOSE ${UVICORN_PORT}
