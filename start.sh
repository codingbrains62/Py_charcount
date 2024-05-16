#!/bin/sh
python manage.py collectstatic --no-input;gunicorn nocout.wsgi:application --workers 5 --threads 5  --timeout 300 --limit-request-line 8091 --bind 0.0.0.0:8000