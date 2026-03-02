from disnake import *
from .command import Command
from utils import SelectUtils, async_int_input, is_valid_index
from log import log


class VcStop(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.vc_clients: list[VoiceClient] | None = None
        self.description = f"{self.name} - stop playing file"

    async def execute(self, *args):
        for i, vc_client in enumerate(self.vc_clients):
            log(f"{i} - {vc_client.channel} {[member.name for member in vc_client.channel.members]}")
        index = await async_int_input()
        if not is_valid_index(index, self.vc_clients):
            return

        vc_client = self.vc_clients[index]

        if vc_client.is_playing():
            vc_client.stop()
        vc_client.stop()
        log("Stopped playing")
