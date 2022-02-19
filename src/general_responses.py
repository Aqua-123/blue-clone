from src.ws import *
from src.list_handling import *
from src.funzies import *
from src.data_handing import *

def matching(name,dictname, message, console, dict):
    keys = list(dictname.keys())
    for i in range(len(keys)):
        re_m = keys[i]
        result = re_m.match(message)
        if result:
            if dict == True:
                if re_m == whos_here:
                    response = reply_whos_here()
                elif re_m == whos_idle:
                    response = reply_whos_idle()
                else:
                    response = list(dictname.values())[i]
                if console is True:
                    print("Console:-%s"%response)
                else:
                    send_message(response)
            elif dict == False:
                if re_m == jok:
                    if console is True:
                        print("Console:- %s"%get_jokes())
                    else:
                        send_message(get_jokes())
                elif re_m == quote:
                    get_quote(console)
                elif re_m == save_message:
                    response = saving_messages(name, result)
                    if console:
                        print("Console:-%s"%response)
                    else:
                        send_message(response)
                else:
                    if console:
                        print("Console:- %s" %list(dictname.values())[i])
                    else:
                        print(dictname.values())
                        send_message(list(dictname.values())[i])
            break