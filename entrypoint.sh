#!/bin/sh

while ! nc -z db 5432; do
  sleep 0.5
done

python3 manage.py makemigrations main

python3 manage.py migrate

exec "$@"
