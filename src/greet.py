from var import *
from src.ws import send_message
from time import perf_counter
from src.data_handing import *
from src.utils import fix_name
from src.list_handling import list_removal

def greet_text(count, name):
    if shorten_greet_toggle is False:
        if count == 1:
            return Greet_1 % name
        elif count == 2:
            return Greet_2 % name
        elif count == 3:
            return Greet_general % name
    else:
        if count == 1:
            return Greet_1_short % name
        elif count == 2:
            return Greet_2_short % name
        elif count == 3:
            return Greet_general_short % name

def send_greet(name):
    if name in greet_timeout:
        if greet_timeout[name] == "1":
            send_message(greet_text(1, name))
            greet_timeout[name] = "2"
        elif greet_timeout[name] == "2":
            send_message(greet_text(2, name))
            greet_timeout[name] = "3"
        elif greet_timeout[name] == "3":
            pass
    else:
        send_message(greet_text(3, name))
        greet_timeout[name] = "1"

def greet(action, result, greet, b):
    global data,saved_messages, list_main_dict, idle_main_dict, timeout_control, stats_list
    if (action in b) and ("user" in b) and "display_name" in b["user"]:
        name = fix_name(b["user"]["display_name"])
        username = b["user"]["username"]
        id = b["user"]["id"]
        if result == "add":
            list_main_dict[id] = name
            stats_list[id] = name
            timeout_control[id] = perf_counter()
            saved_message_handler(str(id),name)
        elif result == "remove":
            list_removal(id)
        id = str(id)
        if greet_status is True and greet is True and id not in data["greet_exempt"]:
            if str(id) in data["custom_greet"]:
                send_message(data["custom_greet"][id])
            elif str(id) in data["knight"]:
                send_message("Greetings %s ~*" % name)
            else:
                send_greet(name)
        update_seen(name,id,username)
