from disnake.ext import *
from disnake import *
from loguru import logger
import asyncio
import winsound
import pickle
import hashlib
import os
import pytz
from asyncio import sleep
import config
from colorama import Fore, init
import Commands
import LocalCommandManager
logger.info("Spy Agent 2.5.0, 2024, progame1201")
logger.info("Running...")
client:Client = Client(intents=Intents.all())
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
def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
def check_file_integrity(file_path):
    global hashes
    current_hash = calculate_file_hash(file_path)
    if current_hash in hashes:
        return False
    else:
        hashes = [calculate_file_hash("guildmutes"), calculate_file_hash("channelmutes")]
        return True

@client.event
async def on_ready():
    global guild
    global channel
    logger.info(f"Welcome {client.user.name}! Bot ID: {client.user.id}")
    await sleep(1)
    print("Choose a server:")
    for i, guild in enumerate(client.guilds):
        print(f"{i}: {guild.name}")
    data = await async_input("server index:")
    guild = client.guilds[int(data)]
    logger.success(f"guild assigned! guild name: {guild.name}, guild owner: {guild.owner}, guild id: {guild.id} guild icon url: {guild.icon.url}")
    await sleep(1)
    print("Choose channel:")
    channels: dict[int, dict[str:int]] = {}
    for i, channel in enumerate(guild.text_channels):
        channels.update({i: {channel.name: channel.id}})
        print(f"{i}: {channel.name}")
    data = await async_input("server index:")
    channel = client.get_channel(list(channels.get(int(data)).values())[0])
    logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
    asyncio.run_coroutine_threadsafe(receive_messages(), client.loop)
    asyncio.run_coroutine_threadsafe(chatting(), client.loop)
    asyncio.run_coroutine_threadsafe(detector(), client.loop)


async def detector():
    global guild
    global channel
    async def reaction_add():
        while True:
            reaction, user = await client.wait_for('reaction_add')
            if channel.id == reaction.message.channel.id:
             print(f"Reaction {reaction.emoji} | was added to: {reaction.message.author}: {reaction.message.content} | by {user.name}")
    async def reaction_remove():
        while True:
            reaction, user = await client.wait_for('reaction_remove')
            if channel.id == reaction.message.channel.id:
             print(f"Reaction {reaction.emoji} | was removed from: {reaction.message.author}: {reaction.message.content} | by {user.name}")
    async def message_delete():
       while True:
        message:Message = await client.wait_for("message_delete")
        if channel.id == message.channel.id:
         print(f"Message {message.content} | was removed from: {message.guild}: {message.channel}: {message.author}")
    async def message_edit():
       while True:
        before, after = await client.wait_for("message_edit")
        if channel.id == after.channel.id:
         print(f"Message: {before.content} | has been changed to: {after.content} |in: {after.guild}: {after.channel}: {after.author}")
    async def guild_remove():
        while True:
            guild = await client.wait_for("guild_remove")
            print(f"The guild: {guild.name} | has been removed from the guild list (this could be due to: The client has been banned. The client was kicked out. The guild owner deleted the guild.")
    if config.detector:
        if config.on_reaction_add:
            asyncio.run_coroutine_threadsafe(reaction_add(), client.loop)
        if config.on_reaction_remove:
            asyncio.run_coroutine_threadsafe(reaction_remove(), client.loop)
        if config.on_message_delete:
            asyncio.run_coroutine_threadsafe(message_delete(), client.loop)
        if config.on_message_edit:
            asyncio.run_coroutine_threadsafe(message_edit(), client.loop)
        if config.on_guild_remove:
            asyncio.run_coroutine_threadsafe(guild_remove(), client.loop)
async def receive_messages():
    global channel
    global guild
    global hashes
    lastmutes:list = await getmutes()
    channels_mute_list = lastmutes[0]
    guild_mute_list = lastmutes[1]
    hashes = [calculate_file_hash("guildmutes"), calculate_file_hash("channelmutes")]
    while True:
      message:Message = await client.wait_for('message')
      date = message.created_at
      rounded_date = date.replace(second=0, microsecond=0)
      rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
      if isinstance(message.channel, DMChannel):
       if config.allow_private_messages:
          msg = f"Private message: {message.channel}: {rounded_date_string} ({message.author.id})"
       else:
           continue
      else:
        if check_file_integrity("guildmutes") or check_file_integrity("channelmutes"):
         lastmutes = await getmutes()
         channels_mute_list = lastmutes[0]
         guild_mute_list = lastmutes[1]

      if message.channel.id in channels_mute_list:
         if message.channel.id != channel.id:
          continue
      if message.guild.id in guild_mute_list:
         if message.guild.id != guild.id:
          continue
      attachment_list = []

      msg = f"{message.guild}: {message.channel}: {rounded_date_string}"
      if isinstance(message.channel, DMChannel):
       if config.allow_private_messages:
          msg = f"Private message: {message.channel}: {rounded_date_string} ({message.author.id})"
       else:
           continue
      if config.display_users_avatars_urls:
          msg += f" ({message.author.avatar.url}) {message.author.name}: {message.content}"
      else:
          msg += f" {message.author.name}: {message.content}"

      if message.attachments:
          for attachment in message.attachments:
              attachment_list.append(attachment.url)
          msg += f" | attachments: {attachment_list}"

      print(f"{msg}\n")
      if config.notification == True:
        if message.author.id != client.user.id:
          winsound.Beep(500, 100)
          winsound.Beep(1000, 100)

async def chatting():
 global guild
 global channel
 logger.info("Starting command manager...")
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
 cm.new(command_name="***edit", func=cmnds.edit)
 print(f"\n{Fore.YELLOW}List of loaded commands:\n{cm.get_keys()}\n{Fore.CYAN}type ***help to get more info!")
 logger.success("Command manager started!")
 await sleep(2)
 await get_history(channel)
 while True:
   await sleep(1)
   senddata = await async_input(f"{Fore.LIGHTBLACK_EX}Message to {guild.name}: {channel.name}:\n{Fore.RESET}")
   if senddata.lower() == "***help":
       print("#####HELP#####\n***Mute - mute any channel\n***Unmute - unmute any channel\n***Delete - delete any message you have selected\n***Reset - Re-select the guild and channel for communication\n***Resetchannel - Re-select a channel for communication\n***File - send a file\n***Muteguild - mute any guild\n***Unmuteguild - unmute any guild\n***Reaction - react any message\n***Privatemsg - Send a private message to the user\n***Gethistory - Get the history of the channel you are on\n#####INFO#####\nall messages are written in the format: guild: channel: author: message\n##############")
       continue
   cmresult = cm.execute(senddata)
   if cmresult != False:
    cmresult:dict = await cmresult()
    if cmresult != None:
       if "channel" in list(cmresult.keys()):
           channel = cmresult["channel"]
       if "guild" in list(cmresult.keys()):
           guild = cmresult["guild"]
    continue
   try:
     await channel.send(senddata)
   except Forbidden:
       print(f"{Fore.RED}It's impossible to send: Forbidden.")

async def get_history(channel:TextChannel):
  messages = []
  try:
   async for message in channel.history(limit=config.history_size, oldest_first=False):
    messages.append(message)
  except Forbidden:
      print(f"{Fore.RED}It's impossible to get: Forbidden.")
      return
  print("Channel history:\n#####################")
  messages.reverse()
  for message in messages:
    date = message.created_at
    rounded_date = date.replace(second=0, microsecond=0)
    rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
    attachment_list = []
    reactions_list = []
    msg = f"{message.channel}: {rounded_date_string} {message.author}: {message.content}"
    if message.attachments:
        for attachment in message.attachments:
            attachment_list.append(attachment.url)
        msg +=f" | attachments: {attachment_list}"

    if message.reactions:
        for reaction in message.reactions:
            reactions_list.append(reaction.emoji)
        msg += f" | reactions: {reactions_list}"
    print(msg)

  print("#####################")
async def async_input(prompt):
    return await asyncio.to_thread(input, prompt)

client.run(config.Token)