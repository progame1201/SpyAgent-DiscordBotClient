from .command import Command
from .commandoutput import CommandOutput
from utils import SelectUtils
from log import log


class VcConnectOutput(CommandOutput):
    def __init__(self, vc_client):
        super().__init__()
        self.vc_client = vc_client


class VcConnect(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} - connect to voice channel"

    async def execute(self, *args):
        channel = await self.select_utils.select_vc_channel(self.guild)
        if not channel:
            log("You entered incorrect channel index. the command will not continue execution.")
            return
        vc_client = await channel.connect()
        log("Connected")
        return VcConnectOutput(vc_client)
