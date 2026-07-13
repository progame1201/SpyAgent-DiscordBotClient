from typing import Literal

from disnake import Client, Guild, TextChannel, VoiceChannel

from log import log, warn
from .validation import is_valid_index, async_int_input

_MAX_THREADS_SHOWN = 4


class SelectUtils:
    def __init__(self, client: Client):
        self.client = client

    async def select_guild(self, stop_if_error: bool = False, to_skip: list[int] | None = None) -> Guild | None:
        if to_skip is None:
            to_skip = []

        guilds = [g for g in self.client.guilds if g.id not in to_skip]
        if not guilds:
            log("Your bot doesn't have any guilds.")
            return None

        log("Please select a guild:")
        for i, guild in enumerate(guilds):
            log(f"  {i} - {guild.name} (id: {guild.id}, {guild.member_count} members)")

        index = await async_int_input("Enter the guild index: ", stop_if_error)
        if not is_valid_index(index, guilds):
            warn("Invalid guild index entered.")
            return None

        return guilds[index]

    @staticmethod
    async def select_channel(
        guild: Guild,
        stop_if_error: bool = False,
        to_skip: list[int] | None = None,
        show_threads: bool = True,
        channel_type: Literal["text", "vc"] = "text"
    ) -> TextChannel | VoiceChannel | None:

        if to_skip is None:
            to_skip = []

        match channel_type:
            case "text":
                channels = guild.text_channels
            case "vc":
                channels = guild.voice_channels
            case _:
                raise ValueError(f"channel_type must be 'text' or 'vc', got {channel_type!r}")

        channels = [ch for ch in channels if ch.id not in to_skip]
        if not channels:
            log(f"Guild doesn't have any {channel_type} channels.")
            return None

        log("Please select a channel:")
        for i, channel in enumerate(channels):
            log(f"  {i} - {channel.name} (id: {channel.id})")
            if show_threads and isinstance(channel, TextChannel) and channel.threads:
                log("  ↳ Threads:")
                for thread in channel.threads[:_MAX_THREADS_SHOWN]:
                    log(f"    ↳ {thread.name} (id: {thread.id})")

        index = await async_int_input("Enter the channel index: ", stop_if_error)
        if not is_valid_index(index, channels):
            warn("Invalid channel index entered.")
            return None

        return channels[index]
