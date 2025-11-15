from disnake import *
from .command import Command
from .commandoutput import CommandOutput
from utils import show_history, SelectUtils


class SetOutput(CommandOutput):
    def __init__(self, channel: TextChannel):
        super().__init__()
        self.channel = channel


class Set(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} <channel id> - set the channel by id."

    async def execute(self, *args):
        try:
            channel = await self.client.fetch_channel(args[0][0])
        except:
            channel = self.channel
        await show_history(channel)
        return SetOutput(channel)
