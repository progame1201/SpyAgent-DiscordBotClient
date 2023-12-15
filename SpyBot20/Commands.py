from disnake import *
from loguru import logger
import asyncio
import pickle
import os
import pytz
from asyncio import sleep
import config
from tkinter import filedialog
from colorama import Fore, init

class Commands:
    '''All commands of SpyAgent 2.1.0+
    '''
    def __init__(self, client=None, guild=None, channel=None):
        self.client = client
        self.channel:TextChannel = channel
        self.guild = guild
        init(autoreset=True)
    def getmutes(self):
        if os.path.exists("channelmutes"):
            if os.path.getsize("channelmutes") > 0:
                data = open("channelmutes", 'rb').read()
                channels_mute_list = pickle.loads(data)
            else:
                channels_mute_list = []
        else:
            open("channelmutes", 'wb').close()
            channels_mute_list = []

        if os.path.exists("guildmutes"):
            if os.path.getsize("guildmutes") > 0:
                data = open("guildmutes", 'rb').read()
                guild_mute_list = pickle.loads(data)
            else:
                guild_mute_list = []
        else:
            open("guildmutes", 'wb').close()
            guild_mute_list = []
        return [channels_mute_list, guild_mute_list]
    async def async_input(self, prompt):
        return await asyncio.to_thread(input, prompt)

    async def get_history(self):
        messages = []
        async for message in self.channel.history(limit=config.history_size, oldest_first=False):
            messages.append(message)
        print("Channel history:\n#####################")
        messages.reverse()
        for message in messages:
            date = message.created_at
            rounded_date = date.replace(second=0, microsecond=0)
            rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
            attachment_list = []
            if message.attachments:
                for attachment in message.attachments:
                    attachment_list.append(attachment.url)
                print(
                    f"{message.channel}: {rounded_date_string} {message.author}: {message.content}, attachments: {attachment_list}")
            else:
                print(f"{message.channel}: {rounded_date_string} {message.author}: {message.content}")
        print("#####################")

    async def mutechannel(self):
        channellistformute = []
        channels_mute_list = self.getmutes()[0]
        for i, mchannel in enumerate(self.guild.text_channels):
            if mchannel.id in channels_mute_list:
                channellistformute.append(mchannel.id)
                continue
            channellistformute.append(mchannel.id)
            print(f"{i}: {mchannel.name}")
        mutechanelname = await self.async_input("type chanel index: ")
        try:
            mchannel = self.client.get_channel(channellistformute[int(mutechanelname)])
            channels_mute_list.append(channellistformute[int(mutechanelname)])
            with open('channelmutes', 'wb') as f:
                towrite = pickle.dumps(channels_mute_list)
                f.write(towrite)
            logger.success(f"Channel '{mchannel.name}' muted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def unmutechannel(self):
        channellistforunmute = []
        channels_mute_list = self.getmutes()[0]
        for i in range(len(channels_mute_list)):
            unmutech = self.client.get_channel(channels_mute_list[i])
            channellistforunmute.append(channels_mute_list[i])
            print(f"{i}: {unmutech}")
        unmutechanelname = await self.async_input("type chanel index: ")
        try:
            mchannel = self.client.get_channel(channellistforunmute[int(unmutechanelname)])
            channels_mute_list.remove(channellistforunmute[int(unmutechanelname)])
            with open('channelmutes', 'wb') as f:
                towrite = pickle.dumps(channels_mute_list)
                f.write(towrite)
            logger.success(f"Channel '{mchannel.name}' unmuted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def delete(self):
        messages = []
        yourmessages: dict[int:Message] = {}
        async for message in self.channel.history(limit=config.history_size, oldest_first=False):
            messages.append(message)
        messages.reverse()
        i = 0
        for message in messages:
            if message.author.id == self.client.user.id:
                yourmessages[i] = message
                date = message.created_at
                rounded_date = date.replace(second=0, microsecond=0)
                rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")
                i += 1
        data = await self.async_input("message index:")
        if data == "" or data == None:
            return
        todelmsg = yourmessages.get(int(data))
        await todelmsg.delete()
        logger.success(f"Message: '{todelmsg.content}' deleted")
    async def reset(self):
        print("Choose a guild:")
        for i, guild in enumerate(self.client.guilds):
            print(f"{i}: {guild.name}")
        data = await self.async_input("server index:")
        if data == "" or data == None:
            return
        guild:Guild = self.client.guilds[int(data)]
        logger.success(f"guild assigned! guild name: {guild.name}, guild owner: {guild.owner}, guild id: {guild.id} guild icon url: {guild.icon.url}")
        await sleep(1)
        print("Choose a channel:")
        channels: dict[int, dict[str:int]] = {}
        for i, channel in enumerate(guild.text_channels):
            channels.update({i: {channel.name: channel.id}})
            print(f"{i}: {channel.name}")
        data = await self.async_input("server index:")
        if data == "" or data == None:
            return
        channel = self.client.get_channel(list(channels.get(int(data)).values())[0])
        logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
        await self.get_history()
        self.channel = channel
        self.guild = guild
        return {"channel":channel,"guild":guild}
    async def resetchannel(self):
        print("Choose a channel:")
        channels: dict[int, dict[str:int]] = {}
        for i, channel in enumerate(self.guild.text_channels):
            channels.update({i: {channel.name: channel.id}})
            print(f"{i}: {channel.name}")
        data = await self.async_input("channel index:")
        if data == "" or data == None:
            return
        channel = self.client.get_channel(list(channels.get(int(data)).values())[0])
        logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
        await self.get_history()
        self.channel = channel
        return {"channel":channel}
    async def file(self):
        try:
            file = filedialog.askopenfilename()
            await self.channel.send(file=File(file))
        except Exception as e:
            print(f"error sending file\n{e}")
    async def status(self):
        print("status list:\nonline\noffline\nidle")
        status = input("status:")
        if status == "online":
            await self.client.change_presence(status=Status.online)
        if status == "offline":
            await self.client.change_presence(status=Status.offline)
        if status == "idle":
            await self.client.change_presence(status=Status.idle)
        if status == "online" or status == "offline" or status == "idle":
            logger.success(f"status changed to {status}")
    async def guildmute(self):
        guildlistformute = []
        guild_mute_list = self.getmutes()[1]
        for i, mguild in enumerate(self.client.guilds):
            if mguild.id in guild_mute_list:
                guildlistformute.append(mguild.id)
                continue
            guildlistformute.append(mguild.id)
            print(f"{i}: {mguild.name}")
        muteguildname = await self.async_input("type guild index: ")
        try:
            mguild = self.client.get_guild(guildlistformute[int(muteguildname)])
            guild_mute_list.append(mguild.id)
            with open('guildmutes', 'wb') as f:
                towrite = pickle.dumps(guild_mute_list)
                f.write(towrite)
            logger.success(f"Guild '{mguild.name}' muted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def unmuteguild(self):
        guildlistforunmute = []
        guild_mute_list = self.getmutes()[1]
        for i in range(len(guild_mute_list)):
            unmuteg = self.client.get_guild(guild_mute_list[i])
            guildlistforunmute.append(guild_mute_list[i])
            print(f"{i}: {unmuteg}")
        unmutechanelname = await self.async_input("type guild index: ")
        try:
            mguild = self.client.get_guild(guildlistforunmute[int(unmutechanelname)])
            guild_mute_list.remove(mguild.id)
            with open('guildmutes', 'wb') as f:
                towrite = pickle.dumps(guild_mute_list)
                f.write(towrite)
            logger.success(f"Guild '{mguild.name}' unmuted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def reaction(self):
        print("1 - emoji list")
        print("2 - type emoji")
        emojiinput = input("type number:")
        if emojiinput == "1":
            emojilist = []
            for i, emoji in enumerate(self.client.guilds[0].emojis):
                emojilist.append(emoji)
                print(f'{i}: {emoji.name} - {emoji}')
            reactemoji = input("type emoji index: ")
            try:
                emoji = emojilist[int(reactemoji)]
            except:
                return
            print("1 - message id")
            print("2 - message list")
            messageinput = await self.async_input("type number:")
            if messageinput == "2":
                messages = []
                async for message in self.channel.history(limit=50, oldest_first=False):
                    messages.append(message)
                messages.reverse()
                for i, message in enumerate(messages):
                    print(f"{i}: {message.author}: {message.content}")
                messageindex = await self.async_input("message index:")
                message = messages[int(messageindex)]
                await message.add_reaction(emoji)
                logger.success(f"message reacted. Emoji: {emoji}")
            if messageinput == "1":
                messageid = int(await self.async_input("message id: "))
                message = await self.channel.fetch_message(int(messageid))
                await message.add_reaction(emoji)
                logger.success(f"message reacted. Emoji: {emoji}")
        if emojiinput == "2":
            emoji = await self.async_input("emoji: ")
            print("1 - message id")
            print("2 - message list")
            messageinput = await self.async_input("type number:")
            if messageinput == "2":
                messages = []
                async for message in self.channel.history(limit=50, oldest_first=False):
                    messages.append(message)
                messages.reverse()
                for i, message in enumerate(messages):
                    print(f"{i}: {message.author}: {message.content}")
                messageindex = await self.async_input("message index:")
                message = messages[int(messageindex)]
                await message.add_reaction(emoji)
                logger.success(f"message reacted. Emoji: {emoji}")
            if messageinput == "1":
             messageid = int(await self.async_input("message id: ") )
             message = await self.channel.fetch_message(int(messageid))
             await message.add_reaction(emoji)
             logger.success(f"message reacted. Emoji: {emoji}")
    async def privatemsg(self):
        usrid = int(await self.async_input("user id:"))
        if usrid < 0:
            return
        user:User = self.client.get_user(usrid)
        msg = await self.async_input(f"{Fore.LIGHTBLACK_EX}Message to {user.name}:")
        await user.send(msg)
    async def pmreset(self):
        usrid = int(await self.async_input("user id:"))
        user: User = self.client.get_user(usrid)
        self.channel = user
        return {"channel":user}
    async def edit(self):
        messages = []
        yourmessages: dict[int:Message] = {}
        async for message in self.channel.history(limit=config.history_size, oldest_first=False):
            messages.append(message)
        messages.reverse()
        i = 0
        for message in messages:
            if message.author.id == self.client.user.id:
                yourmessages[i] = message
                date = message.created_at
                rounded_date = date.replace(second=0, microsecond=0)
                rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")
                i += 1
        data = await self.async_input("message index:")
        if data == "" or data == None:
            return
        edmsg:Message = yourmessages.get(int(data))
        oldcont = edmsg.content
        data = await self.async_input("new message:")
        await edmsg.edit(content=data)
        logger.success(f"Message: {oldcont} | edited to: {data}")

