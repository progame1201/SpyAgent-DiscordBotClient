from disnake import *
from .command import command
from .command_output import command_output
from utils import show_history, Select_utils
from aioconsole import ainput
from Log import log
from colorama import Fore

class guildleave_output(command_output):
    def __init__(self, guild: Guild, channel: TextChannel):
        super().__init__()
        self.guild = guild
        self.channel = channel

class guildleave(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.select_utils = Select_utils(client)
        self.description = "guildleave - choose a guild to exit it"

    async def execute(self, *args):
        log(f"{Fore.WHITE}select the guild you want to leave")
        guild = await self.select_utils.select_guild()
        log(f"{Fore.WHITE}Are you sure about this? You will not be able to return to the guild on your own")
        log(f"{Fore.WHITE}Write the name of the guild to leave it ({guild.name})")
        name = await ainput("name: ")
        if name == guild.name:
            await guild.leave()
        else:
            log(f"{Fore.WHITE}You entered name incorrect")
            return
        if guild.id == self.guild.id:
            guild = await self.select_utils.select_guild()
            channel = await self.select_utils.select_channel(guild)
            await show_history(channel)
            return guildleave_output(guild, channel)
