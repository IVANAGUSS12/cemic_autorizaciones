#!/bin/sh
set -e

export PORT=${PORT:-8080}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-autorizaciones.settings}

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true
python manage.py seed_defaults || true  # crea sectores y superusuario si falta

exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --timeout 120
