# pylint: disable=missing-function-docstring, global-statement, wildcard-import. broad-except, unused-wildcard-import
import json
import random
from pathlib import Path
from threading import Thread
from time import gmtime, perf_counter, sleep, strftime
from timeit import default_timer as timer

import requests
import websocket
from imgurpython.helpers.error import (ImgurClientError,
                                       ImgurClientRateLimitError)

from gc_logging import *
from utils import *
from var import *


def send_message(content):
    jsonmessage = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) + "\",\"id\":null,\"action\":\"speak\"}"}

    jsonmessage_alt = {"command": "message", "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}",
                       "data": "{\"message\":\""+ fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if ALT_UNIVERSE_TOGGLE:
        ws.send(json.dumps(jsonmessage_alt))
    else:
        ws.send(json.dumps(jsonmessage))


def return_id(string):
    try:
        refresh_seen()
        if string.isnumeric():
            _id_ = string
            if _id_ in SEEN_DATA:
                return _id_
            return False
        string = string.replace("#", "")
        count = 0
        possibles = {}
        for _id_ in SEEN_DATA:
            _name_ = SEEN_DATA[_id_]["name"]
            username = SEEN_DATA[_id_]["username"]
            regex1 = re.compile(r'^%s' % fix_name(string), re.I)
            if regex1.search(_name_) or regex1.search(username):
                possibles[_id_] = _name_ + " (#" + username + ")"
            else:
                count += 1
        for _id_ in DATA["nickname"]:
            for nickname in DATA["nickname"][_id_]:
                regex2 = re.compile(string, re.I)
                count += 1
                if regex2.search(nickname):
                    possibles = {}
                    possibles[_id_] = nickname
                else:
                    pass
        total = len(SEEN_DATA)
        for _id_ in DATA["nickname"]:
            total += len(DATA["nickname"][_id_])
        if count == total and len(possibles) == 0:
            return False
        return possibles
    except Exception:
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
        if perf_counter() - time_stamp >= 240:
            val = list(TIMEOUT_CONTROL.keys())[i]
            if val in MAIN_DICT:
                IDLE_DICT[val] = MAIN_DICT[val]
                del MAIN_DICT[val]
        elif perf_counter() - time_stamp < 240:
            val = list(TIMEOUT_CONTROL.keys())[i]
            if val in IDLE_DICT:
                del IDLE_DICT[val]


def clocking():
    global RESET_CLOCK, GREET_TIMEOUT
    if RESET_CLOCK == 500:
        GREET_TIMEOUT, RESET_CLOCK = {}, 0


def refreshdata():
    global DATA
    with open('data.json', 'r') as file:
        DATA = json.loads(file.read())


def update_data_json():
    global DATA
    with open('data.json', 'w') as file:
        json.dump(DATA, file)
    refreshdata()


def refreshmessages():
    global SAVED_MESSAGES
    with open('messages.json', 'r') as file:
        SAVED_MESSAGES = json.loads(file.read())


def update_messages_json():
    global SAVED_MESSAGES
    with open('messages.json', 'w') as file:
        json.dump(SAVED_MESSAGES, file)
    refreshmessages()


def refresh_seen():
    global SEEN_DATA
    with open('seen.json', 'r') as file:
        SEEN_DATA = json.load(file)


def update_seen_json():
    global SEEN_DATA
    with open('seen.json', 'w') as file:
        json.dump(SEEN_DATA, file)


def update_seen(_name_, _id_, _username_):
    time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    _id_ = str(_id_)
    if _id_ not in SEEN_DATA:
        SEEN_DATA[_id_] = {}
    SEEN_DATA[_id_]["name"] = _name_
    SEEN_DATA[_id_]["username"] = _username_
    SEEN_DATA[_id_]["channel_name"] = {"WFAF": time_stamp}
    update_seen_json()


def update_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'w') as file:
        json.dump(IMAGE_CACHE, file)


def refresh_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'r') as file:
        IMAGE_CACHE = json.loads(file.read())


def saved_message_handler(_id_, _name_):
    if _id_ in SAVED_MESSAGES:
        if len(SAVED_MESSAGES[_id_]) == 1:
            output_message = "Hello %s I have a message for you: %s" % (
                _name_, SAVED_MESSAGES[_id_][0])
            sleep(0.9)
            send_message(output_message)
            del SAVED_MESSAGES[_id_]
        else:
            sleep(1)
            output_message = "Hello %s I have a few messages for you from some people" % _name_
            send_message(output_message)
            for messages in SAVED_MESSAGES[_id_]:
                send_message(messages)
                sleep(0.4)
            del SAVED_MESSAGES[_id_]
        update_messages_json()


def greet_text(count, _name_):
    if not SHORTEN_GREET_TOGGLE:
        match count:
            case 1: return Greet_1 % _name_
            case 2: return Greet_2 % _name_
            case 3: return Greet_general % _name_
    else:
        match count:
            case 1: return Greet_1_short % _name_
            case 2: return Greet_2_short % _name_
            case 3: return Greet_general_short % _name_


def send_greet(_name_, _username_):
    if len(_name_) > 3:
        _username_ = ""
    else:
        _username_ = " (#%s)" % _username_
    if _name_ in GREET_TIMEOUT:
        match GREET_TIMEOUT[_name_]:
            case "1":
                send_message(greet_text(1, "%s%s" % (_name_, _username_)))
                GREET_TIMEOUT[_name_] = "2"
            case "2":
                send_message(greet_text(2, "%s%s" % (_name_, _username_)))
                GREET_TIMEOUT[_name_] = "3"
            case "3": pass
    else:
        send_message(greet_text(3, "%s%s" % (_name_, _username_)))
        GREET_TIMEOUT[_name_] = "1"


def greet(action, _result_, greet_var, userdat):
    global DATA, SAVED_MESSAGES, MAIN_DICT, IDLE_DICT, TIMEOUT_CONTROL, STATS_LIST
    if (action in userdat) and ("user" in userdat) and "display_name" in userdat["user"]:
        _name_ = fix_name(userdat["user"]["display_name"])
        username = userdat["user"]["username"]
        _id_ = userdat["user"]["id"]
        if _result_ == "add":
            MAIN_DICT[_id_] = _name_
            STATS_LIST[_id_] = _name_
            TIMEOUT_CONTROL[_id_] = perf_counter()
            saved_message_handler(str(_id_), _name_)
        elif _result_ == "remove":
            list_removal(_id_)
        _id_ = str(_id_)
        if GREET_STATUS and greet_var and _id_ not in DATA["greet_exempt"]:
            if _id_ in DATA["custom_greet"]:
                send_message(DATA["custom_greet"][_id_])
            elif _id_ in DATA["knight"]:
                send_message("Greetings %s ~*" % _name_)
            else:
                send_greet(_name_, username)
        update_seen(_name_, _id_, username)


def dis_en_greets(_id_):
    global GREET_STATUS
    if _id_ == "16008266" and GREET_STATUS:
        send_message(disabling_greet)
        GREET_STATUS = False
    elif _id_ == "20909261" and not GREET_STATUS:
        send_message(re_enabling_greet)
        GREET_STATUS = True


def check_greeters(inputmessage, _id_):
    global GREET_STATUS, DATA
    found = False
    if _id_ in DATA["greeter_fallback"]:
        for reg_m in greet_check:
            res = reg_m.match(inputmessage)
            if inputmessage in DATA["custom_greet"].values() or res or inputmessage == blue_greet:
                dis_en_greets(_id_)
                found = True
                break
        if not found:
            for reg_m in DATA["custom_greet"].values():
                reg = re.compile(r"" + reg_m + r"", re.I)
                res = reg.search(inputmessage)
                if res:
                    dis_en_greets(_id_)
                    break


def saving_messages(_name_, _result_):
    global SAVED_MESSAGES
    _input_ = _result_.group(1).rstrip()
    if _input_.isnumeric():
        _id_ = _input_
    else:
        _id_ = return_id(_input_)
    if _id_:
        if isinstance(_id_, dict):
            if _id_ in SAVED_MESSAGES:
                SAVED_MESSAGES[_id_].append(_name_ + ":- " + _result_.group(2))
            else:
                SAVED_MESSAGES[_id_] = [_name_ + ":- " + _result_.group(2)]
            update_messages_json()
            return save_message_r % _input_
        match len(_id_):
            case 0: return not_seen % _input_
            case 1:
                _id_ = list(_id_.keys())[0]
                if _id_ in SAVED_MESSAGES:
                    SAVED_MESSAGES[_id_].append("%s:- %s" % (_name_, _result_.group(2)))
                else:
                    SAVED_MESSAGES[_id_] = ["%s:- %s" % (_name_, _result_.group(2))]
                update_messages_json()
                return save_message_r % _input_
            case _: return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (result.group(2), fix_message(str(_id_)).replace("{", "").replace("}", "")))
    else:
        return not_seen % _input_


def downvote(cookie, _id_):
    requests.get(karma_url % _id_, cookies=cookie)


def ban_log(banned_id, admin_id):
    if admin_id != 0:
        resp = requests.get(profile_url % int(admin_id), cookies=cookies)
        admin_name = json.loads(resp.text)["user"]["display_name"]
    else:
        admin_name = "Console Admin"
    log = "Banned %s by %s \n" % (banned_id, admin_name)
    with open("log.txt", "a") as file:
        file.write(log)


def thread(_id_):
    banned.add(id)
    for i in cookiejar:
        cookie = {'_prototype_app_session': i}
        Thread(target=downvote, args=(cookie, _id_)).start()


def mute_func(_result_, index):
    global DATA
    _id_ = _result_.group(1)
    match index:
        case 11:
            if _id_ in DATA["mutelist"]:
                return already_ignoring
            DATA["mutelist"].append(_id_)
            update_data_json()
            return start_ignoring % _id_
        case 12:
            if _id_ in DATA["mutelist"]:
                DATA["mutelist"].remove(_id_)
                update_data_json()
                return stop_ignoring % _id_
            return already_not_ignoring % _id_
        case _: return "No match found"


def stalker(_id_, time_now):
    global STALKING_LOG
    filename = str(_id_) + ".txt"
    git_prefix = "stalker-logs/"
    file = git_prefix + filename
    myfile = Path(file)
    if not myfile.is_file():
        file = open(filename, "w")
        file.close()
    while STALKING_LOG[_id_][1]:
        resp = requests.get(profile_url % _id_, cookies=cookies)
        match resp.status_code:
            case 200:
                resp = json.loads(resp.text)["user"]
                tempname = resp["display_name"]
                karma = resp["karma"]
                username = resp["username"]
                gender = resp["gender"]
                time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
                text = logging_text % (
                    str(time), tempname, karma, username, gender)
                with open(filename, "a") as file:
                    file.write(text)
            case 404:
                send_message(stopping_logging % _id_)
                break
            case _:
                if timer() - time_now >= 3600:
                    send_message("Ending stalk session of ID: " + _id_)
                    break
                pass
        sleep(15)
        if not STALKING_LOG[_id_][1]:
            del STALKING_LOG[_id_]
            break


def respond_uptime():
    sr = str(datetime.now() - STARTTIME).split(":")
    if sr[0] == "0":
        match int(sr[1])+0:
            case 0: return just_joined
            case 1: return here_for_one_min
            case _: return here_for_x_mins % str(int(sr[1])+0)
    return here_for_hours_and_mins % (str(sr[0]), str(int(sr[1]) + 0))


def send_stats():
    sr = str(datetime.now() - STARTTIME).split(":")
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    return stats_response % (len(stats), len(STATS_LIST), sr[0], sr[1], str(r))


def start_stalking(_id_):
    if _id_ not in STALKING_LOG:
        t = Thread(target=stalker, args=(_id_, timer()))
        STALKING_LOG[_id_] = [t, True]
        t.start()
        return waking_stalking
    return already_stalking % _id_


def stop_stalking(_id_):
    global STALKING_LOG
    if _id_ in STALKING_LOG:
        STALKING_LOG[_id_][1] = False
        return stopping_stalking % _id_
    return already_not_stalking % _id_


def mod_demod(_result_):
    global DATA
    mod_id = _result_.group(2)
    if _result_.group(1) == "mod":
        if mod_id in DATA["mod"] or mod_id in DATA["admin"]:
            return already_mod % mod_id
        DATA["mod"].append(mod_id)
        update_data_json()
        return mod_response % mod_id
    if _result_.group(1) == "demod":
        if mod_id in DATA["mod"]:
            DATA["mod"].remove(mod_id)
            update_data_json()
            return demod_response % mod_id
        if mod_id in DATA["admin"]:
            DATA["admin"].remove(mod_id)
            update_data_json()
            return demod_response % mod_id
        return not_mod % mod_id


def clear_lists():
    global MAIN_DICT, IDLE_DICT, TIMEOUT_CONTROL
    TIMEOUT_CONTROL.clear()
    MAIN_DICT.clear()
    IDLE_DICT.clear()
    return clear_list


def set_greet(_result_):
    _id_ = _result_.group(1)
    greettext = _result_.group(3)
    if _id_ not in DATA["custom_greet"]:
        DATA["custom_greet"][_id_] = greettext
        update_data_json()
        return greet_set % (_id_, greettext)
    DATA["custom_greet"][_id_] = greettext
    update_data_json()
    return greet_updated % (_id_, greettext)


def get_greet(_result_):
    _id_ = _result_.group(1)
    if _id_ in DATA["custom_greet"]:
        return greet_response % (_id_, DATA["custom_greet"][_id_])
    return greet_not_set % _id_


def remove_greet(_result_):
    _id_ = _result_.group(1)
    if _id_ in DATA["custom_greet"]:
        del DATA["custom_greet"][_id_]
        update_data_json()
        return greet_removed % _id_
    return greet_not_set % _id_


def get_landmine():
    landmine_list = DATA["landmine_words"]
    return fix_message(landmine_list)


def add_landmine(_result_):
    word = _result_.group(1)
    if word not in DATA["landmine_words"]:
        DATA["landmine_words"].append(word)
        update_data_json()
        return landmine_added % word
    return landmine_already_added % word


def remove_landmine(_result_):
    word = _result_.group(1)
    if word in DATA["landmine_words"]:
        DATA["landmine_words"].remove(word)
        update_data_json()
        return landmine_removed % word
    return landmine_not_present % word


def toggle_alt_universe():
    global ALT_UNIVERSE_TOGGLE
    if ALT_UNIVERSE_TOGGLE:
        ALT_UNIVERSE_TOGGLE = False
    else:
        ALT_UNIVERSE_TOGGLE = True


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
    _name_ = _result_.group(1)
    if _name_.isnumeric():
        _id_ = _name_
        if _id_ not in DATA["knight"]:
            DATA["knight"].append(_id_)
            update_data_json()
            return knight_added % _name_
        return knight_already_added % _name_
    _id_ = return_id(_name_)
    if not _id_:
        return not_seen % _name_
    if not isinstance(_id_, dict):
        if _id_ not in DATA["knight"]:
            DATA["knight"].append(_id_)
            update_data_json()
            return knight_added % _name_
        return knight_already_added % _name_
    match len(_id_):
        case 0:
            return not_seen % _name_
        case 1:
            _id_ = list(_id_.keys())[0]
            if _id_ not in DATA["knight"]:
                DATA["knight"].append(_id_)
                update_data_json()
                return knight_added % _name_
            return knight_already_added % _name_
        case _:
            return fix_message("I have seen the following users with the name %s :- %s. Specify the _id_ correspnding to their name" % (_name_, fix_message(str(_id_)).replace("{", "").replace("}", "")))


def remove_knight(_result_):
    _name_ = _result_.group(1)
    if _name_.isnumeric():
        _id_ = _name_
        if _id_ in DATA["knight"]:
            DATA["knight"].remove(_id_)
            update_data_json()
            return knight_removed % _name_
        return knight_not_added % _name_
    _id_ = return_id(_name_)
    if not _id_ or (isinstance(_id_, dict) and len(_id_) == 0):
        return not_seen % _name_
    if not isinstance(_id_, dict):
        if _id_ in DATA["knight"]:
            DATA["knight"].remove(_id_)
            update_data_json()
            return knight_removed % _name_
        return knight_not_added % _name_
    if len(_id_) == 1:
        _id_ = list(_id_.keys())[0]
        if _id_ in DATA["knight"]:
            DATA["knight"].remove(_id_)
            update_data_json()
            return knight_removed % _name_
        return knight_not_added % _name_
    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (_name_, fix_message(str(_id_)).replace("{", "").replace("}", "")))


def toggle_shortened_greet():
    global SHORTEN_GREET_TOGGLE
    if SHORTEN_GREET_TOGGLE:
        SHORTEN_GREET_TOGGLE = False
        return shortened_greet_off
    SHORTEN_GREET_TOGGLE = True
    return shortened_greet_on


def save_nickname(_result_):
    _name_ = _result_.group(1)
    nickname = _result_.group(2)
    if _name_.isnumeric():
        _id_ = _name_
        if _id_ not in DATA["nickname"]:
            DATA["nickname"][_id_] = [nickname]
            update_data_json()
            return nickname_added % (nickname, _name_)
        DATA["nickname"][_id_].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, _name_)
    _id_ = return_id(_name_)
    if not _id_ or (isinstance(_id_, dict) and len(_id_) == 0):
        return not_seen % _name_
    if not isinstance(_id_, dict):
        if _id_ not in DATA["nickname"]:
            DATA["nickname"][_id_] = [nickname]
            update_data_json()
            return nickname_added % (nickname, _name_)
        DATA["nickname"][_id_].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, _name_)
    if len(_id_) == 1:
        _id_ = list(_id_.keys())[0]
        if _id_ not in DATA["nickname"]:
            DATA["nickname"][_id_] = [nickname]
            update_data_json()
            return nickname_added % (nickname, _name_)
        DATA["nickname"][_id_].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, _name_)
    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (name, fix_message(str(id)).replace("{", "").replace("}", "")))


def toggle_greets(_result_):
    global GREET_STATUS
    action = _result_.group(1)
    if action == "enable":
        GREET_STATUS = True
        return done
    if action == "disable":
        if GREET_STATUS:
            GREET_STATUS = False
            return done
        return already_not_greeting
    return "Unexpected response"


def hide(_id_):
    global TIMEOUT_CONTROL, MAIN_DICT, IDLE_DICT
    _id_ = int(_id_)
    del TIMEOUT_CONTROL[int(_id_)]
    if _id_ in MAIN_DICT:
        del MAIN_DICT[_id_]
    if _id_ in IDLE_DICT:
        del IDLE_DICT[_id_]
    return aye_aye


def banfunc(_result_):
    id_ban = _result_.group(1)
    thread(id_ban)
    Thread(target=ban_log, args=(id_ban, id,)).start()
    return banning_response % id_ban


def returnstalk():
    if STALKING_LOG:
        return stalking_following % fix_message(str(STALKING_LOG.keys()))
    return stalking_no_one


def admin_function_init(i, _id_, isadmin, _result_):
    global GREET_STATUS, RUNNING, name, STARTTIME, aichatstate, GREET_TIMEOUT, DATA
    match i:
        case 0: return_response = toggle_greets(_result_)
        case 1: return_response, RUNNING = leaving, False
        case 2 if isadmin: return_response = clear_lists()
        case 3: return_response = respond_uptime()
        case 4: GREET_TIMEOUT, return_response = {}, done
        case 5: return_response = send_stats()
        case 6: return_response = "Mutelist is: %s" % fix_message(str(DATA["mutelist"]))
        case 7: return_response = str(TIMEOUT_CONTROL)
        case 8:
            return_response = restarting
            restart_program()
        case 9: return_response = hide(_id_)
        case 10 if _id_ not in DATA["mutelist"]: return_response = ily_r
        case 11 | 12: return_response = mute_func(_result_, i)
        case 13: return_response = banfunc(_result_)
        case 14: return_response = "Current admins are: %s" % fix_message(str(DATA["admins"]))
        case 15: return_response = str(_result_.group(2))
        case 16: return_response = stop_stalking(str(_result_.group(2)))
        case 17: return_response = returnstalk()
        case 18: aichatstate. return_response = True, done  # type: ignore
        case 19: aichatstate, return_response = False, done
        case 20 if _id_ in ("0", "14267520"): return_response = mod_demod(_result_)
        case 21:
            refreshdata()
            return_response = done
        case 22:
            refreshmessages()
            return_response = done
        case 23 if isadmin: return_response = set_greet(_result_)
        case 24 if isadmin: return_response = get_greet(_result_)
        case 25 if isadmin: return_response = remove_greet(_result_)
        case 26 if isadmin: return_response = add_landmine(_result_)
        case 27 if isadmin: return_response = remove_landmine(_result_)
        case 28 if isadmin: return_response = get_landmine()
        case 29 if _id_ in ("0", "14267520"):
            toggle_alt_universe()
            return_response = done
        case 30 if isadmin: return_response = toggle_spam_check()
        case 31 if isadmin: return_response = get_spam_check_status()
        case 32 if isadmin: return_response = make_knight(_result_)
        case 33 if isadmin: return_response = remove_knight(_result_)
        case 34 if isadmin: return_response = toggle_shortened_greet()
        case 35 if isadmin: return_response = save_nickname(_result_)
        case _: return_response = False
    if return_response:
        if int(_id_) != 0:
            send_message(return_response)
        else:
            print("Admin Command: " + return_response)


def admin_func(inputmessage, _id_, isadmin):
    for i, command in enumerate(admin_commands):
        res = command.match(inputmessage)
        if res:
            admin_function_init(i, _id_, isadmin, res)
            break


def landmine_checker(inputmessage, _id_):
    for word in DATA["landmine_words"]:
        regex1 = re.compile(r"%s" % word, re.I)
        if regex1.search(inputmessage):
            thread(_id_)
            break


def spam_controlling(_id_):
    global SPAM_TIMEOUT
    if _id_ in SPAM_TIMEOUT:
        SPAM_TIMEOUT[_id_].append(perf_counter())
    else:
        SPAM_TIMEOUT[_id_] = [perf_counter()]


def spam_checker():
    for eyedee, spam_keys in SPAM_TIMEOUT.items():
        if eyedee not in banned:
            if len(spam_keys) >= 3 and spam_keys[-1] - spam_keys[-3] < 1.3:
                thread(eyedee)
                return
            if len(spam_keys) >= 5 and spam_keys[-1] - spam_keys[-5] < 3:
                thread(eyedee)
                return


def image_upload(query, urly):
    global CLIENT
    if query in IMAGE_CACHE:
        return IMAGE_CACHE[query][1]
    for i in IMAGE_CACHE:
        if IMAGE_CACHE[i][0] == urly:
            return IMAGE_CACHE[i][1]
    image = CLIENT.upload_from_url(urly)
    link = image["link"].replace("https://", "")
    formattedlink = "Image: " + link
    IMAGE_CACHE[query] = [urly, formattedlink]
    update_image_cache()
    refresh_image_cache()
    return formattedlink


def get_image_link(query, meme):
    url = response().urls(query, 6)
    try:
        if meme:
            return get_meme()
        return image_upload(query, url[-1])
    except ImgurClientError:
        return "Sorry I couldn't find %s" % query
    except ImgurClientRateLimitError:
        return "Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying"


def send_pic(query, meme):
    send_message(get_image_link(query, meme))


def get_meme():
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    r = json.loads(r.text)
    link = r["url"]
    image = CLIENT.upload_from_url(link)
    link = image["link"].replace("https://", "")
    formattedlink = "Image: " + link
    return formattedlink


def send_seen(_id_):
    refresh_seen()
    current_time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    _name_ = SEEN_DATA[_id_]["name"]
    username = SEEN_DATA[_id_]["username"]
    lastseen_list = {}
    for key in SEEN_DATA[_id_]["channel_name"]:
        inputdate = SEEN_DATA[_id_]["channel_name"][key]
        lastseen_list[inputdate] = key
    inputdate = max(lastseen_list)
    channel_name = lastseen_list[inputdate]
    if "WFAF" in SEEN_DATA[_id_]["channel_name"]:
        inputdate = SEEN_DATA[_id_]["channel_name"]["WFAF"].split(" ")[0]
        deltatime = datetime.strptime(current_time, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(
            SEEN_DATA[_id_]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
        match deltatime.days:
            case 0: date_string = "today"
            case 1: date_string = "yesterday"
            case _: date_string = "on " + inputdate.split("-")[1] + "/" + inputdate.split("-")[2]
        if deltatime.seconds//3600 == 0:
            if deltatime.seconds//60 % 60 == 0:
                response_wfaf = "%s (#%s) was last seen %s a couple moments ago in WFAF" % (
                    _name_, username, date_string)
            else:
                response_wfaf = "%s (#%s) was last seen %s %s mins ago in WFAF" % (
                    _name_, username, date_string, deltatime.seconds//60 % 60)
        else:
            response_wfaf = "%s (#%s) was last seen %s %s hours and %s mins ago in WFAF" % (
                _name_, username, date_string, deltatime.seconds//3600, deltatime.seconds//60 % 60)
        if channel_name == "WFAF":
            return response_wfaf
        #Code-block for when top find channel is not wfaf
        date_channel = SEEN_DATA[_id_]["channel_name"][channel_name].split(" ")[
            0]
        deltatime_channel = datetime.strptime(current_time, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(
            SEEN_DATA[_id_]["channel_name"][channel_name], "%Y-%m-%d %H:%M:%S")
        match deltatime_channel.days:
            case 0: date_string_channel = "today"
            case 1: date_string_channel = "yesterday"
            case _: date_string_channel = "on " + date_channel.split("-")[1] + " " + date_channel.strptime("%b")
        if deltatime_channel.seconds//3600 == 0:
            if deltatime_channel.seconds//60 % 60 == 0:
                response_channel = " but was more recently seen %s just now in %s" % (
                    date_string_channel, channel_name)
            else:
                response_channel = " but was more recently seen %s %s mins ago in %s" % (
                    date_string_channel, deltatime_channel.seconds//60 % 60, channel_name)
        else:
            response_channel = " but was more recently seen %s %s hours and %s mins ago in %s" % (
                date_string_channel, deltatime_channel.seconds//3600, deltatime_channel.seconds//60 % 60, channel_name)
        return response_wfaf + response_channel
        
    #Code-block for when _name_ is not found in wfaf
    deltatime = datetime.strptime(
        current_time, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(inputdate, "%Y-%m-%d %H:%M:%S")
    date_channel = SEEN_DATA[_id_]["channel_name"][channel_name].split(" ")[0]
    secs = deltatime.seconds//60 % 60
    match deltatime.days:
        case 0: date_string = "today"
        case 1: date_string = "yesterday"
        case _: date_string = "on " + date_channel.split("-")[1] + " " + date_channel.strptime("%b")
    broiler_response = "I dont remember seeing %s (#%s) in WFAF but they were last seen " % (_name_, username)
    if deltatime.seconds//3600 == 0:
        return  broiler_response + "%s %s mins ago in %s" % ( date_string, secs, channel_name)
    return broiler_response + "%s %s hours and %s mins ago in %s" % (date_string, deltatime.seconds//3600, secs, channel_name)


def log_chats(inputmessage, user_id, inpuser):
    inputdate = datetime.today().strftime('%d-%m-%Y')
    filename = "wfaf-logs/log (%s).txt" % inputdate
    inpname = fix_name(inpuser["display_name"])
    log = message_log_text % (inpname, user_id, inputmessage) + "\n"
    with open(filename, "a+") as file:
        file.write(log)


def list_removal(_id_):
    global MAIN_DICT, TIMEOUT_CONTROL, IDLE_DICT
    if _id_ in TIMEOUT_CONTROL:
        del TIMEOUT_CONTROL[_id_]
    if _id_ in MAIN_DICT:
        del MAIN_DICT[_id_]
    if _id_ in IDLE_DICT:
        del IDLE_DICT[_id_]


def whos_here_appending(_id_):
    global WHOS_HERE_RESPONSE
    try:
        r = requests.get(profile_url % _id_, cookies=cookies, timeout=1)
        r = json.loads(r.text)
        if len(r["user"]["display_name"]) > 3:
            _name_ = r["user"]["display_name"]
        else:
            _name_ = "%s (#%s)" % (r["user"]["display_name"], r["user"]["username"])
    except Exception:
        _id_ = str(_id_)
        _name_ = SEEN_DATA[_id_]["_name_"]
        if len(_name_) <= 3:
            _name_ = "%s (#%s)" % (_name_, SEEN_DATA[_id_]["username"])
    finally:
        WHOS_HERE_RESPONSE.append(_name_)


def reply_whos_here():
    global WHOS_HERE_RESPONSE
    for i in MAIN_DICT:
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    threads.clear()
    idle_len = len(IDLE_DICT)
    match idle_len:
        case 0: resp = whos_here_response_no_lurkers % format_out_list(WHOS_HERE_RESPONSE)
        case 1: resp =  whos_here_response_gen1 % format_out_list(WHOS_HERE_RESPONSE)
        case _: resp = whos_here_response_gen2 % (format_out_list(WHOS_HERE_RESPONSE), idle_len)
    return fix_message(resp)


def reply_whos_idle():
    global WHOS_HERE_RESPONSE
    for i in IDLE_DICT:
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    threads.clear()
    if len(IDLE_DICT) == 0:
        return fix_message(whos_lurking_none)
    return fix_message(whos_lurking_gen % format_out_list(WHOS_HERE_RESPONSE))


def get_seen(_result_):
    while True:
        try:
            refresh_seen()
            string = _result_.group(1)
            if string.isnumeric():
                _id_ = string
                if _id_ in SEEN_DATA:
                    return send_seen(_id_)
                return fix_message("I dont remember seeing user with ID %s" % str(_id_))
            string = string.replace("#", "")
            n = 0
            possibles = {}
            for _id_ in SEEN_DATA:
                _name_ = SEEN_DATA[_id_]["name"]
                username = SEEN_DATA[_id_]["username"]
                regex1 = re.compile(r'^%s' % fix_name(string), re.IGNORECASE)
                if regex1.search(_name_) or regex1.search(username):
                    possibles[_id_] = _name_
                else:
                    n += 1
            for _id_ in DATA["nickname"]:
                for nickname in DATA["nickname"][_id_]:
                    regex2 = re.compile(string, re.IGNORECASE)
                    n += 1
                    if regex2.search(nickname):
                        possibles = {}
                        possibles[_id_] = nickname
                    else:
                        pass
            total = len(SEEN_DATA)
            for _id_ in DATA["nickname"]:
                total += len(DATA["nickname"][_id_])
            if len(possibles) == 1:
                if list(possibles.keys())[0] in SEEN_DATA:
                    return send_seen(list(possibles.keys())[0])
                return fix_message("I dont remember seeing user with name %s" % string)
            if n == total:
                return fix_message("I dont remember seeing user with name %s" % string)
            return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name and ask 'Blue seen ID'" % (string, fix_message(str(possibles)).replace("{", "").replace("}", "")))
        except Exception as error:
            print("Error in get_seen %s" % error)
            sleep(1)


def coin_handling(_result_):
    global DATA
    num = _result_.group(1)
    coin_add = int(num)
    if 1 <= coin_add <= 100 :
        DATA["coins"] = coin_add + DATA["coins"]
        update_data_json()
        if num == "1":
            return adding_one_coin % (coin_add + 0, DATA["coins"])
        return adding_coins % (coin_add + 0, DATA["coins"])
    if coin_add > 100:
        return too_many_coins


def getid(_result_):
    input_str = _result_.group(4)
    _id_ = return_id(input_str)
    if not _id_:
        return not_seen % input_str
    if isinstance(_id_, dict):
        return id_response % (input_str, _id_)
    match len(_id_):
        case 0: return not_seen % input_str
        case 1: return id_response % (input_str, list(_id_.keys())[0])
        case _: return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (input_str, fix_message(str(id)).replace("{", "").replace("}", "")))


def get_jokes():
    resp = requests.get(jokes_url)
    if resp.status_code == 200:
        joke = json.loads(resp.text)["attachments"][0]["text"]
        return joke
    return "Error: " + str(resp.status_code)


def get_quote(console):
    resp = requests.get('https://api.quotable.io/random')
    content = str(resp.json()['content'])
    author = "~ by " + str(resp.json()['author'])
    if console:
        print("Console:- %s" % content)
        sleep(0.2)
        print("Console:- %s" % author)
    else:
        send_message(content)
        sleep(0.2)
        send_message(author)


def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")


def check_singing():
    member_len = len(TIMEOUT_CONTROL)
    if 3 <= member_len <= 4 and random.randint(0, 100000) % 93870 == 0:
        Thread(target=singing).start()


def get_details(_result_):
    _id_ = int(_result_.group(2))
    resp = requests.get(profile_url % _id_, cookies=cookies)
    match resp.status_code:
        case 200:
            resp = json.loads(resp.text)["user"]
            _name_ = resp["display_name"]
            karma = resp["karma"]
            username = resp["username"]
            gender = resp["gender"]
            created = resp["created_at"].split("T")
            if gender:
                return details_response_null_gender % (_id_, _name_, username, karma, created[0], created[1])
            return details_response % (_id_, _name_, username, karma, gender, created[0], created[1])
        case 404: return account_deleted
        case 403: return timeout_error
        case _: return "Unknown condition reached"


def send_feelings(index, _id_, _result_, console):
    global DATA
    input_name = _result_.group(1)
    resp = ""
    match index:
        case 1: resp = sending_love % input_name
        case 2: resp = sending_pats % input_name
        case 3: resp = sending_hugs % _result_.group(4)
        case 4: resp = sending_bonks % input_name
        case 5 if _id_ in DATA["admin"] or console: resp = getid(_result_)
        case 6 if _id_ in DATA["admin"] or console: resp = get_details(_result_)
        case 7: resp = get_seen(_result_)
        case 8: Thread(target=send_pic, args=(input_name, False)).start()
        case 9: Thread(target=send_pic, args=(input_name, True)).start()
    return resp


def coins_feelings(input_message, _id_, console):
    for reg_m in coinsandfeelings:
        _result_ = reg_m.match(input_message)
        if _result_:
            index = coinsandfeelings.index(reg_m)
            if index == 0:
                resp = coin_handling(_result_)
            else:
                resp = send_feelings(index, _id_, _result_, True)
            if resp and resp != "":
                if console:
                    print("Console:-%s" % resp)
                else:
                    send_message(resp)
            break


def console_input():
    while True:
        try:
            text = input()
            _name_ = "Console Admin"
            _result_ = consoleinput.match(text)
            if _result_:
                content = result.group(1)
                send_message(content)
            else:
                whoshere = {
                    whos_here: WHOS_HERE_RESPONSE,
                    whos_idle: whos_idle_r,
                    bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
                    dice: dice_statement % random.randint(1, 6)
                }
                admin_func(text, 0, True)
                matching(fix_name(_name_), response_dict, text, True, False)
                matching(fix_name(_name_), whoshere, text, True, True)
                coins_feelings(text, id, True)
        except Exception as error:
            print(error)


def matching(_name_, dictname, input_text, console, dict_bool):
    def consolecheck(content):
        if console:
            print("Console:- %s" % content)
        else:
            send_message(content)
    for re_m in dictname:
        inputres = re_m.match(input_text)
        if inputres:
            if dict_bool:
                if re_m == whos_here:
                    resp = reply_whos_here()
                elif re_m == whos_idle:
                    resp = reply_whos_idle()
            elif not dict_bool:
                if re_m == jok:
                    resp = get_jokes()
                elif re_m == quote:
                    get_quote(console)
                elif re_m == save_message:
                    resp = saving_messages(_name_, inputres)
            else:
                resp = dictname[re_m]
            if resp:
                consolecheck(resp)
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
            update_seen_json()
            RESET_CLOCK += 1
            result = ws.recv()
            result = json.loads(result)
            remove_blue()
            idle_function()
            clocking()
            check_singing()
            WHOS_HERE_RESPONSE = whos_idle_r = []
            whos_here_res = {
                whos_here: WHOS_HERE_RESPONSE,
                whos_idle: whos_idle_r,
                bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
                dice: dice_statement % random.randint(1, 6)
            }
            if ("identifier" in result) and ("message" in result):
                b = result["message"]
                greet("user_connected", "add", True, b)
                greet("typing", "add", False, b)
                greet("user_disconnected", "remove", False, b)
                greet("messages", "add", False, b)
                if "messages" in b and "user" in b:
                    user = b["user"]
                    ID = str(user["id"])
                    # spam_controlling(ID)
                    # spam_checker()
                    name = fix_name(user["display_name"])
                    message = fix_message(str(b["messages"])).strip("'")
                    print(b["user"]["display_name"] +
                          " (%s) :- " % ID + message)
                    #Thread(target=landmine_checker, args=(message,ID)).start()
                    Thread(target=check_greeters, args=(message, ID,)).start()
                    Thread(target=log_chats, args=(message, ID, user,)).start()
                    if ID not in DATA["mutelist"]:
                        coins_feelings(message, ID, False)
                        matching(fix_name(name), response_dict,
                                 message, False, False)
                        matching(fix_name(name), whos_here_res,
                                 message, False, True)
                    if ID in DATA["admin"]:
                        admin_func(message, ID, True)
                    elif ID in DATA["mod"]:
                        admin_func(message, ID, False)
    except Exception as e:
        print("Hello young boi an error occurred :- %s" % e)
        sleep(5)
