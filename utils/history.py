from disnake import Forbidden

from log import error, user_message
from .message_format import prepare_message
from .images import draw_message_attachments


async def get_history(channel, limit=50):
    messages = []
    try:
        async for message in channel.history(limit=limit):
            messages.append(message)
    except Forbidden:
        error(f"It's impossible to get: Forbidden.")
    return reversed(messages)

async def show_history(channel, draw_images=False):
    messages = await get_history(channel)
    for message in messages:
        user_message(await prepare_message(message, True))
        if draw_images:
            await draw_message_attachments(message)
