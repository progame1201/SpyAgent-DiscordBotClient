import asyncio

from disnake import Client, DMChannel, Forbidden, Guild, Intents, Member, Message, TextChannel
from commands import (
    CommandOutput,
    GuildLeaveOutput,
    MuteOutput,
    ResetOutput,
    SetOutput,
    UnmuteOutput,
    VcConnectOutput,
    VcDisconnectOutput,
    get_commands,
)
from aioconsole import ainput

import config
from log import log, user_message, event, error, warn
from mutes import GuildMute, ChannelMute, MuteUtils
from utils import SelectUtils, prepare_message, show_history, cut_text, draw_message_attachments


log("SpyAgent-DiscordBotClient 3.4.3, 2026, progame1201")
client = Client(intents=Intents.all())

mutes = MuteUtils.get_mutes()
select_utils: SelectUtils | None = None

guild_mutes = []
channel_mutes = []
vc_clients = []
guild: Guild | None = None
channel: TextChannel | None = None

for mute in mutes.channels:
    channel_mutes.append(mute.id)
for mute in mutes.guilds:
    guild_mutes.append(mute.id)
log(f"Loaded mutes: {channel_mutes}, {guild_mutes}")

@client.event
async def on_ready():
    global guild, channel, select_utils

    log(f"Logged in as {client.user.name}", show_time=True)
    select_utils = SelectUtils(client)
    guild = await select_utils.select_guild()
    
    if guild is None:
        warn("Guild is not selected")
        exit(0)
    channel = await select_utils.select_channel(guild)
    if channel is None:
        warn("Channel is not selected")
        exit(0)
        
    await show_history(channel, draw_images=config.DRAW_IMAGES)
    asyncio.create_task(message_sender())

@client.event
async def on_message(message: Message):
    if channel is None:
        warn("Why channel is None?")
        return
    if guild is None and not isinstance(message.channel, DMChannel):
        warn("Why guild is None?")
        return

    if config.WRITE_MSGS_FROM_SEL_CH and message.channel.id != channel.id:
        return
    if not isinstance(message.channel, DMChannel):
        if (message.channel.id in channel_mutes or message.guild.id in guild_mutes) and message.channel.id != channel.id:
            return
    else:
        if (message.channel.id in channel_mutes) and message.channel.id != channel.id:
            return
    try:
        user_message(await prepare_message(message, config.WRITE_MSGS_FROM_SEL_CH))
        if config.DRAW_IMAGES:
            await draw_message_attachments(message)
    except Exception as ex:
        error(f"{message.author.name}:{message.channel}:{message.id}{ex}")

@client.event
async def on_reaction_add(reaction, user):
    if channel is None:
        warn("Why channel is None?")
        return
    if channel.id == reaction.message.channel.id:
        event(
            f"Reaction {reaction.emoji} | was added to: {reaction.message.author}: "
            f"{cut_text(reaction.message.content)} | by {user.name}\n")

@client.event
async def on_reaction_remove(reaction, *args):
    if channel is None:
        warn("Why channel is None?")
        return
    if channel.id == reaction.message.channel.id:
        event(
            f"Reaction {reaction.emoji} | was removed from: {reaction.message.author}: "
            f"{cut_text(reaction.message.content)}\n")

@client.event
async def on_message_delete(message: Message):
    if channel is None:
        warn("Why channel is None?")
        return
    if channel.id == message.channel.id:
        event(f"Message removed {message.author}: {message.content} \n")

@client.event
async def on_message_edit(before, after):
    if channel is None:
        warn("Why channel is None?")
        return
    if channel.id == after.channel.id:
        event(f"Message: {after.author}: {before.content} | has been changed to: {after.content}\n")

@client.event
async def on_guild_channel_delete(channel: TextChannel):
    if guild is None:
        warn("Why guild is None?")
        return
    if channel.guild.id == guild.id:
        event(f"channel {channel.name} has been deleted\n")

@client.event
async def on_guild_channel_create(channel: TextChannel):
    if guild is None:
        warn("Why guild is None?")
        return
    if channel.guild.id == guild.id:
        event(f"channel {channel.name} has been created | id: {channel.id}\n")

@client.event
async def on_guild_join(guild):
    event(f"Client was joined to the {guild.name} guild")

@client.event
async def on_guild_remove(leaved_guild):
    if guild is None:
        warn("Why guild is None?")
        return
    event(
        f"The guild: {leaved_guild.name} has been removed from the guild list (this could be due to: "
        f"The bot has been banned. The bot was kicked out. The guild owner deleted the guild. "
        f"Or you just left the guild)\n")
    if guild.id == leaved_guild.id:
        event(f"Please use {config.COMMAND_PREFIX}reset command")

@client.event
async def on_voice_state_update(member: Member, before, after):
    if guild is None:
        warn("Why guild is None?")
        return
    if member.guild.id == guild.id:
        if before.channel is None and after.channel is not None:
            event(f'{member.name} joined voice channel {after.channel}')
        elif before.channel is not None and after.channel is None:
            event(f'{member.name} left voice channel {before.channel}')

async def message_sender():
    global guild, channel
    while True:
        message: str = await ainput("")
        if channel is None or guild is None:
            warn("Currently channel or guild is not selected for some reason.")
            guild = await select_utils.select_guild()
            if guild is None:
                continue
            channel = await select_utils.select_channel(guild)
            if channel is None:
                continue
            continue
        if message.lower().startswith(config.COMMAND_PREFIX):
            message = message[len(config.COMMAND_PREFIX):]
            if message.lower() == "help":
                print()
                log("HELP:")
                log("help - display help.")
                for command in get_commands(guild, channel, client):
                    log(command.description)
                print()
                continue

            for command in get_commands(guild, channel, client):
                if message.split(" ")[0].lower() != command.name:
                    continue
                output = None
                try:
                    args = message.split(" ")
                    if len(args) > 1:
                        args = args[1:]
                        
                    if command.name == "mute" or command.name == "unmute":  # I tried to use isinstance, but it froze. Idk what the problem is.
                        command.channel_mutes = channel_mutes
                        command.guild_mutes = guild_mutes
                        output: CommandOutput = await command.execute(args)

                    elif command.name == "vcdisconnect" or command.name == "vcplay" or command.name == "vcstop":
                        command.vc_clients = vc_clients
                        output: CommandOutput = await command.execute(args)

                    else:
                        output: CommandOutput = await command.execute(args)
                except Forbidden:
                    log("Cannot execute command: Forbidden.")
                except Exception as ex:
                    error(f"Cannot execute command: {str(ex)}")

                if isinstance(output, ResetOutput):
                    if output.guild is not None and output.channel is not None:
                        guild = output.guild
                        channel = output.channel

                if isinstance(output, SetOutput):
                    channel = output.channel

                if isinstance(output, VcDisconnectOutput):
                    if output.vc_client in vc_clients:
                        vc_clients.remove(output.vc_client)
                    else:
                        warn("VC client was not connected or already disconnected.")

                if isinstance(output, VcConnectOutput):
                    vc_clients.append(output.vc_client)

                if isinstance(output, MuteOutput):
                    if isinstance(output.mute_object, ChannelMute):
                        channel_mutes.append(output.mute_object.id)

                    if isinstance(output.mute_object, GuildMute):
                        guild_mutes.append(output.mute_object.id)

                if isinstance(output, UnmuteOutput):
                    if isinstance(output.mute_object, ChannelMute):
                        if output.mute_object.id in channel_mutes:
                            channel_mutes.remove(output.mute_object.id)
                        else:
                            warn("Channel was not muted or already unmuted.")

                    if isinstance(output.mute_object, GuildMute):
                        if output.mute_object.id in guild_mutes:
                            guild_mutes.remove(output.mute_object.id)

                if isinstance(output, GuildLeaveOutput):
                    guild = output.guild
                    channel = output.channel
                break
            else:
                log(f"Command not found. Use {config.COMMAND_PREFIX}help to see the list of commands.")

            continue
        try:
            await channel.send(message)
        except Forbidden:
            error(f"It's impossible to send: Forbidden.")

client.run(config.TOKEN)