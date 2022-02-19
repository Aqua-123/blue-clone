from var import *
from threading import Thread
from os import execl
from sys import argv, executable
from time import perf_counter, sleep, strftime, gmtime
import json 
import random
from imgurpython.helpers.error import (ImgurClientError,
                                       ImgurClientRateLimitError)

from time import perf_counter
import requests
import json
from pathlib import Path
from timeit import default_timer as timer
from threading import Thread

def send_message(content):
    message = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) +"\",\"id\":null,\"action\":\"speak\"}"}
    message_alt = {"command":"message","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}","data":"{\"message\":\""+fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if alt_unverse_toggle is True:
        ws.send(json.dumps(message_alt))
    else:
        ws.send(json.dumps(message))

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

def downvote(cookie, id):
    requests.get(karma_url % id, cookies=cookie)

def ban_log(banned_id, admin_id):
    print(admin_id)
    if admin_id != 0:
        r = requests.get(profile_url % int(admin_id), cookies=cookies)
        admin_name = json.loads(r.text)["user"]["display_name"]
    else:
        admin_name = "Console Admin"
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
    return response

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


def respond_uptime():
    sr = str(datetime.now() - starttime).split(":")
    if sr[0] == "0":
        if str(int(sr[1])+0) == "0":
            return just_joined
        elif (int(sr[1])+0) == 1:
            return here_for_one_min
        else:
            return here_for_x_mins % str(int(sr[1])+0)
    else:
        return here_for_hours_and_mins % (str(sr[0]), str(int(sr[1]) + 0))


def send_stats():
    sr = str(datetime.now() - starttime).split(":")
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    return stats_response % (len(stats), len(stats_list),sr[0],sr[1],str(r))
    
def start_stalking(id): 
    if id not in stalking_log:
        t = Thread(target=stalker, args=(id, timer()))
        stalking_log[id] = [t, True]
        t.start()
        return waking_stalking
    else:
        return already_stalking%id

def stop_stalking(id):
    global stalking_log
    if id in stalking_log:
        stalking_log[id][1] = False
        return stopping_stalking % id
    else: 
        return already_not_stalking % id

def mod_demod(result):
    global data
    mod_id = result.group(2)
    if result.group(1) == "mod":
        if mod_id in data["mod"] or mod_id in data["admin"]:
            return already_mod % mod_id
        else:
            data["mod"].append(mod_id)
            update_data_json()
            return mod_response % mod_id
    elif result.group(1) == "demod":
        if mod_id in data["mod"]:
            data["mod"].remove(mod_id)
            update_data_json()
            return demod_response % mod_id
        elif mod_id in data["admin"]:
            data["admin"].remove(mod_id)
            update_data_json()
            return demod_response % mod_id
        else:
            return not_mod % mod_id

def clear_lists():
    global list_main_dict, idle_main_dict, timeout_control
    timeout_control.clear()
    list_main_dict.clear()
    idle_main_dict.clear()
    return clear_list


def set_greet(result):
    id = result.group(1)
    greet = result.group(3)
    if id not in data["custom_greet"]:
        data["custom_greet"][id] = greet
        update_data_json()
        return greet_set % (id, greet)
    else:
        data["custom_greet"][id] = greet
        update_data_json()
        return greet_updated % (id, greet)

def get_greet(result):
    id = result.group(1)
    if id in data["custom_greet"]:
        return greet_response % (id, data["custom_greet"][id])
    else:
        return greet_not_set % id

def remove_greet(result):
    id = result.group(1)
    if id in data["custom_greet"]:
        del data["custom_greet"][id]
        update_data_json()
        return greet_removed % id
    else:
        return greet_not_set % id

def get_landmine():
    landmine_list = data["landmine_words"]
    return fix_message(landmine_list)

def add_landmine(result):
    word = result.group(1)
    if word not in data["landmine_words"]:
        data["landmine_words"].append(word)
        update_data_json()
        return landmine_added % word
    else:
        return landmine_already_added % word

def remove_landmine(result):
    word = result.group(1)
    if word in data["landmine_words"]:
        data["landmine_words"].remove(word)
        update_data_json()
        return landmine_removed % word
    else:
        return landmine_not_present % word

def toggle_alt_universe():
    global alt_unverse_toggle
    if alt_unverse_toggle is False:
        alt_unverse_toggle = True
    elif alt_unverse_toggle is True:
        alt_unverse_toggle = False

def toggle_spam_check():
    global spam_check_toggle
    if spam_check_toggle is False:
        spam_check_toggle = True
        return spam_check_on
    else:
        spam_check_toggle = False
        return spam_check_off

def get_spam_check_status():
    if spam_check_toggle is True:
        return spam_check_on
    else:
        return spam_check_off

def make_knight(result):
    name = result.group(1)
    if name.isnumeric():
        id = name
        if id not in data["knight"]:
            data["knight"].append(id)
            update_data_json()
            return knight_added % name
        else:
            return knight_already_added % name
    else:
        id = return_id(name)
        if id is False:
            return not_seen % name
        else:
            if type(id) is not dict:
                if id not in data["knight"]:
                    data["knight"].append(id)
                    update_data_json()
                    return knight_added % name
                else:
                    return knight_already_added % name
            else:
                if len(id) == 1:
                    id = list(id.keys())[0]
                    if id not in data["knight"]:
                        data["knight"].append(id)
                        update_data_json()
                        return knight_added % name
                    else:
                        return knight_already_added % name
                elif len(id) == 0:
                    return not_seen % name
                else:
                    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (name, fix_message(str(id)).replace("{", "").replace("}", "")))

def remove_knight(result):
    name = result.group(1)
    if name.isnumeric():
        id = name
        if id in data["knight"]:
            data["knight"].remove(id)
            update_data_json()
            return knight_removed % name
        else:
            return knight_not_added % name
    else:
        id = return_id(name)
        if id is False or (type(id) is dict and len(id) == 0):
            return not_seen % name
        else:
            if type(id) is not dict:
                if id in data["knight"]:
                    data["knight"].remove(id)
                    update_data_json()
                    return knight_removed % name
                else:
                    return knight_not_added % name
            else:
                if len(id) == 1:
                    id = list(id.keys())[0]
                    if id in data["knight"]:
                        data["knight"].remove(id)
                        update_data_json()
                        return knight_removed % name
                    elif len(id) == 0:
                        return not_seen % name
                    else:
                        return knight_not_added % name
                else:
                    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (name, fix_message(str(id)).replace("{", "").replace("}", "")))


def toggle_shortened_greet():
    global shorten_greet_toggle
    if shorten_greet_toggle is False:
        shorten_greet_toggle = True
        return shortened_greet_on
    else:
        shorten_greet_toggle = False
        return shortened_greet_off

def save_nickname(result):
    name = result.group(1)
    nickname = result.group(2)
    if name.isnumeric():
        id = name
        if id not in data["nickname"]:
            data["nickname"][id] = [nickname]
            update_data_json()
            return nickname_added % (nickname, name)
        else:
            data["nickname"][id].append(nickname)
            update_data_json()
            return nickname_updated % (nickname , name)
    else:
        id = return_id(name)
        if id is False or (type(id) is dict and len(id) == 0):
            return not_seen % name
        else:
            if type(id) is not dict:
                if id not in data["nickname"]:
                    data["nickname"][id] = [nickname]
                    update_data_json()
                    return nickname_added % (nickname, name)
                else:
                    data["nickname"][id].append(nickname)
                    update_data_json()
                    return nickname_updated % (nickname, name)
            else:
                if len(id) == 1:
                    id = list(id.keys())[0]
                    if id not in data["nickname"]:
                        data["nickname"][id] = [nickname]
                        update_data_json()
                        return nickname_added % (nickname, name)
                    else:
                        data["nickname"][id].append(nickname)
                        update_data_json()
                        return nickname_updated % (nickname, name)
                else:
                    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (name, fix_message(str(id)).replace("{", "").replace("}", "")))

def admin_function_init(i, id , isadmin, result):
    global greet_status, running, name, starttime, aichatstate, greet_timeout, data
    if i == 0:
        greet_status = True 
        response = done
    elif i == 1:
        if greet_status is True:
            greet_status = False
            response = done
        else:
            response = already_not_greeting
    elif i == 2 and isadmin:
        response = leaving
        running = False
    elif i == 3 and isadmin: 
        response = clear_lists()
    elif i == 4:
        response = respond_uptime()
    elif i == 5:
        greet_timeout = {}
        response = done
    elif i == 6:
        response = send_stats()
    elif i == 7 and isadmin:
        response = fix_message(str(data["mutelist"]))
    elif i == 8 and isadmin:
        response = str(timeout_control)
    elif i == 9:
        response = restarting
        restart_program()
    elif i == 10 and isadmin:
        del timeout_control[id]
        if id in list_main_dict :
            del list_main_dict[id]
        if id in idle_main_dict:
            del idle_main_dict[id]
        response = aye_aye
    elif i == 11 and id not in data["mutelist"]:
        response = ily_r
    elif i == 12 or i == 13:
        response = mute_func(result,i)
    elif i == 14 and isadmin:
        id_ban = result.group(1)
        thread(id_ban)
        Thread(target = ban_log, args = (id_ban,id,)).start()
        response = banning_response % id_ban
    elif i == 15:
        response = fix_message(str(data["admin"]))
    elif i == 16:
        response = str(result.group(2))
    elif i == 17:
        response = stop_stalking(str(result.group(2)))
    elif i == 18:
        if not stalking_log:
            response =  stalking_no_one
        else:
            response = stalking_following % fix_message(str(stalking_log.keys()))
    elif i == 19:
        aichatstate = True
        response = done
    elif i == 20:
        aichatstate = False
        response = done
    elif i == 21 and id == "0":
        response = mod_demod(result)
    elif i == 22:
        refresh_data()
        response = done
    elif i == 23 :
        refresh_messages()
        response = done
    elif i == 24 and isadmin:
        response = set_greet(result)
    elif i == 25 and isadmin:
        response = get_greet(result)
    elif i == 26 and isadmin:
        response = remove_greet(result)
    elif i == 27 and isadmin:
        response = add_landmine(result)
    elif i == 28 and isadmin:
        response = remove_landmine(result)
    elif i == 29 and isadmin:
        response = get_landmine()
    elif i == 30 and (id == "0" or id == "16986137"):
        toggle_alt_universe()
        response = done
    elif i == 31 and isadmin:
        response = toggle_spam_check()
    elif i == 32 and isadmin:
        response = get_spam_check_status()
    elif i == 33 and isadmin:
        response = make_knight(result)
    elif i == 34 and isadmin:
        response = remove_knight(result)
    elif i == 35 and isadmin:
        response = toggle_shortened_greet()
    elif i == 36 and isadmin:
        response = save_nickname(result)
    if int(id) != 0:
        send_message(response)
    else: 
        if response:
            print("Admin Command: " + response)

def admin_func(message, id , isadmin):
    global greet_status, running, name, starttime, aichatstate,greet_timeout, data
    for i in range(len(admin_commands)):
        result = admin_commands[i].match(message)
        if result:
            admin_function_init(i, id, isadmin, result) 

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
        if id not in banned:
            if len(spam_timeout[id]) >= 3 and spam_timeout[id][-1] - spam_timeout[id][-3] < 1.3:
                    thread(id)
                    break
            elif len(spam_timeout[id]) >= 5 and spam_timeout[id][-1] - spam_timeout[id][-5] < 3:
                    thread(id)
                    break

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
            
    if found is False:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://","")
        formattedlink = "Image: " + link
        image_cache[query] = [urly,formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink

        
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
            
    if found is False:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://","")
        formattedlink = "Image: " + link
        image_cache[query] = [urly,formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink

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
    send_message(get_image_link(query))

def get_meme():
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    r = json.loads(r.text)
    link = r["url"]
    image = client.upload_from_url(link)
    link = image["link"].replace("https://","")
    formattedlink = "Image: " + link
    return formattedlink

def get_meme_link():
    try:
        send_message(get_meme())
    except ImgurClientError:
        send_message("Sorry I couldn't find a meme")
        pass
    except ImgurClientRateLimitError:
        send_message("Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying")
        pass

def send_seen(id):
    refresh_seen()
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    name = seen_data[id]["name"]
    username = seen_data[id]["username"]
    if "WFAF" in seen_data[id]["channel_name"]:
        lastseen_list = {}
        for key in seen_data[id]["channel_name"]:
            date = seen_data[id]["channel_name"][key]
            lastseen_list[date] = key
        date = max(lastseen_list)
        channel_name = lastseen_list[date]
        if channel_name == "WFAF":
            date = seen_data[id]["channel_name"]["WFAF"].split(" ")[0]
            month = date.split("-")[1]
            day = date.split("-")[2]
            deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
            if deltatime.days == 0:
                if deltatime.seconds//3600 == 0:
                    if deltatime.seconds//60%60 == 0:
                        response = "%s (#%s) was last seen today just now in WFAF" % (name, username)
                    else:
                        response = "%s (#%s) was last seen today %s mins ago in WFAF" % (name, username, deltatime.seconds//60%60)
                else:
                    response = "%s (#%s) was last seen today %s hours and %s mins ago in WFAF" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60)
            elif deltatime.seconds//3600 == 1: 
                response = "%s (#%s) was last seen yesterday %s hours and %s mins ago in WFAF" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60)
            else:
                if deltatime.seconds//3600 == 0:
                    response = "%s (#%s) was last seen on %s %s %s mins ago in WFAF" % (name, username, day, month, deltatime.seconds//60%60)
                else:
                    response = "%s ($%s) was last seen on %s %s %s hours and %s mins ago in WFAF" % (name, username, day, month, deltatime.seconds//3600, deltatime.seconds//60%60)
        else:
            date_wfaf = seen_data[id]["channel_name"]["WFAF"].split(" ")[0]
            month_wfaf = date_wfaf.split("-")[1]
            day_wfaf = date_wfaf.split("-")[2]
            date_channel = seen_data[id]["channel_name"][channel_name].split(" ")[0]
            month_channel = date_channel.split("-")[1]
            day_channel = date_channel.split("-")[2]
            deltatime_wfaf = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
            deltatime_channel = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"][channel_name], "%Y-%m-%d %H:%M:%S")
            if deltatime_wfaf.days == 0:
                if deltatime_wfaf.seconds//3600 == 0:
                    if deltatime_wfaf.seconds//60%60 == 0:
                        response_wfaf = "%s (#%s) was last seen today just now in WFAF" % (name, username)
                    else:
                        response_wfaf = "%s (#%s) was last seen today %s mins ago in WFAF" % (name, username, deltatime_wfaf.seconds//60%60)
                else:
                    response_wfaf = "%s (#%s) was last seen today %s hours and %s mins ago in WFAF" % (name, username, deltatime_wfaf.seconds//3600, deltatime_wfaf.seconds//60%60)
            elif deltatime_wfaf.seconds//3600 == 1:
                response_wfaf = "%s (#%s) was last seen yesterday %s hours and %s mins ago in WFAF" % (name, username, deltatime_wfaf.seconds//3600, deltatime_wfaf.seconds//60%60)
            else:
                if deltatime_wfaf.seconds//3600 == 0:
                    response_wfaf = "%s (#%s) was last seen on %s %s %s mins ago in WFAF" % (name, username, day_wfaf, month_wfaf, deltatime_wfaf.seconds//60%60)
                else:
                    response_wfaf = "%s ($%s) was last seen on %s %s %s hours and %s mins ago in WFAF" % (name, username, day_wfaf, month_wfaf, deltatime_wfaf.seconds//3600, deltatime_wfaf.seconds//60%60)

            if deltatime_channel.days == 0:
                if deltatime_channel.seconds//3600 == 0:
                    if deltatime_channel.seconds//60%60 == 0:
                        response_channel = " but was more recently seen today just now in %s" % (channel_name)
                    else:
                        response_channel = " but was more recently seen today %s mins ago in %s" % (deltatime_channel.seconds//60%60, channel_name)
                else:
                    response_channel = " but was more recently seen today %s hours and %s mins ago in %s" % (deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            elif deltatime_channel.seconds//3600 == 1:
                response_channel = " but was more recently seen yesterday %s hours and %s mins ago in %s" % (deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            else:
                if deltatime_channel.seconds//3600 == 0:
                    response_channel = " but was more recently seen on %s %s %s mins ago in %s" % (day_channel, month_channel, deltatime_channel.seconds//60%60, channel_name)
                else:
                    response_channel = " but was more recently seen on %s %s %s hours and %s mins ago in %s" % (day_channel, month_channel, deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            response = response_wfaf + response_channel

    else:
        lastseen_list = {}
        for key in seen_data[id]["channel_name"]:
            date = seen_data[id]["channel_name"][key]
            lastseen_list[date] = key
        date = max(lastseen_list)
        month = date.split("-")[1]
        day =  date.split("-")[2]
        channel = lastseen_list[date]
        time = seen_data[id]["channel_name"][channel].split(" ")[1]
        deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        if deltatime.days == 0:
            if deltatime.seconds//3600 == 0:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen today %s mins ago in %s" % (name, username, deltatime.seconds//60%60, channel)
            else:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen today %s hours and %s mins ago in %s" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60, channel)
        elif deltatime.seconds//3600 == 1:
            response = "I dont remember seeing %s (#%s) in WFAF but they were last seen yesterday %s hours and %s mins ago in %s" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60, channel)
        else:
            if deltatime.seconds//3600 == 0:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen on %s %s %s mins ago in %s" % (name, username, day, month, deltatime.seconds//60%60, channel)
            else:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen on %s %s %s hours and %s mins ago in %s" % (name, username, day, month, deltatime.seconds//3600, deltatime.seconds//60%60, channel)
    return fix_message(response)
def log_chats(message, user_id, user):
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

def thread_function():
    global seen_data
    ws_url = "wss://www.emeraldchat.com/cable"
    origin = "https://www.emeraldchat.com"
    subprots = ["actioncable-v1-json", "actioncable-unsupported"]

    cookie = "user_id=MjExNzQ2MDg%3D--a4763efe1b8631066fdee681d54eec7ba278ca9e"
    list_id =  ["48","56","33","39","38","40","34","51","58","57","41","54","37","53","43","42","49","55","59","44","46","36","60","52","32","50","47","35","45"]
    channel_dict = {'48': 'ice squad ❄️', '56': 'noodle squad 🍜 ', '33': 'roleplaying', '39': 'moon squad 🌑', '38': 'sun squad ☀️', '40': 'conspiracy squad 👽', '34': 'VIP ⭐', '51': 'banana squad 🍌', '58': 'sushi squad 🍣', '57': 'pizza squad 🍕', '41': 'film squad 🍿', '54': 'dragon squad 🐉️', '37': 'pie squad 🥧', '53': 'magic squad 🔮️', '43': 'cake squad 🍰', '42': 'love squad 💘', '49': 'strawberry squad 🍓', '55': 'royal squad 👑', '59': 'bomb squad 💣', '44': 'earth squad 🌎', '46': 'water squad 💧', '36': 'brain squad 🧠', '60': 'owl squad 🦉', '52': 'cosmic squad 🌌', '32': 'general', '50': 'apple squad 🍎', '47': 'lightning squad ⚡', '35': 'air squad 🌪️', '45': 'fire squad 🔥'}

    with open('seen.json', 'r') as f:
        seen_data = json.loads(f.read())

    def update_seen_json():
        global seen_data
        with open('seen.json', 'w') as f:
            json.dump(seen_data, f)

    def update_seen(name,id,username,room_id):
        time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        id = str(id)
        if id not in seen_data:
            seen_data[id] = {}
            seen_data[id]["name"] = name
            seen_data[id]["username"] = username
            seen_data[id]["channel_name"] = {}
            seen_data[id]["channel_name"][channel_dict[room_id]] = time_stamp
        else:
            seen_data[id]["name"] = name
            seen_data[id]["username"] = username
            seen_data[id]["channel_name"][channel_dict[room_id]] = time_stamp
        update_seen_json()

    def connect(n):
        connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n +"\"}"}
        ws.send(json.dumps(connect_json))

    websocket.enableTrace(False)
    ws = websocket.WebSocket()
    ws.connect(ws_url, cookie=cookie, subprotocols=subprots, origin=origin)
    while True:
        try:
            websocket.enableTrace(False)
            ws = websocket.WebSocket()
            ws.connect(ws_url, cookie=cookie, subprotocols=subprots, origin=origin)
            for i in range (0,len(list_id)):
                n = list_id[i]
                connect(n)
            from cl import cl
            cl()
            while True:
                result = ws.recv() #receive message
                result = json.loads(result)
                if ("identifier" in result) and ("message" in result):
                    denty = result["identifier"]
                    denty = json.loads(denty)
                    room_id = denty["room_id"].replace("channel","")
                    b = result["message"]
                    if  "user" in b:
                        user = b["user"]
                        id = str(user["id"])
                        name = fix_name(user["display_name"])
                        username = user["username"]
                        #threading.Thread(target=update_seen, args=(name,id,username,room_id)).start()
                        update_seen(name,id,username,room_id)
        except :
            sleep(5)
            pass

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
def get_seen(result):
    refresh_seen()
    string = result.group(1)
    if string.isnumeric():
        id = string
        print(id)
        if id in seen_data:
            return send_seen(id)
        else:
            return fix_message("I dont remember seeing user with ID %s" % str(id))
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
            if list(possibles.keys())[0] in seen_data:
                return send_seen(list(possibles.keys())[0])
            else:
                return fix_message("I dont remember seeing user with name %s" % string)
        elif n == total :
            return fix_message("I dont remember seeing user with name %s" % string)
        else:
            return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name and ask 'Blue seen ID'"% (string, fix_message(str(possibles)).replace("{", "").replace("}", "")))


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
            
    if found is False:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://","")
        formattedlink = "Image: " + link
        image_cache[query] = [urly,formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink
    
def coin_handling(result):
    global data
    num = result.group(1)
    coin_add = int(num)
    if (coin_add <= 100) and (coin_add >= 1):
        data["coins"] = coin_add + data["coins"]
        update_data_json()
        if num == "1":
            return adding_one_coin % (coin_add + 0, data["coins"])
        else:
            return adding_coins % (coin_add + 0, data["coins"])
    elif coin_add > 100:
        return too_many_coins

def get_id(result):
    String = result.group(4) 
    id = return_id(String)
    if id is False:
        return not_seen % String
    else:
        if type(id) is not dict:
            return id_response % (String,id)
        else:
            if len(id) ==1:
                return id_response % (String,list(id.keys())[0])
            elif len(id) == 0:
                return not_seen % String
            else:
                return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (String, fix_message(str(id)).replace("{", "").replace("}", "")))
        

def get_jokes():
    r = requests.get(jokes_url)
    if r.status_code == 200:
        joke = json.loads(r.text)["attachments"][0]["text"]
        return joke
    else:
        return "Error: " + str(r.status_code)

def get_quote(console):
    r = requests.get('https://api.quotable.io/random')
    content = str(r.json()['content'])
    author = "~ by " + str(r.json()['author'])
    if console is not True:
        send_message(content)
        sleep(0.2)
        send_message(author)
    else:
        print("Console:- %s"%content)
        sleep(0.2)
        print("Console:- %s"%author)

def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")


def check_singing():
    l = len(timeout_control)
    if l <= 4 and random.randint(0, 100000) % 93870 == 0:
        Thread(target=singing).start()

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
    return response

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

def console_input():
    while True:
        text = input()
        name = "Console Admin"
        if consoleinput.match(text):
            content = consoleinput.match(text).group(1)
            send_message(content)
        else:
            whos_here_r = whos_idle_r = []
            whos_here_res = { 
                whos_here: whos_here_r,
                whos_idle: whos_idle_r,
                bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
                dice: dice_statement % random.randint(1, 6)
            }
            admin_func(text, 0, True)
            matching(fix_name(name),response_dict, text, True, False)
            matching(fix_name(name),whos_here_res, text, True, True)
            coins_feelings(text, id, True)


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
Thread(target=console_input).start()
Thread(target=thread_function).start()
while True:
    try:
        ws = websocket.WebSocket()
        websocket.enableTrace(False)
        ws.connect(ws_url, cookie=main_cookie, subprotocols=subprots, origin=origin)
        ws.send(json.dumps(connect_json))
        ws.send(json.dumps(connect_json_blue))
        while running is True:
            update_seen_json()
            reset_clock = reset_clock + 1 
            result = ws.recv() #rece23621807ive message
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
                b = result["message"]
                Thread(target=greet, args=("user_connected", "add", True, b,)).start()
                Thread(target=greet, args=("typing", "add", False, b,)).start()
                Thread(target=greet, args=("user_disconnected", "remove", False, b,)).start()
                Thread(target=greet, args=("messages", "add", False, b,)).start()
                if "messages" in b and "user" in b:
                    user = b["user"]
                    id = str(user["id"])
                    #spam_controlling(id)
                    #spam_checker()
                    name = fix_name(user["display_name"])
                    message = fix_message(str(b["messages"]))
                    print(b["user"]["display_name"] + " (%s) :- "%id + message)
                    #Thread(target=landmine_checker, args=(message,id)).start()
                    Thread(target=check_greeters, args=(message, id,)).start()
                    Thread(target=log_chats, args=(message, id, user,)).start()
                    if id not in data["mutelist"]:
                        coins_feelings(message, id, False)
                        matching(fix_name(name),response_dict, message, False, False)
                        matching(fix_name(name),whos_here_res, message, False, True)
                    if id in data["admin"]:
                        admin_func(message, id, True)
                    elif id in data["mod"]:
                        admin_func(message, id, False)
    except Exception as e:
        print("Hello young boi an error occurred :- %s" %e)        
        sleep(5)
        pass
