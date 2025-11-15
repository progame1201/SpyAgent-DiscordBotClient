from disnake import *


class Command:
    def __init__(self, guild: Guild | None, channel: TextChannel | None, client: Client):
        self.name = self.__class__.__name__.lower()
        self.description = "Command"
        self.guild: Guild | None = guild
        self.channel: TextChannel | None = channel
        self.client: Client = client

    async def execute(self, *args):
        raise NotImplementedError("execute")
