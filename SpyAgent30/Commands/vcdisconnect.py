from disnake import *
from .command import command
from .command_output import command_output
from utils import show_history, Select_utils, try_async_int_input
from Log import log


class vcdisconnect_output(command_output):
    def __init__(self, vc_client):
        super().__init__()
        self.vc_client = vc_client

class vcdisconnect(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
        self.vc_clients:list[VoiceClient] | None = None
        self.description = f"{self.name} - disconnect from voice channel"

    async def execute(self, *args):
        for i, vc_client in enumerate(self.vc_clients):
            log(f"{i} - {vc_client.channel} {[member.name for member in vc_client.channel.members]}")
        index = await try_async_int_input()
        if index is None:
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
        return vcdisconnect_output(vc_client)
