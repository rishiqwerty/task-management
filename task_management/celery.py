import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')

from django.conf import settings


app = Celery('task_management')
app.conf.enable_utc = True
app.conf.timezone = settings.TIME_ZONE
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic Task Scheduler Config (beat schedule)
app.conf.beat_schedule = {
    'mark-overdue-tasks-every-minute': {
        'task': 'tasks.tasks.mark_overdue_tasks',
        'schedule': crontab(),  # runs every minute
    },
    'reprioritize-tasks-every-day': {
        'task': 'tasks.tasks.reprioritize_tasks',
        'schedule': crontab(hour=0, minute=0),  # runs every day at midnight
    },
}
