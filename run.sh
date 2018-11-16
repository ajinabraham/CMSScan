#!/bin/sh
. venv/bin/activate && \
gunicorn --bind 0.0.0.0:7070 app:app --workers 3 --timeout 10000