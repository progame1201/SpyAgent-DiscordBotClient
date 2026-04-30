import os
from disnake import VoiceClient, FFmpegPCMAudio
from tkinter.filedialog import askopenfilename

from .command import Command
from .command_output import CommandOutput
from utils import SelectUtils, async_int_input, is_valid_index
import log as log_module
from log import log


class VcConnectOutput(CommandOutput):
    def __init__(self, vc_client):
        super().__init__()
        self.vc_client = vc_client

class VcConnect(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} - connect to a voice channel"

    async def execute(self, *args):
        channel = await self.select_utils.select_channel(self.guild, channel_type="vc")
        if not channel:
            log("You entered incorrect channel index. the command will not continue execution.")
            return
        vc_client = await channel.connect()
        log("Connected")
        return VcConnectOutput(vc_client)

class VcDisconnectOutput(CommandOutput):
    def __init__(self, vc_client):
        super().__init__()
        self.vc_client = vc_client

class VcDisconnect(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.vc_clients: list[VoiceClient] | None = None
        self.description = f"{self.name} - disconnect from a voice channel"

    async def execute(self, *args):
        if not self.vc_clients:
            log("You're not in a voice channel.")
            return

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

class VcPlay(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.vc_clients: list[VoiceClient] | None = None
        self.description = f"{self.name} - choose and play any file"

    def after_playing(self, error):
        if error:
            log_module.error(f"an error occurred while playing audio: {error}")
        else:
            log_module.log("Audio has finished playing")

    async def execute(self, *args):
        if not self.vc_clients:
            log("You're not in a voice channel.")
            return
        for i, vc_client in enumerate(self.vc_clients):
            log_module.log(f"{i} - {vc_client.channel} {[member.name for member in vc_client.channel.members]}")
        index = await async_int_input()
        if not is_valid_index(index, self.vc_clients):
            return

        vc_client = self.vc_clients[index]

        path = await self.client.loop.run_in_executor(None, askopenfilename)
        log_module.log(path)
        if not path:
            return

        source = FFmpegPCMAudio(path)
        vc_client.play(source, after=self.after_playing)
        log_module.log(f"Started playing {os.path.basename(path)}")

class VcStop(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.vc_clients: list[VoiceClient] | None = None
        self.description = f"{self.name} - stop playing a file"

    async def execute(self, *args):
        if not self.vc_clients:
            log("You're not in a voice channel.")
            return
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