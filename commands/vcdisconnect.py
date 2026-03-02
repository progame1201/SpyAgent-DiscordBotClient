from disnake import *
from .command import Command
from .commandoutput import CommandOutput
from utils import SelectUtils, async_int_input, is_valid_index
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
        index = await async_int_input()
        if not is_valid_index(index, self.vc_clients):
            return

        vc_client = self.vc_clients[index]

        if vc_client.is_playing():
            vc_client.stop()
        await vc_client.disconnect()
        log("Disconnected")
        return VcDisconnectOutput(vc_client)
