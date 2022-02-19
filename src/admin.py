from var import *
import requests
import json
from pathlib import Path
from timeit import default_timer as timer
from threading import Thread
from src.data_handing import *

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
