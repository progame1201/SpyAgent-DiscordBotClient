from disnake import *
from Log import log, user_message, event
from utils import Select_utils, prepare_message, show_history, guild_mute, channel_mute, mute_utils
from aioconsole import ainput
import asyncio
import conifg
from Commands import *


log("SpyAgent-DiscordBotClient 3.0.0, 2024, progame1201")
client = Client(intents=Intents.all())
mutes = mute_utils.get_mutes()

guild_mutes = []
channel_mutes = []

for mute in mutes.channels:
    channel_mutes.append(mute.id)
for mute in mutes.guilds:
    guild_mutes.append(mute.id)
log(f"Loaded mutes: {channel_mutes}, {guild_mutes}")

@client.event
async def on_ready():
    global guild
    global channel

    log(f"Logined in as {client.user.name}", show_time=True)
    select_utils = Select_utils(client)

    guild = await select_utils.select_guild()
    channel = await select_utils.select_channel(guild)
    await show_history(channel)
    await detector()
    asyncio.run_coroutine_threadsafe(message_sender(), client.loop)

@client.event
async def on_message(message:Message):

    if conifg.only_write_messages_from_selected_channel and message.channel != channel:
        return

    if message.channel in channel_mutes or message.guild in guild_mutes and message.channel != channel:
        return

    user_message(await prepare_message(message, conifg.only_write_messages_from_selected_channel))

async def detector():
    async def on_reaction_add(reaction, user):
          if channel.id == reaction.message.channel.id:
           event(f"Reaction {reaction.emoji} | was added to: {reaction.message.author}: {reaction.message.content[:40]} | by {user.name}\n")

    async def on_reaction_remove(reaction, user):
          if channel.id == reaction.message.channel.id:
           event(f"Reaction {reaction.emoji} | was removed from: {reaction.message.author}: {reaction.message.content}\n")

    async def on_message_delete(message:Message):
          if channel.id == message.channel.id:
           event(f"Message removed {message.author}: {message.content[:40]} \n")

    async def on_message_edit(before, after):
          if channel.id == after.channel.id:
           event(f"Message: {after.author}: {before.content[:40]} | has been changed to: {after.author}: {after.content[:40]}\n")
    async def on_guild_channel_delete(channel:channel):
          if channel.guild.id == guild.id:
              event(f"channel {channel.name} has been deleted\n")
    async def on_guild_channel_create(channel:channel):
          if channel.guild.id == guild.id:
              event(f"channel {channel.name} has been created | id: {channel.id}\n")
    async def on_guild_join(guild):
          event(f"Client was joined to the {guild.name} guild")
    async def on_guild_remove(guild):
          event(f"The guild: {guild.name} has been removed from the guild list (this could be due to: The client has been banned. The client was kicked out. The guild owner deleted the guild. Or did you just quit the guild)\n")

    async def on_voice_state_update(member:Member, before, after):
        if member.guild.id == guild.id:
         if before.channel is None and after.channel is not None:
            event(f'{member.name} joined voice channel {after.channel}')
         elif before.channel is not None and after.channel is None:
            event(f'{member.name} left voice channel {before.channel}')

    client.event(on_reaction_add)
    client.event(on_reaction_remove)
    client.event(on_message_delete)
    client.event(on_message_edit)
    client.event(on_guild_remove)
    client.event(on_guild_join)
    client.event(on_guild_channel_create)
    client.event(on_guild_channel_delete)
    client.event(on_voice_state_update)

async def message_sender():
    global guild
    global channel
    while True:
        message:str = await ainput("")
        if message.lower().startswith(conifg.command_prefix):
            message = message.replace(conifg.command_prefix, "").lower()
            if message == "help": #workaround
                print()
                log("HELP:")
                for _command in get_commands(guild, channel, client):
                    log(_command.description)
                print()
            for _command in get_commands(guild, channel, client):
                if message.split(" ")[0] != _command.name:
                    continue

                if _command.name == "mute" or _command.name == "unmute": # I tried to use isinstance, but it froze. Idk what the problem is.
                    _command.channel_mutes = channel_mutes
                    _command.guild_mutes = guild_mutes
                    output: command_output = await _command.execute(message.split(" ")[1:])
                else:
                    output:command_output = await _command.execute(message.split(" ")[1:])

                if isinstance(output, reset_output):
                    guild = output.guild
                    channel = output.channel

                if isinstance(output, set_output):
                    channel = output.channel

                if isinstance(output, mute_output):

                    if isinstance(output.mute_object, channel_mute):
                        channel_mutes.append(output.mute_object.id)

                    if isinstance(output.mute_object, guild_mute):
                        guild_mutes.append(output.mute_object.id)

                if isinstance(output, unmute_output):

                    if isinstance(output.mute_object, channel_mute):
                        channel_mutes.remove(output.mute_object.id)

                    if isinstance(output.mute_object, guild_mute):
                        guild_mutes.remove(output.mute_object.id)

            continue
        await channel.send(message)

client.run(conifg.token)