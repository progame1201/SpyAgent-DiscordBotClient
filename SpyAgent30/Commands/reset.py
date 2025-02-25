from disnake import *
from .command import command
from .command_output import command_output
from utils import show_history, Select_utils


class reset_output(command_output):
    def __init__(self, guild: Guild, channel: TextChannel):
        super().__init__()
        self.guild = guild
        self.channel = channel

class reset(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
        self.description = f"{self.name} - change the channel and guild"

    async def execute(self, *args):
        guild = await self.select_utils.select_guild()
        channel = await self.select_utils.select_channel(guild)
        await show_history(channel)
        return reset_output(guild, channel)
