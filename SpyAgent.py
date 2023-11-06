from disnake.ext import *
from disnake import *
from loguru import logger
import asyncio
import winsound
import pickle
import os
import pytz
from asyncio import sleep
import config
from tkinter import filedialog

logger.info("Spy Agent 2.0, 2023, progame1201")
logger.info("Running...")

logger.info("Loading mutes...")
channels_mute_list = []
guild_mute_list = []
if os.path.exists("channelmutes"):
    if os.path.getsize("channelmutes") > 0:
        data = open("channelmutes", 'rb').read()
        channels_mute_list = pickle.loads(data)
    else:
        logger.warning("Channel mutes file is empty")
else:
    open("channelmutes", 'wb').close()

if os.path.exists("guildmutes"):
    if os.path.getsize("guildmutes") > 0:
        data = open("guildmutes", 'rb').read()
        guild_mute_list = pickle.loads(data)
    else:
        logger.warning("Guild mutes file is empty")
else:
    open("guildmutes", 'wb').close()

client = Client(intents=Intents.all())
@client.event
async def on_ready():
  logger.info(f"Welcome {client.user.name}! Bot ID: {client.user.id}")
  await sleep(1)
  print("Choose a server:")
  for i, guild in enumerate(client.guilds):
      print(f"{i}: {guild.name}")
  data = await async_input("server index:")
  guild = client.guilds[int(data)]
  logger.success(f"guild assigned! guild name: {guild.name}, guild owner: {guild.owner}, guild id: {guild.id}")
  await sleep(1)
  print("Choose channel:")
  channels: dict[int, dict[str:int]] = {}
  for i, channel in enumerate(guild.text_channels):
      channels.update({i: {channel.name: channel.id}})
      print(f"{i}: {channel.name}")
  data = await async_input("server index:")
  channel = client.get_channel(list(channels.get(int(data)).values())[0])
  logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
  await get_history(channel)
  asyncio.run_coroutine_threadsafe(receive_messages(client), client.loop)
  asyncio.run_coroutine_threadsafe(chatting(channel, guild), client.loop)

async def receive_messages(client):
    while True:
      attachment_list = []
      message = await client.wait_for('message')
      if isinstance(message.channel, DMChannel):
        print(f'\nPrivate message: {message.channel}: ({message.author.id}) {message.author.name}: {message.content}')
        continue
      if message.channel.id in channels_mute_list:
          continue
      if message.guild.id in guild_mute_list:
          continue
      if message.attachments:
        for attachment in message.attachments:
          attachment_list.append(attachment.url)
        date = message.created_at
        rounded_date = date.replace(second=0, microsecond=0)
        rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
        print(
          f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}, attachments: {attachment_list}')
      else:
        date = message.created_at
        rounded_date = date.replace(second=0, microsecond=0)
        rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
        print(
          f'\n{message.guild.name}: {message.channel.name}: {rounded_date_string} {message.author.name}: {message.content}')
      if config.notification == True:
          winsound.Beep(500, 100)
          winsound.Beep(1000, 100)


async def chatting(channel:TextChannel, guild:Guild):
 while True:
   await sleep(1)
   senddata = await async_input(f"Message to {guild.name}: {channel.name}:\n")
   if senddata.lower() == "***help":
       print("#####HELP#####\n***Mute - mute any channel\n***Unmute - unmute any channel\n***Delete - delete any message you have selected\n***Reset - Re-select the guild and channel for communication\n***Resetchannel - Re-select a channel for communication\n***File - send a file\n***Muteguild - mute any guild\n***Unmuteguild - unmute any guild\n##############")
       continue
   if senddata.lower() == "***mute":
       channellistformute = []
       for i, mchannel in enumerate(guild.text_channels):
           if mchannel.id in channels_mute_list:
               channellistformute.append(mchannel.id)
               continue
           channellistformute.append(mchannel.id)
           print(f"{i}: {mchannel.name}")
       mutechanelname = await async_input("type chanel index: ")
       try:
           mchannel = client.get_channel(channellistformute[int(mutechanelname)])
           channels_mute_list.append(channellistformute[int(mutechanelname)])
           with open('channelmutes', 'wb') as f:
               towrite = pickle.dumps(channels_mute_list)
               f.write(towrite)
           logger.success(f"Channel '{mchannel.name}' muted")
       except Exception as e:
           print(f"index not found\n{e}")
       continue

   if senddata.lower() == "***unmute":
       channellistforunmute = []
       for i in range(len(channels_mute_list)):
           unmutech = client.get_channel(channels_mute_list[i])
           channellistforunmute.append(channels_mute_list[i])
           print(f"{i}: {unmutech}")
       unmutechanelname = await async_input("type chanel index: ")
       try:
           mchannel = client.get_channel(channellistforunmute[int(unmutechanelname)])
           channels_mute_list.remove(channellistforunmute[int(unmutechanelname)])
           with open('channelmutes', 'wb') as f:
               towrite = pickle.dumps(channels_mute_list)
               f.write(towrite)
           logger.success(f"Channel '{mchannel.name}' unmuted")
       except Exception as e:
           print(f"index not found\n{e}")
       continue
   if senddata.lower() == "***delete":
       messages = []
       yourmessages:dict[int:Message] = {}
       async for message in channel.history(limit=config.history_size, oldest_first=False):
           messages.append(message)
       messages.reverse()
       i = 0
       for message in messages:
           if message.author.id == client.user.id:
             yourmessages[i] = message
             date = message.created_at
             rounded_date = date.replace(second=0, microsecond=0)
             rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
             print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")
             i += 1
       data = await async_input("message index:")
       if data == "" or data == None:
           continue
       todelmsg = yourmessages.get(int(data))
       await todelmsg.delete()
       logger.success(f"Message: '{todelmsg.content}' deleted")
       continue
   if senddata.lower() == "***reset":
       print("Choose a server:")
       for i, guild in enumerate(client.guilds):
           print(f"{i}: {guild.name}")
       data = await async_input("server index:")
       if data == "" or data == None:
           continue
       guild = client.guilds[int(data)]
       logger.success(f"guild assigned! guild name: {guild.name}, guild owner: {guild.owner}, guild id: {guild.id}")
       await sleep(1)
       print("Choose a channel:")
       channels: dict[int, dict[str:int]] = {}
       for i, channel in enumerate(guild.text_channels):
           channels.update({i: {channel.name: channel.id}})
           print(f"{i}: {channel.name}")
       data = await async_input("server index:")
       if data == "" or data == None:
           continue
       channel = client.get_channel(list(channels.get(int(data)).values())[0])
       logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
       await get_history(channel)
       continue
   if senddata.lower() == "***resetchannel":
       print("Choose a channel:")
       channels: dict[int, dict[str:int]] = {}
       for i, channel in enumerate(guild.text_channels):
           channels.update({i: {channel.name: channel.id}})
           print(f"{i}: {channel.name}")
       data = await async_input("channel index:")
       if data == "" or data == None:
           continue
       channel = client.get_channel(list(channels.get(int(data)).values())[0])
       logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
       await get_history(channel)
       continue
   if senddata.lower() == "***file":
       try:
         file = filedialog.askopenfilename()
         await channel.send(file=File(file))
       except Exception as e:
           print(f"error sending file\n{e}")
       continue
   if senddata.lower() == "***Changestatus":
       print("status list:\nonline\noffline\nidle")
       status = input("status:")
       if status == "online":
           await client.change_presence(status=Status.online)
       if status == "offline":
           await client.change_presence(status=Status.offline)
       if status == "idle":
           await client.change_presence(status=Status.idle)
       continue
   if senddata.lower() == "***muteguild":
       guildlistformute = []
       for i, mguild in enumerate(client.guilds):
           if mguild.id in guild_mute_list:
               guildlistformute.append(mguild.id)
               continue
           guildlistformute.append(mguild.id)
           print(f"{i}: {mguild.name}")
       muteguildname = await async_input("type guild index: ")
       try:
           mguild = client.get_guild(guildlistformute[int(muteguildname)])
           guild_mute_list.append(mguild.id)
           with open('guildmutes', 'wb') as f:
               towrite = pickle.dumps(guild_mute_list)
               f.write(towrite)
           logger.success(f"Guild '{mguild.name}' muted")
       except Exception as e:
           print(f"index not found\n{e}")
       continue
   if senddata.lower() == "***unmuteguild":
       guildlistforunmute = []
       for i in range(len(guild_mute_list)):
           unmuteg = client.get_guild(guild_mute_list[i])
           guildlistforunmute.append(guild_mute_list[i])
           print(f"{i}: {unmuteg}")
       unmutechanelname = await async_input("type guild index: ")
       try:
           mguild = client.get_guild(guildlistforunmute[int(unmutechanelname)])
           guild_mute_list.remove(mguild.id)
           with open('guildmutes', 'wb') as f:
               towrite = pickle.dumps(guild_mute_list)
               f.write(towrite)
           logger.success(f"Guild '{mguild.name}' unmuted")
       except Exception as e:
           print(f"index not found\n{e}")
       continue
   await channel.send(senddata)

async def get_history(channel:TextChannel):
  messages = []
  async for message in channel.history(limit=config.history_size, oldest_first=False):
    messages.append(message)
  print("Channel history:\n#####################")
  messages.reverse()
  for message in messages:
    date = message.created_at
    rounded_date = date.replace(second=0, microsecond=0)
    rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
    attachment_list = []
    if message.attachments:
        for attachment in message.attachments:
            attachment_list.append(attachment.url)
        print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}, attachments: {attachment_list}")
    else:
        print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}")
  print("#####################")
async def async_input(prompt):
    return await asyncio.to_thread(input, prompt)

client.run(config.Token)
