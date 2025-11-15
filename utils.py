import os
import pytz
import conifg
import pickle
from PIL import Image
from disnake import *
from io import BytesIO
from colorama import Fore
from aioconsole import ainput
from term_image.image import AutoImage
from log import log, error, user_message


async def async_int_input(prompt=""):
    while True:
        try:
            num = int(await ainput(prompt))
            return num
        except:
            log("enter a number, not text")
            pass


async def try_async_int_input(prompt=""):
    try:
        num = int(await ainput(prompt))
        return num
    except:
        return False


async def get_history(channel, limit=50):
    messages = []
    try:
        async for message in channel.history(limit=limit):
            messages.append(message)
    except Forbidden:
        error(f"It's impossible to get: Forbidden.")
    return reversed(messages)


async def prepare_message(message: Message, only_write_messages_from_selected_channel=True, show_ids=False):
    if "\n" in message.content:
        content = "\n║" + message.content.replace("\n", "\n║")
    else:
        content = message.content
    created_at = message.created_at.astimezone(pytz.timezone(conifg.TIMEZONE))
    compiled_message = f"({created_at.year}-{created_at.month}-{created_at.day} {created_at.hour}:{created_at.minute}:{created_at.second}) "

    if not only_write_messages_from_selected_channel:
        compiled_message += f"[{message.guild.name}] [{message.channel.name}] [{message.author.name}] {content}"
    elif isinstance(message.channel, DMChannel):
        compiled_message += f"[DM] [{message.author.name}] {content}"
    else:
        compiled_message += f"[{message.author.name}] {content}"
    if message.reference and message.reference.message_id:
        try:
            replied_message = await message.channel.fetch_message(message.reference.message_id)

            if len(replied_message.content) >= 60:
                content = f"{replied_message.content[:60]}..."
            else:
                content = replied_message.content

            compiled_message += (f"\n{Fore.YELLOW}↳replies to the message: "
                                 f"[{replied_message.author.name}]"
                                 f"{f" {content}" if content else ""}"
                                 f"{" <attachments>" if replied_message.attachments else ""}")
        except NotFound:
            compiled_message += f"\n{Fore.YELLOW}↳replies to unknown message"
        except Exception as ex:
            log(f"Exception occurred when getting reply: {ex}")

    if message.attachments:
        for attachment in message.attachments:
            compiled_message += f"\n{Fore.YELLOW}↳attachment: {attachment.url}"
    if show_ids:
        compiled_message += f"\n{Fore.YELLOW}↳channel id:{message.channel.id}, message id:{message.id}"
    if message.embeds:
        for embed in message.embeds:
            if not embed.fields and not embed.title and not embed.author.name and not embed.description:
                continue
            compiled_message += (f"\n{Fore.YELLOW}↳[EMBED]"
                                 f"\n   ↳Author        {str(embed.author.name).replace("\n", "    ")}"
                                 f"\n   ↳Title         {str(embed.title).replace("\n", "    ")}"
                                 f"\n   ↳Fields titles {[str(field.name).replace("\n", "    ") for field in embed.fields]}"
                                 f"\n   ↳Fields values {[str(field.value).replace("\n", "    ") for field in embed.fields]}"
                                 f"\n   ↳Description   {str(embed.description).replace("\n", "    ")}")
    if message.reactions:
        compiled_message += f"\n{Fore.YELLOW}↳reactions: "
        for reaction in message.reactions:
            compiled_message += f"[{reaction.emoji} {reaction.count}]"
    return compiled_message


async def show_history(channel, draw_images=False):
    messages = await get_history(channel)
    for message in messages:
        user_message(await prepare_message(message, True))
        if draw_images:
            await draw_message_attachments(message)


async def draw_message_attachments(message):
    for attachment in message.attachments:
        if conifg.DRAW_IMAGES and os.path.splitext(attachment.filename)[1].lower().lower() in [".png", ".jpg", ".jpeg"]:
            img = Image.open(BytesIO(await attachment.read()))
            img = AutoImage(img, height=8)
            img.draw(h_align="left", v_align="top", pad_height=-100, animate=False)


class SelectUtils:
    def __init__(self, client: Client):
        self.client: Client = client

    async def select_guild(self, stop_if_error=False, to_skip=None) -> Guild | None:
        if to_skip is None:
            to_skip = []
        have_guilds = False

        log("Please, select guild from this list:")
        for i, guild in enumerate(self.client.guilds):
            if guild.id in to_skip:
                continue
            have_guilds = True
            log(f"{i} - {guild.name} (id: {guild.id}, {guild.member_count} members)")

        if not have_guilds:
            return

        try:
            if stop_if_error:
                return self.client.guilds[await try_async_int_input("Enter the guild index:")]
            else:
                return self.client.guilds[await async_int_input("Enter the guild index:")]
        except:
            if stop_if_error:
                return
            print("Enter a valid index")

    @staticmethod
    async def select_channel(guild: Guild, stop_if_error=False, to_skip=None,
                             show_threads=True) -> TextChannel | None:
        if to_skip is None:
            to_skip = []
        have_channels = False

        log("Please, select channel from this list:")
        for i, channel in enumerate(guild.text_channels):
            if channel.id in to_skip:
                continue
            have_channels = True
            log(f"{i} - {channel.name} (id: {channel.id})")
            try:
                if channel.threads and show_threads:
                    log("↳Channel threads:")
                    for thread in channel.threads[:4]:
                        log(f"  ↳{thread.name} (id: {thread.id})")
            except Exception as ex:
                print(ex)

        if not have_channels:
            return

        try:
            if stop_if_error:
                return guild.text_channels[await try_async_int_input("Enter the channel index:")]
            else:
                return guild.text_channels[await async_int_input("Enter the channel index:")]
        except:
            if stop_if_error:
                return
            print("Enter a valid index")

    @staticmethod
    async def select_vc_channel(guild: Guild, stop_if_error=False, to_skip=None, ) -> VoiceChannel | None:
        if to_skip is None:
            to_skip = []
        channels = False

        log("Please, select channel from this list:")
        for i, channel in enumerate(guild.voice_channels):
            if channel.id in to_skip:
                continue
            channels = True
            log(f"{i} - {channel.name} {[member.name for member in channel.members]}")
        if not channels:
            return

        try:
            if stop_if_error:
                return guild.voice_channels[await try_async_int_input("Enter the channel index:")]
            else:
                return guild.voice_channels[await async_int_input("Enter the channel index:")]
        except:
            if stop_if_error:
                return
            print("Enter a valid index")


class GuildMute:
    def __init__(self, id):
        self.id = id


class ChannelMute:
    def __init__(self, id):
        self.id = id


class MutePare:
    def __init__(self, guilds_list, channels_list):
        self.guilds = guilds_list
        self.channels = channels_list


class MuteUtils:
    def __init__(self):
        pass

    @staticmethod
    def _read_mutes():
        if not os.path.exists("mutes") or os.path.getsize("mutes") <= 0:
            return []
        with open("mutes", 'rb') as f:
            mutes: list = pickle.loads(f.read())
        if not mutes:
            return []
        return mutes

    @staticmethod
    def add_mute(mute_object):
        mutes = MuteUtils._read_mutes()
        mutes.append(mute_object)
        with open("mutes", 'wb') as f:
            f.write(pickle.dumps(mutes))

    @staticmethod
    def remove_mute(mute_object):
        try:
            mutes = MuteUtils._read_mutes()
            mutes.remove(mute_object)
        except:
            return
        with open("mutes", 'wb') as f:
            f.write(pickle.dumps(mutes))

    @staticmethod
    def remove_mute_by_id(id):
        try:
            mutes = MuteUtils._read_mutes()
            for mute in mutes:
                if mute.id == id:
                    mutes.remove(mute)
        except:
            return
        with open("mutes", 'wb') as f:
            f.write(pickle.dumps(mutes))

    @staticmethod
    def get_mutes():
        mutes = MuteUtils._read_mutes()
        guild_mutes = []
        channel_mutes = []
        for mute in mutes:
            if isinstance(mute, ChannelMute):
                channel_mutes.append(mute)
            if isinstance(mute, GuildMute):
                guild_mutes.append(mute)
        return MutePare(guild_mutes, channel_mutes)
