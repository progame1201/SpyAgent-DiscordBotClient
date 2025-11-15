from .command import Command
from .commandoutput import CommandOutput
from utils import log, SelectUtils, MuteUtils, ChannelMute, GuildMute


class UnmuteOutput(CommandOutput):
    def __init__(self, mute_object):
        super().__init__()
        self.mute_object = mute_object


class Unmute(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <guild aliases:`[\"g\", \"2\", \"guild\"]`; channel aliases: `[\"ch\", \"c\", \"1\", \"channel\"]`> - remove the channel or guild from mute"
        self.guild_mutes = []
        self.channel_mutes = []
        self.select_utils = SelectUtils(self.client)

    async def execute(self, *args):
        if not args[0]:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return
        args = args[0]
        if args[0] in ["ch", "c", "1", "channel"]:
            channel = await self.select_utils.select_channel(self.guild, True,
                                                             to_skip=[channel.id for channel in self.guild.text_channels
                                                                      if channel.id not in self.channel_mutes],
                                                             show_threads=False)
            if not channel:
                log("You entered incorrect chanel index. the command will not continue execution.")
                return
            MuteUtils.remove_mute_by_id(channel.id)
            log(f"unmuted {channel.name}")
            return UnmuteOutput(ChannelMute(channel.id))
        elif args[0] in ["g", "2", "guild"]:
            guild = await self.select_utils.select_guild(True, to_skip=[guild.id for guild in self.client.guilds if
                                                                        guild.id not in self.guild_mutes])
            if not guild:
                log("You entered incorrect guild index. the command will not continue execution.")
                return
            MuteUtils.remove_mute_by_id(guild.id)
            log(f"unmuted {guild.name}")
            return UnmuteOutput(GuildMute(guild.id))
        else:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return
