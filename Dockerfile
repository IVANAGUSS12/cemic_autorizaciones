FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev sed ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Asegura permisos + fin de línea LF dentro de la imagen
RUN chmod +x /app/entrypoint.sh \
    && sed -i 's/\r$//' /app/entrypoint.sh

RUN mkdir -p /app/staticfiles /app/media
EXPOSE 8080

# Ejecuta vía sh -c (vuelve a normalizar por si acaso)
CMD ["sh","-c","/bin/chmod +x /app/entrypoint.sh && sed -i 's/\\r$//' /app/entrypoint.sh && ./entrypoint.sh"]

