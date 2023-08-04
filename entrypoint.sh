#!/bin/sh

python manage.py compilemessages -l ru

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn stethoscope.wsgi:application --bind 0:8000 \
    & celery -A stethoscope worker --loglevel=info \
    & celery -A stethoscope beat --loglevel=info \
    & celery -A stethoscope flower --loglevel=info
