#!/bin/bash

set -e

cd /app

python manage.py migrate --no-input
#python manage.py import_csv
python manage.py runserver 0.0.0.0:8000
