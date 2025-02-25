from colorama import Fore, init
from datetime import datetime
init(autoreset=True)


def log(string, end="\n", show_time=False):
    if show_time:
        print(f"{Fore.CYAN}[{datetime.now()}] {string}", end=end)
        return
    print(f"{Fore.CYAN}{string}", end=end)

def user_message(string, end="\n", show_time=True):
    print(f"{Fore.WHITE}{string}", end=end)

def event(string, end="\n", show_time=True):
    if show_time:
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [EVENT] {string}", end=end)
        return
    print(f"{Fore.LIGHTCYAN_EX}[EVENT] {string}", end=end)

def error(string, end="\n", show_time=True):
    if show_time:
        print(f"{Fore.RED}[{datetime.now()}] [ERROR] {string}", end=end)
        return
    print(f"{Fore.RED}[ERROR] {string}", end=end)
