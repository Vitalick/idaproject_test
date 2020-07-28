#!/usr/bin/env bash

sleep 3;
python manage.py migrate

sleep 3;
gunicorn idaproject_test.wsgi:application --bind 0.0.0.0:8000