release: python manage.py migrate
web: gunicorn Wise.wsgi --log-file -
celery: celery -A Wise worker -l info
celerybeat: celery -A Wise beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
celeryworker2: REMAP_SIGTERM=SIGQUIT celery -A Wise worker --beat --loglevel=info