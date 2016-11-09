#!/bin/bash

# Command untuk menghidupkan Celery
# celery -A zeus.celery worker --loglevel=info
. venv/bin/activate
export FLASK_APP=app.py
flask run
