FROM python:3.11-slim

ENV APP_HOME=/app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install gettext libpq-dev gcc -y

RUN pip install --upgrade pip

WORKDIR $APP_HOME/stethoscope/requirements
COPY ./stethoscope/requirements/ .
RUN pip install --no-cache-dir -r prod.txt

WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE stethoscope.settings

# Create a user to avoid running containers as root in production
RUN addgroup --system backend_user \
    && adduser --system --ingroup backend_user backend_user

COPY . .
RUN  mkdir staticfiles media \
    && chown -R backend_user:backend_user $APP_HOME

# change user
USER backend_user

# This script will run before every command executed in the container
RUN  sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh
ENTRYPOINT  ["./entrypoint.sh"]
