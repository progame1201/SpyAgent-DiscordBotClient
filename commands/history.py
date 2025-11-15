from .command import Command
from utils import show_history


class History(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <channel id> - Get the history of the channel you are on. Or from channel by id."

    async def execute(self, *args):
        if args[0]:
            try:
                channel = await self.client.fetch_channel(args[0][0])
            except:
                channel = self.channel
        else:
            channel = self.channel
        await show_history(channel)