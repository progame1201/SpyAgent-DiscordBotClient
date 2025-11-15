from disnake import *
from .command import Command
from utils import try_async_int_input, get_history, log, prepare_message, user_message


class Edit(Command):
    def __init__(self, *args):
        super().__init__(*args)
        self.description = f"{self.name} <message> - Edit the message"

    async def execute(self, *args):
        history = await get_history(self.channel, limit=50)
        history = [message for message in history if message.author.id == self.client.user.id]

        for i, message in enumerate(history):
            user_message(f"{i} - {await prepare_message(message)}")

        index = await try_async_int_input("enter message index: ")
        if index is False:
            log("You entered incorrect message index. the command will not continue execution.")
        if len(history) - 1 < index or index < 0:
            log("You entered incorrect message index. the command will not continue execution.")
        message: Message = history[index]

        await message.edit(content=" ".join(args[0]))
        log("edited.")
