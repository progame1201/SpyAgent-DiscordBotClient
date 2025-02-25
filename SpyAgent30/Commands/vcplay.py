from disnake import *
from .command import command
import os
from .command_output import command_output
from utils import show_history, Select_utils, try_async_int_input
from Log import log, error
from tkinter.filedialog import askopenfilename



class vcplay(command):
    def __init__(self, guild: Guild, channel: TextChannel, client: Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
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
        index = await try_async_int_input()
        if index is None:
            log("You entered incorrect message index. the command will not continue execution.")
        if len(self.vc_clients) - 1 > index or index < 0:
            log("You entered incorrect message index. the command will not continue execution.")

        vc_client = self.vc_clients[index]

        path = askopenfilename(title="select file")
        if not path:
            return

        source = FFmpegPCMAudio(path)
        vc_client.play(source, after=self.after_playing)
        log(f"Started playing {os.path.basename(path)}")