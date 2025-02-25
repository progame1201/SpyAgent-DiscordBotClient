from disnake import *
from .command import command
from utils import try_async_int_input, get_history, log, prepare_message, user_message
from aioconsole import ainput
from colorama import Fore


class reaction(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.description = f"{self.name} <mode: 1 - choose the emoji yourself; 2 - Select an emoji from the list of all emojis> - Put a reaction under the message"


    async def execute(self, *args):
        if not args[0]:
            log("You entered incorrect reaction mode. the command will not continue execution.")
            return
        args = args[0]

        history = await get_history(self.channel, limit=50)

        for i, message in enumerate(history):
            user_message(f"{i} - {await prepare_message(message)}")

        index = await try_async_int_input("enter message index: ")

        if index is None:
            log("You entered incorrect message index. the command will not continue execution.")
            return
        if len(history) - 1 < index or index < 0:
            log("You entered incorrect message index. the command will not continue execution.")
            return

        message:Message = history[index]

        if args[0] in ["1"]:
            emoji = await ainput("emoji: ")

        elif args[0] in ["2"]:
            for i, emoji in enumerate(self.client.emojis):
                log(f'{i}: {emoji.name} - {emoji.url}')

            index = await try_async_int_input("enter emoji index: ")

            if not index:
                log("You entered incorrect emoji index. the command will not continue execution.")
            if len(self.client.emojis) - 1 < index or index < 0:
                log("You entered incorrect emoji index. the command will not continue execution.")

            emoji = self.client.emojis[index]
        else:
            log("You entered incorrect reaction mode. the command will not continue execution.")
            return

        await message.add_reaction(emoji)
        log("added reaction")
