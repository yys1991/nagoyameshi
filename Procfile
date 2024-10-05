"""release: python manage.py migrate
release: python manage.py createuser
web: gunicorn config.wsgi:application --log-file -
"""

release: python manage.py migrate && python manage.py createuser
web: gunicorn config.wsgi:application --log-file -

