import os
from io import BytesIO

import pytz
from PIL import Image
from colorama import Fore
from aioconsole import ainput
from term_image.image import AutoImage
from disnake import Client, DMChannel, Forbidden, Guild, Message, NotFound, TextChannel, VoiceChannel

from log import log, error, user_message, warn
import config


def is_valid_index(index, obj_list):
    if index is None:
        log("You entered incorrect index. the command will not continue execution.")
        return False

    if len(obj_list) - 1 < index or index < 0:
        log("You entered incorrect index. the command will not continue execution.")
        return False

    return True

async def async_int_input(prompt="", one_attempt=True):
    while True:
        try:
            return int(await ainput(prompt))
        except:
            if one_attempt:
                return None
            log("enter a number, not text")

async def get_history(channel, limit=50):
    messages = []
    try:
        async for message in channel.history(limit=limit):
            messages.append(message)
    except Forbidden:
        error(f"It's impossible to get: Forbidden.")
    return reversed(messages)

def flatten_newlines(text) -> str:
    return str(text).replace("\n", "    ")

def cut_text(text, max_length=40) -> str:
    return text if len(text) < max_length else f"{text[:max_length]}..."
    
async def prepare_message(message: Message, only_write_messages_from_selected_channel=True, show_ids=False):
    if "\n" in message.content:
        content = "\n↳║" + message.content.replace("\n", "\n ║")
    else:
        content = message.content

    created_at = message.created_at.astimezone(pytz.timezone(config.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
    compiled_message = f"({created_at}) "

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
                replied_content = f"{replied_message.content[:60]}..."
            else:
                replied_content = replied_message.content

            compiled_message += (f"\n{Fore.YELLOW}↳replies to the message: "
                                 f"[{replied_message.author.name}]"
                                 f"{replied_content}"
                                 f"{' <attachments>' if replied_message.attachments else ''}")
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
            author = flatten_newlines(embed.author.name)
            title = flatten_newlines(embed.title)
            fields_titles = [flatten_newlines(field.name) for field in embed.fields]
            fields_values = [flatten_newlines(field.value) for field in embed.fields]
            description = flatten_newlines(embed.description)

            compiled_message += (f"\n{Fore.YELLOW}↳[EMBED]"
                                 f"\n   ↳Author        {author}"
                                 f"\n   ↳Title         {title}"
                                 f"\n   ↳Fields titles {fields_titles}"
                                 f"\n   ↳Fields values {fields_values}"
                                 f"\n   ↳Description   {description}")
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
        if config.DRAW_IMAGES and os.path.splitext(attachment.filename)[1].lower() in [".png", ".jpg", ".jpeg"]:
            img = Image.open(BytesIO(await attachment.read()))
            img = AutoImage(img, height=8)
            img.draw(h_align="left", v_align="top", pad_height=-100, animate=False)

class SelectUtils:
    def __init__(self, client: Client):
        self.client: Client = client

    async def select_guild(self, stop_if_error=False, to_skip=None) -> Guild | None:
        if to_skip is None:
            to_skip = []

        guilds = [guild for guild in self.client.guilds if guild.id not in to_skip]

        if len(guilds) == 0:
            log("Your bot doesn't have any guilds.")
            return

        log("Please, select guild from this list:")
        for i, guild in enumerate(guilds):
            log(f"{i} - {guild.name} (id: {guild.id}, {guild.member_count} members)")

        try:
            return guilds[await async_int_input("Enter the guild index:", stop_if_error)]
        except:
            warn("You entered an invalid index")

    @staticmethod
    async def select_channel(guild: Guild, stop_if_error=False, to_skip=None,
                             show_threads=True, channel_type="text") -> TextChannel | VoiceChannel | None:
        if to_skip is None:
            to_skip = []
        if not isinstance(guild, Guild):
            warn("guild is not Guild")
            return

        match channel_type:
            case "text":
                channels = guild.text_channels
            case "vc":
                channels = guild.voice_channels
            case _:
                raise ValueError("channel_type can only be text or vc")

        channels = [channel for channel in channels if channel.id not in to_skip]
        if len(channels) == 0:
            log(f"Guild doesn't have any {channel_type} channels.")
            return


        log("Please, select channel from this list:")
        for i, channel in enumerate(channels):
            log(f"{i} - {channel.name} (id: {channel.id})")
            try:
                if isinstance(channel, TextChannel):
                    if channel.threads and show_threads:
                        log("↳Channel threads:")
                        for thread in channel.threads[:4]:
                            log(f"  ↳{thread.name} (id: {thread.id})")
            except Exception as ex:
                print(ex)
        try:
            return channels[await async_int_input("Enter the channel index:", stop_if_error)]
        except:
            return