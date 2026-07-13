from aioconsole import ainput

from log import log


def is_valid_index(index, obj_list):
    if index is None:
        log("You entered incorrect index. the command will not continue execution.")
        return False

    if len(obj_list) - 1 < index or index < 0:
        log("You entered incorrect index. the command will not continue execution.")
        return False

    return True

async def async_int_input(prompt="", one_attempt=True):
    while True:
        try:
            return int(await ainput(prompt))
        except:
            if one_attempt:
                return None
            log("enter a number, not text")
