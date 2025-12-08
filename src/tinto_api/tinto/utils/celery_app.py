from celery import Celery
import os

celery_host = str(os.getenv('CELERY_HOST', 'localhost'))
celery_pass = str(os.getenv('CELERY_PASS'))
celery_port = 30059


redis_url = f'redis://:{celery_pass}@{celery_host}:{celery_port}/1' 

app = Celery( 'tinto', broker= redis_url,backend=redis_url )


app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=10 * 60,
)

if __name__ == '__main__':
    app.start()
