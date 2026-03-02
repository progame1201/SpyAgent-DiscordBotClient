from disnake import *
from .command import Command
import os
from utils import SelectUtils, async_int_input, is_valid_index
from log import log
from tkinter.filedialog import askopenfilename


class VcPlay(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.vc_clients: list[VoiceClient] | None = None
        self.description = f"{self.name} - choose and play any file"

    def after_playing(self, error):
        if error:
            error(f"an error occurred while playing audio: {error}")
        else:
            log("Audio has finished playing")

    async def execute(self, *args):
        for i, vc_client in enumerate(self.vc_clients):
            log(f"{i} - {vc_client.channel} {[member.name for member in vc_client.channel.members]}")
        index = await async_int_input()
        if not is_valid_index(index, self.vc_clients):
            return

        vc_client = self.vc_clients[index]

        path = await self.client.loop.run_in_executor(None, askopenfilename)
        log(path)
        if not path:
            return

        source = FFmpegPCMAudio(path)
        vc_client.play(source, after=self.after_playing)
        log(f"Started playing {os.path.basename(path)}")
