import json
from time import gmtime, strftime, sleep
from ws import send_message
from var import *
from utils import fix_message, return_id

def refresh_data():
    global data
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    
def update_data_json():
    global data
    with open('data.json', 'w') as f:
        json.dump(data, f)
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

def refresh_messages():
    global saved_messages
    with open('messages.json', 'r') as f:
        saved_messages= json.loads(f.read())

def update_messages_json():
    global saved_messages
    with open('messages.json', 'w') as f:
        json.dump(saved_messages, f)
    with open('messages.json', 'r') as f:
        saved_messages = json.loads(f.read())

def refresh_seen():
    global seen_data
    with open('seen.json', 'r') as f:
        seen_data = json.load(f)

def update_seen_json():
    global seen_data
    with open('seen.json', 'w') as f:
        json.dump(seen_data, f)

def update_seen(name,id,username):
    time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    id = str(id)
    if id not in seen_data:
        seen_data[id] = {}
        seen_data[id]["name"] = name
        seen_data[id]["username"] = username
        seen_data[id]["channel_name"] = {"WFAF": time_stamp}
    else:
        seen_data[id]["name"] = name
        seen_data[id]["username"] = username
        seen_data[id]["channel_name"]["WFAF"] = time_stamp
    update_seen_json()

def update_image_cache():
    global image_cache
    with open('image_cache.json', 'w') as f:
        json.dump(image_cache, f)

def refresh_image_cache():
    global image_cache
    with open('image_cache.json', 'r') as f:
        image_cache = json.loads(f.read())

def saved_message_handler(id,name):
    if id in saved_messages:
        if len(saved_messages[id]) ==1:
            message = "Hello %s I have a message for you: %s" % (name, saved_messages[id][0])
            sleep(0.9)
            send_message(message)
            del saved_messages[id]
        else:
            sleep(1)
            message = "Hello %s I have a few messages for you from some people" % name
            send_message(message)
            for messages in saved_messages[id]:
                send_message(messages)
                sleep(0.4)
            del saved_messages[id]
        update_messages_json()


def saving_messages(name, result):
    global saved_messages
    String = result.group(1).rstrip()
    if String.isnumeric():
        id = String
    else:
        id = return_id(String)
    if id is not False:
        if type(id) is not dict:
            if id in saved_messages:
                saved_messages[id].append(name + ":- " + result.group(2))
            else:
                saved_messages[id] = [name + ":- " + result.group(2)]
            print(saved_messages)
            update_messages_json()
            return save_message_r%String
        else:
            if len(id) == 1:
                id = list(id.keys())[0]
                if id in saved_messages:
                    saved_messages[id].append(name + ":- " + result.group(2))
                else:
                    saved_messages[id] = [name + ":- " + result.group(2)]
                update_messages_json()
                print(saved_messages)
                return save_message_r%String
            elif len(id) == 0:
                return not_seen % String
            else:
                return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (result.group(2), fix_message(str(id)).replace("{", "").replace("}", "")))
    else:
        return not_seen % String