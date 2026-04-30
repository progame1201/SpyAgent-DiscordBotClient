import inspect
from datetime import datetime

from colorama import Fore, init

init(autoreset=True)


def log(string, end="\n", show_time=False):
    text = f"{Fore.CYAN}"
    if show_time:
        text += f"[{datetime.now()}]"
    text += f" {string}"

    print(text, end=end)

def user_message(string, end="\n"):
    print(f"{Fore.WHITE}{string}", end=end)

def event(string, end="\n", show_time=True):
    text = f"{Fore.LIGHTCYAN_EX}"
    if show_time:
        text += f"[{datetime.now()}]"
    text += f"[EVENT] {string}"

    print(text, end=end)

def warn(string, end="\n", show_time=True):
    text = f"{Fore.YELLOW}"
    if show_time:
        text += f"[{datetime.now()}]"

    caller = inspect.stack()[1]
    text += f"{caller.lineno}:{caller.function} [WARN] {string}"

    print(text, end=end)

def error(string, end="\n", show_time=True):
    text = f"{Fore.RED}"
    if show_time:
        text += f"[{datetime.now()}]"

    caller = inspect.stack()[1]
    text += f"{caller.lineno}:{caller.function} [ERROR] {string}"

    print(text, end=end)
