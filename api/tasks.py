from celery import shared_task
from datetime import datetime

@shared_task
def print_task(task_name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_description = f"{timestamp} - {task_name}"
    print(task_description)