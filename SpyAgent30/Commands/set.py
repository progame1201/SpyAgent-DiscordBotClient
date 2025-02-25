from disnake import *
from .command import command
from .command_output import command_output
from utils import show_history, Select_utils


class set_output(command_output):
    def __init__(self, channel: TextChannel):
        super().__init__()
        self.channel = channel

class set(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
        self.description = f"{self.name} <channel id> - set the channel by id."
    async def execute(self, *args):
        try:
            channel = await self.client.fetch_channel(args[0][0])
        except:
            channel = self.channel
        await show_history(channel)
        return set_output(channel)