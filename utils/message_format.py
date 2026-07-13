import pytz
from colorama import Fore
from disnake import DMChannel, Message, NotFound

from log import log
import config
from .text import flatten_newlines, cut_text


def _format_content(message: Message) -> str:
    if "\n" in message.content:
        return "\n↳║" + message.content.replace("\n", "\n ║")
    return message.content

def _format_header(message: Message, only_write_messages_from_selected_channel: bool) -> str:
    created_at = message.created_at.astimezone(pytz.timezone(config.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
    content = _format_content(message)

    if isinstance(message.channel, DMChannel):
        return f"({created_at}) [DM] [{message.author.name}] {content}"
    if not only_write_messages_from_selected_channel:
        return f"({created_at}) [{message.guild.name}] [{message.channel.name}] [{message.author.name}] {content}"
    return f"({created_at}) [{message.author.name}] {content}"

async def _format_reply(message: Message) -> str:
    if not (message.reference and message.reference.message_id):
        return ""

    try:
        replied_message = await message.channel.fetch_message(message.reference.message_id)
    except NotFound:
        return f"\n{Fore.YELLOW}↳replies to unknown message"
    except Exception as ex:
        log(f"Exception occurred when getting reply: {ex}")
        return ""

    replied_content = cut_text(replied_message.content, 60)
    attachments_note = " <attachments>" if replied_message.attachments else ""
    return (f"\n{Fore.YELLOW}↳replies to the message: "
            f"[{replied_message.author.name}]"
            f"{replied_content}"
            f"{attachments_note}")

def _format_attachments(message: Message) -> str:
    return "".join(f"\n{Fore.YELLOW}↳attachment: {attachment.url}" for attachment in message.attachments)

def _format_ids(message: Message) -> str:
    return f"\n{Fore.YELLOW}↳channel id:{message.channel.id}, message id:{message.id}"

def _format_embeds(message: Message) -> str:
    result = ""
    for embed in message.embeds:
        if not embed.fields and not embed.title and not embed.author.name and not embed.description:
            continue
        author = flatten_newlines(embed.author.name)
        title = flatten_newlines(embed.title)
        fields_titles = [flatten_newlines(field.name) for field in embed.fields]
        fields_values = [flatten_newlines(field.value) for field in embed.fields]
        description = flatten_newlines(embed.description)

        result += (f"\n{Fore.YELLOW}↳[EMBED]"
                   f"\n   ↳Author        {author}"
                   f"\n   ↳Title         {title}"
                   f"\n   ↳Fields titles {fields_titles}"
                   f"\n   ↳Fields values {fields_values}"
                   f"\n   ↳Description   {description}")
    return result

def _format_reactions(message: Message) -> str:
    if not message.reactions:
        return ""
    reactions = "".join(f"[{reaction.emoji} {reaction.count}]" for reaction in message.reactions)
    return f"\n{Fore.YELLOW}↳reactions: {reactions}"

async def prepare_message(message: Message, only_write_messages_from_selected_channel=True, show_ids=False):
    compiled_message = _format_header(message, only_write_messages_from_selected_channel)
    compiled_message += await _format_reply(message)
    compiled_message += _format_attachments(message)
    if show_ids:
        compiled_message += _format_ids(message)
    compiled_message += _format_embeds(message)
    compiled_message += _format_reactions(message)
    return compiled_message
