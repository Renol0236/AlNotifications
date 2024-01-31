from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.forms.models import model_to_dict
from .models import Notifications
from asgiref.sync import async_to_sync

from discord.ext import commands
import asyncio

import discord

# @shared_task
# def send_task_to_bot(instance_id):
#     print('start task')
#     notification = Notifications.objects.get(id=instance_id)
#     print('in task:')
#     print(notification.id)
#     class FakeContext:
#         async def send(self, notifaction):
#             print(notifaction.id)
#
#     ctx = FakeContext()
#     async_to_sync(send_notification)(notification)
#     print('Sent notifi', notification.id, 'to discord botdir')

# def bot_def(id):
#     intents = discord.Intents.all()
#
#     client = discord.Client(intents=intents)
#
#     @client.event
#     async def on_ready():
#         print(f'Logged in as {client.user.name}')
#         for guild in client.guilds:
#             for channel in guild.text_channels:
#                 await channel.send('HELLO')
#
#     async def send_notification(notification):
#         print('task accepted (bot)')
#         for guild in client.guilds:
#             print(guild)
#             for channel in guild.text_channels:
#                 print(channel)
#                 try:
#                     await channel.send(f'ACCEPTED {notification.id}')
#                 except discord.Forbidden:
#                     print(f"Бот не имеет прав на отправку сообщений в {channel.name} канал гильдии {guild.name}")
#                 except discord.HTTPException:
#                     print(f"Не удалось отправить сообщение в {channel.name} канал гильдии {guild.name}")
#
#     client.loop.create_task(send_notification())
# @shared_task
# def send_task_to_bot(instance_id):
#     notification = Notifications.objects.get(id=instance_id)
#     bot_def(notification)

@shared_task
def send_task_to_bot(instance_id):
    notification_instance = Notifications.objects.get(id=instance_id)
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_def(notification_instance))

@shared_task
def send_task_to_bot(instance_id):
    notification_instance = Notifications.objects.get(id=instance_id)
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_def(notification_instance))

async def bot_def(notification):
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    async def send_notification(notification):  # Объявление функции до использования
        print('task accepted (bot)')
        for guild in client.guilds:
            print(guild)
            for channel in guild.text_channels:
                print(channel)
                try:
                    await channel.send(f'ACCEPTED {notification.id} {notification.title} {notification.message}')
                except discord.Forbidden:
                    print(f"Бот не имеет прав на отправку сообщений в {channel.name} канал гильдии {guild.name}")
                except discord.HTTPException:
                    print(f"Не удалось отправить сообщение в {channel.name} канал гильдии {guild.name}")

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}')
        for guild in client.guilds:
            for channel in guild.text_channels:
                await channel.send('HELLO')

        await send_notification(notification)
        await client.close()

    await client.start('MTE5NzQ0MTczOTk1OTU2NjM1Ng.GmKp3M.S0MKHLyfRwaF7IvQ--3zS-xvAlHuxHoYXLbrOw')