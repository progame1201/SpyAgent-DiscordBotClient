from .command import Command
from utils import try_async_int_input, get_history, log, prepare_message, user_message
from colorama import Fore


class Reply(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <message> - reply to a message<br>"

    async def execute(self, *args):
        if not args[0]:
            log("enter a message.")
            return
        history = await get_history(self.channel, limit=30)
        for i, message in enumerate(history):
            user_message(f"{Fore.LIGHTWHITE_EX}{i}{Fore.YELLOW} - {await prepare_message(message)}")
        index = await try_async_int_input("enter message index: ")
        if index is False:
            log("You entered incorrect message index. the command will not continue execution.")
            return
        if len(history) - 1 < index or index < 0:
            log("You entered incorrect message index. the command will not continue execution.")
            return
        message = history[index]

        await message.Reply(" ".join(args[0]))
