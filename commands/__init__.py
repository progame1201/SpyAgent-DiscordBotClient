from .command import Command
from .commandoutput import CommandOutput
from .basic_commands import Delete, Edit, File, History, Reply, Reaction
from .channel_management_commands import (
    ResetOutput,
    Reset,
    Set,
    SetOutput,
    MuteOutput,
    Mute,
    Unmute,
    UnmuteOutput,
    GuildLeaveOutput,
    GuildLeave,
)
from .vc_commands import (
    VcPlay,
    VcDisconnectOutput,
    VcDisconnect,
    VcConnectOutput,
    VcConnect,
    VcStop,
)


def get_commands(guild, channel, client):
    commands = [
        Reset,
        Set,
        File,
        History,
        Reply,
        Delete,
        Mute,
        Unmute,
        Edit,
        Reaction,
        GuildLeave,
        VcDisconnect,
        VcConnect,
        VcPlay,
        VcStop
    ]
    return [command(guild, channel, client) for command in commands]