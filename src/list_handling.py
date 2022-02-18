from var import *
import requests
import json
from threading import Thread
from utils import fix_message

def list_removal(id):
    global list_main_dict, timeout_control, idle_main_dict
    if id in timeout_control:
        del timeout_control[id]
    if id in list_main_dict:
        del list_main_dict[id]
    if id in idle_main_dict:
        del idle_main_dict[id]

def whos_here_appending(id):
    global whos_here_r
    r = requests.get(profile_url % id, cookies=cookies)
    r = json.loads(r.text)
    whos_here_r.append(r["user"]["display_name"])

def reply_whos_here():
    global whos_here_r
    for i in list_main_dict:
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads.clear()
    idle_len = len(idle_main_dict)
    whos_here_r = fix_message(str(whos_here_r))
    if idle_len == 0:
        response = whos_here_response_no_lurkers % whos_here_r
    elif idle_len == 1:
        response = whos_here_response_gen1 % whos_here_r
    elif idle_len > 1:
        response = whos_here_response_gen2 % (whos_here_r, idle_len)
    return fix_message(response)

def reply_whos_idle():
    global whos_here_r
    for i in idle_main_dict.keys():
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads.clear()
    whos_idle_r = str(whos_here_r)
    if len(idle_main_dict) == 0:
        response = whos_lurking_none
    elif len(idle_main_dict) > 0:
        response = whos_lurking_gen % whos_idle_r
    return fix_message(response)