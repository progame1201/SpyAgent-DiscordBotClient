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
from colorama import Fore, init
import Commands
import LocalCommandManager
logger.info("Spy Agent 2.1.0, 2023, progame1201")
logger.info("Running...")
client = Client(intents=Intents.all())
init(autoreset=True)

async def getmutes():
    if os.path.exists("channelmutes"):
        if os.path.getsize("channelmutes") > 0:
            data = open("channelmutes", 'rb').read()
            channels_mute_list = pickle.loads(data)
        else:
            channels_mute_list = []
    else:
        open("channelmutes", 'wb').close()
        channels_mute_list = []

    if os.path.exists("guildmutes"):
        if os.path.getsize("guildmutes") > 0:
            data = open("guildmutes", 'rb').read()
            guild_mute_list = pickle.loads(data)
        else:
            guild_mute_list = []
    else:
        open("guildmutes", 'wb').close()
        guild_mute_list = []
    return [channels_mute_list, guild_mute_list]

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
  logger.info("Starting command manager...")
  global cm
  global cmnds
  cm = LocalCommandManager.Manager()
  cmnds = Commands.Commands(client=client, guild=guild, channel=channel)
  cm.new(command_name="***reset", func=cmnds.reset)
  cm.new(command_name="***resetchannel", func=cmnds.resetchannel)
  cm.new(command_name="***file", func=cmnds.file)
  cm.new(command_name="***delete", func=cmnds.delete)
  cm.new(command_name="***status", func=cmnds.status)
  cm.new(command_name="***mute", func=cmnds.mutechannel)
  cm.new(command_name="***unmute", func=cmnds.unmutechannel)
  cm.new(command_name="***muteguild", func=cmnds.guildmute)
  cm.new(command_name="***unmuteguild", func=cmnds.unmuteguild)
  cm.new(command_name="***gethistory", func=cmnds.get_history)
  cm.new(command_name="***reaction", func=cmnds.reaction)
  cm.new(command_name="***privatemsg", func=cmnds.privatemsg)
  print(f"\n{Fore.YELLOW}List of loaded commands:\n{cm.get_keys()}\n{Fore.CYAN}type ***help to get more info!")
  logger.success("Command manager started!")
  await get_history(channel)
  asyncio.run_coroutine_threadsafe(receive_messages(client), client.loop)
  asyncio.run_coroutine_threadsafe(chatting(channel, guild), client.loop)

async def receive_messages(client):
    while True:
      attachment_list = []
      message = await client.wait_for('message')
      if isinstance(message.channel, DMChannel):
       if config.allow_private_messages == True:
        print(f'\nPrivate message: {message.channel}: ({message.author.id}) {message.author.name}: {message.content}')
       continue
      muteslist = await getmutes()
      channels_mute_list = muteslist[0]
      guild_mute_list = muteslist[1]
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
 global cm
 global cmnds
 while True:
   await sleep(1)
   senddata = await async_input(f"{Fore.LIGHTBLACK_EX}Message to {guild.name}: {channel.name}:\n")
   if senddata.lower() == "***help":
       print("#####HELP#####\n***Mute - mute any channel\n***Unmute - unmute any channel\n***Delete - delete any message you have selected\n***Reset - Re-select the guild and channel for communication\n***Resetchannel - Re-select a channel for communication\n***File - send a file\n***Muteguild - mute any guild\n***Unmuteguild - unmute any guild\n***Reaction - react any message\n##############")
       continue
   cmresult = cm.execute(senddata)
   if cmresult != False:
    cmresult: dict = await cmresult()
    if cmresult != None:
       if "channel" in list(cmresult.keys()):
           channel = cmresult["channel"]
       if "guild" in list(cmresult.keys()):
           guild = cmresult["guild"]
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