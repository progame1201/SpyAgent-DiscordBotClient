from .command import Command
from .reset import ResetOutput, Reset
from .set import Set, SetOutput
from .commandoutput import CommandOutput
from .file import File
from .history import History
from .reply import Reply
from .delete import Delete
from .mute import MuteOutput, Mute
from .unmute import Unmute, UnmuteOutput
from .edit import Edit
from .reaction import Reaction
from .guildleave import GuildLeaveOutput, GuildLeave
from .vcplay import VcPlay
from .vcdisconnect import VcDisconnectOutput, VcDisconnect
from .vcconnect import VcConnectOutput, VcConnect
from .vcstop import VcStop


def get_commands(guild, channel, client):
    return [
        Reset(guild, channel, client),
        Set(guild, channel, client),
        File(guild, channel, client),
        History(guild, channel, client),
        Reply(guild, channel, client),
        Delete(guild, channel, client),
        Mute(guild, channel, client),
        Unmute(guild, channel, client),
        Edit(guild, channel, client),
        Reaction(guild, channel, client),
        GuildLeave(guild, channel, client),
        VcDisconnect(guild, channel, client),
        VcConnect(guild, channel, client),
        VcPlay(guild, channel, client),
        VcStop(guild, channel, client),
    ]