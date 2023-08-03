# -*- coding: utf-8 -*-
import os

try:
  import asyncio
except:
    os.system("python -m pip install asyncio")
    import asyncio
import time
try:
  import pytz
except:
    os.system("python -m pip install pytz")
    import asyncio
import winsound
try:
 import discord
except:
    os.system("python -m pip install discord.py")
    import asyncio
import threading
from tkinter import filedialog
print("SpyAgent 1.7.1, progame1201")

TOKEN = input("Token: ")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
guild_assigned = False
save_attachments = input("save attachments true? [y/n] ").lower()
notification = input("notification true? [y/n] ").lower()
Сopyingmessages = input("Сopying messages true? [y/n] ").lower()
DmMode = input("DM mode true? [y/n] ")
guildid = 0
channel_id = 0
mutelist = []
givehistory = 0
@client.event
async def on_ready():
  global givehistory
  global client
  global guild
  global Сopyingmessages
  global channel
  global guild_assigned
  global guildid
  global channel_id
  if DmMode != "y":
    if not guild_assigned:
        print("server names:")
        for i, guild in enumerate(client.guilds):
            print(f"{i}: {guild.name}")

        guildid = input("server index: ")
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

        messages.reverse()

        for message in messages:
            date = message.created_at
            timezone = pytz.timezone('Europe/Moscow')
            rounded_date = date.replace(second=0, microsecond=0)
            rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
            print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}")
        if Сopyingmessages == "y":
            await save_channel_messages(channel)

        print(f'The bot receives messages. Channel selected: {channel.name}')
        threading.Thread(target=send_messages, daemon=True).start()
        await receive_messages(channel)
    else:
        print('The specified channel was not found.')
        raise Exception("The specified channel was not found.").with_traceback(channel)
  else:
    global user_id
    global user
    user_id = input("User ID: ")
    user = client.get_user(int(user_id))
    if user == None:
        print("User not found")
        time.sleep(10)
        raise Exception("User not found").with_traceback(user)
    messages = []
    async for message in user.history(limit=30, oldest_first=False):
        messages.append(message)

    messages.reverse()

    for message in messages:
        date = message.created_at
        timezone = pytz.timezone('Europe/Moscow')
        rounded_date = date.replace(second=0, microsecond=0)
        rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
        print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}")
    threading.Thread(target=DmMessaging, daemon=True).start()
    await on_DMmessage()


def DmMessaging():
  global user
  global user_id
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  if user is None:
      print('Invalid User ID')
  while True:
    message = loop.run_until_complete(async_input(f"message to {user.name}: "))
    if message == "***Reset":
        user_id = loop.run_until_complete(async_input("User ID: "))
        user = client.get_user(int(user_id))

        if user is None:
            print('Invalid User ID')
        asyncio.run_coroutine_threadsafe(historyManagerDM(), client.loop)
        time.sleep(2)
        continue
    if message == "***Userlist":
        userlist = []
        i=0
        for user in client.users:
            userlist.append(user.id)
            print(f"{i}: ({user.id}) {user.name}")
            i +=1
        userid = input("type user index: ")
        user_id = userlist[int(userid)]
        user = client.get_user(int(user_id))
        if user is None:
            print('Invalid User ID')
        asyncio.run_coroutine_threadsafe(historyManagerDM(), client.loop)
        time.sleep(2)
        continue
    try:
        asyncio.run_coroutine_threadsafe(user.send(message), client.loop)
        print(f'a private message has been sent to the user {user}')
    except discord.Forbidden:
        print(f'I dont have permission to send private messages to the user {user}')
async def on_DMmessage():
    while True:
          attachment_list = []
          message = await client.wait_for('message')
          if isinstance(message.channel,discord.DMChannel):
              if message.attachments:
                  if save_attachments == "y":
                      for attachment in message.attachments:
                          attachment_list.append(attachment.filename)
                          await attachment.save(attachment.filename)
                  else:
                      for attachment in message.attachments:
                          attachment_list.append(attachment.url)
                  print(f'\nprivate message: {message.channel}: ({message.author.id}) {message.author.name}: {message.content}, attachments: {attachment_list}')
                  if notification == "y":
                      if str(message.author.name) != str(client.user.name):
                          winsound.Beep(500, 100)
                          winsound.Beep(1000, 100)
              else:
               print(f'\nprivate message: {message.channel}: ({message.author.id}) {message.author.name}: {message.content}')
               if notification == "y":
                  if str(message.author.name) != str(client.user.name):
                      winsound.Beep(500, 100)
                      winsound.Beep(1000, 100)
async def save_channel_messages(channel):
    print("SpyAgentINFO: Сopying messages")
    with open('messages.txt', 'w', encoding='utf-8') as file:
        async for message in channel.history(limit=None):
            date = message.created_at
            timezone = pytz.timezone('Europe/Moscow')
            rounded_date = date.replace(second=0, microsecond=0)
            rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
            file.write(f'{message.author.name}: {rounded_date_string} {message.content}\n')


async def receive_messages(channel):
    while True:
        attachment_list = []
        message = await client.wait_for('message')
        if isinstance(message.channel, discord.DMChannel):
            print(
                f'\nprivate message: {message.channel}: ({message.author.id}) {message.author.name}: {message.content}')
            if notification == "y":
                if str(message.author.name) != str(client.user.name):
                    winsound.Beep(500, 100)
                    winsound.Beep(1000, 100)
            continue
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
          timezone = pytz.timezone('Europe/Moscow')
          rounded_date = date.replace(second=0, microsecond=0)
          rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
          print(f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}, attachments: {attachment_list}')
        else:
          date = message.created_at
          timezone = pytz.timezone('Europe/Moscow')
          rounded_date = date.replace(second=0, microsecond=0)
          rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
          print(f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}')

        if notification == "y":
            if str(message.author.name) != str(client.user.name):
              winsound.Beep(500, 100)
              winsound.Beep(1000, 100)


def send_messages():
    global givehistory
    global channel
    global guild
    global channel_id
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        time.sleep(0.5)
        channel = client.get_channel(int(channel_id))
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
            print()
            asyncio.run_coroutine_threadsafe(historyManager(), client.loop)
            time.sleep(2)
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
        if user_input == "***File":
            filepath = input("File path:")
            with open(filepath, 'rb') as image_file:
                # Отправка изображения на сервер Discord от имени бота
                asyncio.run_coroutine_threadsafe(channel.send(file=discord.File(filepath)), client.loop)
            continue
        if user_input == "***Reaction":
            print("1 - emoji list")
            print("2 - type emoji")
            emojiinput = input("type number:")
            if emojiinput == "1":
                i = 0
                emojilist = []
                for emoji in client.guilds[0].emojis:
                    emojilist.append(emoji)
                    print(f'{i}: {emoji.name} - {emoji}')
                    i += 1
                reactemoji = input("type emoji index: ")
                try:
                  emoji = emojilist[int(reactemoji)]
                except:
                    continue
            if emojiinput == "2":
                emoji = input("emoji: ")
            print("1 - message id")
            print("2 - message list")
            messageinput = input("type number:")
            if messageinput == "2":
                asyncio.run_coroutine_threadsafe(ReactEmojiList(emoji), client.loop)
            if messageinput == "1":
                asyncio.run_coroutine_threadsafe(ReactEmojiMessage(emoji), client.loop)
            global next
            next = 0
            while True:
              if next == 1:
                break
              else:
                  continue
            continue
        asyncio.run_coroutine_threadsafe(channel.send(user_input), client.loop)

async def ReactEmojiMessage(emoji):
    global next
    messageid = input("message id: ")
    message = await channel.fetch_message(int(messageid))
    await message.add_reaction(emoji)
    print(f"message reacted. Emoji: {emoji}")
    next = 1
async def ReactEmojiList(emoji):
    global next
    messages = []
    async for message in channel.history(limit=30, oldest_first=False):
        messages.append(message)

    messages.reverse()
    i = 0
    for message in messages:
        attachment_list = []
        date = message.created_at
        timezone = pytz.timezone('Europe/Moscow')
        rounded_date = date.replace(second=0, microsecond=0)
        rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
        print(f"{i}: {message.author}: {message.content}")
        i += 1
    messageindex = input("message index:")
    message = messages[int(messageindex)]
    await message.add_reaction(emoji)
    print(f"message reacted. Emoji: {emoji}")
    next = 1

async def async_input(prompt):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, prompt)

async def historyManager():
     messages = []
     async for message in channel.history(limit=30, oldest_first=False):
        messages.append(message)

     messages.reverse()

     for message in messages:
         attachment_list = []
         if message.attachments:
             if save_attachments == "y":
                 for attachment in message.attachments:
                     attachment_list.append(attachment.filename)
                     await attachment.save(attachment.filename)
             else:
                 for attachment in message.attachments:
                     attachment_list.append(attachment.url)
             date = message.created_at
             timezone = pytz.timezone('Europe/Moscow')
             rounded_date = date.replace(second=0, microsecond=0)
             rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
             print(f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}, attachments: {attachment_list}')
         else:
             date = message.created_at
             timezone = pytz.timezone('Europe/Moscow')
             rounded_date = date.replace(second=0, microsecond=0)
             rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
             print(f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}')


async def historyManagerDM():
    messages = []
    async for message in user.history(limit=30, oldest_first=False):
        messages.append(message)

    messages.reverse()

    for message in messages:
        date = message.created_at
        timezone = pytz.timezone('Europe/Moscow')
        rounded_date = date.replace(second=0, microsecond=0)
        rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
        print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}")

client.run(TOKEN)
