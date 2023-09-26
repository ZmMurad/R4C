from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# Установите переменную окружения DJANGO_SETTINGS_MODULE, чтобы Celery знал о настройках Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R4C.settings')

app = Celery('R4C')


# Загрузите настройки из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
# Автоматически обнаруживайте и регистрируйте задачи в приложениях Django
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'every': {
        'task': 'orders.tasks.check_robot_availability',
        'schedule': crontab(minute='*/2'),# по умолчанию выполняет каждую минуту, очень гибко
    },                                                              # настраивается

}