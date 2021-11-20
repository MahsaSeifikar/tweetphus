#!/bin/sh


set -o errexit
set -o nounset

celery -A api.celery_app.app worker -l info

exec "$@"