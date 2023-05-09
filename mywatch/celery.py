import os

from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywatch.settings')

app = Celery('mywatch', broker='redis://192.168.56.6:6379')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.humanize(with_defaults=False, censored=True)
# Load task modules from all registered Django apps.
# app.conf.update(configs)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#  ../bin/celery -A mywatch  worker -l info