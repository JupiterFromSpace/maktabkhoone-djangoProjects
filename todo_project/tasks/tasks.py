from celery import shared_task
from .models import Task


@shared_task
def delete_done_tasks():
    deleted_count, _ = Task.objects.filter(is_done=True).delete()
    return f'{deleted_count} تسک انجام شده حذف شد.'