from disnake import *
from .command import command
from .command_output import command_output
from utils import log, Select_utils, mute_utils, channel_mute, guild_mute


class mute_output(command_output):
    def __init__(self, mute_object):
        super().__init__()
        self.mute_object = mute_object

class mute(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.description = "mute <guild aliases:[\"g\", \"2\", \"guild\"]; channel aliases: [\"ch\", \"c\", \"1\", \"channel\"]> - select a channel or guild for mute"
        self.guild_mutes = []
        self.channel_mutes = []
        self.select_utils = Select_utils(client)

    async def execute(self, *args):
        if not args[0]:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return
        if args[0][0] in ["ch", "c", "1", "channel"]:
            channel = await self.select_utils.select_channel(self.guild, True, to_skip=self.channel_mutes, show_threads=False)
            if not channel:
                log("You entered incorrect chanel index. the command will not continue execution.")
                return
            mute_obj = channel_mute(channel.id)
            mute_utils.add_mute(mute_obj)
            log(f"muted {channel.name}")
            return mute_output(mute_obj)
        elif args[0][0] in ["g", "2", "guild"]:
            guild = await self.select_utils.select_guild(True, to_skip=self.guild_mutes)
            if not guild:
                log("You entered incorrect guild index. the command will not continue execution.")
                return
            mute_obj = guild_mute(guild.id)
            mute_utils.add_mute(mute_obj)
            log(f"muted {guild.name}")
            return mute_output(mute_obj)
        else:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return