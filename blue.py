# pylint: disable=missing-function-docstring, global-statement, wildcard-import, broad-except, unused-wildcard-import
import json
import random
from pathlib import Path
from threading import Thread
from time import gmtime, perf_counter, sleep, strftime
from timeit import default_timer as timer
from unidecode import unidecode
import requests
import websocket
from imgurpython.helpers.error import (ImgurClientError,
                                       ImgurClientRateLimitError)

from db import db_update, get_last_record_id, regex_query, return_name
from gc_logging import *
from utils import *
from var import *


def reduce_space(text):
    # swap all spaces more than one space with a single space
    space_regex = re.compile(r'\s+')
    return space_regex.sub(' ', text)

def remove_newline(text):
    newline_regex = re.compile(r'(\\n)+')
    return newline_regex.sub('', text)

def sender(content, delay):
    sleep(delay)
    jsonmessage = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" +
        fix_message(content) +
        "\",\"id\":null,\"action\":\"speak\"}"}

    jsonmessage_alt = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}",
        "data": "{\"message\":\"" +
        fix_message(content) +
        "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if ALT_UNIVERSE_TOGGLE:
        ws.send(json.dumps(jsonmessage_alt))
    else:
        ws.send(json.dumps(jsonmessage))

def calculate_delay(id):
    delay = 1.5
    if id not in delay_handle:
        return 0
    if perf_counter() - delay_handle[id] < delay:
        return delay - (perf_counter() - delay_handle[id])
    return 0
    
def send_message(content):
    content = reduce_space(content)
    content = remove_newline(content)
    delay = calculate_delay(ID)
    delay_handle[ID] = perf_counter()
    Thread(target=sender, args=(content,delay,)).start()

def return_id(string):
    try:
        possibles = {}
        if string.isnumeric():
            return string
        string = string.replace("#", "")
        for id_inp in DATA["nickname"]:
            for nickname in DATA["nickname"][id_inp]:
                regex2 = re.compile(string, re.I)
                if regex2.search(nickname):
                    return id_inp
        query_res = regex_query(string)
        if len(query_res) == 1:
            return query_res[0][0]
        if len(query_res) > 1:
            possibles.clear()
            for i in query_res:
                possibles[i[0]] = f"{i[1]}(#{str(i[2])})"
        return possibles
    except re.error:
        return {}
    except Exception as error:
        return_id(string)


def remove_blue():
    if 21550262 in MAIN_DICT:
        del MAIN_DICT[21550262]
    if 21550262 in IDLE_DICT:
        del IDLE_DICT[21550262]
    if 21550262 in TIMEOUT_CONTROL:
        del TIMEOUT_CONTROL[21550262]


def idle_function():
    idle_check = list(TIMEOUT_CONTROL.values())
    for i, time_stamp in enumerate(idle_check):
        val = list(TIMEOUT_CONTROL.keys())[i]
        if perf_counter() - time_stamp >= 240 and val in MAIN_DICT:
            IDLE_DICT[val] = MAIN_DICT[val]
            del MAIN_DICT[val]
        elif perf_counter() - time_stamp < 240 and val in IDLE_DICT:
            del IDLE_DICT[val]


def clocking():
    global RESET_CLOCK, GREET_TIMEOUT
    RESET_CLOCK += 1
    if RESET_CLOCK == 500:
        GREET_TIMEOUT, RESET_CLOCK = {}, 0


def refreshdata():
    global DATA
    with open('data.json', 'r', encoding='utf-8') as file:
        DATA = json.loads(file.read())
    return done


def update_data_json():
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(DATA, file)
    refreshdata()


def refreshmessages():
    global SAVED_MESSAGES
    with open('messages.json', 'r', encoding='utf-8') as file:
        SAVED_MESSAGES = json.loads(file.read())
    return done


def update_messages_json():
    with open('messages.json', 'w', encoding='utf-8') as file:
        json.dump(SAVED_MESSAGES, file)
    refreshmessages()


def update_image_cache():
    with open('image_cache.json', 'w', encoding='utf-8') as file:
        json.dump(IMAGE_CACHE, file)


def refresh_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'r', encoding='utf-8') as file:
        IMAGE_CACHE = json.loads(file.read())


def saved_message_handler(id_inp, name_inp):
    if id_inp not in SAVED_MESSAGES:
        return
    if len(SAVED_MESSAGES[id_inp]) == 1:
        output_message = f"Hello {name_inp} I have a message for you: {SAVED_MESSAGES[id_inp][0]}"
        sleep(0.9)
        send_message(output_message)
    else:
        sleep(1)
        output_message = f"Hello {name_inp} I have a few messages for you from some people"
        send_message(output_message)
        for messages in SAVED_MESSAGES[id_inp]:
            send_message(messages)
            sleep(0.4)
    del SAVED_MESSAGES[id_inp]
    update_messages_json()


def greet_text(count, name_inp):
    if SHORTEN_GREET_TOGGLE:
        if count == 1:
            return Greet_1_short % name_inp
        elif count == 2:
            return Greet_2_short % name_inp
        elif count == 3:
            return Greet_general_short % name_inp
    if count == 1:
        return Greet_1 % name_inp
    elif count == 2:
        return Greet_2 % name_inp
    elif count == 3:
        return Greet_general % name_inp


def send_greet(name_inp, username_inp):
    name = name_inp
    if len(name_inp) <= 3:
        username_inp = f" (#{username_inp})"
        name = f"{name_inp} {username_inp}"
    if name_inp not in GREET_TIMEOUT:
        send_message(greet_text(3, name))
        GREET_TIMEOUT[name_inp] = "1"
        return
    current_state = GREET_TIMEOUT[name_inp]
    if current_state == "1":
        send_message(greet_text(1, name))
        GREET_TIMEOUT[name_inp] = "2"
    elif current_state == "2":
        send_message(greet_text(2, name))
        GREET_TIMEOUT[name_inp] = "3"
    elif current_state == "3":
        pass


def greet(action, _result_, greet_var, userdat):
    if not ((action in userdat) and ("user" in userdat)
            and "display_name" in userdat["user"]):
        return
    name_inp = fix_name(userdat["user"]["display_name"])
    username = userdat["user"]["username"]
    id_inp = userdat["user"]["id"]
    if _result_ == "add":
        MAIN_DICT[id_inp] = name_inp
        STATS_LIST[id_inp] = name_inp
        TIMEOUT_CONTROL[id_inp] = perf_counter()
        saved_message_handler(str(id_inp), name_inp)
    elif _result_ == "remove":
        list_removal(id_inp)
    id_inp = str(id_inp)
    if GREET_STATUS and greet_var and id_inp not in DATA["greet_exempt"]:
        if id_inp in DATA["custom_greet"]:
            send_message(DATA["custom_greet"][id_inp])
        elif id_inp in DATA["knight"]:
            send_message(f"Greetings {name_inp} ~*")
        else:
            send_greet(name_inp, username)
    ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if greet_var:
        db_update(id_inp, name_inp, username, "None", "WFAF", "Joined", ts)
    elif _result_ == "remove":
        db_update(id_inp, name_inp, username, "None", "WFAF", "Left", ts)
    elif "messages" in userdat:
        text = fix_message(str(userdat["messages"])).strip("'")
        db_update(id_inp, name_inp, username, text, "WFAF", "Message", ts)
    else:
        db_update(id_inp, name_inp, username, "None", "WFAF", "Typing", ts)


def dis_en_greets(id_inp):
    global GREET_STATUS
    if id_inp == "16008266" and GREET_STATUS:
        send_message(disabling_greet)
        GREET_STATUS = False
    elif id_inp == "20909261" and not GREET_STATUS:
        send_message(re_enabling_greet)
        GREET_STATUS = True


def check_greeters(inputmessage, id_inp):
    if id_inp not in DATA["greeter_fallback"]:
        return
    for reg_m in greet_check:
        if inputmessage in DATA["custom_greet"].values() or reg_m.match(
                inputmessage) or inputmessage == blue_greet:
            dis_en_greets(id_inp)
            return
    for reg_m in DATA["custom_greet"].values():
        reg = re.compile(r"" + reg_m + r"", re.I)
        if reg.search(inputmessage):
            dis_en_greets(id_inp)
            return


def saving_messages(name_inp, _result_):
    _input_ = _result_.group(1).rstrip()
    id_inp = return_id(_input_)
    if not id_inp:
        return not_seen % _input_
    if not isinstance(id_inp, dict):
        if id_inp not in SAVED_MESSAGES:
            SAVED_MESSAGES[id_inp] = []
        SAVED_MESSAGES[id_inp].append(name_inp + ":- " + _result_.group(2))
        update_messages_json()
        return save_message_r % _input_
    if len(id_inp) == 0:
        return not_seen % _input_
    elif len(id_inp) == 1:
        id_inp = list(id_inp.keys())[0]
        if id_inp not in SAVED_MESSAGES:
            SAVED_MESSAGES[id_inp] = []
        SAVED_MESSAGES[id_inp].append(f"{name_inp}:- {_result_.group(2)}")
        update_messages_json()
        return save_message_r % _input_
    else:
        return fix_message(
            f"I have seen the following users with the name {_result_.group(2)} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")


def downvote(cookie, id_inp):
    requests.get(karma_url % id_inp, cookies=cookie)


def ban_log(banned_id, admin_id):
    admin_name = "Console Admin"
    if admin_id != 0:
        admin_name = name_from_id(admin_id)
    log = f"Banned {name_from_id(banned_id)} by {admin_name} \n"
    with open("log.txt", "a") as file:
        file.write(log)


def thread(id_inp):
    banned.add(id)
    for i in cookiejar:
        cookie = {'_prototype_app_session': i}
        Thread(target=downvote, args=(cookie, id_inp)).start()


def mute_func(_result_, index):
    inp = _result_.group(1)
    id_inp = return_id(inp)
    if not id_inp:
        return not_seen % inp
    if not isinstance(id_inp, dict):
        id_inp = id_inp
    elif len(id_inp) == 0:
        return not_seen % inp
    elif len(id_inp) == 1:
        id_inp = list(id_inp.keys())[0]
    else:
        return fix_message(
            f"I have seen the following users with the name {_result_.group(2)} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")
    if index == 11:
        if id_inp in DATA["mutelist"]:
            return already_ignoring % name_from_id(id_inp)
        DATA["mutelist"].append(id_inp)
        return start_ignoring % name_from_id(id_inp)
    if index == 12:
        if id_inp in DATA["mutelist"]:
            DATA["mutelist"].remove(id_inp)
            return stop_ignoring % name_from_id(id_inp)
        return already_not_ignoring % name_from_id(id_inp)
    else:
        return "No match found"


def stalker(id_inp, time_now):
    filename = str(id_inp) + ".txt"
    git_prefix = "stalker-logs/"
    file = git_prefix + filename
    myfile = Path(file)
    if not myfile.is_file():
        file = open(file, "w")
        file.close()
    while STALKING_LOG[id_inp][1]:
        resp = requests.get(profile_url % id_inp, cookies=cookies)
        if resp.status_code == 200:
            resp = json.loads(resp.text)["user"]
            time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
            text = logging_text % (str(time),
                                   resp["display_name"],
                                   resp["karma"],
                                   resp["username"],
                                   resp["gender"])
            with open(file, "a") as file:
                file.write(text)
        if resp.status_code == 404:
            send_message(stopping_logging % id_inp)
            break
        else:
            if timer() - time_now < 3600:
                pass
            send_message(f"Ending stalk session of ID: {id_inp}")
            break
        sleep(15)
        if not STALKING_LOG[id_inp][1]:
            del STALKING_LOG[id_inp]
            break


def respond_uptime():
    sr = str(datetime.now() - STARTTIME).split(":")
    if sr[0] == "0":
        mins = int(sr[1]) + 0
        if mins == 0:
            return just_joined
        elif mins == 1:
            return here_for_one_min
        else:
            return here_for_x_mins % str(int(sr[1]) + 0)
    elif sr[0] == "1":
        return here_for_an_hour
    return here_for_hours_and_mins % (str(sr[0]))


def send_stats():
    sr = str(datetime.now() - STARTTIME).split(":")
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    return stats_response % (len(stats), len(STATS_LIST), sr[0], sr[1], str(r))


def start_stalking(id_inp):
    if id_inp in STALKING_LOG:
        return already_stalking % id_inp
    thr = Thread(target=stalker, args=(id_inp, timer()))
    STALKING_LOG[id_inp] = [thr, True]
    thr.start()
    return waking_stalking


def stop_stalking(id_inp):
    if id_inp not in STALKING_LOG:
        return already_not_stalking % id_inp
    STALKING_LOG[id_inp][1] = False
    return stopping_stalking % id_inp


def mod_demod(_result_):
    mod_id = _result_.group(2)
    if _result_.group(1) == "mod":
        if mod_id in DATA["mod"] or mod_id in DATA["admin"]:
            return already_mod % mod_id
        DATA["mod"].append(mod_id)
        update_data_json()
        return mod_response % mod_id
    if mod_id not in DATA["mod"] and mod_id not in DATA["admin"]:
        return not_mod % mod_id
    if mod_id in DATA["admin"]:
        DATA["admin"].remove(mod_id)
    if mod_id in DATA["mod"]:
        DATA["mod"].remove(mod_id)
    update_data_json()
    return demod_response % mod_id


def clear_lists():
    TIMEOUT_CONTROL.clear()
    MAIN_DICT.clear()
    IDLE_DICT.clear()
    return clear_list


def set_greet(_result_):
    id_inp = _result_.group(1)
    greettext = _result_.group(3)
    DATA["custom_greet"][id_inp] = greettext
    update_data_json()
    return greet_updated % (id_inp, greettext)


def get_greet(_result_):
    id_inp = _result_.group(1)
    if id_inp in DATA["custom_greet"]:
        return greet_response % (id_inp, DATA["custom_greet"][id_inp])
    return greet_not_set % id_inp


def remove_greet(_result_):
    id_inp = _result_.group(1)
    if id_inp not in DATA["custom_greet"]:
        return greet_not_set % id_inp
    del DATA["custom_greet"][id_inp]
    update_data_json()
    return greet_removed % id_inp


def get_landmine():
    landmine_list = DATA["landmine_words"]
    return fix_message(landmine_list)


def add_landmine(_result_):
    word = _result_.group(1)
    if word in DATA["landmine_words"]:
        return landmine_already_added % word
    DATA["landmine_words"].append(word)
    update_data_json()
    return landmine_added % word


def remove_landmine(_result_):
    word = _result_.group(1)
    if word not in DATA["landmine_words"]:
        return landmine_not_present % word
    DATA["landmine_words"].remove(word)
    update_data_json()
    return landmine_removed % word


def toggle_alt_universe():
    global ALT_UNIVERSE_TOGGLE
    if ALT_UNIVERSE_TOGGLE:
        ALT_UNIVERSE_TOGGLE = False
    else:
        ALT_UNIVERSE_TOGGLE = True
    return done


def toggle_spam_check():
    global SPAM_CHECK_TOGGLE
    if SPAM_CHECK_TOGGLE:
        SPAM_CHECK_TOGGLE = False
        return spam_check_off
    SPAM_CHECK_TOGGLE = True
    return spam_check_on


def get_spam_check_status():
    if SPAM_CHECK_TOGGLE:
        return spam_check_on
    return spam_check_off


def make_knight(_result_):
    name_inp = _result_.group(1)
    if name_inp.isnumeric():
        id_inp = name_inp
        if id_inp in DATA["knight"]:
            return knight_already_added % name_inp
        DATA["knight"].append(id_inp)
        update_data_json()
        return knight_added % name_inp
    id_inp = return_id(name_inp)
    if not id_inp:
        return not_seen % name_inp
    if not isinstance(id_inp, dict):
        if id_inp in DATA["knight"]:
            return knight_already_added % name_inp
        DATA["knight"].append(id_inp)
        update_data_json()
        return knight_added % name_inp
    if len(id_inp) == 0:
        return not_seen % name_inp
    if len(id_inp) == 1:
        id_inp = list(id_inp.keys())[0]
        if id_inp in DATA["knight"]:
            return knight_already_added % name_inp
        DATA["knight"].append(id_inp)
        update_data_json()
        return knight_added % name_inp
    return fix_message(
        f"I have seen the following users with the name {name_inp} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")


def remove_knight(_result_):
    name_inp = _result_.group(1)
    id_inp = name_inp
    if not name_inp.isnumeric():
        id_inp = return_id(id_inp)
    if not id_inp or (isinstance(id_inp, dict) and len(id_inp) == 0):
        return not_seen % name_inp
    if not isinstance(id_inp, dict):
        if id_inp not in DATA["knight"]:
            return knight_not_added % name_inp
        DATA["knight"].remove(id_inp)
        update_data_json()
        return knight_removed % name_inp
    if len(id_inp) != 1:
        return fix_message(
            f"I have seen the following users with the name {name_inp} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")
    id_inp = list(id_inp.keys())[0]
    if id_inp not in DATA["knight"]:
        return knight_not_added % name_inp
    DATA["knight"].remove(id_inp)
    update_data_json()
    return knight_removed % name_inp


def toggle_shortened_greet():
    global SHORTEN_GREET_TOGGLE
    if SHORTEN_GREET_TOGGLE:
        SHORTEN_GREET_TOGGLE = False
        return shortened_greet_off
    SHORTEN_GREET_TOGGLE = True
    return shortened_greet_on


def save_nickname(_result_):
    name_inp = _result_.group(1)
    nickname = _result_.group(2)
    id_inp = name_inp
    if not id_inp.isnumeric():
        id_inp = return_id(id_inp)
    if not id_inp or (isinstance(id_inp, dict) and len(id_inp) == 0):
        return not_seen % name_inp
    if not isinstance(id_inp, dict):
        if id_inp not in DATA["nickname"]:
            DATA["nickname"][id_inp] = []
        DATA["nickname"][id_inp].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, name_inp)
    if len(id_inp) == 1:
        id_inp = list(id_inp.keys())[0]
        if id_inp not in DATA["nickname"]:
            DATA["nickname"][id_inp] = []
        DATA["nickname"][id_inp].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, name_inp)
    return fix_message(
        f"I have seen the following users with the name {input_name} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")


def toggle_greets(_result_):
    global GREET_STATUS
    action = _result_.group(1)
    if action == "enable":
        GREET_STATUS = True
        return done
    if GREET_STATUS:
        GREET_STATUS = False
        return done
    return already_not_greeting


def hide(id_inp):
    id_inp = int(id_inp)
    del TIMEOUT_CONTROL[int(id_inp)]
    if id_inp in MAIN_DICT:
        del MAIN_DICT[id_inp]
    if id_inp in IDLE_DICT:
        del IDLE_DICT[id_inp]
    return aye_aye


def banfunc(id_inp, _result_):
    id_ban = _result_.group(1)
    thread(id_ban)
    Thread(target=ban_log, args=(id_ban, id_inp,)).start()
    return banning_response % name_from_id(id_ban)


def returnstalk():
    if STALKING_LOG:
        return stalking_following % fix_message(str(STALKING_LOG.keys()))
    return stalking_no_one


def toggle_insult_func(_result_):
    global insult_control
    action = _result_.group(1)
    if action == "enable":
        insult_control = True
        return done
    insult_control = False
    return done

def get_wall_id(user_id):
    url = f"https://emeraldchat.com/profile_json?id={user_id}"
    resp = requests.get(url, cookies = cookies)
    if resp.status_code == 200:
        return resp.json()["wall_id"]
    return None

def get_wall_posts(wall_id):
    url = f"https://emeraldchat.com/microposts_default?id={wall_id}"
    resp = requests.get(url, cookies = cookies)
    if resp.status_code == 200:
        return resp.json()["microposts"]
    return None

def get_post_contents(post_id):
    url = f"https://emeraldchat.com/micropost_json?id={post_id}"
    resp = requests.get(url, cookies = cookies)
    if resp.status_code == 200:
        post = resp.json()["micropost"]
        return post["content"]
    return None

def test_mega(content):
    mega_regex = re.compile(r"https://mega\.nz/((folder|file)/([^#]+)#(.+)|#(F?)!([^!]+)!(.+))", re.MULTILINE)
    mega_match = mega_regex.search(content)
    return bool(mega_match)

def test_dropbox(content):
    # check if contains word dropbox
    dropbox_regex = re.compile(r"dropbox", re.I)
    dropbox_match = dropbox_regex.search(content)
    return bool(dropbox_match)

def is_flaged(content):
    if test_mega(content) or test_dropbox(content): 
        return True
    return False

def log_link(id, link):
    file = open("report_links.txt", "a+")
    for line in file:
        if link in line:
            return
    file.write(f"{id} - {link}\n")
    file.close()

# segment array into chunks of size n
def segment(array, n):
    for i in range(0, len(array), n):
        yield array[i:i + n]
    return array

def report_id(_result_):
    id_inp = _result_.group(1)
    wall_id = get_wall_id(id_inp)
    if not wall_id:
        return
    wall_posts = get_wall_posts(wall_id)
    if not wall_posts:
        return
    if len(wall_posts) > 90:
        wall_posts = segment(wall_posts, 90)
    else: 
        wall_posts = [wall_posts]
    for seg in wall_posts:
        for post in seg:
            content = get_post_contents(post)
            if content and is_flaged(content):
                log_link(id_inp, content)
        sleep(15)
    
def admin_function_init(i, id_inp, isadmin, _result_):
    global RUNNING, aichatstate
    if i == 0:
        return_response = toggle_greets(_result_)
    elif i == 1:
        return_response, RUNNING = leaving, False
    elif i == 2 and isadmin:
        return_response = clear_lists()
    elif i == 3:
        return_response = respond_uptime()
    elif i == 4:
        GREET_TIMEOUT.clear()
        return_response = done
    elif i == 5:
        return_response = send_stats()
    elif i == 6:
        mutelist = DATA["mutelist"]
        return_response = f"Mutelist is: {join_list(mutelist)}"
    elif i == 7:
        return_response = str(TIMEOUT_CONTROL)
    elif i == 8:
        restart_program()
    elif i == 9:
        return_response = hide(id_inp)
    elif i == 10 and id_inp not in DATA["mutelist"]:
        return_response = ily_r
    elif i == 11 or i == 12:
        return_response = mute_func(_result_, i)
    elif i == 13 and isadmin:
        return_response = banfunc(id_inp, _result_)
    elif i == 14:
        adminlist = DATA["admin"] + DATA["mod"]
        return_response = f"Current admins are: {join_list(adminlist)}"
    elif i == 15:
        return_response = str(_result_.group(2))
    elif i == 16:
        return_response = stop_stalking(str(_result_.group(2)))
    elif i == 17:
        return_response = returnstalk()
    elif i == 18:
        aichatstate, return_response = True, done
    elif i == 19:
        aichatstate, return_response = False, done
    elif i == 20 and is_creator(id_inp):
        return_response = mod_demod(_result_)
    elif i == 21:
        return_response = refreshdata()
    elif i == 22:
        return_response = refreshmessages()
    elif i == 23 and isadmin:
        return_response = set_greet(_result_)
    elif i == 24 and isadmin:
        return_response = get_greet(_result_)
    elif i == 25 and isadmin:
        return_response = remove_greet(_result_)
    elif i == 26 and isadmin:
        return_response = add_landmine(_result_)
    elif i == 27 and isadmin:
        return_response = remove_landmine(_result_)
    elif i == 28 and isadmin:
        return_response = get_landmine()
    elif i == 29 and is_creator(id_inp):
        return_response = toggle_alt_universe()
    elif i == 30 and isadmin:
        return_response = toggle_spam_check()
    elif i == 31 and isadmin:
        return_response = get_spam_check_status()
    elif i == 32 and isadmin:
        return_response = make_knight(_result_)
    elif i == 33 and isadmin:
        return_response = remove_knight(_result_)
    elif i == 34:
        return_response = toggle_shortened_greet()
    elif i == 35 and isadmin:
        return_response = save_nickname(_result_)
    elif i == 36:
        return_response = toggle_insult_func(_result_)
    elif i == 37:
        return_response = "Okay, thank you for reporting ^^"
        Thread(target=report_id, args=(_result_,)).start()
    else:
        return_response = False
    if return_response:
        if int(id_inp) != 0:
            send_message(return_response)
        else:
            print(f"Admin Command: {return_response}")


def admin_func(inputmessage, id_inp, isadmin):
    if not isadmin and id_inp not in DATA["mod"]:
        return
    for i, command in enumerate(admin_commands):
        res = command.match(inputmessage)
        if res:
            admin_function_init(i, id_inp, isadmin, res)
            return


def landmine_checker(inputmessage, id_inp):
    for word in DATA["landmine_words"]:
        regex1 = re.compile(r"%s" % word, re.I)
        if regex1.search(inputmessage):
            thread(id_inp)
            return


def spam_controlling(id_inp):
    if id_inp not in SPAM_TIMEOUT:
        SPAM_TIMEOUT[id_inp] = []
    SPAM_TIMEOUT[id_inp].append(perf_counter())


def spam_checker():
    for eyedee, spam_keys in SPAM_TIMEOUT.items():
        if eyedee in banned:
            continue
        if (len(spam_keys) >= 3 and spam_keys[-1] - spam_keys[-3] < 1.3) or (
                len(spam_keys) >= 5 and spam_keys[-1] - spam_keys[-5] < 3):
            thread(eyedee)


def image_upload(query, urly):
    if query in IMAGE_CACHE:
        return IMAGE_CACHE[query][1]
    for i in IMAGE_CACHE:
        if IMAGE_CACHE[i][0] == urly:
            return IMAGE_CACHE[i][1]
    image = CLIENT.upload_from_url(urly)
    formattedlink = image_to_link(image)
    IMAGE_CACHE[query] = [urly, formattedlink]
    update_image_cache()
    refresh_image_cache()
    return formattedlink


refresh_image_cache()


def get_image_link(query, meme):
    try:
        if meme:
            return get_meme()
        url = response().urls(query, 6)
        return image_upload(query, url[-1])
    except ImgurClientError:
        return f"Sorry I couldn't find {query}"
    except ImgurClientRateLimitError:
        return "Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying"


def send_pic(query, meme):
    send_message(get_image_link(query, meme))


def get_meme():
    resp = requests.get("https://meme-api.herokuapp.com/gimme")
    resp = json.loads(resp.text)
    link = resp["url"]
    image = CLIENT.upload_from_url(link)
    return image_to_link(image)


def send_seen_db(id_inp):
    query_res = get_last_record_id(id_inp, False)
    channel_name = query_res[4]
    inputdate =str(query_res[-1])
    deltatime = return_deltatime(inputdate)
    name, inp_user = query_res[1], query_res[2]
    date_string = return_datestring(deltatime.days, inputdate)
    resp = f"{date_string} {deltatime.seconds//3600} hours ago "
    if deltatime.seconds // 3600 == 0:
        resp = f"{date_string} {deltatime.seconds//60 % 60} mins ago "
    if deltatime.seconds // 60 % 60 == 0:
        resp = f"{date_string} a couple moments ago "
    if channel_name == "WFAF":
        return f"{name} (#{inp_user}) was last seen {resp}in WFAF"
    res = get_last_record_id(id_inp, True)
    channel_name = channel_dict[channel_name]
    if not res:
        mins = deltatime.seconds // 60 % 60
        hours = deltatime.seconds // 3600
        date_channel = inputdate.split(" ")[0]
        date_string = return_datestring(deltatime.days, date_channel)
        broiler_response = f"I dont remember seeing {name} (#{inp_user}) in WFAF but they were last seen "
        if hours != 0:
            return broiler_response + \
                f"{date_string} {hours} hours ago in {channel_name}"
        if mins == 0:
            return broiler_response + f"a couple moments ago in {channel_name}"
        return broiler_response + \
            f"{date_string} {mins} mins ago in {channel_name}"
    deltatime_wfaf = return_deltatime(res[-1])
    date_string = return_datestring(deltatime_wfaf.days, inputdate)
    hours_wfaf = deltatime_wfaf.seconds // 3600
    mins_wfaf = deltatime_wfaf.seconds // 60 % 60
    ree = f"{name} (#{inp_user}) was last seen {date_string} {hours_wfaf} hours ago "
    if hours_wfaf == 0:
        ree = f"{name} (#{inp_user}) was last seen {date_string} {mins_wfaf} mins ago "
    if deltatime_wfaf.seconds // 60 % 60 == 0:
        ree = f"{name} (#{inp_user}) was last seen {date_string} a couple moments ago "
    if (hours_wfaf == 0 and deltatime.seconds // 3600 == 0 and mins_wfaf == deltatime.seconds // 60 % 60) or (deltatime_wfaf.days == deltatime.days and hours_wfaf == deltatime.seconds // 3600):
        return f"{name} (#{inp_user}) was last seen {resp} in {channel_name} and WFAF"
    return f"{ree}in WFAF but was more recently seen {resp} in {channel_name}"


def log_chats(inputmessage, user_id, inpuser):
    inputdate = datetime.today().strftime('%d-%m-%Y')
    filename = f"wfaf-logs/log ({inputdate}).txt"
    inpname = fix_name(inpuser["display_name"])
    log = message_log_text % (inpname, user_id, inputmessage) + "\n"
    with open(filename, "a+", encoding='utf-8' ) as file:
        file.write(log)


def list_removal(id_inp):
    if id_inp in TIMEOUT_CONTROL:
        del TIMEOUT_CONTROL[id_inp]
    if id_inp in MAIN_DICT:
        del MAIN_DICT[id_inp]
    if id_inp in IDLE_DICT:
        del IDLE_DICT[id_inp]


def whos_here_appending(id_inp):
    try:
        resp = requests.get(profile_url % id_inp, cookies=cookies, timeout=0.2)
        resp = json.loads(resp.text)
        name_inp = resp["user"]["display_name"]
        if len(name_inp) <= 3:
            username_inp = resp["user"]["username"]
            name_inp = f"{name_inp} ({username_inp})"
    except Exception:
        name_inp = return_name(id_inp)
    finally:
        PLACEHOLDER_LIST.append(name_inp)


def dict_thread_starter(input_dict):
    thread_list = []
    for i in input_dict:
        thread_list.append(Thread(target=whos_here_appending, args=(i,)))
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()


def reply_whos_here():
    PLACEHOLDER_LIST.clear()
    dict_thread_starter(MAIN_DICT)
    threads.clear()
    idle_len = len(IDLE_DICT)
    if idle_len == 0:
        resp = whos_here_response_no_lurkers % format_out_list(
            PLACEHOLDER_LIST)
    elif idle_len == 1:
        resp = whos_here_response_gen1 % format_out_list(PLACEHOLDER_LIST)
    else:
        resp = whos_here_response_gen2 % (
            format_out_list(PLACEHOLDER_LIST), idle_len)
    return fix_message(resp)


def reply_whos_idle():
    PLACEHOLDER_LIST.clear()
    dict_thread_starter(IDLE_DICT)
    return fix_message(whos_lurking_none) if len(IDLE_DICT) == 0 else fix_message(
        whos_lurking_gen % format_out_list(PLACEHOLDER_LIST))


def name_from_id(id_inp):
    name_return = ""
    try:
        resp = requests.get(profile_url % int(id_inp), cookies=cookies)
        resp = json.loads(resp.text)
        name_return = resp["user"]["display_name"]
    except Exception:
        try:
            name_return = return_name(id_inp)
        except Exception:
            name_return = id_inp
    return name_return

def fix_seen(text):
    rege = re.compile(r' 1 hours\s*')
    text = re.sub(rege, ' an hour ', text)
    rege = re.compile(r' 1 mins\s*')
    text = re.sub(rege, 'a minute ', text)
    rege = re.compile(r' 1 secs\s*')
    text = re.sub(rege, 'a second ', text)
    rege = re.compile(r' 1 days\s*')
    text = re.sub(rege, 'a day ', text)
    return text

def get_seen(_result_, id_inp):
    try:
        string = _result_.group(1).strip()
        me_regex = re.compile(r"m\s*e(\\n)*\s*$", re.I)
        if me_regex.match(string):
            string = str(id_inp)
        if string.isnumeric():
            seeny = fix_message(send_seen_db(string)) 
            return fix_seen(seeny)
        string = string.replace("#", "")
        possibles = {}
        for id_inp in DATA["nickname"]:
            for nickname in DATA["nickname"][id_inp]:
                regex2 = re.compile(string, re.I)
                if regex2.search(nickname):
                    possibles = {id_inp: nickname}
                    break
        if len(possibles) == 0:
            query_res = regex_query(string)
            if len(query_res) == 1:
                seeny = send_seen_db(query_res[0][0])
                return fix_seen(seeny)
            for i in query_res:
                possibles[i[0]] = i[1] + "(#" + str(i[2]) + ")"
        if len(possibles) == 1:
            try:
                seeny = send_seen_db(list(possibles.keys())[0])
                return fix_seen(seeny)
            except Exception as e:
                print(e)
                return fix_message(
                    f"I dont remember seeing anyone named {string}")
        if len(possibles) == 0:
            return fix_message(f"I dont remember seeing anyone named {string}")
        return fix_message(
            f"I have seen the following users with the name {string} :- {curly_replace(str(possibles))}. Specify the ID correspnding to their name and ask 'Blue seen ID'")
    except Exception as e:
        print(e)
        return fix_message(
            f"I dont remember seeing {name_from_id(string)} around")


def coin_handling(_result_):
    num = _result_.group(1)
    coin_add = int(num) + 0
    if coin_add > 100:
        return too_many_coins
    DATA["coins"] += coin_add
    update_data_json()
    return (adding_one_coin if num == "1" else adding_coins) % (
        coin_add, DATA["coins"])


def getid(_result_):
    input_str = _result_.group(4).strip()
    id_inp = return_id(input_str)
    if not id_inp:
        return not_seen % input_str
    if not isinstance(id_inp, dict):
        if input_str.isnumeric():
            return id_response % (name_from_id(input_str), id_inp)
        return id_response % (name_from_id(id_inp), id_inp)
    if len(id_inp) == 0:
        return not_seen % input_str
    if len(id_inp) == 1:
        return id_response % (input_str, list(id_inp.keys())[0])
    return fix_message(
        f"I have seen the following users with the name {input_str} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")


def get_jokes():
    resp = requests.get(jokes_url)
    if resp.status_code == 200:
        joke = json.loads(resp.text)["attachments"][0]["text"]
        return joke
    return "I am unable to fetch a joke at the moment. Please try again later"


def get_quote(console):
    resp = requests.get('https://api.quotable.io/random')
    content = str(resp.json()['content'])
    author = "~ by " + str(resp.json()['author'])
    if console:
        print(f"Console:- {content}")
        sleep(0.2)
        print(f"Console:- {author}")
    else:
        send_message(content)
        sleep(0.2)
        send_message(author)
    return ""


def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")


def check_singing():
    member_len = len(TIMEOUT_CONTROL)
    if 3 <= member_len <= 4 and random.randint(0, 100000) % 93870 == 0:
        Thread(target=singing).start()


def get_details(_result_):
    id_inp = int(_result_.group(2))
    resp = requests.get(profile_url % id_inp, cookies=cookies)
    if resp.status_code == 200:
        resp = json.loads(resp.text)["user"]
        name_inp = resp["display_name"]
        karma = resp["karma"]
        username = resp["username"]
        gender = resp["gender"]
        created = resp["created_at"].split("T")
        if not gender:
            return details_response_null_gender % (
                id_inp, name_inp, username, karma, created[0], created[1])
        return details_response % (
            id_inp, name_inp, username, karma, gender, created[0], created[1])
    if resp.status_code == 404:
        return account_deleted
    if resp.status_code == 403:
        return timeout_error
    return "Unknown condition reached"


def get_insult(res):
    if not insult_control:
        return ""
    input_name = res.group(1)
    result = requests.get(insult_url)
    result = json.loads(result.text)["insult"]
    return f"{input_name}, {result}"


def send_feelings(index, id_inp, _result_, console):
    input_name = _result_.group(1)
    if (not input_name or index == 3) and index not in (8,9):
        input_name = _result_.group(4)
    if input_name:
        input_name = input_name.replace("\n", "").strip()
        me_regex = re.compile(r"m\s*e(\\n)*\b", re.I)
        input_name = re.sub(me_regex, "you", input_name)
        myself_regex = re.compile(r"my\s*self\s*(\\n)*\b", re.I)
        input_name = re.sub(myself_regex, "you", input_name)
        my_regex = re.compile(r"my\s*(\\n)*\b", re.I)
        input_name = re.sub(my_regex, "your", input_name)
    resp = ""
    if index == 1:
        resp = sending_love % input_name
    elif index == 2:
        resp = sending_pats % input_name
    elif index == 3:
        resp = sending_hugs % input_name
    elif index == 4:
        blue_regex = re.compile(r"blue|yourself(\\n)*\b", re.I)
        if id_inp == "25033006":
            resp = "No Mr. Pengu uwu"

        elif re.search(blue_regex, input_name):
            resp = "Nu ;-;"
        else:
            resp = sending_bonks % input_name
    elif index == 5 and (id_inp in DATA["admin"] or console):
        resp = getid(_result_)
    elif index == 6 and (id_inp in DATA["admin"] or console):
        resp = get_details(_result_)
    elif index == 7:
        resp = get_seen(_result_, id_inp)
    elif index in (8, 9):
        arg = False
        if index == 9:
            arg = True
        Thread(target=send_pic, args=(
            input_name, arg)).start()
    elif index == 10:
        resp = get_insult(_result_)
    return resp


def coins_feelings(input_message, id_inp, console):
    for reg_m in coinsandfeelings:
        _result_ = reg_m.match(input_message)
        if not _result_:
            continue
        index = coinsandfeelings.index(reg_m)
        resp = send_feelings(index, id_inp, _result_, True)
        if index == 0:
            resp = coin_handling(_result_)
        if not resp:
            return
        if console:
            print(f"Console:- {resp}")
        else:
            send_message(resp)


def console_init():
    try:
        text = input()
        name_inp = "Console Admin"
        _result_ = consoleinput.match(text)
        if _result_:
            content = _result_.group(1)
            send_message(content)
        else:
            whoshere = {
                whos_here: PLACEHOLDER_LIST,
                whos_idle: PLACEHOLDER_LIST,
                list_all: PLACEHOLDER_LIST,
                bored: im_bored_list[random.randint(0, len(im_bored_list) - 1)],
                dice: dice_statement % random.randint(1, 6)
            }
            admin_func(text, 0, True)
            matching(fix_name(name_inp), response_dict, text, True, False)
            matching(fix_name(name_inp), whoshere, text, True, True)
            coins_feelings(text, id, True)
    except Exception as error:
        print(error)


def console_input():
    while True:
        console_init()


def guessing_starter(input_id, input_message):
    if not (guessing_game.match(input_message) and guessing_game_status):
        return
    if input_id in DATA["guess"]:
        send_message(
            "You already have a game started, try guessing a number !")
        return
    number = random.randint(1, 100)
    DATA["guess"][ID] = [number, 0]
    update_data_json()
    send_message(
        "Okay, I have chosen a number between 1 and 100. Guess what it is!")


def guesser(input_id, input_message):
    if not(guessing_game_status and input_id in DATA["guess"]):
        return
    res = guessing.match(input_message)
    if not res:
        return
    guess = int(res.group(1))
    if DATA["guess"][input_id][1] > 5:
        original_num = DATA["guess"][input_id][0]
        send_message(
            f"You have guessed incorrectly 6 times. The number was {original_num}" )
        del DATA["guess"][input_id]
    elif guess == DATA["guess"][input_id][0]:
        send_message(f"You guessed it! The number was {guess}")
        del DATA["guess"][input_id]
    elif guess > DATA["guess"][input_id][0]:
        send_message("Your guess was too high! Try again!")
        DATA["guess"][input_id][1] += 1
    elif guess < DATA["guess"][input_id][0]:
        send_message("Your guess was too low! Try again!")
        DATA["guess"][input_id][1] += 1
    update_data_json()


def consolecheck(content, console):
    if console:
        print(f"Console:- {content}")
    else:
        send_message(content)

def send_both_lists(isconsole):
    resp = reply_whos_here()
    consolecheck(resp, isconsole)
    resp = reply_whos_idle()
    consolecheck(resp, isconsole)

def matching(name_inp, dictname, input_text, console, dict_bool):
    for re_m in dictname:
        inputres = re_m.match(input_text)
        if not inputres:
            continue
        resp = dictname[re_m]
        if dict_bool:
            if re_m == whos_here:
                resp = reply_whos_here()
            elif re_m == whos_idle:
                resp = reply_whos_idle()
            elif re_m == list_all:
                Thread(target=send_both_lists, args=(console,)).start()
                resp = None
        else:
            if re_m == jok:
                resp = get_jokes()
            elif re_m == quote:
                resp = get_quote(console)
            elif re_m == save_message:
                resp = saving_messages(name_inp, inputres)
        if resp:
            consolecheck(resp, console)
        break


Thread(target=console_input).start()
Thread(target=thread_function).start()
while True:
    try:
        ws = websocket.WebSocket()
        websocket.enableTrace(False)
        ws.connect(ws_url, cookie=main_cookie,
                   subprotocols=subprots, origin=origin)
        ws.send(json.dumps(connect_json))
        ws.send(json.dumps(connect_json_blue))
        while RUNNING:
            result = ws.recv()
            result = json.loads(result)
            remove_blue()
            idle_function()
            clocking()
            check_singing()
            whos_here_res = {
                whos_here: PLACEHOLDER_LIST,
                whos_idle: PLACEHOLDER_LIST,
                list_all: PLACEHOLDER_LIST,
                bored: im_bored_list[random.randint(0, len(im_bored_list) - 1)],
                dice: dice_statement % random.randint(1, 6)
            }
            if not (("identifier" in result) and ("message" in result)):
                continue
            b = result["message"]
            greet("user_connected", "add", True, b)
            greet("typing", "add", False, b)
            greet("user_disconnected", "remove", False, b)
            greet("messages", "add", False, b)
            if not ("messages" in b and "user" in b):
                continue
            user = b["user"]
            ID = str(user["id"])
            input_name = fix_name(user["display_name"])
            MESSAGE = fix_message(str(b["messages"])).strip("'")
            MESSAGE = unidecode(MESSAGE)
            print(f"{input_name} ({ID}) :- {MESSAGE}")
            Thread(target=check_greeters, args=(MESSAGE, ID,)).start()
            Thread(target=log_chats, args=(MESSAGE, ID, user,)).start()
            admin_func(MESSAGE, ID, True if ID in DATA["admin"] else False)
            guessing_starter(ID, MESSAGE)
            guesser(ID, MESSAGE)
            if ID in DATA["mutelist"]:
                continue
            coins_feelings(MESSAGE, ID, False)
            matching(fix_name(input_name), response_dict,
                     MESSAGE, False, False)
            matching(fix_name(input_name), whos_here_res, MESSAGE, False, True)
    except Exception as e:
        print(e)
        sleep(1)
