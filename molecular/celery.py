from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from gobble.tasks import naver_realtime_new, naver_major_new

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'molecular.settings')

app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# REFERENCE: https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
# Celerybeat 태스크 추가/정의
from celery.schedules import crontab

app.conf.beat_schedule = {
    'naver_major_new': {
        'task': 'gobble.tasks.naver_major_new',
        'schedule': timedelta(hours=3),
        'args': (),
    },
    'naver_realtime_new': {
        'task': 'gobble.tasks.naver_realtime_new',
        'schedule': timedelta(minutes=1),
        'args': (),
    }
}
