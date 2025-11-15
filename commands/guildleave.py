from disnake import *
from .command import Command
from .commandoutput import CommandOutput
from utils import show_history, SelectUtils
from aioconsole import ainput
from log import log
from colorama import Fore


class GuildLeaveOutput(CommandOutput):
    def __init__(self, guild: Guild, channel: TextChannel):
        super().__init__()
        self.guild = guild
        self.channel = channel


class GuildLeave(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} - choose a guild to exit it"

    async def execute(self, *args):
        log(f"{Fore.WHITE}select the guild you want to leave")
        guild = await self.select_utils.select_guild(stop_if_error=True)
        if not guild:
            log("You entered incorrect guild index. the command will not continue execution.")
            return
        log(f"{Fore.WHITE}Are you sure about this? You will not be able to return to the guild on your own")
        log(f"{Fore.WHITE}Write the name of the guild to leave it ({guild.name})")
        name = await ainput("name: ")
        if name == guild.name:
            await guild.leave()
        else:
            log(f"{Fore.WHITE}You entered name incorrect")
            return
        # if guild.id == self.guild.id:
        #     guild = await self.select_utils.select_guild()
        #     channel = await self.select_utils.select_channel(guild)
        #     await show_history(channel)
        #     return GuildLeaveOutput(guild, channel)
