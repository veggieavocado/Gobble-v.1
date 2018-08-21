from celery import shared_task

from gobble.module.data_send import NaverDataSend

n = NaverDataSend()

@shared_task
def naver_major_new():
    n.data_send('new', 'major')
    return True

@shared_task
def naver_realtime_new():
    n.data_send('new', 'rt')
    return True

@shared_task
def naver_major_all():
    n.data_send('all', 'major')
    return True

@shared_task
def naver_realtime_all():
    n.data_send('all', 'rt')
    return True
