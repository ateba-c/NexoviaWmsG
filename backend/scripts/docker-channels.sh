#!/bin/sh
set -e

python manage.py migrate --noinput
daphne -b 0.0.0.0 -p 8001 config.asgi:application
