from redis import Redis
import os

celery_host = str(os.getenv('CELERY_HOST'))
celery_pass = str(os.getenv('CELERY_PASS'))

# if not celery_host or celery_pass:
    # raise ValueError('Redis host or redis pass are not set')

minerva = Redis(host=celery_host, port=30059, password=celery_pass)