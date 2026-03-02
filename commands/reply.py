from .command import Command
from utils import async_int_input, get_history, log, prepare_message, user_message, is_valid_index
from colorama import Fore


class Reply(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <message> - reply to a message<br>"

    async def execute(self, *args):
        if not args[0]:
            log("enter a message.")
            return
        history = list(await get_history(self.channel, limit=30))  # This is a list because nothing will work without conversion.
        for i, message in enumerate(history):
            user_message(f"{Fore.LIGHTWHITE_EX}{i}{Fore.YELLOW} - {await prepare_message(message)}")
        index = await async_int_input("enter message index: ")
        if not is_valid_index(index, history):
            return
        message = history[index]
        await message.reply(" ".join(args[0]))
