# 1. ESPECIFICAR LA IMAGEN BASE
# Usamos una imagen oficial de Python, idealmente una versión slim o alpine para menor tamaño.
# Usaré python:3.11-slim como ejemplo, puedes cambiar 3.11 a tu versión específica.
FROM python:3.11-slim

# 2. ESTABLECER VARIABLES DE ENTORNO
# Configuraciones importantes para Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. ESTABLECER EL DIRECTORIO DE TRABAJO
# Aquí es donde Docker trabajará dentro del contenedor.
WORKDIR /app

# 4. INSTALAR DEPENDENCIAS
# Copia solo el archivo de requerimientos primero.
# Esto mejora el caching de Docker: si requirements.txt no cambia, este paso no se repite.
COPY requirements.txt .

# Instala las dependencias de Python.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. COPIAR EL CÓDIGO DEL PROYECTO
# Copia todo el contenido de tu carpeta /Backend (donde está este Dockerfile)
# al directorio de trabajo /app dentro del contenedor.
COPY . /app

# 6. DEFINIR EL PUERTO (OPCIONAL)
# Exponer el puerto. Railway lo ignora y usa la variable $PORT, pero es buena práctica.
EXPOSE 8000

# 7. DEFINIR EL COMANDO DE ARRANQUE (ENTRYPOINT/CMD)
# Este es el comando que se ejecuta cuando el contenedor inicia.
# Reemplazamos el Start Command que definiste en Railway con este,
# y es preferible hacerlo aquí para una configuración más portable.

# CMD ejecuta la migración de Alembic y luego inicia Uvicorn.
# Asegúrate de que tu main:app sea correcto.
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]