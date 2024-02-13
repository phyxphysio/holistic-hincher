python manage.py migrate

# Start Gunicorn with the application bound to 0.0.0.0:8000
exec gunicorn holistic_hincher.wsgi:application --bind 0.0.0.0:8000
