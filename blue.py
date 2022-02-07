import datetime
import json
import random
import re
from datetime import datetime
from os import execl
from pathlib import Path
from sys import argv, executable
from threading import Thread
from time import gmtime, perf_counter, sleep, strftime
from timeit import default_timer as timer
from weakref import ref

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError,ImgurClientRateLimitError
from simple_image_download import simple_image_download as simp

response = simp.simple_image_download

#from unidecode import unidecode

import requests
#import emojis
import websocket

from var import *

client_id = '887b16bbc4ae6a7'
client_secret = '4c6b97527a8ede18e1b3e4d2b1b85b3fcf2fcb03'
client = ImgurClient(client_id, client_secret)

with open('data.json', 'r') as f:
    data = json.loads(f.read())
with open('messages.json', 'r') as f:
    saved_messages = json.loads(f.read())
with open('seen.json', 'r') as f:
    seen_data = json.loads(f.read())
with open('image_cache.json', 'r') as f:
    image_cache = json.loads(f.read())


#util
def restart_program():
    update_seen_json()
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    execl(executable, executable, *argv)

#util
def update_data_json():
    global data
    with open('data.json', 'w') as f:
        json.dump(data, f)
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

#util
def refresh_data():
    global data
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

#util
def refresh_messages():
    global saved_messages
    with open('messages.json', 'r') as f:
        saved_messages= json.loads(f.read())

#util
def refresh_seen():
    global seen_data
    with open('seen.json', 'r') as f:
        seen_data = json.loads(f.read())

#util
def update_messages_json():
    global saved_messages
    with open('messages.json', 'w') as f:
        json.dump(saved_messages, f)
    with open('messages.json', 'r') as f:
        saved_messages = json.loads(f.read())

#util
def update_seen_json():
    global seen_data
    with open('seen.json', 'w') as f:
        json.dump(seen_data, f)

#util
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

def update_image_cache():
    global image_cache
    with open('image_cache.json', 'w') as f:
        json.dump(image_cache, f)

def refresh_image_cache():
    global image_cache
    with open('image_cache.json', 'r') as f:
        image_cache = json.loads(f.read())

    
#util
def fix_name(name):
    for chars in forbiden_chars:
        name.replace(chars, '')
    return name

#util
def fix_message(message):
    chars = ('"[]‘')
    for c in chars:
        message = message.replace(c, "")
    for c in forbiden_chars:
        message = message.replace(c, "")
    message.replace(".", ".").replace(".",".​")
    return message

#connection
def send_message(content):
    message = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) + "\",\"id\":null,\"action\":\"speak\"}"}
    message_alt = {"command":"message","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}","data":"{\"message\":\""+fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if alt_unverse_toggle is True:
        ws.send(json.dumps(message_alt))
    else:
        ws.send(json.dumps(message))

def send_seen(id):
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    name = seen_data[id]["name"]
    date = seen_data[id]["time"].split(" ")[0]
    month = date.split("-")[1]
    day = date.split("-")[2]
    deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["time"], "%Y-%m-%d %H:%M:%S")
    if deltatime.days == 0:
        send_message("%s was last seen today %s hours and %s mins ago in WFAF" % (name, deltatime.seconds//3600, deltatime.seconds//60%60))
    elif deltatime.days == 1:
        send_message("%s was last seen yesterday %s hours and %s mins ago in WFAF" % (name, deltatime.seconds//3600, deltatime.seconds//60%60))
    else:
        send_message("%s was last seen on %s %s %s hours and %s mins ago in WFAF" % (name, day, month, deltatime.seconds//3600, deltatime.seconds//60%60))

def get_seen(result):
    string = result.group(1)
    if string.isnumeric():
        id = string
        if id in seen_data:
            send_seen(id)
        else:
            send_message("I dont remember seeing user with ID %s" % str(id))
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
        if len(possibles) == 1:
            send_seen(list(possibles.keys())[0])
        elif n == total :
            send_message("I dont remember seeing user with name %s" % string)
        else:
            send_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name and ask 'Blue seen ID'"% (string, fix_message(str(possibles)).replace("{", "").replace("}", "")))

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

def list_removal(id):
    if id in timeout_control:
        del timeout_control[id]
    if id in list_main_dict:
        del list_main_dict[id]
    if id in idle_main_dict:
        del idle_main_dict[id]

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

def greet(action, result, greet):
    global data,saved_messages
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

def get_jokes():
    r = requests.get(jokes_url)
    if r.status_code == 200:
        joke = json.loads(r.text)["attachments"][0]["text"]
        send_message(joke)
    else:
        send_message("Error: " + str(r.status_code))

def get_quote():
    r = requests.get('https://api.quotable.io/random')
    content = str(r.json()['content'])
    author = "~ by " + str(r.json()['author'])
    send_message(content)
    sleep(0.2)
    send_message(author)


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
    send_message(fix_message(response))


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
    send_message(fix_message(response))

def saving_messages(name, result):
    global saved_messages
    String = result.group(1).rstrip()
    if String.isnumeric():
        id = String
    else:
        id = return_id(String)
    if id is not False:
        if id in saved_messages:
            saved_messages[id].append(name + ":- " + result.group(2))
        else:
            saved_messages[id] = [name + ":- " + result.group(2)]
        update_messages_json()
        send_message(save_message_r%String)
    else:
        send_message(not_seen % String)

"""def get_food_emoji(food):
    #food = result.group(1)
    l = len(food.split())
    if l == 1:
        try: 
            emoji = emojis.db.get_emoji_by_alias(food)
            emoji = emoji.emoji
            print(emoji)
        except AttributeError:
            try:
                emojilist = []
                emoji = emojis.db.get_emojis_by_tag(food)
                for i in emoji:
                    emojilist.append(i)
                print(emojilist[0].emoji)
            except AttributeError :
                #send_message(food_not_found)
                print("Food not found")
            except IndexError:
                print("Food not found")
    elif l > 1:
        result = ""
        allfound = True
        for i in food.split():
            try:
                emoji = emojis.db.get_emoji_by_alias(i)
                emoji = emoji.emoji
                result += emoji
            except AttributeError:
                try:
                    emojilist = []
                    emoji = emojis.db.get_emojis_by_tag(i)
                    for i in emoji:
                        emojilist.append(i)
                    result += emojilist[0].emoji
                except AttributeError :
                    allfound = False
                    pass
                except IndexError:
                    allfound = False
                    pass
        if allfound:
            print(result)
        elif len(result) == 0:
            print("Food not found")
        else :
            print("I could only find some of the food", result)
        
"""

def matching(name,dictname, message):
    global whos_here_res
    keys = list(dictname.keys())
    for i in range(len(keys)):
        re_m = keys[i]
        result = re_m.match(message)
        if result:
            if dictname == whos_here_res:
                if re_m == whos_here:
                    reply_whos_here()
                elif re_m == whos_idle:
                    reply_whos_idle()
                else:
                    send_message(list(dictname.values())[i])
            elif dictname == response_dict:
                if re_m == jok:
                    get_jokes()
                elif re_m == quote:
                    get_quote()
                elif re_m == save_message:
                    saving_messages(name, result)
                else:
                    send_message(list(dictname.values())[i])
            break


def idle_function():
    idle_check = list(timeout_control.values())
    for i in range(len(idle_check)):
        x = idle_check[i]
        if t_start - x >= 240:
            val = list(timeout_control.keys())[i]
            if val in list_main_dict:
                idle_main_dict[val] = list_main_dict[val]
                del list_main_dict[val]
        elif t_start - x < 240:
            val = list(timeout_control.keys())[i]
            if val in idle_main_dict:
                del idle_main_dict[val]


def remove_blue():
    global list_main_dict, idle_main_dict, timeout_control
    if "21550262" in list_main_dict:
        del list_main_dict["21550262"]
    if "21550262" in idle_main_dict:
        del idle_main_dict["21550262"]
    if "21550262" in timeout_control:
        del timeout_control["21550262"]


"""def update_git(mutelist):
    newmute = str(mutelist)
    chars = "[]'\n"
    for c in chars:
        newmute.replace(c, "")
    muted_contents = repo.get_contents("muted.txt")
    repo.update_file(muted_contents.path, "update muted",
                     newmute, muted_contents.sha, branch="main")
"""

def mute_func(result, index):
    global data
    id = result.group(1)
    if index == 12:
        if id in data["mutelist"]:
            response = already_ignoring
        else:
            data["mutelist"].append(id)
            update_data_json()
            response = start_ignoring % id
    elif index == 13:
        if id in data["mutelist"]:
            data["mutelist"].remove(id)
            update_data_json()
            response = stop_ignoring % id
        else:
            response = already_not_ignoring % id
    send_message(response)


def downvote(cookie, id):
    r = requests.get(karma_url % id, cookies=cookie)

def ban_log(banned_id, admin_id):
    r = requests.get(profile_url % int(admin_id), cookies=cookies)
    admin_name = json.loads(r.text)["user"]["display_name"]
    log = admin_name + "(" + str(admin_id) + \
        ")"  " banned " + str(banned_id) + "\n"
    with open("log.txt", "a") as f:
        f.write(log)


def thread(id):
    banned.add(id)
    for c in cookiejar:
        c = c.split(",")
        cookie = {'remember_token': c[0], 'user_id': c[1]}
        Thread(target=downvote, args=(cookie, id)).start()


def fix_file_path(path):
    path.replace(
        'ContentFile(path="', '').replace('")', '')
    return path

def stalker(id, time_now):
    global stalking_log
    filename = str(id) + ".txt"
    git_prefix = "stalker-logs/"
    file = git_prefix + filename
    myfile = Path(file)
    if not myfile.is_file():
        file = open(filename, "w")
        file.close()
    while stalking_log[id][1] is True:
        r = requests.get(profile_url % id, cookies=cookies)
        if r.status_code == 200:
            r = json.loads(r.text)["user"]
            name = r["display_name"]
            karma = r["karma"]
            username = r["username"]
            gender = r["gender"]
            time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
            text = logging_text % (str(time), name, karma, username, gender)
            file = open(filename,"a")
            file.write(text)      
            file.close()
        elif r.status_code == 404 or r is None:
            send_message(stopping_logging % id)
            break
        elif timer() - time_now >= 3600:
            send_message("Ending stalk session of ID: " + id)
            break
        else:
            pass
        sleep(15)
        if stalking_log[id][1] == False:
            del stalking_log[id]
            break

def clear_lists():
    global list_main_dict, idle_main_dict, timeout_control
    send_message(clear_list)
    timeout_control.clear()
    list_main_dict.clear()
    idle_main_dict.clear()


def respond_uptime():
    sr = str(datetime.now() - starttime).split(":")
    if sr[0] == "0":
        if str(int(sr[1])+0) == "0":
            send_message(just_joined)
        elif (int(sr[1])+0) == 1:
            send_message(here_for_one_min)
        else:
            send_message(here_for_x_mins % str(int(sr[1])+0) )
    else:
        send_message(here_for_hours_and_mins % (str(sr[0]), str(int(sr[1]) + 0)))


def send_stats():
    sr = str(datetime.now() - starttime).split(":")
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    response = stats_response % (len(stats), len(stats_list),sr[0],sr[1],str(r))
    send_message(response)

def start_stalking(id): 
    if id not in stalking_log:
        t = Thread(target=stalker, args=(id, timer()))
        stalking_log[id] = [t, True]
        t.start()
        send_message(waking_stalking)
    else:
        send_message(already_stalking%id)

def stop_stalking(id):
    global stalking_log
    if id in stalking_log:
        stalking_log[id][1] = False
        send_message(stopping_stalking % id)
    else: 
        send_message(already_not_stalking % id)

def mod_demod(result):
    global data
    mod_id = result.group(2)
    if result.group(1) == "mod":
        if mod_id in data["mod"] or mod_id in data["admin"]:
            send_message(already_mod % mod_id)
        else:
            data["mod"].append(mod_id)
            send_message(mod_response % mod_id)
            update_data_json()
    elif result.group(1) == "demod":
        if mod_id in data["mod"]:
            data["mod"].remove(mod_id)
            send_message(demod_response % mod_id)
            update_data_json()
        elif mod_id in data["admin"]:
            data["admin"].remove(mod_id)
            send_message(demod_response % mod_id)
            update_data_json()
        else:
            send_message(not_mod % mod_id)

def set_greet(result):
    id = result.group(1)
    greet = result.group(3)
    if id not in data["custom_greet"]:
        data["custom_greet"][id] = greet
        update_data_json()
        send_message(greet_set % (id, greet))
    else:
        data["custom_greet"][id] = greet
        update_data_json()
        send_message(greet_updated % (id, greet))

def get_greet(result):
    id = result.group(1)
    if id in data["custom_greet"]:
        send_message(greet_response % (id, data["custom_greet"][id]))
    else:
        send_message(greet_not_set % id)

def remove_greet(result):
    id = result.group(1)
    if id in data["custom_greet"]:
        del data["custom_greet"][id]
        update_data_json()
        send_message(greet_removed % id)
    else:
        send_message(greet_not_set % id)

def get_landmine():
    landmine_list = data["landmine_words"]
    send_message(fix_message(landmine_list))

def add_landmine(result):
    word = result.group(1)
    if word not in data["landmine_words"]:
        data["landmine_words"].append(word)
        update_data_json()
        send_message(landmine_added % word)
    else:
        send_message(landmine_already_added % word)

def remove_landmine(result):
    word = result.group(1)
    if word in data["landmine_words"]:
        data["landmine_words"].remove(word)
        update_data_json()
        send_message(landmine_removed % word)
    else:
        send_message(landmine_not_present % word)

def toggle_alt_universe():
    global alt_unverse_toggle
    send_message(done)
    if alt_unverse_toggle is False:
        alt_unverse_toggle = True
    elif alt_unverse_toggle is True:
        alt_unverse_toggle = False

def toggle_spam_check():
    global spam_check_toggle
    if spam_check_toggle is False:
        spam_check_toggle = True
        send_message(spam_check_on)
    else:
        spam_check_toggle = False
        send_message(spam_check_off)

def get_spam_check_status():
    if spam_check_toggle is True:
        send_message(spam_check_on)
    else:
        send_message(spam_check_off)

def return_id(string):
    n = 0
    for id in seen_data:
        name = seen_data[id]["name"]
        username = seen_data[id]["username"]
        regex1 = re.compile(string, re.IGNORECASE)
        n+=1
        if regex1.search(name) or regex1.search(username):
            return(id)
            break
        else: 
            pass
    if n == len(seen_data):
        for id in data["nickname"]:
            for nickanme in data["nickname"][id]:
                regex2 = re.compile(string, re.IGNORECASE)
                n+=1
                if regex2.search(nickanme):
                    return(id)
                    break
                else:
                    pass
    total = len(seen_data) 
    for id in data["nickname"]:
        total+=len(data["nickname"][id])
    if n == total:
        return(False)

def make_knight(result):
    name = result.group(1)
    if name.isnumeric():
        id = name
        if id not in data["knight"]:
            data["knight"].append(id)
            update_data_json()
            send_message(knight_added % name)
        else:
            send_message(knight_already_added % name)
    else:
        id = return_id(name)
        if id is False:
            send_message(not_seen % name)
        else:
            if id not in data["knight"]:
                data["knight"].append(id)
                update_data_json()
                send_message(knight_added % name)
            else:
                send_message(knight_already_added % name)

def remove_knight(result):
    name = result.group(1)
    if name.isnumeric():
        id = name
        if id in data["knight"]:
            data["knight"].remove(id)
            update_data_json()
            send_message(knight_removed % name)
        else:
            send_message(knight_not_added % name)
    else:
        id = return_id(name)
        if id is False:
            send_message(not_seen % name)
        else:
            if id in data["knight"]:
                data["knight"].remove(id)
                update_data_json()
                send_message(knight_removed % name)
            else:
                send_message(knight_not_added % name)

def toggle_shortened_greet():
    global shorten_greet_toggle
    if shorten_greet_toggle is False:
        shorten_greet_toggle = True
        send_message(shortened_greet_on)
    else:
        shorten_greet_toggle = False
        send_message(shortened_greet_off)

def save_nickname(result):
    name = result.group(1)
    nickname = result.group(2)
    if name.isnumeric():
        id = name
        if id not in data["nickname"]:
            data["nickname"][id] = [nickname]
            update_data_json()
            send_message(nickname_added % (nickname, name))
        else:
            data["nickname"][id].append(nickname)
            update_data_json()
            send_message(nickname_updated % (nickname , name))
    else:
        id = return_id(name)
        if id is False:
            send_message(not_seen % name)
        else:
            if id not in data["nickname"]:
                data["nickname"][id] = [nickname]
                update_data_json()
                send_message(nickname_added % (nickname, name))
            else:
                data["nickname"][id].append(nickname)
                update_data_json()
                send_message(nickname_updated % (nickname, name))


def admin_function_init(i, id , isadmin, result):
    global greet_status, running, name, starttime, aichatstate,greet_timeout, data
    if i == 0:
        greet_status = True 
        send_message(done)
    elif i == 1:
        if greet_status is True:
            greet_status = False
            send_message(done)
        else:
            send_message(already_not_greeting)
    elif i == 2 and isadmin:
        send_message(leaving)
        running = False
    elif i == 3 and isadmin: 
        clear_lists()
    elif i == 4:
        respond_uptime()
    elif i == 5:
        greet_timeout = {}
        send_message(done)
    elif i == 6:
        send_stats()
    elif i == 7 and isadmin:
        send_message(fix_message(str(data["mutelist"])))
    elif i == 8 and isadmin:
        send_message(str(timeout_control))
    elif i == 9:
        send_message(restarting)
        restart_program()
    elif i == 10 and isadmin:
        del timeout_control[id]
        if id in list_main_dict :
            del list_main_dict[id]
        if id in idle_main_dict:
            del idle_main_dict[id]
        send_message(aye_aye)
    elif i == 11 and id not in data["mutelist"]:
        send_message(ily_r)
    elif i == 12 or i == 13:
        mute_func(result,i)
    elif i == 14 and isadmin:
        id_ban = result.group(1)
        thread(id_ban)
        Thread(target = ban_log, args = (id_ban,id,)).start()
        send_message(banning_response % id_ban)
    elif i == 15:
        send_message(fix_message(str(data["admin"])))
    elif i == 16:
        start_stalking(str(result.group(2)))
    elif i == 17:
        stop_stalking(str(result.group(2)))
    elif i == 18:
        if not stalking_log:
            send_message(stalking_no_one)
        else:
            send_message(stalking_following % fix_message(str(stalking_log.keys())))
    elif i == 19:
        aichatstate = True
        send_message(done)
    elif i == 20:
        aichatstate = False
        send_message(done)
    elif i == 21 and id == "16986137":
        mod_demod(result)
    elif i == 22:
        refresh_data()
        send_message(done)
    elif i == 23 :
        refresh_messages()
        send_message(done)
    elif i == 24 and isadmin:
        set_greet(result)
    elif i == 25 and isadmin:
        get_greet(result)
    elif i == 26 and isadmin:
        remove_greet(result)
    elif i == 27 and isadmin:
        add_landmine(result)
    elif i == 28 and isadmin:
        remove_landmine(result)
    elif i == 29 and isadmin:
        get_landmine()
    elif i == 30 and id == "16986137":
        toggle_alt_universe()
    elif i == 31 and isadmin:
        toggle_spam_check()
    elif i == 32 and isadmin:
        get_spam_check_status()
    elif i == 33 and isadmin:
        make_knight(result)
    elif i == 34 and isadmin:
        remove_knight(result)
    elif i == 35 and isadmin:
        toggle_shortened_greet()
    elif i == 36 and isadmin:
        save_nickname(result)

def admin_func(message, id , isadmin):
    for i in range(len(admin_commands)):
        result = admin_commands[i].match(message)
        if result:
            admin_function_init(i, id, isadmin, result) 
            
def image_upload(query,urly):
    global client
    found = False
    if query in image_cache:
        return image_cache[query][1]
    for i in image_cache:
        if image_cache[i][0] == urly:
            found = True
            print(image_cache[i][1])
            return image_cache[i][1]
            break
            
    if found is False:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://","")
        formattedlink = "Image: " + link
        image_cache[query] = [urly,formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink

def processing(query,url):
    """if query in image_cache:
        return image_upload(image_cache[query])
    elif url in image_cache.values():
        return image_upload(url)
    else:
        image_cache[query] = url
        update_image_cache()
        refresh_image_cache()"""
    return image_upload(query,url)

def get_image_link(query):
    url =  response().urls(query, 6)
    try:
        return image_upload(query,url[-1])
    except ImgurClientError:
        send_message("Sorry I couldn't find %s" % query)
        pass
    except ImgurClientRateLimitError:
        send_message("Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying")
        pass
def send_pic(query):
    send_message(fix_message(get_image_link(query)))


def coin_handling(result):
    global data
    num = result.group(1)
    coin_add = int(num)
    #coins_contents = repo.get_contents("coins.txt")
    if (coin_add <= 100) and (coin_add >= 1):
        data["coins"] = coin_add + data["coins"]
        update_data_json()
        #old github fuckery to update the file
        """repo.update_file(coins_contents.path, "coins update", str(
            coin_new), coins_contents.sha, branch="main")"""
        if num == "1":
            send_message(adding_one_coin % (coin_add + 0, data["coins"]))
        else:
            send_message(adding_coins % (coin_add + 0, data["coins"]))
    elif coin_add > 100:
        send_message(too_many_coins)

def get_id(result):
    String = result.group(4) 
    id = return_id(String)
    if id is False:
        send_message(not_seen % String)
    else:
        send_message(id_response % (String,id))

"""def get_id(result):
    name = result.group(4)
    if not name.isnumrix():
        regex1 = re.compile(r"^" + name + "\\n*", re.I)"""
        
def get_details(result):
    id = int(result.group(2))
    r = requests.get(profile_url % id, cookies = cookies)
    if r.status_code == 200:
        r = json.loads(r.text)["user"]
        name = r["display_name"]
        karma = r["karma"]
        username = r["username"]
        gender = r["gender"]
        created = r["created_at"].split("T")
        if gender is None:
            response = details_response_null_gender%(id,name,username,created[0],created[1])
        else:
            response = details_response % (id, name, username, karma, gender, created[0], created[1])
    elif r.status_code == 404 or id is None:
        response = account_deleted
    elif r.status_code == 403:
        response = timeout_error
    send_message(response)

def send_feelings(index, id, result):
    global data
    name = result.group(1)
    if index ==1:
        response = sending_love % name
        send_message(response)
    elif index == 2:
        response = sending_pats % name
        send_message(response)
    elif index == 3:
        name = result.group(4)
        response = sending_hugs % name
        send_message(response)
    elif index == 4:
        response = sending_bonks % name
        send_message(response)
    elif index == 5 and id in data["admin"]:
        get_id(result)
    elif index == 6 and str(id) in data["admin"]:
        get_details(result)   
    elif index == 7:
        get_seen(result)
    elif index == 8:
        query = result.group(1)
        Thread(target=send_pic, args=(query,)).start()

def dis_en_greets(id):
    global greet_status
    if id == "16008266" and greet_status == True:
        send_message(disabling_greet)
        greet_status = False
    elif id == "20909261" and greet_status == False:
        send_message(re_enabling_greet)
        greet_status = True

def check_greeters(message, id):
    global greet_status,data
    found = False
    if id in data["greeter_fallback"]:
        for reg_m in greet_check:
            result = reg_m.search(message)
            if message in data["custom_greet"].values() or result or message == blue_greet:
                dis_en_greets(id)
                found = True
                break
        if found is False:
            for reg_m in data["custom_greet"].values():
                reg = re.compile(r"" + reg_m + r"", re.I)
                result = reg.search(message)
                if result:
                    dis_en_greets(id)
                    break

def coins_feelings(message, id):
    for reg_m in coinsandfeelings:
        result = reg_m.match(message)
        if result:
            index = coinsandfeelings.index(reg_m)
            if index == 0:
                coin_handling(result)
            else:
                send_feelings(index, id, result)
            break

def log_chats(message, user_id):
    date = datetime.today().strftime('%d-%m-%Y')
    filename = "wfaf-logs/log (%s).txt" % date
    myfile = Path(filename)
    if myfile.is_file():
        name = fix_name(user["display_name"])
        log = fix_message(message_log_text % (name, user_id, message)) + "\n"
        file = open(filename, "a")
        file.write(log)
        file.close()
    else:
        file = open(filename, "w")
        file.close()
        log_chats(message, user_id)

def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")


def check_singing():
    l = len(timeout_control)
    if l <= 4 and random.randint(0, 100000) % 93870 == 0:
        Thread(target=singing).start()

def clocking():
    global reset_clock, greet_timeout
    if reset_clock == 500:
        greet_timeout, reset_clock = {}, 0

def landmine_checker(message,id):
    for word in data["landmine_words"]:
        regex1 = re.compile(r"%s"% word, re.I)
        if regex1.search(message):
           thread(id)
           break

def spam_controlling(id):
    global spam_timeout
    if id in spam_timeout:
        spam_timeout[id].append(perf_counter())
    else:
        spam_timeout[id] = [perf_counter()]

def spam_checker():
    for id in spam_timeout:
        if len(spam_timeout[id]) >= 3 and spam_timeout[id][-1] - spam_timeout[id][-3] < 1.3:
            if id not in banned:
                thread(id)
                break
        elif len(spam_timeout[id]) >= 5 and spam_timeout[id][-1] - spam_timeout[id][-5] < 3:
            if id not in banned:
                thread(id)
                break

'''def repeated_words_appender(id,message):
    global repeated_msg
    if id in repeated_msg:
        repeated_msg[id].append(message)
    else:
        repeated_msg[id] = [message]

def repetition_spam_control():
    global repeated_msg
    for id in repeated_msg:
        if len(repeated_msg[id]) >= 3 and repeated_msg[id][-1] == repeated_msg[id][-3]:
            warned.add(id)
            send_message(repeated_message_warning % id )
        elif len(repeated_msg[id]) >= 5 and repeated_msg[id][-1] == repeated_msg[id][-5]:
            if id not in banned and id in warned:
                thread(id)
                break'''

while True:
    try:
        websocket.enableTrace(False)
        ws = websocket.WebSocket()
        ws.connect(ws_url, cookie=main_cookie, subprotocols=subprots, origin=origin)
        ws.send(json.dumps(connect_json))
        ws.send(json.dumps(connect_json_blue))
        while running is True:
            update_seen_json()
            t_start = perf_counter() #start time
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
                b = result["message"]
                Thread(target=greet, args=("user_connected", "add", True,)).start()
                Thread(target=greet, args=("typing", "add", False,)).start()
                Thread(target=greet, args=("user_disconnected", "remove", False,)).start()
                Thread(target=greet, args=("messages", "add", False,)).start()
                if "messages" in b and "user" in b:
                    user = b["user"]
                    id = str(user["id"])
                    spam_controlling(id)
                    spam_checker()
                    name = fix_name(user["display_name"])
                    message = fix_message(str(b["messages"]))
                    print(b["user"]["display_name"] + ":- " + message)
                    Thread(target=landmine_checker, args=(message,id)).start()
                    Thread(target=check_greeters, args=(message, id,)).start()
                    Thread(target=log_chats, args=(message, id,)).start()
                    if id not in data["mutelist"]:
                        coins_feelings(message, id)
                        matching(fix_name(name),response_dict, message)
                        matching(fix_name(name),whos_here_res, message)
                    if id in data["admin"]:
                        admin_func(message, id, True)
                    elif id in data["mod"]:
                        admin_func(message, id, False)
    except Exception as e:
        print("Hello young boi an error occurred :- %s" %e)        
        sleep(5)
        pass
