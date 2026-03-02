from .command import Command
from utils import async_int_input, get_history, log, prepare_message, user_message, is_valid_index


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
