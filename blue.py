import json
import random
from threading import Thread
from time import sleep

from imgurpython import ImgurClient
from simple_image_download import simple_image_download as simp

from src.admin import *
from src.admin_init import *
from src.autoban import *
from src.console_admin import *
from src.data_handing import *
from src.feelings_init import *
from src.funzies import *
from src.general_responses import *
from src.greet import *
from src.greeter_fallback import *
from src.image_upload import *
from src.list_handling import *
from src.utils import *
from src.ws import *
from src.logging import *

response = simp.simple_image_download

import websocket

from var import *

client = ImgurClient(client_id, client_secret)

with open('data.json', 'r') as f:
    data = json.loads(f.read())
with open('messages.json', 'r') as f:
    saved_messages = json.loads(f.read())
with open('seen.json', 'r') as f:
    seen_data = json.loads(f.read())
with open('image_cache.json', 'r') as f:
    image_cache = json.loads(f.read())

Thread(target=console_input).start()
Thread(target=thread_function).start()
while True:
    try:
        websocket.enableTrace(False)
        ws = websocket.WebSocket()
        ws.connect(ws_url, cookie=main_cookie, subprotocols=subprots, origin=origin)
        ws.send(json.dumps(connect_json))
        ws.send(json.dumps(connect_json_blue))
        while running is True:
            update_seen_json()
            reset_clock = reset_clock + 1 
            result = ws.recv() #receive message
            result = json.loads(result)
            remove_blue() 
            idle_function()
            clocking()
            check_singing()
            whos_here_r = whos_idle_r = []
            whos_here_res = { 
                whos_here: whos_here_r,
                whos_idle: whos_idle_r,
                bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
                dice: dice_statement % random.randint(1, 6)
            }
            if ("identifier" in result) and ("message" in result):
                denty = result["identifier"]
                denty = json.loads(denty)
                room_id = denty["room_id"]
                #print(room_id)
                b = result["message"]
                Thread(target=greet, args=("user_connected", "add", True, b,)).start()
                Thread(target=greet, args=("typing", "add", False, b,)).start()
                Thread(target=greet, args=("user_disconnected", "remove", False, b,)).start()
                Thread(target=greet, args=("messages", "add", False, b,)).start()
                if "messages" in b and "user" in b:
                    user = b["user"]
                    id = str(user["id"])
                    spam_controlling(id)
                    #spam_checker()
                    name = fix_name(user["display_name"])
                    message = fix_message(str(b["messages"]))
                    print(b["user"]["display_name"] + " (%s) :- "%id + message)
                    Thread(target=landmine_checker, args=(message,id)).start()
                    Thread(target=check_greeters, args=(message, id,)).start()
                    Thread(target=log_chats, args=(message, id,)).start()
                    if id not in data["mutelist"]:
                        coins_feelings(message, id, False)
                        matching(fix_name(name),response_dict, message, False)
                        matching(fix_name(name),whos_here_res, message, False)
                    if id in data["admin"]:
                        admin_func(message, id, True)
                    elif id in data["mod"]:
                        admin_func(message, id, False)
    except Exception as e:
        print("Hello young boi an error occurred :- %s" %e)        
        sleep(5)
        pass
