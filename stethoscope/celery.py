import logging
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stethoscope.settings')

app = Celery('stethoscope')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-email': {
        'task': 'mailings.tasks.send_weekly_email',
        'schedule': crontab(day_of_week=5, hour=9, minute=0),
    },
    'cleanup_non_activated_users': {
        'task': 'users.tasks.delete_non_activated_users_task',
        'schedule': settings.USER_NON_ACTIVATED_ACCOUNT_CLEANUP_PERIOD,
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    logger.info(f'Request: {self.request!r}')
