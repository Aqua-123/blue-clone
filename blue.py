# pylint: disable=missing-function-docstring, global-statement, wildcard-import. broad-except, unused-wildcard-import, global-variable-not-assigned
import json
import random
from pathlib import Path
from threading import Thread
from time import gmtime, perf_counter, sleep, strftime
from timeit import default_timer as timer

import requests
import websocket
from cleverbotfree import Cleverbot
from imgurpython.helpers.error import (ImgurClientError,
                                       ImgurClientRateLimitError)

from db import db_update, get_last_record_id, regex_query, return_name
from gc_logging import *
from utils import *
from var import *


def send_message(content):
    jsonmessage = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) + "\",\"id\":null,\"action\":\"speak\"}"}

    jsonmessage_alt = {"command": "message", "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}",
                       "data": "{\"message\":\"" + fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if ALT_UNIVERSE_TOGGLE:
        ws.send(json.dumps(jsonmessage_alt))
    else:
        ws.send(json.dumps(jsonmessage))


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
    except Exception as e:
        print(e)
        return_id(string)


def remove_blue():
    global MAIN_DICT, IDLE_DICT, TIMEOUT_CONTROL
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
    with open('data.json', 'r') as file:
        DATA = json.loads(file.read())
    return done 


def update_data_json():
    global DATA
    with open('data.json', 'w') as file:
        json.dump(DATA, file)
    refreshdata()


def refreshmessages():
    global SAVED_MESSAGES
    with open('messages.json', 'r') as file:
        SAVED_MESSAGES = json.loads(file.read())
    return done


def update_messages_json():
    global SAVED_MESSAGES
    with open('messages.json', 'w') as file:
        json.dump(SAVED_MESSAGES, file)
    refreshmessages()


def update_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'w') as file:
        json.dump(IMAGE_CACHE, file)


def refresh_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'r') as file:
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
        match count:
            case 1: return Greet_1_short % name_inp
            case 2: return Greet_2_short % name_inp
            case 3: return Greet_general_short % name_inp
    match count:
        case 1: return Greet_1 % name_inp
        case 2: return Greet_2 % name_inp
        case 3: return Greet_general % name_inp


def send_greet(name_inp, username_inp):
    name = name_inp
    if len(name_inp) <= 3:
        username_inp = f" (#{username_inp})"
        name = f"{name_inp} {username_inp}"
    if name_inp not in GREET_TIMEOUT:
        send_message(greet_text(3, name))
        GREET_TIMEOUT[name_inp] = "1"
        return 
    match GREET_TIMEOUT[name_inp]:
        case "1":
            send_message(greet_text(1, name))
            GREET_TIMEOUT[name_inp] = "2"
        case "2":
            send_message(greet_text(2, name))
            GREET_TIMEOUT[name_inp] = "3"
        case "3": pass
 


def greet(action, _result_, greet_var, userdat):
    global DATA, SAVED_MESSAGES, MAIN_DICT, IDLE_DICT, TIMEOUT_CONTROL, STATS_LIST
    if not ((action in userdat) and ("user" in userdat) and "display_name" in userdat["user"]):
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
        db_update(id_inp, name_inp, username, "None", "WFAF","Joined", ts)
    elif  _result_ == "remove":
        db_update(id_inp, name_inp, username, "None", "WFAF", "Left", ts)
    elif "messages" in userdat:
        message = fix_message(str(userdat["messages"])).strip("'")
        db_update(id_inp, name_inp, username, message, "WFAF", "Message",ts)
    else:
        db_update(id_inp, name_inp, username,"None", "WFAF", "Typing", ts)


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
        if inputmessage in DATA["custom_greet"].values() or reg_m.match(inputmessage) or inputmessage == blue_greet:
            dis_en_greets(id_inp)
            return
    for reg_m in DATA["custom_greet"].values():
        reg = re.compile(r"" + reg_m + r"", re.I)
        if reg.search(inputmessage):
            dis_en_greets(id_inp)
            return


def saving_messages(name_inp, _result_):
    global SAVED_MESSAGES
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
    match len(id_inp):
        case 0: return not_seen % _input_
        case 1:
            id_inp = list(id_inp.keys())[0]
            if id_inp not in SAVED_MESSAGES:
                SAVED_MESSAGES[id_inp] = []
            SAVED_MESSAGES[id_inp].append(f"{name_inp}:- {_result_.group(2)}")
            update_messages_json()
            return save_message_r % _input_
        case _: return fix_message(f"I have seen the following users with the name {_result_.group(2)} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name" )


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
    global DATA
    id_inp = _result_.group(1)
    match index:
        case 11:
            if id_inp in DATA["mutelist"]:
                return already_ignoring
            DATA["mutelist"].append(id_inp)
            return start_ignoring % name_from_id(id_inp)
        case 12:
            if id_inp in DATA["mutelist"]:
                DATA["mutelist"].remove(id_inp)
                return stop_ignoring % name_from_id(id_inp)
            return already_not_ignoring % name_from_id(id_inp)
        case _: return "No match found"


def stalker(id_inp, time_now):
    global STALKING_LOG
    filename = str(id_inp) + ".txt"
    git_prefix = "stalker-logs/"
    file = git_prefix + filename
    myfile = Path(file)
    if not myfile.is_file():
        file = open(file, "w")
        file.close()
    while STALKING_LOG[id_inp][1]:
        resp = requests.get(profile_url % id_inp, cookies=cookies)
        match resp.status_code:
            case 200:
                resp = json.loads(resp.text)["user"]
                time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
                text = logging_text % (str(time), resp["display_name"], resp["karma"], resp["username"], resp["gender"])
                with open(file, "a") as file:
                    file.write(text)
            case 404:
                send_message(stopping_logging % id_inp)
                break
            case _:
                if timer() - time_now >= 3600:
                    send_message(f"Ending stalk session of ID: {id_inp}")
                    break
                pass
        sleep(15)
        if not STALKING_LOG[id_inp][1]:
            del STALKING_LOG[id_inp]
            break


def respond_uptime():
    sr = str(datetime.now() - STARTTIME).split(":")
    if sr[0] == "0":
        match int(sr[1])+0:
            case 0: return just_joined
            case 1: return here_for_one_min
            case _: return here_for_x_mins % str(int(sr[1])+0)
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
    t = Thread(target=stalker, args=(id_inp, timer()))
    STALKING_LOG[id_inp] = [t, True]
    t.start()
    return waking_stalking


def stop_stalking(id_inp):
    global STALKING_LOG
    if id_inp not in STALKING_LOG:
        return already_not_stalking % id_inp
    STALKING_LOG[id_inp][1] = False
    return stopping_stalking % id_inp


def mod_demod(_result_):
    global DATA
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
    global MAIN_DICT, IDLE_DICT, TIMEOUT_CONTROL
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
    if len(id_inp) ==1:
        id_inp = list(id_inp.keys())[0]
        if id_inp in DATA["knight"]:
            return knight_already_added % name_inp
        DATA["knight"].append(id_inp)
        update_data_json()
        return knight_added % name_inp
    return fix_message(f"I have seen the following users with the name {name_inp} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")


def remove_knight(_result_):
    name_inp = _result_.group(1)
    id_inp = name_inp
    if not name_inp.isnumeric():
        id_inp = return_id(id_inp)
    if not id_inp or (isinstance(id_inp, dict) and len(id_inp) == 0):
        return not_seen % name_inp
    if not isinstance(id_inp, dict):
        if not id_inp in DATA["knight"]: 
            return knight_not_added % name_inp
        DATA["knight"].remove(id_inp)
        update_data_json()
        return knight_removed % name_inp
    if len(id_inp) != 1:
        return fix_message(f"I have seen the following users with the name {name_inp} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name" )
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
    if not id_inp.isnumeric(): id_inp = return_id(id_inp)
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
    return fix_message(f"I have seen the following users with the name {name} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name")


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
    global TIMEOUT_CONTROL, MAIN_DICT, IDLE_DICT
    id_inp = int(id_inp)
    del TIMEOUT_CONTROL[int(id_inp)]
    if id_inp in MAIN_DICT: del MAIN_DICT[id_inp]
    if id_inp in IDLE_DICT: del IDLE_DICT[id_inp]
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

def admin_function_init(i, id_inp, isadmin, _result_):
    global GREET_STATUS, RUNNING, name, STARTTIME, aichatstate, GREET_TIMEOUT, DATA
    match i:
        case 0: return_response = toggle_greets(_result_)
        case 1: return_response, RUNNING = leaving, False
        case 2 if isadmin: return_response = clear_lists()
        case 3: return_response = respond_uptime()
        case 4: GREET_TIMEOUT, return_response = {}, done
        case 5: return_response = send_stats()
        case 6: return_response = "Mutelist is: %s" % " ,".join(DATA["mutelist"])
        case 7: return_response = str(TIMEOUT_CONTROL)
        case 8: restart_program()
        case 9: return_response = hide(id_inp)
        case 10 if id_inp not in DATA["mutelist"]: return_response = ily_r
        case 11 | 12: return_response = mute_func(_result_, i)
        case 13: return_response = banfunc(id_inp, _result_)
        case 14: return_response = "Current admins are: %s" % " ,".join(DATA["admins"])
        case 15: return_response = str(_result_.group(2))
        case 16: return_response = stop_stalking(str(_result_.group(2)))
        case 17: return_response = returnstalk()
        case 18: aichatstate, return_response = True, done
        case 19: aichatstate, return_response = False, done
        case 20 if is_creator(id_inp): return_response = mod_demod(_result_)
        case 21: return_response = refreshdata()
        case 22: return_response = refreshmessages()
        case 23 if isadmin: return_response = set_greet(_result_)
        case 24 if isadmin: return_response = get_greet(_result_)
        case 25 if isadmin: return_response = remove_greet(_result_)
        case 26 if isadmin: return_response = add_landmine(_result_)
        case 27 if isadmin: return_response = remove_landmine(_result_)
        case 28 if isadmin: return_response = get_landmine()
        case 29 if is_creator(id_inp): return_response = toggle_alt_universe()
        case 30 if isadmin: return_response = toggle_spam_check()
        case 31 if isadmin: return_response = get_spam_check_status()
        case 32 if isadmin: return_response = make_knight(_result_)
        case 33 if isadmin: return_response = remove_knight(_result_)
        case 34 if isadmin: return_response = toggle_shortened_greet()
        case 35 if isadmin: return_response = save_nickname(_result_)
        case 36: return_response = toggle_insult_func(_result_)
        case _: return_response = False
    if return_response:
        send_message(return_response) if int(id_inp) != 0 else print(f"Admin Command: {return_response}")


def admin_func(inputmessage, id_inp, isadmin):
    if not isadmin and id_inp not in DATA["mod"]:  return
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
    global SPAM_TIMEOUT
    if id_inp not in SPAM_TIMEOUT: SPAM_TIMEOUT[id_inp] = []
    SPAM_TIMEOUT[id_inp].append(perf_counter())


def spam_checker():
    for eyedee, spam_keys in SPAM_TIMEOUT.items():
        if eyedee in banned: continue
        if (len(spam_keys) >= 3 and spam_keys[-1] - spam_keys[-3] < 1.3) or (len(spam_keys) >= 5 and spam_keys[-1] - spam_keys[-5] < 3):
            thread(eyedee)

def image_upload(query, urly):
    global CLIENT
    if query in IMAGE_CACHE: return IMAGE_CACHE[query][1]
    for i in IMAGE_CACHE:
        if IMAGE_CACHE[i][0] == urly: return IMAGE_CACHE[i][1]
    image = CLIENT.upload_from_url(urly)
    formattedlink = image_to_link(image)
    IMAGE_CACHE[query] = [urly, formattedlink]
    update_image_cache()
    refresh_image_cache()
    return formattedlink


refresh_image_cache()


def get_image_link(query, meme):
    try:
        if meme: return get_meme()
        url = response().urls(query, 6)
        return image_upload(query, url[-1])
    except ImgurClientError:
        return f"Sorry I couldn't find {query}"
    except ImgurClientRateLimitError:
        return "Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying"


def send_pic(query, meme):
    send_message(get_image_link(query, meme))


def get_meme():
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    r = json.loads(r.text)
    link = r["url"]
    image = CLIENT.upload_from_url(link)
    return image_to_link(image)


def send_seen_db(id_inp):
    query_res = get_last_record_id(id_inp, False)
    channel_name = query_res[4]
    inputdate = query_res[-1]
    deltatime = return_deltatime(inputdate)
    name, user = query_res[1], query_res[2]
    date_string = return_datestring(deltatime.days,inputdate)
    resp = f"{date_string} {deltatime.seconds//3600} hours ago "
    if deltatime.seconds//3600 == 0:
        resp = f"{date_string} {deltatime.seconds//60 % 60} mins ago "
    if deltatime.seconds//60 % 60 == 0:
        resp = f"{date_string} a couple moments ago "
    if channel_name == "WFAF":
        return f"{name} (#{user}) was last seen {resp}in WFAF"
    res = get_last_record_id(id_inp, True)
    channel_name = channel_dict[channel_name]
    if not res:
        secs = deltatime.seconds//60 % 60
        date_channel = inputdate.split(" ")[0]
        date_string = return_datestring(deltatime.days,date_channel)
        broiler_response = f"I dont remember seeing {name} (#{user}) in WFAF but they were last seen "
        if deltatime.seconds//3600 != 0:
            return broiler_response + f"{date_string} {deltatime.seconds//3600} hours ago in {channel_name}"
        if deltatime.seconds//60 % 60 == 0:
            return broiler_response + f"a couple moments ago in {channel_name}" 
        return broiler_response + f"{date_string} {secs} mins ago in {channel_name}" 
    deltatime_wfaf = return_deltatime(res[-1])
    date_string = return_datestring(deltatime_wfaf.days,inputdate)
    re = f"{name} (#{user}) was last seen {date_string} {deltatime_wfaf.seconds//3600} hours ago "
    if deltatime_wfaf.seconds//3600 == 0:
        re = f"{name} (#{user}) was last seen {date_string} {deltatime_wfaf.seconds//60 % 60} mins ago " 
    if deltatime_wfaf.seconds//60 % 60 == 0:
        re = f"{name} (#{user}) was last seen {date_string} a couple moments ago "
    return f"{re}in WFAF but was more recently seen {resp} in {channel_name}"


def log_chats(inputmessage, user_id, inpuser):
    inputdate = datetime.today().strftime('%d-%m-%Y')
    filename = f"wfaf-logs/log ({inputdate}).txt"
    inpname = fix_name(inpuser["display_name"])
    log = message_log_text % (inpname, user_id, inputmessage) + "\n"
    with open(filename, "a+") as file: file.write(log)


def list_removal(id_inp):
    global MAIN_DICT, TIMEOUT_CONTROL, IDLE_DICT
    if id_inp in TIMEOUT_CONTROL: del TIMEOUT_CONTROL[id_inp]
    if id_inp in MAIN_DICT: del MAIN_DICT[id_inp]
    if id_inp in IDLE_DICT: del IDLE_DICT[id_inp]


def whos_here_appending(id_inp):
    global WHOS_HERE_RESPONSE
    try:
        r = requests.get(profile_url % id_inp, cookies=cookies, timeout=1)
        r = json.loads(r.text)
        name_inp = r["user"]["display_name"]
        if len(name_inp) <= 3:
            name_inp = "%s (#%s)" % (name_inp, r["user"]["username"])
    except Exception:
        name_inp = return_name(id_inp)
    finally:
        WHOS_HERE_RESPONSE.append(name_inp)

def dict_thread_starter(dict):
    threads = []
    for i in dict:
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

def reply_whos_here():
    global WHOS_HERE_RESPONSE
    dict_thread_starter(MAIN_DICT)
    threads.clear()
    idle_len = len(IDLE_DICT)
    match idle_len:
        case 0: resp = whos_here_response_no_lurkers % format_out_list(WHOS_HERE_RESPONSE)
        case 1: resp = whos_here_response_gen1 % format_out_list(WHOS_HERE_RESPONSE)
        case _: resp = whos_here_response_gen2 % (format_out_list(WHOS_HERE_RESPONSE), idle_len)
    return fix_message(resp)


def reply_whos_idle():
    global WHOS_HERE_RESPONSE
    dict_thread_starter(IDLE_DICT)
    return fix_message(whos_lurking_none) if len(IDLE_DICT) == 0 else fix_message(whos_lurking_gen % format_out_list(WHOS_HERE_RESPONSE))


def name_from_id(id_inp):
    try:
        resp = requests.get(profile_url % int(id_inp), cookies=cookies)
        resp = json.loads(resp.text)
        name = resp["user"]["display_name"]
    except:
        name = return_name(id_inp) #fallback when everything is idiotic 
    finally: return name


def get_seen(_result_):
    try:
        string = _result_.group(1)
        if string.isnumeric():
            return fix_message(send_seen_db(string))
        string = string.replace("#", "")
        possibles = {}
        for id_inp in DATA["nickname"]:
            for nickname in DATA["nickname"][id_inp]:
                regex2 = re.compile(string, re.I)
                if regex2.search(nickname):
                    possibles = {id_inp:nickname}
                    break
        if len(possibles) == 0:
            query_res = regex_query(string)
            if len(query_res) == 1:
                return send_seen_db(query_res[0][0])
            for i in query_res:
                possibles[i[0]] = i[1] + "(#" + str(i[2]) + ")"
        if len(possibles) == 1:
            try:
                return send_seen_db(list(possibles.keys())[0])
            except:
                return fix_message(f"I dont remember seeing user with name {string}")
        if len(possibles) == 0:
            return fix_message(f"I dont remember seeing user with name {string}")
        return fix_message(f"I have seen the following users with the name {string} :- {curly_replace(str(possibles))}. Specify the ID correspnding to their name and ask 'Blue seen ID'" )
    except Exception as e:
        return fix_message(f"I dont remember seeing {name_from_id(string)} around")


def coin_handling(_result_):
    global DATA
    num = _result_.group(1)
    coin_add = int(num) + 0
    if coin_add > 100 : return too_many_coins
    DATA["coins"] += coin_add
    update_data_json()
    return (adding_one_coin if num == "1" else adding_coins) % (coin_add, DATA["coins"])


def getid(_result_):
    input_str = _result_.group(4)
    id_inp = return_id(input_str)
    if not id_inp:
        return not_seen % input_str
    if not isinstance(id_inp, dict):
        if input_str.isnumeric():
            return id_response % (name_from_id(input_str), id_inp)
        return id_response % (name_from_id(id_inp), id_inp)
    match len(id_inp):
        case 0: return not_seen % input_str
        case 1: return id_response % (input_str, list(id_inp.keys())[0])
        case _: return fix_message(f"I have seen the following users with the name {input_str} :- {curly_replace(str(id_inp))}. Specify the ID correspnding to their name" )


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
    return


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
    match resp.status_code:
        case 200:
            resp = json.loads(resp.text)["user"]
            name_inp = resp["display_name"]
            karma = resp["karma"]
            username = resp["username"]
            gender = resp["gender"]
            created = resp["created_at"].split("T")
            if gender:
                return details_response_null_gender % (id_inp, name_inp, username, karma, created[0], created[1])
            return details_response % (id_inp, name_inp, username, karma, gender, created[0], created[1])
        case 404: return account_deleted
        case 403: return timeout_error
        case _: return "Unknown condition reached"


def get_insult(res):
    if not insult_control: return 
    name = res.group(1)
    r = requests.get(insult_url)
    r = json.loads(r.text)
    r = r["insult"]
    return f"{name}, {r}"


def send_feelings(index, id_inp, _result_, console):
    global DATA
    input_name = _result_.group(1)
    resp = ""
    match index:
        case 1: resp = sending_love % input_name
        case 2: resp = sending_pats % input_name
        case 3: resp = sending_hugs % _result_.group(4)
        case 4: resp = sending_bonks % input_name
        case 5 if id_inp in DATA["admin"] or console: resp = getid(_result_)
        case 6 if id_inp in DATA["admin"] or console: resp = get_details(_result_)
        case 7: resp = get_seen(_result_)
        case 8|9: Thread(target=send_pic, args=(input_name, False if index == 8 else True)).start()
        case 10: resp = get_insult(_result_)
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
        if resp and resp != "":
            if console: print(f"Console:- {resp}")
            else: send_message(resp)
        return



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
                whos_here: [],
                whos_idle: [],
                bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
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

def guessing_starter(id,message):
    if not (guessing_game.match(message) and guessing_game_status):
        return
    if id in DATA["guess"]:
        send_message("You already have a game started, try guessing a number !")
        return
    number = random.randint(1, 100)
    DATA["guess"][ID] = [number, 0]
    update_data_json()
    send_message("Okay, I have chosen a number between 1 and 100. Guess what it is!")

def guesser (id,message):
    if not( guessing_game_status and id in DATA["guess"]):
        return 
    res = guessing.match(message)
    if not res:
        return 
    guess = int(res.group(1))
    if DATA["guess"][id][1] > 5:
        send_message("You have guessed incorrectly 6 times. The number was %s" % DATA["guess"][id][0])
        del DATA["guess"][id]
    elif guess == DATA["guess"][id][0]:
        send_message(f"You guessed it! The number was {guess}")
        del DATA["guess"][id]
    elif guess > DATA["guess"][id][0]:
        send_message("Your guess was too high! Try again!")
        DATA["guess"][id][1] += 1
    elif guess < DATA["guess"][id][0]:
        send_message("Your guess was too low! Try again!")
        DATA["guess"][id][1] += 1
    update_data_json()


def matching(name_inp, dictname, input_text, console, dict_bool):
    def consolecheck(content):
        print(f"Console:- {content}") if console else send_message(content)
    for re_m in dictname:
        inputres = re_m.match(input_text)
        if not inputres: continue
        resp = dictname[re_m]
        if dict_bool:
            if re_m == whos_here: resp = reply_whos_here()
            elif re_m == whos_idle: resp = reply_whos_idle()
        else: 
            if re_m == jok: resp = get_jokes()
            elif re_m == quote: resp = get_quote(console)
            elif re_m == save_message: resp = saving_messages(name_inp, inputres)
        if resp: consolecheck(resp)
        break

@Cleverbot.connect
def chat(bot, user_input):
    return bot.single_exchange(user_input)

def ai_handler(message):
    if not aichatstate:
        return
    res = ai.match(message)
    if res:
        bot = chat(res.group(1))
        if bot == "":
            bot = "I don't know what you mean"
        send_message(bot)

Thread(target=console_input).start()
Thread(target=thread_function).start()
while True:
    try:
        ws = websocket.WebSocket()
        websocket.enableTrace(False)
        ws.connect(ws_url, cookie=main_cookie,subprotocols=subprots, origin=origin)
        ws.send(json.dumps(connect_json))
        ws.send(json.dumps(connect_json_blue))
        while RUNNING:
            result = ws.recv()
            result = json.loads(result)
            remove_blue()
            idle_function()
            clocking()
            check_singing()
            WHOS_HERE_RESPONSE = []
            whos_here_res = {
                whos_here: WHOS_HERE_RESPONSE,
                whos_idle: WHOS_HERE_RESPONSE,
                bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
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
            name = fix_name(user["display_name"])
            message = fix_message(str(b["messages"])).strip("'")
            print(f"{name} ({ID}) :- {message}")
            Thread(target=check_greeters, args=(message, ID,)).start()
            Thread(target=log_chats, args=(message, ID, user,)).start()
            admin_func(message, ID, True if ID in DATA["admin"] else False)
            guessing_starter(ID, message)
            guesser(ID, message)
            if ID in DATA["mutelist"]: continue
            coins_feelings(message, ID, False)
            matching(fix_name(name), response_dict, message, False, False)
            matching(fix_name(name), whos_here_res, message, False, True)
            Thread(target=ai_handler, args=(message,)).start()
    except Exception as e:
        print("Hello young boi an error occurred :- %s" % e)
        sleep(5)
