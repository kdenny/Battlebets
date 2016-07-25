from __future__ import absolute_import

import os

from celery import Celery
from celery.decorators import task


from django.conf import settings  # noqa

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Battlebets.settings')
app = Celery('Battlebets')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@task(name="sum_two_numbers")
def add(x, y):
    return x + y


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))