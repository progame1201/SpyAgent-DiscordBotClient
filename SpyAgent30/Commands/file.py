from disnake import *
from .command import command
from Log import log
from utils import Select_utils
from tkinter.filedialog import askopenfilename


class file(command):
    def __init__(self, guild: Guild, channel: TextChannel, client: Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
        self.description = f"{self.name} <message> - send file with message"

    async def execute(self, *args):
        path = askopenfilename(title="select file")
        if not path:
            return
        await self.channel.send(content=" ".join(args[0]), file=File(path))
