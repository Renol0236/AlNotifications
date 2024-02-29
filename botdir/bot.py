import discord
import threading
import asyncio
from discord.ext import commands

# intents = discord.Intents.all()
#
# bot = commands.Bot(command_prefix='!', intents=intents)
#
# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user.name}')
#     for guild in bot.guilds:
#         for channel in guild.text_channels:
#             await channel.send('HELLO')
#
#
#
# async def send_notification(notification):
#     print('task accepted (bot)')
#     print(bot)
#     for guild in bot.guilds:
#         print(guild)
#         for channel in guild.text_channels:
#             print(channel)
#             try:
#                 await channel.send(f'ACCEPTED {notification.id}')
#             except discord.Forbidden:
#                 print(f"Бот не имеет прав на отправку сообщений в {channel.name} канал гильдии {guild.name}")
#             except discord.HTTPException:
#                 print(f"Не удалось отправить сообщение в {channel.name} канал гильдии {guild.name}")
#
# async def start_send_notification(notification):
#     print('ok')
#     await send_notification(notification)
#
# async def run_bot():
#     await bot.start('MTE5NzQ0MTczOTk1OTU2NjM1Ng.GmKp3M.S0MKHLyfRwaF7IvQ--3zS-xvAlHuxHoYXLbrOw')
#

intents = discord.Intents.all()
client = discord.Client(intents=intents)


async def send_notification(notification, client):
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

def run_bot():
    client.run('MTE5NzQ0MTczOTk1OTU2NjM1Ng.GmKp3M.S0MKHLyfRwaF7IvQ--3zS-xvAlHuxHoYXLbrOw')
