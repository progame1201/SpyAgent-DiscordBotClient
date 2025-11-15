from .command import Command
from .commandoutput import CommandOutput
from utils import log, SelectUtils, MuteUtils, ChannelMute, GuildMute


class MuteOutput(CommandOutput):
    def __init__(self, mute_object):
        super().__init__()
        self.mute_object = mute_object


class Mute(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <guild aliases:[\"g\", \"2\", \"guild\"]; channel aliases: [\"ch\", \"c\", \"1\", \"channel\"]> - select a channel or guild for mute"
        self.guild_mutes = []
        self.channel_mutes = []
        self.select_utils = SelectUtils(self.client)

    async def execute(self, *args):
        if not args[0]:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return
        args = args[0]

        if args[0] in ["ch", "c", "1", "channel"]:
            channel = await self.select_utils.select_channel(self.guild, True, to_skip=self.channel_mutes,
                                                             show_threads=False)
            if not channel:
                log("You entered incorrect chanel index. the command will not continue execution.")
                return
            mute_obj = ChannelMute(channel.id)
            MuteUtils.add_mute(mute_obj)
            log(f"muted {channel.name}")
            return MuteOutput(mute_obj)
        elif args[0] in ["g", "2", "guild"]:
            guild = await self.select_utils.select_guild(True, to_skip=self.guild_mutes)
            if not guild:
                log("You entered incorrect guild index. the command will not continue execution.")
                return
            mute_obj = GuildMute(guild.id)
            MuteUtils.add_mute(mute_obj)
            log(f"muted {guild.name}")
            return MuteOutput(mute_obj)
        else:
            log("You entered incorrect mute mode. the command will not continue execution.")
            return
