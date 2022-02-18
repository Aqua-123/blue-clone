from data_handing import *
from var import *
from os import execl
from sys import argv, executable
from time import perf_counter

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
    update_seen_json()
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    execl(executable, executable, *argv)


def return_id(string):
    refresh_seen()
    print(string)
    if string.isnumeric():
        id = string
        if id in seen_data:
            return id
        else:
            return False
    else:
        string = string.replace("#", "")
        n = 0
        possibles = {}
        for id in seen_data:
            name = seen_data[id]["name"]
            username = seen_data[id]["username"]
            regex1 = re.compile(r'%s' % fix_name(string), re.IGNORECASE)    
            if regex1.search(name) or regex1.search(username):
                possibles[id] = name
            else: n += 1
        for id in data["nickname"]:
            for nickname in data["nickname"][id]:
                regex2 = re.compile(string, re.IGNORECASE)
                n+=1
                if regex2.search(nickname):
                    possibles[id] = nickname
                else:
                    pass
        total = len(seen_data) 
        for id in data["nickname"]:
            total+=len(data["nickname"][id])    
        if n == total:
            return False
        else:
            return possibles


def remove_blue():
    global list_main_dict, idle_main_dict, timeout_control
    if "21550262" in list_main_dict:
        del list_main_dict["21550262"]
    if "21550262" in idle_main_dict:
        del idle_main_dict["21550262"]
    if "21550262" in timeout_control:
        del timeout_control["21550262"]


def idle_function():
    idle_check = list(timeout_control.values())
    for i in range(len(idle_check)):
        x = idle_check[i]
        if perf_counter() - x >= 240:
            val = list(timeout_control.keys())[i]
            if val in list_main_dict:
                idle_main_dict[val] = list_main_dict[val]
                del list_main_dict[val]
        elif perf_counter() - x < 240:
            val = list(timeout_control.keys())[i]
            if val in idle_main_dict:
                del idle_main_dict[val]

def clocking():
    global reset_clock, greet_timeout
    if reset_clock == 500:
        greet_timeout, reset_clock = {}, 0
