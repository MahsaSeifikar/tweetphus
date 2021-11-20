from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
import logging
from django.conf import settings
import tweepy
  
logger = logging.getLogger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
CELERY_BROKER_URL="sqla+postgresql://admin:pass@postgres:5432/test_db"
CELERY_RESULT_BACKEND="db+postgresql://admin:pass@postgres:5432/test_db"

app = Celery(
    "crawler_app",
)

# add for django
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf["task_acks_late"] = True
app.conf["worker_prefetch_multiplier"] = 1
app.conf.task_ignore_result = True
app.conf.task_store_errors_even_if_ignored = True
