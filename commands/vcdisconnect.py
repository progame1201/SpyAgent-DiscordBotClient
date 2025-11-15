from disnake import *
from .command import Command
from .commandoutput import CommandOutput
from utils import SelectUtils, try_async_int_input
from log import log


class VcDisconnectOutput(CommandOutput):
    def __init__(self, vc_client):
        super().__init__()
        self.vc_client = vc_client


class VcDisconnect(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.vc_clients: list[VoiceClient] | None = None
        self.description = f"{self.name} - disconnect from voice channel"

    async def execute(self, *args):
        for i, vc_client in enumerate(self.vc_clients):
            log(f"{i} - {vc_client.channel} {[member.name for member in vc_client.channel.members]}")
        index = await try_async_int_input()
        if index is False:
            log("You entered incorrect message index. the command will not continue execution.")
            return
        if len(self.vc_clients) - 1 > index or index < 0:
            log("You entered incorrect message index. the command will not continue execution.")
            return

        vc_client = self.vc_clients[index]

        if vc_client.is_playing():
            vc_client.stop()
        await vc_client.disconnect()
        log("Disconnected")
        return VcDisconnectOutput(vc_client)
