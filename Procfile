release: python manage.py migrate
release: python manage.py createuser
web: gunicorn config.wsgi:application --log-file -
