from disnake import *
from .command import Command
from .commandoutput import CommandOutput
from utils import show_history, SelectUtils


class ResetOutput(CommandOutput):
    def __init__(self, guild: Guild, channel: TextChannel):
        super().__init__()
        self.guild = guild
        self.channel = channel


class Reset(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} - change the channel and guild"

    async def execute(self, *args):
        guild = await self.select_utils.select_guild()
        channel = await self.select_utils.select_channel(guild)
        await show_history(channel)
        return ResetOutput(guild, channel)
