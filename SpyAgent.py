# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime

import winsound
import discord
import threading

print("SpyAgent 1.3.0, progame1201")

TOKEN = input("Token: ")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
guild_assigned = False
save_attachments = input("save attachments true? [y/n] ").lower()
notification = input("notification true? [y/n] ").lower()
Сopyingmessages = input("Сopying messages true? [y/n] ").lower()
guildid = 0
channel_id = 0
mutelist = []

@client.event
async def on_ready():
    global client
    global guild
    global Сopyingmessages
    global channel
    global guild_assigned
    global guildid
    global channel_id

    if not guild_assigned:
        print("server names:")
        for i, guild in enumerate(client.guilds):
            print(f"{i}: {guild.name}")

        guildid = int(input("server index: "))
        print(f'bot {client.user} connected to server: {client.guilds[int(guildid)].name}')
        channellist = []
        print("channel names:")
        guild = client.guilds[int(guildid)]
        for i, channel in enumerate(guild.text_channels):
            channellist.append(channel.id)
            print(f"{i}: {channel.name}")
        chnlindx = input("chanel index: ")
        try:
         channel_id = channellist[int(chnlindx)]
        except:
         channel_id = 0
        guild_assigned = True

    channel = client.get_channel(channel_id)
    if channel:
        messages = []

        async for message in channel.history(limit=30, oldest_first=False):
            messages.append(message)

        # Развернуть список с сообщениями
        messages.reverse()

        for message in messages:
            date = message.created_at
            rounded_date = date.replace(second=0, microsecond=0)
            rounded_date_string = rounded_date.strftime('%Y-%m-%d %H:%M')
            print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}")
        if Сopyingmessages == "y":
            await save_channel_messages(channel)

        print(f'The bot receives messages. Channel selected: {channel.name}')
        threading.Thread(target=send_messages, daemon=True).start()
        await receive_messages(channel)
    else:
        print('The specified channel was not found.')


async def save_channel_messages(channel):
    print("SpyAgentINFO: Сopying messages")
    with open('messages.txt', 'w', encoding='utf-8') as file:
        async for message in channel.history(limit=None):
            date = message.created_at

            rounded_date = date.replace(second=0, microsecond=0)

            rounded_date_string = rounded_date.strftime('%Y-%m-%d %H:%M')

            file.write(f'{message.author.name}: {rounded_date_string} {message.content}\n')


async def receive_messages(channel):
    while True:
        attachment_list = []
        message = await client.wait_for('message')
        if message.channel.name in mutelist:
            continue
        if message.attachments:
          if save_attachments == "y":
            for attachment in message.attachments:
                attachment_list.append(attachment.filename)
                await attachment.save(attachment.filename)
          else:
              for attachment in message.attachments:
                  attachment_list.append(attachment.url)
          date = message.created_at
          rounded_date = date.replace(second=0, microsecond=0)
          rounded_date_string = rounded_date.strftime('%Y-%m-%d %H:%M')
          print(f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}, attachments: {attachment_list}')
        else:
          date = message.created_at
          rounded_date = date.replace(second=0, microsecond=0)
          rounded_date_string = rounded_date.strftime('%Y-%m-%d %H:%M')
          print(f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}')

        if notification == "y":
            if str(message.author.name) != str(client.user.name):
              winsound.Beep(500, 100)
              winsound.Beep(1000, 100)


def send_messages():
    global channel
    global guild
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        user_input = loop.run_until_complete(async_input(f'Enter a message to send to {guild.name}: {channel.name}: '))
        if user_input == "***Reset":
            print("server names:")
            for i, guild in enumerate(client.guilds):
                print(f"{i}: {guild.name}")
            guildid = int(input("server index: "))
            guild = client.guilds[int(guildid)]
            channellist = []
            print("channel names:")
            for i, channel in enumerate(guild.text_channels):
                channellist.append(channel.id)
                print(f"{i}: {channel.name}")
            chnlindx = input("chanel index: ")
            try:
                channel_id = channellist[int(chnlindx)]
            except:
                channel_id = 0
            channel = client.get_channel(int(channel_id))
            print(f'Channel selected: {channel.name}')
            continue

        if user_input == "***Mute":
            channellistformute = []
            for i, channel in enumerate(guild.text_channels):
                channellistformute.append(channel.name)
                print(f"{i}: {channel.name}")
            mutechanelname = input("type chanel index: ")
            try:
              mutelist.append(channellistformute[int(mutechanelname)])
            except:
               print("index not found")
            continue

        if user_input == "***Unmute":
            channellistforunmute = []
            for i in range(len(mutelist)):
                channellistforunmute.append(mutelist[i])
                print(f"{i}: {mutelist[i]}")
            unmutechanelname = input("type chanel index: ")
            try:
              mutelist.remove(channellistforunmute[int(unmutechanelname)])
            except:
              print("index not found")
            continue
        asyncio.run_coroutine_threadsafe(channel.send(user_input), client.loop)


async def async_input(prompt):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, prompt)


client.run(TOKEN)
