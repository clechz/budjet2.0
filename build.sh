#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python budjet/manage.py collectstatic --no-input
python budjet/manage.py migrate