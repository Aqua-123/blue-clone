# pylint: disable=missing-function-docstring, global-statement, wildcard-import
import json
from pathlib import Path
import random
from threading import Thread
from time import gmtime, perf_counter, sleep, strftime
from timeit import default_timer as timer

from imgurpython.helpers.error import ImgurClientError, ImgurClientRateLimitError
import requests

from gc_logging import *
from utils import *
from var import *


def send_message(content):
    jsonmessage = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) + "\",\"id\":null,\"action\":\"speak\"}"}

    jsonmessage_alt = {"command": "message", "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}",
                       "data": "{\"message\":\""+fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if ALT_UNIVERSE_TOGGLE:
        ws.send(json.dumps(jsonmessage_alt))
    else:
        ws.send(json.dumps(jsonmessage))


def return_id(string):
    try:
        refresh_seen()
        if string.isnumeric():
            inputid = string
            if inputid in seen_data:
                return inputid
            return False
        string = string.replace("#", "")
        count = 0
        possibles = {}
        for inputid in seen_data:
            inputname = seen_data[inputid]["name"]
            username = seen_data[inputid]["username"]
            regex1 = re.compile(r'^%s' % fix_name(string), re.IGNORECASE)
            if regex1.search(inputname) or regex1.search(username):
                possibles[inputid] = inputname + " (#" + username + ")"
            else:
                count += 1
        for inputid in DATA["nickname"]:
            for nickname in DATA["nickname"][inputid]:
                regex2 = re.compile(string, re.IGNORECASE)
                count += 1
                if regex2.search(nickname):
                    possibles = {}
                    possibles[inputid] = nickname
                else:
                    pass
        total = len(seen_data)
        for inputid in DATA["nickname"]:
            total += len(DATA["nickname"][inputid])
        if count == total and len(possibles) == 0:
            return False
        return possibles
    except:
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
    global saved_messages
    with open('messages.json', 'r') as file:
        saved_messages = json.loads(file.read())


def update_messages_json():
    global saved_messages
    with open('messages.json', 'w') as file:
        json.dump(saved_messages, file)
    refreshmessages()


def refresh_seen():
    global seen_data
    with open('seen.json', 'r') as file:
        seen_data = json.load(file)


def update_seen_json():
    global seen_data
    with open('seen.json', 'w') as file:
        json.dump(seen_data, file)


def update_seen(inputname, inputid, inputusername):
    time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    inputid = str(inputid)
    if inputid not in seen_data:
        seen_data[inputid] = {}
    seen_data[inputid]["name"] = inputname
    seen_data[inputid]["username"] = inputusername
    seen_data[inputid]["channel_name"] = {"WFAF": time_stamp}
    update_seen_json()


def update_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'w') as file:
        json.dump(IMAGE_CACHE, file)


def refresh_image_cache():
    global IMAGE_CACHE
    with open('image_cache.json', 'r') as file:
        IMAGE_CACHE = json.loads(file.read())


def saved_message_handler(inputid, inputname):
    if inputid in saved_messages:
        if len(saved_messages[inputid]) == 1:
            output_message = "Hello %s I have a message for you: %s" % (
                inputname, saved_messages[inputid][0])
            sleep(0.9)
            send_message(output_message)
            del saved_messages[inputid]
        else:
            sleep(1)
            output_message = "Hello %s I have a few messages for you from some people" % inputname
            send_message(output_message)
            for messages in saved_messages[inputid]:
                send_message(messages)
                sleep(0.4)
            del saved_messages[inputid]
        update_messages_json()


def greet_text(count, inputname):
    if not SHORTEN_GREET_TOGGLE:
        match count:
            case 1: return Greet_1 % inputname
            case 2: return Greet_2 % inputname
            case 3: return Greet_general % inputname
    else:
        match count:
            case 1: return Greet_1_short % inputname
            case 2: return Greet_2_short % inputname
            case 3: return Greet_general_short % inputname


def send_greet(inputname, inputusername):
    if len(inputname) > 3:
        inputusername = ""
    else:
        inputusername = " (#%s)" % inputusername
    if inputname in GREET_TIMEOUT:
        match GREET_TIMEOUT[inputname]:
            case "1":
                send_message(greet_text(1, "%s%s" %
                             (inputname, inputusername)))
                GREET_TIMEOUT[inputname] = "2"
            case "2":
                send_message(greet_text(2, "%s%s" %
                             (inputname, inputusername)))
                GREET_TIMEOUT[inputname] = "3"
            case "3": pass
    else:
        send_message(greet_text(3, "%s%s" % (inputname, inputusername)))
        GREET_TIMEOUT[inputname] = "1"


def greet(action, result, greet, b):
    global DATA, saved_messages, MAIN_DICT, IDLE_DICT, TIMEOUT_CONTROL, stats_list
    if (action in b) and ("user" in b) and "display_name" in b["user"]:
        inputname = fix_name(b["user"]["display_name"])
        username = b["user"]["username"]
        inputid = b["user"]["id"]
        if result == "add":
            MAIN_DICT[inputid] = inputname
            stats_list[inputid] = inputname
            TIMEOUT_CONTROL[inputid] = perf_counter()
            saved_message_handler(str(inputid), inputname)
        elif result == "remove":
            list_removal(inputid)
        inputid = str(inputid)
        if greet_status and greet and inputid not in DATA["greet_exempt"]:
            if inputid in DATA["custom_greet"]:
                send_message(DATA["custom_greet"][inputid])
            elif inputid in DATA["knight"]:
                send_message("Greetings %s ~*" % inputname)
            else:
                send_greet(inputname, username)
        update_seen(inputname, inputid, username)


def dis_en_greets(inputid):
    global greet_status
    if inputid == "16008266" and greet_status:
        send_message(disabling_greet)
        greet_status = False
    elif inputid == "20909261" and not greet_status:
        send_message(re_enabling_greet)
        greet_status = True


def check_greeters(message, id):
    global greet_status, DATA
    found = False
    if id in DATA["greeter_fallback"]:
        for reg_m in greet_check:
            result = reg_m.match(message)
            if message in DATA["custom_greet"].values() or result or message == blue_greet:
                dis_en_greets(id)
                found = True
                break
        if not found:
            for reg_m in DATA["custom_greet"].values():
                reg = re.compile(r"" + reg_m + r"", re.I)
                result = reg.search(message)
                if result:
                    dis_en_greets(id)
                    break


def saving_messages(name, result):
    global saved_messages
    String = result.group(1).rstrip()
    if String.isnumeric():
        inputid = String
    else:
        inputid = return_id(String)
    if inputid:
        if type(inputid) is not dict:
            if inputid in saved_messages:
                saved_messages[inputid].append(name + ":- " + result.group(2))
            else:
                saved_messages[inputid] = [name + ":- " + result.group(2)]
            update_messages_json()
            return save_message_r % String
        match len(inputid):
            case 0: return not_seen % String
            case 1:
                inputid = list(inputid.keys())[0]
                if inputid in saved_messages:
                    saved_messages[inputid].append(
                        name + ":- " + result.group(2))
                else:
                    saved_messages[inputid] = [name + ":- " + result.group(2)]
                update_messages_json()
                return save_message_r % String
            case _: return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (result.group(2), fix_message(str(inputid)).replace("{", "").replace("}", "")))
    else:
        return not_seen % String


def downvote(cookie, inputid):
    requests.get(karma_url % inputid, cookies=cookie)


def ban_log(banned_id, admin_id):
    if admin_id != 0:
        r = requests.get(profile_url % int(admin_id), cookies=cookies)
        admin_name = json.loads(r.text)["user"]["display_name"]
    else:
        admin_name = "Console Admin"
    log = "Banned %s by %s \n" % (banned_id, admin_name)
    with open("log.txt", "a") as f:
        f.write(log)


def thread(id):
    banned.add(id)
    for c in cookiejar:
        cookie = {'_prototype_app_session': c}
        Thread(target=downvote, args=(cookie, id)).start()


def mute_func(result, index):
    global DATA
    inputid = result.group(1)
    match index:
        case 11:
            if inputid in DATA["mutelist"]:
                return already_ignoring
            DATA["mutelist"].append(inputid)
            update_data_json()
            response = start_ignoring % inputid
        case 12:
            if inputid in DATA["mutelist"]:
                DATA["mutelist"].remove(inputid)
                update_data_json()
                return stop_ignoring % inputid
                response = already_not_ignoring % inputid
        case _: response = "No match found"
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
    while stalking_log[id][1]:
        r = requests.get(profile_url % id, cookies=cookies)
        match r.status_code:
            case 200:
                r = json.loads(r.text)["user"]
                name = r["display_name"]
                karma = r["karma"]
                username = r["username"]
                gender = r["gender"]
                time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
                text = logging_text % (
                    str(time), name, karma, username, gender)
                with open(filename, "a") as f:
                    f.write(text)
            case 404:
                send_message(stopping_logging % id)
                break
            case _:
                if timer() - time_now >= 3600:
                    send_message("Ending stalk session of ID: " + id)
                    break
                else:
                    pass
        sleep(15)
        if not stalking_log[id][1]:
            del stalking_log[id]
            break


def respond_uptime():
    sr = str(datetime.now() - starttime).split(":")
    if sr[0] == "0":
        match int(sr[1])+0:
            case 0: return just_joined
            case 1: return here_for_one_min
            case _: return here_for_x_mins % str(int(sr[1])+0)
    return here_for_hours_and_mins % (str(sr[0]), str(int(sr[1]) + 0))


def send_stats():
    sr = str(datetime.now() - starttime).split(":")
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    return stats_response % (len(stats), len(stats_list), sr[0], sr[1], str(r))


def start_stalking(id):
    if id not in stalking_log:
        t = Thread(target=stalker, args=(id, timer()))
        stalking_log[id] = [t, True]
        t.start()
        return waking_stalking
    return already_stalking % id


def stop_stalking(id):
    global stalking_log
    if id in stalking_log:
        stalking_log[id][1] = False
        return stopping_stalking % id
    return already_not_stalking % id


def mod_demod(result):
    global DATA
    mod_id = result.group(2)
    if result.group(1) == "mod":
        if mod_id in DATA["mod"] or mod_id in DATA["admin"]:
            return already_mod % mod_id
        DATA["mod"].append(mod_id)
        update_data_json()
        return mod_response % mod_id
    if result.group(1) == "demod":
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


def set_greet(result):
    inputid = result.group(1)
    greet = result.group(3)
    if inputid not in DATA["custom_greet"]:
        DATA["custom_greet"][inputid] = greet
        update_data_json()
        return greet_set % (inputid, greet)
    DATA["custom_greet"][inputid] = greet
    update_data_json()
    return greet_updated % (inputid, greet)


def get_greet(result):
    inputid = result.group(1)
    if inputid in DATA["custom_greet"]:
        return greet_response % (inputid, DATA["custom_greet"][inputid])
    return greet_not_set % inputid


def remove_greet(result):
    inputid = result.group(1)
    if inputid in DATA["custom_greet"]:
        del DATA["custom_greet"][inputid]
        update_data_json()
        return greet_removed % inputid
    return greet_not_set % inputid


def get_landmine():
    landmine_list = DATA["landmine_words"]
    return fix_message(landmine_list)


def add_landmine(result):
    word = result.group(1)
    if word not in DATA["landmine_words"]:
        DATA["landmine_words"].append(word)
        update_data_json()
        return landmine_added % word
    return landmine_already_added % word


def remove_landmine(result):
    word = result.group(1)
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


def make_knight(result):
    inputname = result.group(1)
    if inputname.isnumeric():
        inputid = inputname
        if inputid not in DATA["knight"]:
            DATA["knight"].append(inputid)
            update_data_json()
            return knight_added % inputname
        return knight_already_added % inputname
    inputid = return_id(inputname)
    if not inputid:
        return not_seen % inputname
    if type(inputid) is not dict:
        if inputid not in DATA["knight"]:
            DATA["knight"].append(inputid)
            update_data_json()
            return knight_added % inputname
        return knight_already_added % inputname
    match len(inputid):
        case 0:
            return not_seen % inputname
        case 1:
            inputid = list(inputid.keys())[0]
            if inputid not in DATA["knight"]:
                DATA["knight"].append(inputid)
                update_data_json()
                return knight_added % inputname
            return knight_already_added % inputname
        case _:
            return fix_message("I have seen the following users with the name %s :- %s. Specify the inputid correspnding to their name" % (inputname, fix_message(str(inputid)).replace("{", "").replace("}", "")))


def remove_knight(result):
    inputname = result.group(1)
    if inputname.isnumeric():
        inputid = inputname
        if inputid in DATA["knight"]:
            DATA["knight"].remove(inputid)
            update_data_json()
            return knight_removed % inputname
        return knight_not_added % inputname
    inputid = return_id(inputname)
    if not inputid or (type(inputid) is dict and len(inputid) == 0):
        return not_seen % inputname
    if type(inputid) is not dict:
        if inputid in DATA["knight"]:
            DATA["knight"].remove(inputid)
            update_data_json()
            return knight_removed % inputname
        return knight_not_added % inputname
    if len(inputid) == 1:
        inputid = list(inputid.keys())[0]
        if inputid in DATA["knight"]:
            DATA["knight"].remove(inputid)
            update_data_json()
            return knight_removed % inputname
        return knight_not_added % inputname
    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (inputname, fix_message(str(inputid)).replace("{", "").replace("}", "")))


def toggle_shortened_greet():
    global SHORTEN_GREET_TOGGLE
    if SHORTEN_GREET_TOGGLE:
        SHORTEN_GREET_TOGGLE = False
        return shortened_greet_off
    SHORTEN_GREET_TOGGLE = True
    return shortened_greet_on


def save_nickname(inputresult):
    inputname = inputresult.group(1)
    nickname = inputresult.group(2)
    if inputname.isnumeric():
        inputid = inputname
        if inputid not in DATA["nickname"]:
            DATA["nickname"][inputid] = [nickname]
            update_data_json()
            return nickname_added % (nickname, inputname)
        DATA["nickname"][inputid].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, inputname)
    inputid = return_id(inputname)
    if not inputid or (type(inputid) is dict and len(inputid) == 0):
        return not_seen % inputname
    if type(inputid) is not dict:
        if inputid not in DATA["nickname"]:
            DATA["nickname"][inputid] = [nickname]
            update_data_json()
            return nickname_added % (nickname, inputname)
        DATA["nickname"][inputid].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, inputname)
    if len(inputid) == 1:
        inputid = list(inputid.keys())[0]
        if inputid not in DATA["nickname"]:
            DATA["nickname"][inputid] = [nickname]
            update_data_json()
            return nickname_added % (nickname, inputname)
        DATA["nickname"][inputid].append(nickname)
        update_data_json()
        return nickname_updated % (nickname, inputname)
    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (name, fix_message(str(id)).replace("{", "").replace("}", "")))


def toggle_greets(result):
    global greet_status
    action = result.group(1)
    if action == "enable":
        greet_status = True
        return done
    if action == "disable":
        if greet_status:
            greet_status = False
            return done
        return already_not_greeting
    return "Unexpected response"


def hide(id):
    global TIMEOUT_CONTROL, MAIN_DICT, IDLE_DICT
    id = int(id)
    del TIMEOUT_CONTROL[int(id)]
    if id in MAIN_DICT:
        del MAIN_DICT[id]
    if id in IDLE_DICT:
        del IDLE_DICT[id]
    return aye_aye


def banfunc(result):
    id_ban = result.group(1)
    thread(id_ban)
    Thread(target=ban_log, args=(id_ban, id,)).start()
    return banning_response % id_ban


def returnstalk():
    if stalking_log:
        return stalking_following % fix_message(str(stalking_log.keys()))
    return stalking_no_one


def admin_function_init(i, id, isadmin, result):
    global greet_status, running, name, starttime, aichatstate, GREET_TIMEOUT, DATA
    match i:
        case 0: response = toggle_greets(result)
        case 1: response, running = leaving, False
        case 2 if isadmin: response = clear_lists()
        case 3: response = respond_uptime()
        case 4: GREET_TIMEOUT, response = {}, done
        case 5: response = send_stats()
        case 6: response = "Mutelist is: %s" % fix_message(str(DATA["mutelist"]))
        case 7: response = str(TIMEOUT_CONTROL)
        case 8:
            response = restarting
            restart_program()
        case 9: response = hide(id)
        case 10 if id not in DATA["mutelist"]: response = ily_r
        case 11 | 12: response = mute_func(result, i)
        case 13: response = banfunc(result)
        case 14: response = "Current admins are: %s" % fix_message(str(DATA["admins"]))
        case 15: response = str(result.group(2))
        case 16: response = stop_stalking(str(result.group(2)))
        case 17: response = returnstalk()
        #pywrite: disable
        case 18: aichatstate. response = True, done  # type: ignore
        case 19: aichatstate, response = False, done
        case 20 if id == "0" or id == "14267520": response = mod_demod(result)
        case 21:
            refreshdata()
            response = done
        case 22:
            refreshmessages()
            response = done
        case 23 if isadmin: response = set_greet(result)
        case 24 if isadmin: response = get_greet(result)
        case 25 if isadmin: response = remove_greet(result)
        case 26 if isadmin: response = add_landmine(result)
        case 27 if isadmin: response = remove_landmine(result)
        case 28 if isadmin: response = get_landmine()
        case 29 if id == "0" or id == "14267520":
            toggle_alt_universe()
            response = done
        case 30 if isadmin: response = toggle_spam_check()
        case 31 if isadmin: response = get_spam_check_status()
        case 32 if isadmin: response = make_knight(result)
        case 33 if isadmin: response = remove_knight(result)
        case 34 if isadmin: response = toggle_shortened_greet()
        case 35 if isadmin: response = save_nickname(result)
        case _: response = False
    if response:
        if int(id) != 0:
            send_message(response)
        else:
            print("Admin Command: " + response)


def admin_func(message, id, isadmin):
    for i in range(len(admin_commands)):
        result = admin_commands[i].match(message)
        if result:
            admin_function_init(i, id, isadmin, result)
            break


def landmine_checker(message, id):
    for word in DATA["landmine_words"]:
        regex1 = re.compile(r"%s" % word, re.I)
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


def image_upload(query, urly):
    global client
    found = False
    if query in IMAGE_CACHE:
        return IMAGE_CACHE[query][1]
    for i in IMAGE_CACHE:
        if IMAGE_CACHE[i][0] == urly:
            found = True
            return IMAGE_CACHE[i][1]
    if not found:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://", "")
        formattedlink = "Image: " + link
        IMAGE_CACHE[query] = [urly, formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink


def get_image_link(query):
    url = response().urls(query, 6)
    try:
        return image_upload(query, url[-1])
    except ImgurClientError:
        send_message("Sorry I couldn't find %s" % query)
        pass
    except ImgurClientRateLimitError:
        send_message(
            "Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying")
        pass


def send_pic(query):
    send_message(get_image_link(query))


def get_meme():
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    r = json.loads(r.text)
    link = r["url"]
    image = client.upload_from_url(link)
    link = image["link"].replace("https://", "")
    formattedlink = "Image: " + link
    return formattedlink


def get_meme_link():
    try:
        send_message(get_meme())
    except ImgurClientError:
        send_message("Sorry I couldn't find a meme")
        pass
    except ImgurClientRateLimitError:
        send_message(
            "Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying")
        pass


def send_seen(id):
    refresh_seen()
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    name = seen_data[id]["name"]
    username = seen_data[id]["username"]
    lastseen_list = {}
    for key in seen_data[id]["channel_name"]:
        date = seen_data[id]["channel_name"][key]
        lastseen_list[date] = key
    date = max(lastseen_list)
    channel_name = lastseen_list[date]
    if "WFAF" in seen_data[id]["channel_name"]:
        date = seen_data[id]["channel_name"]["WFAF"].split(" ")[0]
        deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(
            seen_data[id]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
        match deltatime.days:
            case 0: date_string = "today"
            case 1: date_string = "yesterday"
            case _: date_string = "on " + date.split("-")[1] + "/" + date.split("-")[2]
        if deltatime.seconds//3600 == 0:
            if deltatime.seconds//60 % 60 == 0:
                response_wfaf = "%s (#%s) was last seen %s a couple moments ago in WFAF" % (
                    name, username, date_string)
            else:
                response_wfaf = "%s (#%s) was last seen %s %s mins ago in WFAF" % (
                    name, username, date_string, deltatime.seconds//60 % 60)
        else:
            response_wfaf = "%s (#%s) was last seen %s %s hours and %s mins ago in WFAF" % (
                name, username, date_string, deltatime.seconds//3600, deltatime.seconds//60 % 60)
        if channel_name == "WFAF":
            response = response_wfaf
        else:
            date_channel = seen_data[id]["channel_name"][channel_name].split(" ")[
                0]
            deltatime_channel = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(
                seen_data[id]["channel_name"][channel_name], "%Y-%m-%d %H:%M:%S")
            match deltatime_channel.days:
                case 0: date_string_channel = "today"
                case 1: date_string_channel = "yesterday"
                case _: date_string_channel = "on " + date_channel.split("-")[1] + "/" + date_channel.split("-")[2]
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
            response = response_wfaf + response_channel
    else:
        deltatime = datetime.strptime(
            r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_channel = seen_data[id]["channel_name"][channel_name].split(" ")[
            0]
        secs = deltatime.seconds//60 % 60
        match deltatime.days:
            case 0: date_string = "today"
            case 1: date_string = "yesterday"
            case _: date_string = "on " + date_channel.split("-")[1] + "/" + date_channel.split("-")[2]
        if deltatime.seconds//3600 == 0:
            response = "I dont remember seeing %s (#%s) in WFAF but they were last seen %s %s mins ago in %s" % (
                name, username, date_string, secs, channel_name)
        else:
            response = "I dont remember seeing %s (#%s) in WFAF but they were last seen %s %s hours and %s mins ago in %s" % (
                name, username, date_string, deltatime.seconds//3600, secs, channel_name)
    return fix_message(response)


def log_chats(message, user_id, user):
    date = datetime.today().strftime('%d-%m-%Y')
    filename = "wfaf-logs/log (%s).txt" % date
    myfile = Path(filename)
    if myfile.is_file():
        name = fix_name(user["display_name"])
        log = fix_message(message_log_text % (name, user_id, message)) + "\n"
        with open(filename, "a") as f:
            f.write(log)
    else:
        with open(filename, "w") as f:
            f.write("")
        log_chats(message, user_id, user)


def list_removal(id):
    global MAIN_DICT, TIMEOUT_CONTROL, IDLE_DICT
    if id in TIMEOUT_CONTROL:
        del TIMEOUT_CONTROL[id]
    if id in MAIN_DICT:
        del MAIN_DICT[id]
    if id in IDLE_DICT:
        del IDLE_DICT[id]


def whos_here_appending(id):
    global whos_here_r
    try:
        r = requests.get(profile_url % id, cookies=cookies, timeout=1)
        r = json.loads(r.text)
        if len(r["user"]["display_name"]) > 3:
            whos_here_r.append(r["user"]["display_name"])
        else:
            whos_here_r.append("%s (#%s)" % (
                r["user"]["display_name"], r["user"]["username"]))
    except:
        id = str(id)
        name = seen_data[id]["name"]
        if len(name) > 3:
            whos_here_r.append(name)
        else:
            whos_here_r.append("%s (#%s)" % (name, seen_data[id]["username"]))


def reply_whos_here():
    global whos_here_r
    for i in MAIN_DICT:
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads.clear()
    idle_len = len(IDLE_DICT)
    whos_here_r = ",".join(whos_here_r)
    match idle_len:
        case 0: response = whos_here_response_no_lurkers % whos_here_r
        case 1: response = whos_here_response_gen1 % whos_here_r
        case _: response = whos_here_response_gen2 % (whos_here_r, idle_len)
    return fix_message(response)


def reply_whos_idle():
    global whos_here_r
    for i in IDLE_DICT.keys():
        threads.append(Thread(target=whos_here_appending, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads.clear()
    whos_idle_r = ",".join(whos_here_r)
    if len(IDLE_DICT) == 0:
        response = whos_lurking_none
    else:
        response = whos_lurking_gen % whos_idle_r
    return fix_message(response)


def get_seen(result):
    try:
        refresh_seen()
        string = result.group(1)
        if string.isnumeric():
            id = string
            if id in seen_data:
                return send_seen(id)
            return fix_message("I dont remember seeing user with ID %s" % str(id))
        string = string.replace("#", "")
        n = 0
        possibles = {}
        for id in seen_data:
            name = seen_data[id]["name"]
            username = seen_data[id]["username"]
            regex1 = re.compile(r'^%s' % fix_name(string), re.IGNORECASE)
            if regex1.search(name) or regex1.search(username):
                possibles[id] = name
            else:
                n += 1
        for id in DATA["nickname"]:
            for nickname in DATA["nickname"][id]:
                regex2 = re.compile(string, re.IGNORECASE)
                n += 1
                if regex2.search(nickname):
                    possibles = {}
                    possibles[id] = nickname
                else:
                    pass
        total = len(seen_data)
        for id in DATA["nickname"]:
            total += len(DATA["nickname"][id])
        if len(possibles) == 1:
            if list(possibles.keys())[0] in seen_data:
                return send_seen(list(possibles.keys())[0])
            return fix_message("I dont remember seeing user with name %s" % string)
        if n == total:
            return fix_message("I dont remember seeing user with name %s" % string)
        return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name and ask 'Blue seen ID'" % (string, fix_message(str(possibles)).replace("{", "").replace("}", "")))
    except Exception as e:
        print("Error in get_seen %s" % e)
        get_seen(result)


def image_upload(query, urly):
    global client
    found = False
    if query in IMAGE_CACHE:
        return IMAGE_CACHE[query][1]
    for i in IMAGE_CACHE:
        if IMAGE_CACHE[i][0] == urly:
            found = True
            return IMAGE_CACHE[i][1]
    if not found:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://", "")
        formattedlink = "Image: " + link
        IMAGE_CACHE[query] = [urly, formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink


def coin_handling(result):
    global DATA
    num = result.group(1)
    coin_add = int(num)
    if coin_add <= 100 and coin_add >= 1:
        DATA["coins"] = coin_add + DATA["coins"]
        update_data_json()
        if num == "1":
            return adding_one_coin % (coin_add + 0, DATA["coins"])
        return adding_coins % (coin_add + 0, DATA["coins"])
    if coin_add > 100:
        return too_many_coins


def get_id(result):
    String = result.group(4)
    id = return_id(String)
    if id is False:
        return not_seen % String
    else:
        if type(id) is not dict:
            return id_response % (String, id)
        match len(id):
            case 0: return not_seen % String
            case 1: return id_response % (String, list(id.keys())[0])
            case _: return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name" % (String, fix_message(str(id)).replace("{", "").replace("}", "")))


def get_jokes():
    r = requests.get(jokes_url)
    if r.status_code == 200:
        joke = json.loads(r.text)["attachments"][0]["text"]
        return joke
    return "Error: " + str(r.status_code)


def get_quote(console):
    r = requests.get('https://api.quotable.io/random')
    content = str(r.json()['content'])
    author = "~ by " + str(r.json()['author'])
    if not console:
        send_message(content)
        sleep(0.2)
        send_message(author)
    else:
        print("Console:- %s" % content)
        sleep(0.2)
        print("Console:- %s" % author)


def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")


def check_singing():
    l = len(TIMEOUT_CONTROL)
    if l <= 4 and random.randint(0, 100000) % 93870 == 0:
        Thread(target=singing).start()


def get_details(result):
    id = int(result.group(2))
    r = requests.get(profile_url % id, cookies=cookies)
    match r.status_code:
        case 200:
            r = json.loads(r.text)["user"]
            name = r["display_name"]
            karma = r["karma"]
            username = r["username"]
            gender = r["gender"]
            created = r["created_at"].split("T")
            if gender:
                response = details_response_null_gender % (
                    id, name, username, karma, created[0], created[1])
            else:
                response = details_response % (
                    id, name, username, karma, gender, created[0], created[1])
        case 404:
            response = account_deleted
        case 403:
            response = timeout_error
        case _:
            response = "Unknown condition reached"
    return response


def send_feelings(index, id, result, console):
    global DATA
    name = result.group(1)
    response = ""
    match index:
        case 1: response = sending_love % name
        case 2: response = sending_pats % name
        case 3: response = sending_hugs % result.group(4)
        case 4: response = sending_bonks % name
        case 5 if id in DATA["admin"] or console: response = get_id(result)
        case 6 if id in DATA["admin"] or console: response = get_details(result)
        case 7: response = get_seen(result)
        case 8: Thread(target=send_pic, args=(name,)).start()
        case 9: Thread(target=get_meme_link).start()
    return response


def coins_feelings(message, id, console):
    for reg_m in coinsandfeelings:
        result = reg_m.match(message)
        if result:
            index = coinsandfeelings.index(reg_m)
            if index == 0:
                response = coin_handling(result)
            else:
                response = send_feelings(index, id, result, True)
            if response and response != "":
                if console:
                    print("Console:-%s" % response)
                else:
                    send_message(response)
            break


def console_input():
    while True:
        try:
            text = input()
            name = "Console Admin"
            result = consoleinput.match(text)
            if result:
                content = result.group(1)
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
                matching(fix_name(name), response_dict, text, True, False)
                matching(fix_name(name), whos_here_res, text, True, True)
                coins_feelings(text, id, True)
        except Exception as e:
            print(e)


def matching(name, dictname, message, console, dict):
    keys = list(dictname.keys())

    def consolecheck(content):
        if console:
            print("Console:- %s" % content)
        else:
            send_message(content)
    for i in range(len(keys)):
        re_m = keys[i]
        result = re_m.match(message)
        if result:
            if dict:
                if re_m == whos_here:
                    response = reply_whos_here()
                elif re_m == whos_idle:
                    response = reply_whos_idle()
                else:
                    response = list(dictname.values())[i]
                consolecheck(response)
            elif not dict:
                if re_m == jok:
                    consolecheck(get_jokes())
                elif re_m == quote:
                    get_quote(console)
                elif re_m == save_message:
                    response = saving_messages(name, result)
                    consolecheck(response)
                else:
                    consolecheck(dictname[re_m])
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
        while running is True:
            update_seen_json()
            RESET_CLOCK = RESET_CLOCK + 1
            result = ws.recv()
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
                greet("user_connected", "add", True, b)
                greet("typing", "add", False, b)
                greet("user_disconnected", "remove", False, b)
                greet("messages", "add", False, b)
                if "messages" in b and "user" in b:
                    user = b["user"]
                    id = str(user["id"])
                    # spam_controlling(id)
                    # spam_checker()
                    name = fix_name(user["display_name"])
                    message = fix_message(str(b["messages"])).strip("'")
                    print(b["user"]["display_name"] +
                          " (%s) :- " % id + message)
                    #Thread(target=landmine_checker, args=(message,id)).start()
                    Thread(target=check_greeters, args=(message, id,)).start()
                    Thread(target=log_chats, args=(message, id, user,)).start()
                    if id not in DATA["mutelist"]:
                        coins_feelings(message, id, False)
                        matching(fix_name(name), response_dict,
                                 message, False, False)
                        matching(fix_name(name), whos_here_res,
                                 message, False, True)
                    if id in DATA["admin"]:
                        admin_func(message, id, True)
                    elif id in DATA["mod"]:
                        admin_func(message, id, False)
    except Exception as e:
        print("Hello young boi an error occurred :- %s" % e)
        sleep(5)
        pass
