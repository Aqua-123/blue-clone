from ws import *
from list_handling import *
from funzies import *
from data_handing import *

def matching(name,dictname, message, console):
    global whos_here_res
    keys = list(dictname.keys())
    for i in range(len(keys)):
        re_m = keys[i]
        result = re_m.match(message)
        if result:
            if dictname == whos_here_res:
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
            elif dictname == response_dict:
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
                        send_message(list(dictname.values())[i])
            break