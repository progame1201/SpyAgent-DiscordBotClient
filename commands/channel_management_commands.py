from disnake import TextChannel, Guild
from aioconsole import ainput
from colorama import Fore

from .command import Command
from .command_output import CommandOutput
from utils import show_history, SelectUtils
from mutes import MuteUtils, ChannelMute, GuildMute
from log import log


class MuteOutput(CommandOutput):
    def __init__(self, mute_object):
        super().__init__()
        self.mute_object = mute_object

class Mute(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <guild aliases:`[\"g\", \"2\", \"guild\"]`; channel aliases: `[\"ch\", \"c\", \"1\", \"channel\"]`> - select a channel or guild to mute"
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

class ResetOutput(CommandOutput):
    def __init__(self, guild: Guild, channel: TextChannel):
        super().__init__()
        self.guild = guild
        self.channel = channel

class Reset(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} - change the channel and guild"

    async def execute(self, *args):
        guild = await self.select_utils.select_guild(stop_if_error=True)
        if guild is None:
            log("You entered incorrect guild index. the command will not continue execution.")
            return
        channel = await self.select_utils.select_channel(guild, stop_if_error=True)
        if channel is None:
            log("You entered incorrect channel index. the command will not continue execution.")
        await show_history(channel)
        return ResetOutput(guild, channel)

class SetOutput(CommandOutput):
    def __init__(self, channel: TextChannel):
        super().__init__()
        self.channel = channel

class Set(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} <channel id> - set the channel by ID"

    async def execute(self, *args):
        try:
            channel = await self.client.fetch_channel(int(args[0][0]))
        except:
            log("You entered incorrect channel index. the command will not continue execution.")
            return
        await show_history(channel)
        return SetOutput(channel)

class GuildLeaveOutput(CommandOutput):
    def __init__(self, guild: Guild, channel: TextChannel):
        super().__init__()
        self.guild = guild
        self.channel = channel

class GuildLeave(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} - choose a guild to leave"

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
