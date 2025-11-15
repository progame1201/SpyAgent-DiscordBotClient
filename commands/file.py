from disnake import *
from .command import Command
from utils import SelectUtils
from tkinter.filedialog import askopenfilename


class File(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} <message> - send file with message"

    async def execute(self, *args):
        path = askopenfilename(title="select file")
        if not path:
            return
        await self.channel.send(content=" ".join(args[0]), file=File(path))
