from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.forms.models import model_to_dict
from .models import Notifications
from asgiref.sync import async_to_sync, sync_to_async
from django.core.cache import cache
from discord.ext import commands
from celery.exceptions import SoftTimeLimitExceeded
from django.db import transaction
from django_celery_results.models import TaskResult
import asyncio
from asyncio import Queue
import logging
import discord
import threading

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=8, default_retry_delay=6)
def send_task_to_bot(self, instance_id):
    try:
        with transaction.atomic():
            notification_instance = get_notification_instance(instance_id)
            discord_profile = get_discord_profile(instance_id)
            async_to_sync(bot_def)(notification_instance, discord_profile)

            notification_instance.is_sent = True
            notification_instance.save()

            return "Task completed successfully"
    except SoftTimeLimitExceeded:
        self.retry()
    except Exception as exc:
        logger.error(f"An error occurred: {exc}")
        raise self.retry(exc=exc)

def get_notification_instance(instance_id):
    return Notifications.objects.get(id=instance_id)

def get_discord_profile(instance_id):
    notification = Notifications.objects.get(id=instance_id)
    return notification.user.userprofile.discord_profile
async def bot_def(notification_instance, discord_profile):
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix='!', intents=intents)

    async def on_ready():

        logger.info(f'Logged in as {client.user.name}')
        print(f'Task accepted (bot) - Notification ID: {notification_instance.id}')
        print(f'Task: {notification_instance.id}, user_discord: {discord_profile.global_name}, discord_id: {discord_profile.discord_id}')

        user = await client.fetch_user(discord_profile.discord_id)
        try:
            embed = discord.Embed(
                title=notification_instance.title,
                description=notification_instance.message,
                color=discord.Color.blue()
            )

            await user.send(embed=embed)
        except discord.Forbidden:
            logger.warning(f"Bot doesn't have permission to send a direct message to the user.")
        except discord.HTTPException:
            logger.error(f"Failed to send direct message to the user.")

        await client.close()

    client.event(on_ready)

    token = 'MTE5NzQ0MTczOTk1OTU2NjM1Ng.GmKp3M.S0MKHLyfRwaF7IvQ--3zS-xvAlHuxHoYXLbrOw'
    await client.start(token)