#!/usr/bin/env bash
set -e

python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn autorizaciones.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers ${WEB_CONCURRENCY:-3} \
  --access-logfile - --error-logfile - --log-level info --timeout 120

