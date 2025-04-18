from disnake import *
from .command import command
from utils import try_async_int_input, get_history, log, prepare_message, user_message
from colorama import Fore


class reply(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.description = f"{self.name} <message> - reply to a message<br>"

    async def execute(self, *args):
        if not args[0]:
            log("enter a message.")
            return
        history = await get_history(self.channel, limit=30)
        for i, message in enumerate(history):
            user_message(f"{Fore.LIGHTWHITE_EX}{i}{Fore.YELLOW} - {await prepare_message(message)}")
        index = await try_async_int_input("enter message index: ")
        if index is None:
            log("You entered incorrect message index. the command will not continue execution.")
            return
        if len(history) - 1 < index or index < 0:
            log("You entered incorrect message index. the command will not continue execution.")
            return
        message = history[index]

        await message.reply(" ".join(args[0]))
