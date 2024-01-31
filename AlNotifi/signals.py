from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from AlNotifi.models import Notifications
from .tasks import send_task_to_bot

@receiver(post_save, sender=Notifications)
def create_or_update_task(sender, instance, created, **kwargs):
    print('signal called')
    if created:
        send_task_to_bot.delay(instance.id)
        print('signal passed')