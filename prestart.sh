#!/usr/bin/env bash

sleep 2;
python manage.py migrate

gunicorn idaproject_test.wsgi:application --bind 0.0.0.0:8000