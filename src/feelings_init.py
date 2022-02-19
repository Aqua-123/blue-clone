from src.feelings import *
from var import *
from threading import Thread
from src.last_seen import *
from src.image_upload import *

def send_feelings(index, id, result,console):
    global data
    name = result.group(1)
    response = ""
    if index ==1:
        response = sending_love % name
    elif index == 2:
        response = sending_pats % name
    elif index == 3:
        name = result.group(4)
        response = sending_hugs % name
    elif index == 4:
        response = sending_bonks % name
    elif index == 5 and (id in data["admin"] or console is True):
        response = get_id(result)
    elif index == 6 and (str(id) in data["admin"] or console is True):
        response = get_details(result)   
    elif index == 7:
        response = get_seen(result)
    elif index == 8:
        query = result.group(1)
        Thread(target=send_pic, args=(query,)).start()
    elif index == 9:
        Thread(target=get_meme_link).start()
    return response

def coins_feelings(message, id, console):
    for reg_m in coinsandfeelings:
        result = reg_m.match(message)
        if result:
            index = coinsandfeelings.index(reg_m)
            if index == 0:
                response = coin_handling(result)
            else:
                response = send_feelings(index, id, result,True)
            if response != "":
                if console:
                    print("Console:-%s"%response)
                else:
                    send_message(response)
            break