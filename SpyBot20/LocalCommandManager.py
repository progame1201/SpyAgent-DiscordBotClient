import disnake


class Manager():
    '''Commands manager of SpyAgent 2.11.0+ discord bot.
    Manager version 1.1.0
    '''

    def __init__(self):
        self.commands = {}
    def new(self, command_name:str, func):
        self.commands.update({command_name:func})
        return True
    async def execute(self, command_name: str, command_mode=False):
        if command_name.lower() in list(self.commands.keys()):
            func = self.commands[command_name.lower()]
            return await func(command_mode)
        else:
            return False

    def get_keys(self):
        return "\n".join(self.commands.keys())

