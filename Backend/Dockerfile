FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev libmariadb-dev-compat \
    libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# COPIAR SOLO requirements primero
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# COPIAR EL RESTO DEL PROYECTO
COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT"]
