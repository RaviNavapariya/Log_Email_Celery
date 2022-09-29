import os
from celery import Celery
from celery.schedules import crontab  



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Logproject.settings")
app = Celery("Logproject")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {  
    'send_feedback_email_task' :  {  
        'task': 'logapp.tasks.send_feedback_email_task',  
        'schedule': crontab(minute='*/1'),  
    }     
}  

app.autodiscover_tasks()


@app.task(bind=True)
def hello_world(self):
    print('Hello world!')