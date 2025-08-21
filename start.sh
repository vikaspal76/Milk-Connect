#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (optional, recommended)
python manage.py migrate --noinput

# Start the Django server with 0.0.0.0 for Render
gunicorn MilkConnet.wsgi:application --bind 0.0.0.0:$PORT

