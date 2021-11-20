#!/bin/sh


set -o errexit
set -o nounset

sleep 20
python3 api/manage.py makemigrations &&
python3 api/manage.py migrate && 

python3 api/manage.py makemigrations crawller &&
python3 api/manage.py migrate && 
python3 api/manage.py runserver 0.0.0.0:8000

exec "$@"