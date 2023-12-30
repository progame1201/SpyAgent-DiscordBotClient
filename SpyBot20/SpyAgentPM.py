import disnake
from disnake.ext import *
from disnake import *
from loguru import logger
import asyncio
import winsound
import pickle
import os
import pytz
from asyncio import sleep
import config
from colorama import Fore, init
import Commands
import LocalCommandManager
init(autoreset=True)
class Handler:
    def __init__(self, client, startid):
        self.client:Client = client
        self.channel = self.client.get_user(startid)
        asyncio.run_coroutine_threadsafe(self.receive_messages(), client.loop)
        asyncio.run_coroutine_threadsafe(self.chatting(), client.loop)
        asyncio.run_coroutine_threadsafe(self.detector(), client.loop)

    async def receive_messages(self):
        while True:
            attachment_list = []
            message: Message = await self.client.wait_for('message')
            if isinstance(message.channel, DMChannel):
                    date = message.created_at
                    rounded_date = date.replace(second=0, microsecond=0)
                    rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
                    if message.attachments:
                        for attachment in message.attachments:
                            attachment_list.append(attachment.url)
                        if config.display_users_avatars_urls:
                           print(f'\n{message.channel}: {rounded_date_string} ({message.author.avatar.url}) ({message.author.id}) {message.author.name}: {message.content}, attachments: {attachment_list}')
                        else:
                            print(f'\n{message.channel}: {rounded_date_string} ({message.author.id}) {message.author.name}: {message.content}, attachments: {attachment_list}')
                    else:
                        print(f'\n{message.channel}: {rounded_date_string} ({message.author.id}) {message.author.name}: {message.content}')
                    if config.notification == True:
                     if message.author.id != client.user.id:
                      winsound.Beep(500, 100)
                      winsound.Beep(1000, 100)

    async def detector(self):
        async def reaction_add():
            while True:
                reaction, user = await self.client.wait_for('reaction_add')
                if self.channel.id == reaction.message.author.id:
                    print(f"Reaction {reaction.emoji} | was added to: {reaction.message.channel}: {reaction.message.author}: {reaction.message.content}")

        async def reaction_remove():
            while True:
                reaction, user = await self.client.wait_for('reaction_remove')
                if self.channel.id == reaction.message.author.id:
                    print(f"Reaction {reaction.emoji} | was removed from: {reaction.message.channel}: {reaction.message.author}: {reaction.message.content}")

        async def message_delete():
            while True:
                message: Message = await self.client.wait_for("message_delete")
                if self.channel.id == message.author.id:
                    print(f"Message {message.content} | was removed from: {message.channel}: {message.author}")

        async def message_edit():
            while True:
                before, after = await self.client.wait_for("message_edit")
                if self.channel.id == after.author.id:
                    print(f"Message: {before.content} | has been changed to: {after.content} |in: {after.channel}: {after.author}")

        if config.detector:
            if config.on_reaction_add:
                asyncio.run_coroutine_threadsafe(reaction_add(), self.client.loop)
            if config.on_reaction_remove:
                asyncio.run_coroutine_threadsafe(reaction_remove(), self.client.loop)
            if config.on_message_delete:
                asyncio.run_coroutine_threadsafe(message_delete(), self.client.loop)
            if config.on_message_edit:
                asyncio.run_coroutine_threadsafe(message_edit(), self.client.loop)
    async def chatting(self):
        logger.info("Starting command manager...")
        cm = LocalCommandManager.Manager()
        cmnds = Commands.Commands(client=client, channel=self.channel)
        cm.new(command_name="***reset", func=cmnds.pmreset)
        cm.new(command_name="***file", func=cmnds.file)
        cm.new(command_name="***delete", func=cmnds.delete)
        cm.new(command_name="***status", func=cmnds.status)
        cm.new(command_name="***gethistory", func=cmnds.get_history)
        cm.new(command_name="***reaction", func=cmnds.reaction)
        cm.new(command_name="***edit", func=cmnds.edit)
        print(f"\n{Fore.YELLOW}List of loaded commands:\n{cm.get_keys()}\n{Fore.CYAN}")
        logger.success("Command manager started!")
        await self.get_history(channel=self.channel)
        while True:
            await sleep(1)
            senddata = await self.async_input(f"{Fore.LIGHTBLACK_EX}Message to {self.channel.name}:\n{Fore.RESET}")
            cmresult = cm.execute(senddata)
            if cmresult != False:
                cmresult: dict = await cmresult()
                if cmresult != None:
                    if "channel" in list(cmresult.keys()):
                        self.channel = cmresult["channel"]
                        await self.get_history(channel=self.channel)
                continue
            try:
             await self.channel.send(senddata)
            except Forbidden:
                print("It's impossible to send: Forbidden.")

    async def get_history(self):
        messages = []
        try:
            async for message in self.channel.history(limit=config.history_size, oldest_first=False):
                messages.append(message)
        except Forbidden:
            print(f"{Fore.RED}It's impossible to get: Forbidden.")
            return
        print("Channel history:\n#####################")
        messages.reverse()
        for message in messages:
            date = message.created_at
            rounded_date = date.replace(second=0, microsecond=0)
            rounded_date_string = rounded_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M')
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
            print(msg)

        print("#####################")

    async def async_input(self, prompt):
        return await asyncio.to_thread(input, prompt)
if __name__ == "__main__":
    logger.info("❄Spy Agent Private Messages 1.1.0❄, 2023-2024, progame1201")
    client = disnake.Client(intents=Intents.all())
    userid = int(input("user id: "))
    @client.event
    async def on_ready():
      hnd = Handler(client=client, startid=userid)
    client.run(config.Token)