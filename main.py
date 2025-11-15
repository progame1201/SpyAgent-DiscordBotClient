import conifg
import asyncio
from disnake import *
from commands import *
from aioconsole import ainput
from log import log, user_message, event, error
from utils import SelectUtils, prepare_message, show_history, GuildMute, ChannelMute, MuteUtils, draw_message_attachments


log("SpyAgent-DiscordBotClient 3.3.0, 2025, progame1201")
client = Client(intents=Intents.all())

mutes = MuteUtils.get_mutes()

guild_mutes = []
channel_mutes = []
vc_clients = []

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
    select_utils = SelectUtils(client)

    guild = await select_utils.select_guild()
    channel = await select_utils.select_channel(guild)
    await show_history(channel, draw_images=conifg.DRAW_IMAGES)
    asyncio.run_coroutine_threadsafe(message_sender(), client.loop)


@client.event
async def on_message(message: Message):
    if conifg.WRITE_MESSAGES_ONLY_FROM_SELECTED_CHANNEL and message.channel != channel:
        return

    if message.channel in channel_mutes or message.guild in guild_mutes and message.channel != channel:
        return

    user_message(
        await prepare_message(
            message,
            conifg.WRITE_MESSAGES_ONLY_FROM_SELECTED_CHANNEL,
        )
    )
    if conifg.DRAW_IMAGES:
        await draw_message_attachments(message)


@client.event
async def on_reaction_add(reaction, user):
    if channel.id == reaction.message.channel.id:
        event(
            f"Reaction {reaction.emoji} | was added to: {reaction.message.author}: "
            f"{reaction.message.content if len(reaction.message.content) < 40 else f"{reaction.message.content[:40]}..."} | by {user.name}\n")


@client.event
async def on_reaction_remove(reaction, *args):
    if channel.id == reaction.message.channel.id:
        event(
            f"Reaction {reaction.emoji} | was removed from: {reaction.message.author}: "
            f"{reaction.message.content if len(reaction.message.content) < 40 else f"{reaction.message.content[:40]}..."}\n")


@client.event
async def on_message_delete(message: Message):
    if channel.id == message.channel.id:
        event(f"Message removed {message.author}: {message.content} \n")


@client.event
async def on_message_edit(before, after):
    if channel.id == after.channel.id:
        event(f"Message: {after.author}: {before.content} | has been changed to: {after.content}\n")


@client.event
async def on_guild_channel_delete(channel: TextChannel):
    if channel.guild.id == guild.id:
        event(f"channel {channel.name} has been deleted\n")


@client.event
async def on_guild_channel_create(channel: TextChannel):
    if channel.guild.id == guild.id:
        event(f"channel {channel.name} has been created | id: {channel.id}\n")


@client.event
async def on_guild_join(guild):
    event(f"Client was joined to the {guild.name} guild")


@client.event
async def on_guild_remove(guild):
    event(
        f"The guild: {guild.name} has been removed from the guild list (this could be due to: "
        f"The client has been banned. The client was kicked out. The guild owner deleted the guild. "
        f"Or did you just leave the guild)\n")


@client.event
async def on_voice_state_update(member: Member, before, after):
    if member.guild.id == guild.id:
        if before.channel is None and after.channel is not None:
            event(f'{member.name} joined voice channel {after.channel}')
        elif before.channel is not None and after.channel is None:
            event(f'{member.name} left voice channel {before.channel}')


async def message_sender():
    global guild
    global channel
    while True:
        message: str = await ainput("")
        if message.lower().startswith(conifg.COMMAND_PREFIX):
            message = message.replace(conifg.COMMAND_PREFIX, "").lower()
            if message == "help":
                print()
                log("HELP:")
                for command in get_commands(guild, channel, client):
                    log(command.description)
                print()
            for command in get_commands(guild, channel, client):
                if message.split(" ")[0] != command.name:
                    continue

                if command.name == "mute" or command.name == "unmute":  # I tried to use isinstance, but it froze. Idk what the problem is.
                    command.channel_mutes = channel_mutes
                    command.guild_mutes = guild_mutes
                    output: CommandOutput = await command.execute(message.split(" ")[1:])

                elif command.name == "vcdisconnect" or command.name == "vcplay" or command.name == "vcstop":
                    command.vc_clients = vc_clients
                    output: CommandOutput = await command.execute(message.split(" ")[1:])

                else:
                    output: CommandOutput = await command.execute(message.split(" ")[1:])

                if isinstance(output, ResetOutput):
                    guild = output.guild
                    channel = output.channel

                if isinstance(output, SetOutput):
                    channel = output.channel

                if isinstance(output, VcDisconnectOutput):
                    vc_clients.remove(output.vc_client)

                if isinstance(output, VcConnectOutput):
                    vc_clients.append(output.vc_client)

                if isinstance(output, MuteOutput):
                    if isinstance(output.mute_object, ChannelMute):
                        channel_mutes.append(output.mute_object.id)

                    if isinstance(output.mute_object, GuildMute):
                        guild_mutes.append(output.mute_object.id)

                if isinstance(output, UnmuteOutput):

                    if isinstance(output.mute_object, ChannelMute):
                        channel_mutes.remove(output.mute_object.id)

                    if isinstance(output.mute_object, GuildMute):
                        guild_mutes.remove(output.mute_object.id)

                if isinstance(output, GuildLeaveOutput):
                    guild = output.guild
                    channel = output.channel

            continue
        try:
            await channel.send(message)
        except Forbidden:
            error(f"It's impossible to send: Forbidden.")


client.run(conifg.TOKEN)
