from disnake import *
from .command import command
from .command_output import command_output
from utils import log, Select_utils, mute_utils, channel_mute, guild_mute


class unmute_output(command_output):
    def __init__(self, mute_object):
        super().__init__()
        self.mute_object = mute_object

class unmute(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.description = f"{self.name} <guild aliases:`[\"g\", \"2\", \"guild\"]`; channel aliases: `[\"ch\", \"c\", \"1\", \"channel\"]`> - remove the channel or guild from mute"
        self.guild_mutes = []
        self.channel_mutes = []
        self.select_utils = Select_utils(client)

    async def execute(self, *args):
        if not args[0]:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return
        args = args[0]
        if args[0] in ["ch", "c", "1", "channel"]:
            channel = await self.select_utils.select_channel(self.guild, True, to_skip=[channel.id for channel in self.guild.text_channels if channel.id not in self.channel_mutes], show_threads=False)
            if not channel:
                log("You entered incorrect chanel index. the command will not continue execution.")
                return
            mute_utils.remove_mute_by_id(channel.id)
            log(f"unmuted {channel.name}")
            return unmute_output(channel_mute(channel.id))
        elif args[0] in ["g", "2", "guild"]:
            guild = await self.select_utils.select_guild(True, to_skip=[guild.id for guild in self.client.guilds if guild.id not in self.guild_mutes])
            if not guild:
                log("You entered incorrect guild index. the command will not continue execution.")
                return
            mute_utils.remove_mute_by_id(guild.id)
            log(f"unmuted {guild.name}")
            return unmute_output(guild_mute(guild.id))
        else:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return