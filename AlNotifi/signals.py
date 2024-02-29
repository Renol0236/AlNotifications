from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from AlNotifi.models import Notifications
from .tasks import send_task_to_bot
from django.utils import timezone
from datetime import timedelta, datetime
from asgiref.sync import sync_to_async
from Notifications.celery import app

@receiver(post_save, sender=Notifications)
def create_or_update_task(sender, instance, created, **kwargs):
    if created:
        eta_time = datetime.now()
        result = send_task_to_bot.apply_async(args=[instance.id], eta=instance.time)
        task_id = result.id
        instance.task_id = task_id
        instance.save()

@receiver(pre_delete, sender=Notifications)
def revoke_celery_task(sender, instance, **kwargs):
    task_id = instance.task_id
    if task_id:
        app.control.revoke(task_id, terminate=True)