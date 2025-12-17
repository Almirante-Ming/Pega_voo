from celery import Celery
import os

celery_host = str(os.getenv('CELERY_HOST'))
celery_pass = str(os.getenv('CELERY_PASS'))
celery_port = str(os.getenv('CELERY_PORT'))


redis_url = f'redis://:{celery_pass}@{celery_host}:{celery_port}/1' 

app = Celery('tinto', broker= redis_url,backend=redis_url)


app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Manaus',
    enable_utc=False,
    task_track_started=True,
    task_time_limit=10 * 60,
)
