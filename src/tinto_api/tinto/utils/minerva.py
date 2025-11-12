from redis import Redis
import os


minerva = Redis(host=str(os.getenv('CELERY_HOST')), port=30059, password=str(os.getenv('CELERY_PASS')))