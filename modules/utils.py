from os import execl
from sys import argv, executable
from time import gmtime, perf_counter, sleep, strftime
import json
from var import *

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    execl(executable, executable, *argv)

def refresh_data():
    global data
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

def update_data_json():
    global data
    with open('data.json', 'w') as f:
        json.dump(data, f)
    refresh_data()

def refresh_messages():
    global saved_messages
    with open('messages.json', 'r') as f:
        saved_messages= json.loads(f.read())

def update_messages_json():
    global saved_messages
    with open('messages.json', 'w') as f:
        json.dump(saved_messages, f)
    refresh_messages()

def refresh_seen():
    global seen_data
    with open('seen.json', 'r') as f:
        seen_data = json.loads(f.read())

def update_seen_json():
    global seen_data
    with open('seen.json', 'w') as f:
        json.dump(seen_data, f)
    refresh_seen()

def update_seen(name,id,username):
    time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    id = int(id) 
    if id not in seen_data:
        seen_data[id] = {}
        seen_data[id]["name"] = name
        seen_data[id]["username"] = username
        seen_data[id]["time"] = time_stamp
    else:
        seen_data[id]["name"] = name
        seen_data[id]["username"] = username
        seen_data[id]["time"] = time_stamp
    update_seen_json()
    refresh_seen()

def fix_name(name):
    for chars in forbiden_chars:
        name.replace(chars, '')
    return name

def fix_message(messages):
    chars = ('"[]‘')
    for c in chars:
        messages = messages.replace(c, "")
    for c in forbiden_chars:
        messages = messages.replace(c, "")
    return messages
