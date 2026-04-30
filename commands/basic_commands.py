import asyncio
from tkinter.filedialog import askopenfilename

import disnake
from colorama import Fore
from aioconsole import ainput
from disnake import Message, Forbidden, HTTPException

from .command import Command
from utils import (
    async_int_input,
    get_history,
    prepare_message,
    user_message,
    is_valid_index,
    show_history,
    SelectUtils,
)
from log import log


class Delete(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} - delete a message"

    async def execute(self, *args):
        history = await get_history(self.channel, limit=50)
        history = [message for message in history if message.author.id == self.client.user.id]

        for i, message in enumerate(history):
            user_message(f"{i} - {await prepare_message(message)}")

        index = await async_int_input("enter message index: ")
        if not is_valid_index(index, history):
            return
        message = history[index]
        await message.delete()
        log("deleted.")



class Edit(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <message> - edit a message"

    async def execute(self, *args):
        if len(args[0]) == 0:
            log("enter a message.")
            return

        history = await get_history(self.channel, limit=50)
        history = [message for message in history if message.author.id == self.client.user.id]

        for i, message in enumerate(history):
            user_message(f"{i} - {await prepare_message(message)}")

        index = await async_int_input("enter message index: ")
        if not is_valid_index(index, history):
            return
        message: Message = history[index]
        await message.edit(content=" ".join(args[0]))
        log("edited.")


class File(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.select_utils = SelectUtils(self.client)
        self.description = f"{self.name} <message> - send a file with a message"

    async def execute(self, *args):
        path = await asyncio.to_thread(askopenfilename, title="select file")
        if not path:
            return
        await self.channel.send(content=" ".join(args[0]), file=disnake.File(path))

class History(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <channel id> - get the history of the current channel or a channel by ID"

    async def execute(self, *args):
        if args[0]:
            channel = await self.client.fetch_channel(int(args[0][0]))
        else:
            channel = self.channel
        await show_history(channel)


class Reply(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <message> - reply to a message"

    async def execute(self, *args):
        if not args[0]:
            log("enter a message.")
            return
        history = list(await get_history(self.channel, limit=30))
        for i, message in enumerate(history):
            user_message(f"{Fore.LIGHTWHITE_EX}{i}{Fore.YELLOW} - {await prepare_message(message)}")
        index = await async_int_input("enter message index: ")
        if not is_valid_index(index, history):
            return
        message = history[index]

        await message.reply(" ".join(args[0]))


class Reaction(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <mode: 1 - utf-8 emoji; 2 - select an emoji from the list of all emojis> - add a reaction to a message"

    async def execute(self, *args):
        if not args[0]:
            log("You entered incorrect reaction mode. Available modes: 1 - choose the emoji yourself; 2 - Select an emoji from the list of all emojis")
            return
        args = args[0]

        history = list(await get_history(self.channel, limit=50))

        for i, message in enumerate(history):
            user_message(f"{i} - {await prepare_message(message)}")

        index = await async_int_input("enter message index: ")
        if not is_valid_index(index, history):
            return

        message: Message = history[index]

        if args[0] in ["1"]:
            emoji = await ainput("emoji: ")

        elif args[0] in ["2"]:
            if len(self.client.emojis) == 0:
                log("You don't have access to any custom emojis in any servers. 🥀")
                return
            for i, emoji in enumerate(self.client.emojis):
                log(f"{i}: {emoji.name} - {emoji.url}")

            index = await async_int_input("enter emoji index: ")
            if not is_valid_index(index, self.client.emojis):
                return

            emoji = self.client.emojis[index]
        else:
            log("You entered incorrect reaction mode. the command will not continue execution.")
            return
        await message.add_reaction(emoji)
        log("added reaction")