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
    message = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) +"\",\"id\":null,\"action\":\"speak\"}"}
    message_alt = {"command":"message","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}","data":"{\"message\":\""+fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if alt_unverse_toggle is True:
        ws.send(json.dumps(message_alt))
    else:
        ws.send(json.dumps(message))

def return_id(string):
    try:
        refresh_seen()
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
                regex1 = re.compile(r'^%s' % fix_name(string), re.IGNORECASE)    
                if regex1.search(name) or regex1.search(username):
                    possibles[id] = name + " (#" + username + ")"
                else: n += 1
            for id in data["nickname"]:
                for nickname in data["nickname"][id]:
                    regex2 = re.compile(string, re.IGNORECASE)
                    n+=1
                    if regex2.search(nickname):
                        possibles = {}
                        possibles[id] = nickname
                    else:
                        pass
            total = len(seen_data) 
            for id in data["nickname"]:
                total+=len(data["nickname"][id])
            if n == total and len(possibles) == 0:
                return False
            else:
                return possibles
    except:
        return_id(string)

def remove_blue():
    global list_main_dict, idle_main_dict, timeout_control
    if 21550262 in list_main_dict:
        del list_main_dict[21550262]
    if 21550262 in idle_main_dict:
        del idle_main_dict[21550262]
    if 21550262 in timeout_control:
        del timeout_control[21550262]


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
    if not shorten_greet_toggle :
        match count:
            case 1: return Greet_1 % name
            case 2: return Greet_2 % name
            case 3: return Greet_general % name
    else:
        match count:
            case 1: return Greet_1_short % name
            case 2: return Greet_2_short % name
            case 3: return Greet_general_short % name

def send_greet(name, username):
    if len(name) > 3: username = ""
    else: username = " (#%s)" % username
    if name in greet_timeout:
        match greet_timeout[name]:
            case "1":
                send_message(greet_text(1, "%s%s"% (name, username)))
                greet_timeout[name] = "2"
            case "2":
                send_message(greet_text(2, "%s%s"% (name, username)))
                greet_timeout[name] = "3"
            case "3": pass
    else:
        send_message(greet_text(3, "%s%s"% (name, username)))
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
        if greet_status and greet and id not in data["greet_exempt"]:
            if id in data["custom_greet"]:
                send_message(data["custom_greet"][id])
            elif id in data["knight"]:
                send_message("Greetings %s ~*" % name)
            else:
                send_greet(name, username)
        update_seen(name,id,username)

def dis_en_greets(id):
    global greet_status
    if id == "16008266" and greet_status:
        send_message(disabling_greet)
        greet_status = False
    elif id == "20909261" and not greet_status:
        send_message(re_enabling_greet)
        greet_status = True

def check_greeters(message, id):
    global greet_status,data
    found = False
    if id in data["greeter_fallback"]:
        for reg_m in greet_check:
            result = reg_m.match(message)
            if message in data["custom_greet"].values() or result or message == blue_greet:
                dis_en_greets(id)
                found = True
                break
        if not found :
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
    if id :
        if type(id) is not dict:
            if id in saved_messages:
                saved_messages[id].append(name + ":- " + result.group(2))
            else:
                saved_messages[id] = [name + ":- " + result.group(2)]
            update_messages_json()
            return save_message_r%String
        else:
            match len(id):
                case 0: return not_seen % String
                case 1:
                    id = list(id.keys())[0]
                    if id in saved_messages:
                        saved_messages[id].append(name + ":- " + result.group(2))
                    else:
                        saved_messages[id] = [name + ":- " + result.group(2)]
                    update_messages_json()
                    return save_message_r % String
                case _: return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (result.group(2), fix_message(str(id)).replace("{", "").replace("}", "")))
    else:
        return not_seen % String

def downvote(cookie, id):
    requests.get(karma_url % id, cookies=cookie)

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
    global data
    id = result.group(1)
    match index:
        case 11:
            if id in data["mutelist"]:
                response = already_ignoring
            else:
                data["mutelist"].append(id)
                update_data_json()
                response = start_ignoring % id
        case 12:
            if id in data["mutelist"]:
                data["mutelist"].remove(id)
                update_data_json()
                response = stop_ignoring % id
            else:
                response = already_not_ignoring % id
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
                text = logging_text % (str(time), name, karma, username, gender)
                with open(filename, "a") as f:
                    f.write(text)
            case 404 :
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
        return already_stalking % id

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
    if alt_unverse_toggle: alt_unverse_toggle = False
    else: alt_unverse_toggle = True    

def toggle_spam_check():
    global spam_check_toggle
    if spam_check_toggle:
        spam_check_toggle = False
        return spam_check_off
    else:
        spam_check_toggle = True
        return spam_check_on

def get_spam_check_status():
    if spam_check_toggle : return spam_check_on
    else: return spam_check_off

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
        if not id :
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
                match len(id):
                    case 0:
                        return not_seen % name
                    case 1:
                        id = list(id.keys())[0]
                        if id not in data["knight"]:
                            data["knight"].append(id)
                            update_data_json()
                            return knight_added % name
                        else:
                            return knight_already_added % name
                    case _:
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
        if not id or (type(id) is dict and len(id) == 0):
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
                    else:
                        return knight_not_added % name
                else:
                    return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (name, fix_message(str(id)).replace("{", "").replace("}", "")))


def toggle_shortened_greet():
    global shorten_greet_toggle
    if shorten_greet_toggle:
        shorten_greet_toggle = False
        return shortened_greet_off
    else:
        shorten_greet_toggle = True
        return shortened_greet_on

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
        if not id or (type(id) is dict and len(id) == 0):
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

def toggle_greets(result):
    global greet_status
    action = result.group(1)
    if action == "enable":
        greet_status = True 
        response = done
    elif action == "disable":
        if greet_status :
            greet_status = False
            response = done
        else:
            response = already_not_greeting
    else: response = "Unexpected response"
    return response

def hide(id):
    global timeout_control, list_main_dict, idle_main_dict
    id = int(id)
    del timeout_control[int(id)]
    if id in list_main_dict :
        del list_main_dict[id]
    if id in idle_main_dict:
        del idle_main_dict[id]
    return aye_aye

def banfunc(result):
    id_ban = result.group(1)
    thread(id_ban)
    Thread(target = ban_log, args = (id_ban,id,)).start()
    return banning_response % id_ban

def returnstalk():
    if stalking_log:
        response = stalking_following % fix_message(str(stalking_log.keys()))
    else:
        response = stalking_no_one
    return response

def admin_function_init(i, id , isadmin, result):
    global greet_status, running, name, starttime, aichatstate, greet_timeout, data
    match i:
        case 0:response = toggle_greets(result)
        case 1:response, running = leaving, False
        case 2 if isadmin:response = clear_lists()
        case 3: response = respond_uptime()
        case 4: greet_timeout, response = {}, done
        case 5: response = send_stats()
        case 6: response = "Mutelist is: %s" % fix_message(str(data["mutelist"]))
        case 7: response = str(timeout_control)
        case 8:
            response = restarting
            restart_program()
        case 9: response = hide(id)
        case 10 if id not in data["mutelist"]: response = ily_r
        case 11 | 12: response = mute_func(result,i)
        case 13: response = banfunc(result)
        case 14: response = "Current admins are: %s" % fix_message(str(data["admins"]))
        case 15: response = str(result.group(2))
        case 16: response = stop_stalking(str(result.group(2)))
        case 17: response = returnstalk()
        #pywrite: disable
        case 18: aichatstate. response = True, done #type: ignore
        case 19: aichatstate, response = False, done
        case 20 if id == "0" or id == "14267520": response = mod_demod(result)
        case 21: 
            refresh_data()
            response = done
        case 22:
            refresh_messages()
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
        if int(id) != 0 :
            send_message(response)
        else: 
            print("Admin Command: " + response)

def admin_func(message, id , isadmin):
    for i in range(len(admin_commands)):
        result = admin_commands[i].match(message)
        if result:
            admin_function_init(i, id, isadmin, result) 
            break

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
            return image_cache[i][1]
            
    if not found:
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
    lastseen_list = {}
    for key in seen_data[id]["channel_name"]:
        date = seen_data[id]["channel_name"][key]
        lastseen_list[date] = key
    date = max(lastseen_list)
    channel_name = lastseen_list[date]
    if "WFAF" in seen_data[id]["channel_name"]:
        date = seen_data[id]["channel_name"]["WFAF"].split(" ")[0]
        deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
        match deltatime.days:
            case 0: date_string = "today"
            case 1: date_string = "yesterday"
            case _: date_string = "on " + date.split("-")[1] + "/" + date.split("-")[2]
        if deltatime.seconds//3600 == 0:
            if deltatime.seconds//60%60 == 0:
                response_wfaf = "%s (#%s) was last seen %s a couple moments ago in WFAF" % (name, username, date_string)
            else:
                response_wfaf = "%s (#%s) was last seen %s %s mins ago in WFAF" % (name, username, date_string, deltatime.seconds//60%60)
        else:
            response_wfaf = "%s (#%s) was last seen %s %s hours and %s mins ago in WFAF" % (name, username, date_string, deltatime.seconds//3600, deltatime.seconds//60%60)
        if channel_name == "WFAF":
            response = response_wfaf
        else:
            date_channel = seen_data[id]["channel_name"][channel_name].split(" ")[0]
            deltatime_channel = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"][channel_name], "%Y-%m-%d %H:%M:%S")
            match deltatime_channel.days:
                case 0: date_string_channel = "today"
                case 1: dato_string_channel = "yesterday"
                case _: date_string_channel = "on " + date_channel.split("-")[1] + "/" + date_channel.split("-")[2]
            if deltatime_channel.seconds//3600 == 0:
                if deltatime_channel.seconds//60%60 == 0:
                    response_channel = " but was more recently seen %s just now in %s" % (date_string_channel, channel_name)
                else:
                    response_channel = " but was more recently seen %s %s mins ago in %s" % (date_string_channel, deltatime_channel.seconds//60%60, channel_name)
            else:
                response_channel = " but was more recently seen %s %s hours and %s mins ago in %s" % (date_string_channel, deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            response = response_wfaf + response_channel
    else:
        deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_channel = seen_data[id]["channel_name"][channel_name].split(" ")[0]
        secs = deltatime.seconds//60%60
        match deltatime.days:
            case 0: date_string = "today"
            case 1: date_string = "yesterday"
            case _: date_string = "on " + date_channel.split("-")[1] + "/" + date_channel.split("-")[2]
        if deltatime.seconds//3600 == 0:
            response = "I dont remember seeing %s (#%s) in WFAF but they were last seen %s %s mins ago in %s" % (name, username, date_string, secs, channel_name)
        else:
            response = "I dont remember seeing %s (#%s) in WFAF but they were last seen %s %s hours and %s mins ago in %s" % (name, username, date_string, deltatime.seconds//3600, secs, channel_name)
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
    global list_main_dict, timeout_control, idle_main_dict
    if id in timeout_control:
        del timeout_control[id]
    if id in list_main_dict:
        del list_main_dict[id]
    if id in idle_main_dict:
        del idle_main_dict[id]

def whos_here_appending(id):
    global whos_here_r
    try:
        r = requests.get(profile_url % id, cookies=cookies, timeout=1)
        r = json.loads(r.text)
        if len(r["user"]["display_name"]) > 3:
            whos_here_r.append(r["user"]["display_name"])
        else:
            whos_here_r.append("%s (#%s)" % (r["user"]["display_name"],r["user"]["username"]))
    except:
        id = str(id)
        name = seen_data[id][name]
        if len(name) > 3:
            whos_here_r.append(name)
        else:
            whos_here_r.append("%s (#%s)" % (name, seen_data[id]["username"]))

def reply_whos_here():
    global whos_here_r
    for i in list_main_dict: threads.append(Thread(target=whos_here_appending, args=(i,)))
    for t in threads: t.start()
    for t in threads: t.join()
    threads.clear()
    idle_len = len(idle_main_dict)
    whos_here_r = fix_message(str(whos_here_r))
    match idle_len:
        case 0: response = whos_here_response_no_lurkers % whos_here_r
        case 1: response = whos_here_response_gen1 % whos_here_r
        case _: response = whos_here_response_gen2 % (whos_here_r, idle_len)
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
            else:
                return fix_message("I dont remember seeing user with ID %s" % str(id))
        else:
            string = string.replace("#", "")
            n = 0
            possibles = {}
            for id in seen_data:
                name = seen_data[id]["name"]
                username = seen_data[id]["username"]
                regex1 = re.compile(r'^%s' % fix_name(string), re.IGNORECASE)
                if regex1.search(name) or regex1.search(username):
                    possibles[id] = name
                else: n += 1
            for id in data["nickname"]:
                for nickname in data["nickname"][id]:
                    regex2 = re.compile(string, re.IGNORECASE)
                    n+=1
                    if regex2.search(nickname):
                        possibles = {}
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
    except Exception as e:
        print("Error in get_seen %s" % e)
        get_seen(result)   

def image_upload(query,urly):
    global client
    found = False
    if query in image_cache:
        return image_cache[query][1]
    for i in image_cache:
        if image_cache[i][0] == urly:
            found = True
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
            match len(id):
                case 0: return not_seen % String
                case 1: return id_response % (String,list(id.keys())[0])
                case _: return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (String, fix_message(str(id)).replace("{", "").replace("}", "")))

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
    if not console :
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
    match r.status_code:
        case 200:
            r = json.loads(r.text)["user"]
            name = r["display_name"]
            karma = r["karma"]
            username = r["username"]
            gender = r["gender"]
            created = r["created_at"].split("T")
            if gender:
                response = details_response_null_gender % (id,name,username,karma,created[0],created[1])
            else:
                response = details_response % (id, name, username, karma, gender, created[0], created[1])
        case 404 :
            response = account_deleted
        case 403:
            response = timeout_error
        case _:
            response = "Unknown condition reached"
    return response

def send_feelings(index, id, result,console):
    global data
    name = result.group(1)
    response = ""
    match index:
        case 1: response = sending_love % name
        case 2: response = sending_pats % name
        case 3: response = sending_hugs % result.group(4)
        case 4: response = sending_bonks % name
        case 5 if id in data["admin"] or console: response = get_id(result)
        case 6 if id in data["admin"] or console: response = get_details(result)  
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
                response = send_feelings(index, id, result,True)
            if response and response != "":
                if console:
                    print("Console:-%s"%response)
                else:
                    send_message(response)
            break

def console_input():
    while True:
        try:
            text = input()
            name = "Console Admin"
            result = consoleinput.match(text)
            if result :
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
                matching(fix_name(name),response_dict, text, True, False)
                matching(fix_name(name),whos_here_res, text, True, True)
                coins_feelings(text, id, True)
        except Exception as e:
            print(e)

def matching(name,dictname, message, console, dict):
    keys = list(dictname.keys())
    def consolecheck(content):
        if console : print("Console:- %s" % content)
        else: send_message(content)
    for i in range(len(keys)):
        re_m = keys[i]
        result = re_m.match(message)
        if result:
            if dict :
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
        ws.connect(ws_url, cookie=main_cookie, subprotocols=subprots, origin=origin)
        ws.send(json.dumps(connect_json))
        ws.send(json.dumps(connect_json_blue))
        while running is True:
            update_seen_json()
            reset_clock = reset_clock + 1 
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
                    #spam_controlling(id)
                    #spam_checker()
                    name = fix_name(user["display_name"])
                    message = fix_message(str(b["messages"])).strip("'")
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
