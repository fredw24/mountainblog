web: gunicorn mountainblog.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrateg.wsgi
