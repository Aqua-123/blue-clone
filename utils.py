# pylint: disable-all
from var import *
from sys import argv, executable
from os import execl

def fix_message(message):
    chars = ('"[]‘')
    for c in chars:
        message = message.replace(c, "")
    for c in forbiden_chars:
        message = message.replace(c, "")
    message = message.replace(".",".​")
    return message

def fix_name(name):
    for chars in forbiden_chars:
        name.replace(chars, '')
    return name

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    execl(executable, executable, *argv)

def format_out_list(input_list):
    return ", ".join(input_list)

