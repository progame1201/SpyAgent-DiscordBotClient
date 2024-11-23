from .command import command
from .reset import reset_output, reset
from .set import set, set_output
from .command_output import command_output
from .file import file
from .history import history
from .reply import reply
from .delete import delete
from .mute import mute_output, mute
from .unmute import unmute, unmute_output
from .edit import edit
from .reaction import reaction
from .guildleave import guildleave_output, guildleave

def get_commands(guild, channel, client):
    return [
        reset(guild, channel, client),
        set(guild, channel, client),
        file(guild, channel, client),
        history(guild, channel, client),
        reply(guild, channel, client),
        delete(guild, channel, client),
        mute(guild, channel, client),
        unmute(guild, channel, client),
        edit(guild, channel, client),
        reaction(guild, channel, client),
        guildleave(guild, channel, client),
    ]