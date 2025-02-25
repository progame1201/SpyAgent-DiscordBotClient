from disnake import *
from .command import command
from .command_output import command_output
from utils import show_history, Select_utils
from Log import log


class vcconnect_output(command_output):
    def __init__(self, vc_client):
        super().__init__()
        self.vc_client = vc_client

class vcconnect(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
        self.description = f"{self.name} - connect to voice channel"

    async def execute(self, *args):
        channel = await self.select_utils.select_vc_channel(self.guild)
        if not channel:
            log("You entered incorrect channel index. the command will not continue execution.")
            return
        vc_client = await channel.connect()
        log("Connected")
        return vcconnect_output(vc_client)
