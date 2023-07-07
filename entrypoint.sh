#!/bin/sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn stethoscope.wsgi:application --bind 0:8000
