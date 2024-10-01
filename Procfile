release: python manage.py migrate
release: python manage.py loaddata data3.json
release: python manage.py loaddata data4.json

web: gunicorn config.wsgi:application --log-file -
