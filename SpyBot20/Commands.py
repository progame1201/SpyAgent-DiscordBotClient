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
import pyttsx3

class Commands:
    '''All commands of SpyAgent 2.9.0+
       most of the commands were taken from version 1.0.0-2.0.0, which is why their code maybe bad.
    '''
    def __init__(self, client=None, guild=None, channel=None):
        self.client:Client = client
        self.channel:TextChannel = channel
        self.guild = guild
        self.vcchlients:list[VoiceClient] = []
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
    async def raw_history(self):
        messages = []
        try:
            async for message in self.channel.history(limit=config.history_size, oldest_first=False):
                messages.append(message)
        except Forbidden:
            print(f"{Fore.RED}It's impossible to get: Forbidden.")
            return False
        messages.reverse()
        return messages
    async def get_history(self):
        messages = await self.raw_history()
        if messages == False:
            return
        print("Channel history:\n#####################")
        for message in messages:
            rounded_date_string = message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
            attachment_list = []
            reactions_list = []
            msg = f"{message.channel}: {rounded_date_string} {message.author}: {message.content}"
            if message.attachments:
                for attachment in message.attachments:
                    attachment_list.append(attachment.url)
                msg += f" | attachments: {attachment_list}"

            if message.reactions:
                for reaction in message.reactions:
                    reactions_list.append(reaction.emoji)
                msg += f" | reactions: {reactions_list}"
            if config.allow_reference_display:
                if message.reference and message.reference.message_id:
                    reference = await message.channel.fetch_message(message.reference.message_id)
                    msg += f" | reference: reply: {reference.author.name}: {reference.content}"
            print(msg)

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
            channels_mute_list.append(mchannel.id)
            with open('channelmutes', 'wb') as f:
                f.write(pickle.dumps(channels_mute_list))
            logger.success(f"Channel '{mchannel.name}' muted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def unmutechannel(self):
        channellistforunmute = []
        channels_mute_list = self.getmutes()[0]
        for i in range(len(channels_mute_list)):
            unmutech = self.client.get_channel(channels_mute_list[i])
            channellistforunmute.append(unmutech.id)
            print(f"{i}: {unmutech.name}")
        unmutechanelname = await self.async_input("type chanel index: ")
        try:
            mchannel = self.client.get_channel(channellistforunmute[int(unmutechanelname)])
            channels_mute_list.remove(mchannel.id)
            with open('channelmutes', 'wb') as f:
                f.write(pickle.dumps(channels_mute_list))
            logger.success(f"Channel '{mchannel.name}' unmuted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def delete(self):
        messages = await self.raw_history()
        if messages == False:
            return
        yourmessages: dict[int:Message] = {}

        for i, message in enumerate(messages):
            if message.author.id == self.client.user.id:
                yourmessages[i] = message
                rounded_date_string = message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")
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
        self.channel = channel
        self.guild = guild
        await self.get_history()
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
        self.channel = channel
        await self.get_history()
        return {"channel":channel}
    async def into(self):
        id = await self.async_input("channel id:")
        channel = self.client.get_channel(int(id))
        await channel.send(await self.async_input("message:"))

    async def file(self):
        try:
            file = filedialog.askopenfilename()
            await self.channel.send(file=File(file))
        except Exception as e:
            print(f"error sending file\n{e}")
    async def status(self):
        statuses:dict = {"online":Status.online,"offline":Status.offline, "idle":Status.idle}
        print("statuses:")
        for key in statuses.keys():
            print(key)
        status = input("status:")
        if status.lower() in statuses.keys():
            await self.client.change_presence(status=statuses[status])
            logger.success(f"status changed to {status}")
    async def activity(self):
        print("activities list: game\nstreaming\nlistening\nwatching")
        activity = await self.async_input("activity:")
        name = await self.async_input("activity name:")
        await self.client.change_presence(activity=None)
        if activity.lower() == "game":
            await self.client.change_presence(activity=Game(name=name))
        if activity.lower() == "streaming":
            await self.client.change_presence(activity=Streaming(name=name, url=await self.async_input("url:")))
        if activity.lower() == "listening":
            await self.client.change_presence(activity=Activity(type=ActivityType.listening, name=name))
        if activity.lower() == "watching":
            await self.client.change_presence(activity=Activity(type=ActivityType.watching, name=name))
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
                f.write(pickle.dumps(guild_mute_list))
            logger.success(f"Guild '{mguild.name}' muted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def unmuteguild(self):
        guildlistforunmute = []
        guild_mute_list = self.getmutes()[1]
        for i in range(len(guild_mute_list)):
            unmuteg = self.client.get_guild(guild_mute_list[i])
            guildlistforunmute.append(unmuteg.id)
            print(f"{i}: {unmuteg}")
        unmutechanelname = await self.async_input("type guild index: ")
        try:
            mguild = self.client.get_guild(guildlistforunmute[int(unmutechanelname)])
            guild_mute_list.remove(mguild.id)
            with open('guildmutes', 'wb') as f:
                f.write(pickle.dumps(guild_mute_list))
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
        if emojiinput == "2":
            emoji = await self.async_input("emoji: ")
        print("1 - message id")
        print("2 - message list")
        messageinput = await self.async_input("type number:")
        if messageinput == "2":
            messages = await self.raw_history()
            if messages == False:
                return
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

    async def setuser(self):
        usrid = int(await self.async_input("user id:"))
        print("checking availability...")
        sure = False
        for user in self.client.users:
            if user.id == usrid:
                sure = True
                break
        if sure == False:
           allowed = await self.async_input("the user was not found in the list of users. Continue? [y / n]")
           if allowed.lower() != "y":
            return
        else:
            print("User has been found")
        user: User = self.client.get_user(usrid)
        self.channel = user
        await self.get_history()
        return {"channel":user}
    async def edit(self):
        messages = await self.raw_history()
        if messages == False:
            return
        yourmessages: dict[int:Message] = {}

        for i, message in enumerate(messages):
            if message.author.id == self.client.user.id:
                yourmessages[i] = message
                rounded_date_string = message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")

        data = await self.async_input("message index:")
        if data == "" or data == None:
            return
        edmsg:Message = yourmessages.get(int(data))
        oldcont = edmsg.content
        data = await self.async_input("new message:")
        await edmsg.edit(content=data)
        logger.success(f"Message: {oldcont} | edited to: {data}")
    async def set(self):
        id = await self.async_input("channel id:")
        self.channel = self.client.get_channel(int(id))
        await self.get_history()
        return {"channel": self.channel}
    async def reply(self):
        messages = await self.raw_history()
        replymessages:dict[int,Message] = {}
        if messages == False:
            return
        for i, msg in enumerate(messages):
            replymessages[i] = msg
            print(f"{i}: {msg.channel}: {msg.author}: {msg.content}")
        id = int(await self.async_input("message index:"))
        if id < 0:
            return
        await replymessages[id].reply(await self.async_input("message:"))
    async def vcpaly(self):
        for i, client in enumerate(self.vcchlients):
            print(f"{i}:{client.channel.name}")
        id = await self.async_input("channel index:")
        if int(id) < 0:
            return
        vcch = self.vcchlients[int(id)]
        print("opend methods:\n1: by path\n2: by filedialog")
        method = await self.async_input("open method:")
        if method == "1":
         path = await self.async_input("path:")
        elif method == "2":
            path = filedialog.askopenfilename()
        if path == "" or path == None or path == " ":
            return
        source = FFmpegPCMAudio(path)
        vcch.play(source, after=self.VC_after_playing)
        logger.success("Audio playback has started")

    def VC_after_playing(self, error):
        if error:
            pass
        else:
            logger.info("Audio has finished playing")
    async def vcconnect(self):
        print("Choose a channel:")
        channels: dict[int, dict[str:int]] = {}
        for i, channel in enumerate(self.guild.voice_channels):
            channels.update({i: {channel.name: channel.id}})
            print(f"{i}: {channel.name}")
        data = await self.async_input("channel index:")
        if data == "" or data == None:
            return
        try:
            vcchannel:VoiceChannel = self.client.get_channel(list(channels.get(int(data)).values())[0])
            for client in self.client.voice_clients:
                if client.channel.guild.id == vcchannel.guild.id:
                    await client.disconnect()
            self.vcchlients.append(await vcchannel.connect())
            logger.success(f"connected! channel name {vcchannel.name}, channel id: {vcchannel.id}")
            return
        except Forbidden:
            logger.error(f"{Fore.RED}It's impossible to connect: Forbidden.")
            return
    async def vctts(self):
        for i, client in enumerate(self.vcchlients):
            print(f"{i}:{client.channel.name}")
        id = await self.async_input("channel index:")
        if int(id) < 0:
            return
        vcch = self.vcchlients[int(id)]
        message = await self.async_input("tts message:")
        engine = pyttsx3.init()
        engine.save_to_file(text=message, filename="VC_TEMP_TTS.wav")
        engine.runAndWait()
        source = FFmpegPCMAudio("VC_TEMP_TTS.wav")
        vcch.play(source, after=self.VC_after_playing)
        logger.success("Audio playback has started")
    async def vcdisconnect(self):
        for i, client in enumerate(self.client.voice_clients):
            print(f"{i}:{client.channel.name}")
        id = await self.async_input("channel index:")
        if int(id) < 0:
            return
        for client in self.vcchlients:
            if self.client.voice_clients[int(id)].channel.id == client.channel.id:
                self.vcchlients.remove(client)
                break
        await self.client.voice_clients[int(id)].disconnect(force=True)

        logger.success("Disconnected")
    async def vcstop(self):
        for i, client in enumerate(self.vcchlients):
            print(f"{i}:{client.channel.name}")
        id = await self.async_input("channel index:")
        try:
         self.vcchlients[int(id)].source.cleanup()
        except:
            pass
        logger.success("Stoped playing.")


