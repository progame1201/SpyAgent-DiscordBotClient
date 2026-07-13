import os
import pickle


class GuildMute:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, GuildMute) and self.id == other.id

    def __hash__(self):
        return hash((GuildMute, self.id))

class ChannelMute:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, ChannelMute) and self.id == other.id

    def __hash__(self):
        return hash((ChannelMute, self.id))

class MutePare:
    def __init__(self, guilds_list, channels_list):
        self.guilds = guilds_list
        self.channels = channels_list

class MuteUtils:
    def __init__(self):
        pass

    @staticmethod
    def _read_mutes():
        if not os.path.exists("mutes") or os.path.getsize("mutes") <= 0:
            return []
        with open("mutes", 'rb') as f:
            mutes: list = pickle.loads(f.read())
        if not mutes:
            return []
        return mutes

    @staticmethod
    def add_mute(mute_object):
        mutes = MuteUtils._read_mutes()
        mutes.append(mute_object)
        with open("mutes", 'wb') as f:
            f.write(pickle.dumps(mutes))

    @staticmethod
    def remove_mute(mute_object):
        try:
            mutes = MuteUtils._read_mutes()
            mutes.remove(mute_object)
        except:
            return
        with open("mutes", 'wb') as f:
            f.write(pickle.dumps(mutes))

    @staticmethod
    def remove_mute_by_id(id):
        try:
            mutes = MuteUtils._read_mutes()
            mutes = [m for m in mutes if m.id != id]
        except:
            return
        with open("mutes", 'wb') as f:
            f.write(pickle.dumps(mutes))

    @staticmethod
    def get_mutes():
        mutes = MuteUtils._read_mutes()
        guild_mutes = []
        channel_mutes = []
        for mute in mutes:
            if isinstance(mute, ChannelMute):
                channel_mutes.append(mute)
            if isinstance(mute, GuildMute):
                guild_mutes.append(mute)
        return MutePare(guild_mutes, channel_mutes)