#!/bin/sh
set -e

echo "Esperando conexión a la base de datos..."
python - <<'PY'
import socket, time, os
host = os.environ.get("DATABASE_URL", "")
if "@" in host:
    host = host.split("@")[1].split(":")[0]
for i in range(10):
    try:
        socket.gethostbyname(host)
        print("✅ Base de datos resolvió correctamente")
        break
    except socket.gaierror:
        print("⏳ Esperando DNS...")
        time.sleep(3)
else:
    print("❌ No se pudo resolver el host de la base de datos")
    exit(1)
PY

# Migraciones
python manage.py migrate --noinput

# Archivos estáticos
python manage.py collectstatic --noinput || true

# Ejecutar app
gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:$PORT
