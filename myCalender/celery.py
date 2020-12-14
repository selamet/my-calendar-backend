import os
from celery import Celery
import dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myCalender.settings')
dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

celery_app = Celery('calendar')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()