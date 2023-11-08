@echo off
start "" python manage.py runserver
timeout /t 5
start "" http://localhost:8000/csv_processor/process/