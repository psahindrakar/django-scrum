#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
python manage.py makemigrations  

# migrate db, so we have the latest db schema
python manage.py migrate  

# Gunicorn command should be run from where manage.py of django is located. Creates 2 worker processes and listens at 8000 port
/usr/local/bin/gunicorn scrum.wsgi -w 2 -b :8000
# python manage.py runserver 0.0.0.0:8000