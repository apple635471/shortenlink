#!/bin/bash
cd shortenlink
set -x 
python manage.py makemigrations app
python manage.py migrate
# python manage.py createsuperuser
python manage.py collectstatic --noinput
gunicorn shortenlink.wsgi:application --bind 0.0.0.0:8000