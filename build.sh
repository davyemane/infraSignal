#!/bin/bash
# Installation des dépendances
pip install -r requirements.txt

# Faire les migrations
python manage.py makemigrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --no-input