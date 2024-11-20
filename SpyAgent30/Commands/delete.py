from disnake import *
from .command import command
from utils import try_async_int_input, get_history, log, prepare_message, user_message
from colorama import Fore


class delete(command):
    def __init__(self, guild:Guild, channel:TextChannel, client:Client):
        super().__init__(guild, channel, client)
        self.description = "delete - delete a message"


    async def execute(self, *args):
        history = await get_history(self.channel, limit=50)
        history = [message for message in history if message.author.id == self.client.user.id]

        for i, message in enumerate(history):
            user_message(f"{Fore.LIGHTWHITE_EX}{i}{Fore.YELLOW} - {await prepare_message(message)}")

        index = await try_async_int_input("enter message index: ")
        if not index:
            log("You entered incorrect message index. the command will not continue execution.")
        if len(history) - 1 < index and index < 0:
            log("You entered incorrect message index. the command will not continue execution.")
        message = history[index]

        await message.delete()
        log("deleted.")