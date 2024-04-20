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
import tkinter as tk
from tkinter import simpledialog
import queue
import threading

def get_command_runner(q, prompt):
    root = tk.Tk()
    root.withdraw()
    command = simpledialog.askstring(title=prompt, prompt=prompt, parent=root)
    q.put(command)
    root.destroy()

class Commands:
    '''All commands of SpyAgent 2.11.0+
       most of the commands were taken from version 1.0.0-2.0.0, which is why their code maybe bad.
    '''
    def __init__(self, client=None, guild=None, channel=None):
        self.client:Client = client
        self.channel:TextChannel = channel
        self.guild:Guild = guild
        self.vcchlients:list[VoiceClient] = []
        init(autoreset=True)

    async def input_type_check(self, prompt, command_mode):
        if command_mode == True:
            print(prompt)
            q = queue.Queue()
            threading.Thread(target=get_command_runner, args=(q,prompt,)).start()
            while q.empty():
                await asyncio.sleep(0.1)
            user_input = q.get()
            return user_input
        else:
            user_input = await self.async_input(prompt)
            return user_input
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
    async def get_history(self, command_mode=False):
        messages = await self.raw_history()
        if messages == False:
            return
        print("Channel history:\n#####################")
        for message in messages:
            date = message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
            attachment_list = []
            reactions_list = []
            msg = f"{message.channel}: {date} {message.author}: {message.content}"
            if message.attachments:
                for attachment in message.attachments:
                    attachment_list.append(attachment.url)
                msg += f"\n↳attachments: {attachment_list}"

            if message.reactions:
                for reaction in message.reactions:
                    reactions_list.append(reaction.emoji)
                msg += f"\n↳reactions: {reactions_list}"
            if message.reference and message.reference.message_id and config.allow_reference_display != False:
                reference = await message.channel.fetch_message(message.reference.message_id)
                if reference.content and reference.author.name:
                    msg += f"\n↳reference: reply: {reference.author.name}: {reference.content}"
            print(msg)

        print("#####################")

    async def mutechannel(self, command_mode):
        channellistformute = []
        channels_mute_list = self.getmutes()[0]
        for i, mchannel in enumerate(self.guild.text_channels):
            if mchannel.id in channels_mute_list:
                channellistformute.append(mchannel.id)
                continue
            channellistformute.append(mchannel.id)
            print(f"{i}: {mchannel.name}")
        mutechanelname = await self.input_type_check("type chanel index: ", command_mode)
        try:
            mchannel = self.client.get_channel(channellistformute[int(mutechanelname)])
            channels_mute_list.append(mchannel.id)
            with open('channelmutes', 'wb') as f:
                f.write(pickle.dumps(channels_mute_list))
            logger.success(f"Channel '{mchannel.name}' muted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def unmutechannel(self, command_mode):
        channellistforunmute = []
        channels_mute_list = self.getmutes()[0]
        for i in range(len(channels_mute_list)):
            unmutech = self.client.get_channel(channels_mute_list[i])
            channellistforunmute.append(unmutech.id)
            print(f"{i}: {unmutech.name}")
        unmutechanelname = await self.input_type_check("type chanel index: ", command_mode)
        try:
            mchannel = self.client.get_channel(channellistforunmute[int(unmutechanelname)])
            channels_mute_list.remove(mchannel.id)
            with open('channelmutes', 'wb') as f:
                f.write(pickle.dumps(channels_mute_list))
            logger.success(f"Channel '{mchannel.name}' unmuted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def delete(self, command_mode):
        messages = await self.raw_history()
        if messages == False:
            return
        yourmessages: dict[int:Message] = {}

        for i, message in enumerate(messages):
            if message.author.id == self.client.user.id:
                yourmessages[i] = message
                rounded_date_string = message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")
        data = await self.input_type_check("message index:", command_mode)
        if data == "" or data == None:
            return
        todelmsg = yourmessages.get(int(data))
        await todelmsg.delete()
        logger.success(f"Message: '{todelmsg.content}' deleted")
    async def reset(self, command_mode):
        print("Choose a guild:")
        for i, guild in enumerate(self.client.guilds):
            print(f"{i}: {guild.name}")
        data = await self.input_type_check("server index:", command_mode)
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
        data = await self.input_type_check("server index:", command_mode)
        if data == "" or data == None:
            return
        channel = self.client.get_channel(list(channels.get(int(data)).values())[0])
        logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
        self.channel = channel
        self.guild = guild
        await self.get_history()
        return {"channel":channel,"guild":guild}
    async def resetchannel(self, command_mode):
        print("Choose a channel:")
        channels: dict[int, dict[str:int]] = {}
        for i, channel in enumerate(self.guild.text_channels):
            channels.update({i: {channel.name: channel.id}})
            print(f"{i}: {channel.name}")
        data = await self.input_type_check("channel index:", command_mode)
        if data == "" or data == None:
            return
        channel = self.client.get_channel(list(channels.get(int(data)).values())[0])
        logger.success(f"channel assigned! channel name {channel.name}, channel id: {channel.id}")
        self.channel = channel
        await self.get_history()
        return {"channel":channel}
    async def into(self, command_mode):
        id = await self.input_type_check("channel id:", command_mode)
        channel = self.client.get_channel(int(id))
        await channel.send(await self.input_type_check("message:", command_mode))

    async def file(self, command_mode):
        try:
            file = filedialog.askopenfilename()
            await self.channel.send(file=File(file))
        except Exception as e:
            print(f"error sending file\n{e}")
    async def status(self, command_mode):
        statuses:dict = {"online":Status.online,"offline":Status.offline, "idle":Status.idle}
        print("statuses:")
        for key in statuses.keys():
            print(key)
        status = await self.input_type_check("status:", command_mode)
        if status.lower() in statuses.keys():
            await self.client.change_presence(status=statuses[status])
            logger.success(f"status changed to {status}")
    async def activity(self, command_mode):
        name = await self.input_type_check("description of the activity:", command_mode)
        activities = {"game":Game(name=name), "listening":Activity(type=ActivityType.listening, name=name), "watching":Activity(type=ActivityType.watching, name=name)}
        print("activities list:")
        for activity in activities.keys():
            print(activity)
        activity = await self.input_type_check("activity:", command_mode)
        if activity in activities.keys():
            await self.client.change_presence(activity=activities[activity])

    async def guildmute(self, command_mode):
        guildlistformute = []
        guild_mute_list = self.getmutes()[1]
        for i, mguild in enumerate(self.client.guilds):
            if mguild.id in guild_mute_list:
                guildlistformute.append(mguild.id)
                continue
            guildlistformute.append(mguild.id)
            print(f"{i}: {mguild.name}")
        muteguildname = await self.input_type_check("type guild index: ", command_mode)
        try:
            mguild = self.client.get_guild(guildlistformute[int(muteguildname)])
            guild_mute_list.append(mguild.id)
            with open('guildmutes', 'wb') as f:
                f.write(pickle.dumps(guild_mute_list))
            logger.success(f"Guild '{mguild.name}' muted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def unmuteguild(self, command_mode):
        guildlistforunmute = []
        guild_mute_list = self.getmutes()[1]
        for i in range(len(guild_mute_list)):
            unmuteg = self.client.get_guild(guild_mute_list[i])
            guildlistforunmute.append(unmuteg.id)
            print(f"{i}: {unmuteg}")
        unmutechanelname = await self.input_type_check("type guild index: ", command_mode)
        try:
            mguild = self.client.get_guild(guildlistforunmute[int(unmutechanelname)])
            guild_mute_list.remove(mguild.id)
            with open('guildmutes', 'wb') as f:
                f.write(pickle.dumps(guild_mute_list))
            logger.success(f"Guild '{mguild.name}' unmuted")
        except Exception as e:
            print(f"index not found\n{e}")
    async def reaction(self, command_mode):
        print("1 - emoji list")
        print("2 - type emoji")
        emojiinput = await self.input_type_check("type number:", command_mode)
        if emojiinput == "1":
            emojilist = []
            for i, emoji in enumerate(self.client.guilds[0].emojis):
                emojilist.append(emoji)
                print(f'{i}: {emoji.name} - {emoji}')
            reactemoji = await self.input_type_check("type emoji index: ", command_mode)
            try:
                emoji = emojilist[int(reactemoji)]
            except:
                return
        if emojiinput == "2":
            emoji = await self.input_type_check("emoji: ", command_mode)
        print("1 - message id")
        print("2 - message list")
        messageinput = await self.input_type_check("type number:", command_mode)
        if messageinput == "2":
            messages = await self.raw_history()
            if messages == False:
                return
            for i, message in enumerate(messages):
                print(f"{i}: {message.author}: {message.content}")
            messageindex = await self.input_type_check("message index:", command_mode)
            message = messages[int(messageindex)]
            await message.add_reaction(emoji)
            logger.success(f"message reacted. Emoji: {emoji}")
            if messageinput == "1":
             messageid = int(await self.input_type_check("message id: ", command_mode) )
             message = await self.channel.fetch_message(int(messageid))
             await message.add_reaction(emoji)
             logger.success(f"message reacted. Emoji: {emoji}")
    async def privatemsg(self, command_mode):
        usrid = int(await self.input_type_check("user id:", command_mode))
        if usrid < 0:
            return
        user:User = self.client.get_user(usrid)
        msg = await self.input_type_check(f"{Fore.LIGHTBLACK_EX}Message to {user.name}:", command_mode)
        await user.send(msg)

    async def setuser(self, command_mode):
        usrid = int(await self.input_type_check("user id:", command_mode))
        print("checking availability...")
        sure = False
        for user in self.client.users:
            if user.id == usrid:
                sure = True
                break
        if sure == False:
           allowed = await self.input_type_check("the user was not found in the list of users. Continue? [y / n]", command_mode)
           if allowed.lower() != "y":
            return
        else:
            print("User has been found")
        user: User = self.client.get_user(usrid)
        self.channel = user
        await self.get_history()
        return {"channel":user}
    async def edit(self, command_mode):
        messages = await self.raw_history()
        if messages == False:
            return
        yourmessages: dict[int:Message] = {}

        for i, message in enumerate(messages):
            if message.author.id == self.client.user.id:
                yourmessages[i] = message
                rounded_date_string = message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                print(f"{i}: {message.channel}: {rounded_date_string} {message.author}: {message.content}")

        data = await self.input_type_check("message index:", command_mode)
        if data == "" or data == None:
            return
        edmsg:Message = yourmessages.get(int(data))
        oldcont = edmsg.content
        data = await self.input_type_check("new message:", command_mode)
        await edmsg.edit(content=data)
        logger.success(f"Message: {oldcont} | edited to: {data}")
    async def set(self, command_mode):
        id = await self.input_type_check("channel id:", command_mode)
        self.channel = self.client.get_channel(int(id))
        await self.get_history()
        return {"channel": self.channel}
    async def reply(self, command_mode):
        messages = await self.raw_history()
        replymessages:dict[int,Message] = {}
        if messages == False:
            return
        for i, msg in enumerate(messages):
            replymessages[i] = msg
            print(f"{i}: {msg.channel}: {msg.author}: {msg.content}")
        id = int(await self.input_type_check("message index:", command_mode))
        if id < 0:
            return
        await replymessages[id].reply(await self.input_type_check("message:", command_mode))
    async def vcpaly(self, command_mode):
        for i, client in enumerate(self.vcchlients):
            print(f"{i}:{client.channel.name}")
        id = await self.input_type_check("channel index:", command_mode)
        if int(id) < 0:
            return
        vcch = self.vcchlients[int(id)]
        print("opened methods:\n1: by path\n2: by filedialog")
        method = await self.input_type_check("open method:", command_mode)
        if method == "1":
         path = await self.input_type_check("path:", command_mode)
        elif method == "2":
            path = filedialog.askopenfilename()
        if path == "" or path == None or path == " ":
            return
        source = FFmpegPCMAudio(path)
        vcch.play(source, after=self.VC_after_playing)
        logger.success("Audio playback has started")

    def VC_after_playing(self, error):
        if os.path.exists("VC_TEMP_TTS.wav"):
            os.remove("VC_TEMP_TTS.wav")
        if error:
            pass
        else:
            logger.info("Audio has finished playing")
    async def vcconnect(self, command_mode):
        print("Choose a channel:")
        channels: dict[int, dict[str:int]] = {}
        for i, channel in enumerate(self.guild.voice_channels):
            channels.update({i: {channel.name: channel.id}})
            print(f"{i}: {channel.name} {[member.name for member in channel.members]}")
        data = await self.input_type_check("channel index:", command_mode)
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
    async def vctts(self, command_mode):
        for i, client in enumerate(self.vcchlients):
            print(f"{i}:{client.channel.name}")
        id = await self.input_type_check("channel index:", command_mode)
        if int(id) < 0:
            return
        vcch = self.vcchlients[int(id)]
        message = await self.input_type_check("tts message:", command_mode)
        engine = pyttsx3.init()
        engine.save_to_file(text=message, filename="VC_TEMP_TTS.wav")
        engine.runAndWait()
        source = FFmpegPCMAudio("VC_TEMP_TTS.wav")
        vcch.play(source, after=self.VC_after_playing)
        logger.success("Audio playback has started")
    async def vcdisconnect(self, command_mode):
        for i, client in enumerate(self.client.voice_clients):
            print(f"{i}:{client.channel.name}")
        id = await self.input_type_check("channel index:", command_mode)
        if int(id) < 0:
            return
        for client in self.vcchlients:
            if self.client.voice_clients[int(id)].channel.id == client.channel.id:
                self.vcchlients.remove(client)
                break
        await self.client.voice_clients[int(id)].disconnect(force=True)

        logger.success("Disconnected")
    async def vcstop(self, command_mode):
        for i, client in enumerate(self.vcchlients):
            print(f"{i}:{client.channel.name}")
        id = await self.input_type_check("channel index:", command_mode)
        try:
         self.vcchlients[int(id)].source.cleanup()
        except:
            pass
        logger.success("Stoped playing.")
    async def leave(self, command_mode):
        print(f"Do you really want to quit from {self.guild.name}?")
        confirmation = await self.input_type_check("yes or no: ", command_mode).lower()
        if confirmation == "yes" or confirmation == "y":
         await self.guild.leave()
         logger.success("I'm leaving the current guild.")
    async def help(self, command_mode):
        print("#####HELP#####\n***Mute - mute any channel\n***Unmute - unmute any channel\n***Delete - delete any message you have selected\n***Reset - Re-select the guild and channel for communication\n***Resetchannel - Re-select a channel for communication\n***File - send a file\n***Muteguild - mute any guild\n***Unmuteguild - unmute any guild\n***Reaction - react any message\n***Privatemsg - Send a private message to the user\n***Gethistory - Get the history of the channel you are on\n***into - send a message to any channel (by ID)\n***set - set the channel (by ID)\n***setuser - It works as a Spy Agent PM setting the user as a channel\n***reply - reply to a message\n***vcplay - turns on music\n***vcstop - turns off the music\n***edit - edit any message\n***vcconnect - connect to any voice channel\n***vcdisconnect - disconnect from voice channel\n***vctts - plays tts message to the voice channel\n***activity - to put an activity on the bot, for example: playing a game\n***guildleave - allows you to exit the guild you are in\n#####INFO#####\nall messages are written in the format: guild: channel: author: message\n##############")


