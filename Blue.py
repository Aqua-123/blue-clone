from websocket import create_connection
from concurrent.futures import TimeoutError as ConnectionTimeoutError
import websocket
import random
import json
import requests
import re
from datetime import date,datetime
from os import execl
from sys import executable,argv
from time import gmtime, strftime,sleep,perf_counter
from github import Github
from vars import *
import threading

#Restarts the current program.
restart_program = lambda : execl(executable,executable, * argv)
name = " "

def reconnect():
    while connection == True:
        websocket.enableTrace(False)
        ws = websocket.WebSocket()
        ws.connect("wss://www.emeraldchat.com/cable",
                cookie=main_cookie,
                subprotocols=["actioncable-v1-json", "actioncable-unsupported"],
                origin="https://www.emeraldchat.com")
        if ws.connected == True:
            ws.send(json.dumps(connect_json))
            connection = False
        if ws.connected == False : sleep(1)
            
def fix_name(name):
    for c in forbiden_chars : return(name.replace(c,""))

def send_message(content):
    """Function for sending messages
    with the argument of content of text"""
    
    if response_kill == False:
        message = {
            "command": "message", 
            "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
            "data": "{\"message\":\"" + content + "\",\"id\":null,\"action\":\"speak\"}"}
        ws.send(json.dumps(message))
       
def greet_text(count,name):
    """Control which message is to be
    send with context to the greet control"""
 
    Greet_1 = ("Hi, " + name + \
    ", retrying won't help, "
    "you can try asking "
    "'what is wfaf' for more info :D")
    
    Greet_2 = "Hi again, " + name + ", try asking 'what is wfaf' for more info :D "
    
    Greet_general = ("Hi, " + name + \
        ", Welcome to WFAF, "
        "which stands for Waiting For A Friend, "
        "Let's keep it family-friendly,"
        " Enjoy your stay :D ")
    if count == 1 : return Greet_1
    elif count == 2 : return Greet_2
    elif count == 3 : return Greet_general

def send_greet(name):
    """Checks which greet is to be sent 
    with reference to the saved greet_timeout
    stamps in the dictionary"""
     
    if name in greet_timeout.keys():
        if (greet_timeout[name] == "1"):
            send_message(greet_text(1, name))
            greet_timeout[name] = "2"
        elif greet_timeout[name] == "2":
            send_message(greet_text(2, name))
            greet_timeout[name] = "3"
        elif greet_timeout[name] == "3" : pass
    else:
        send_message(greet_text(3, name))
        greet_timeout[name] = "1"

def greet(action, result, greet):
    """Function to do greetings and handling of 
    main, idle and stats lists"""
    
    if (action in b.keys()) and ("user" in b.keys()):
        user = b["user"]
        if "display_name" in user.keys():
            name = fix_name(user["display_name"])
            id = user["id"]
            if result == "add":
                list_main.add(name)
                list_main_dict[id] = name
                stats_list[id] = name
                timeout_control[id] = perf_counter()
            elif (result == "remove"):
                if id in timeout_control.keys() : del timeout_control[id]
                if id in list_main_dict.keys(): del list_main_dict[id]
                if id in idle_main_dict.keys() : del idle_main_dict[id]
                if name in idle_main : idle_main.remove(name)
                elif name in list_main : list_main.remove(name)
            if (greet == True) and ("id" in user) and (action == "user_connected"):
                stats.append(name)
                timeout_control[id] = perf_counter()
                if (greet_status == True):
                    ids = user["id"]
                    if str(ids) in custom_greet_id.keys() : send_message(custom_greet_id[str(ids)])
                    else : send_greet(name)
                        
def get_joke():
    """Fetches jokes from API mentioned
    and returns it as value of var joke"""
    r = requests.get("https://icanhazdadjoke.com/slack")
    joke = json.loads(r.text)["attachments"][0]["text"]
    return(joke)
    
def get_quote():
    """Fetches quotes from the API mentioned 
    and returns it as value of var response3"""
    r = requests.get('https://api.quotable.io/random')
    response3 = r.json()['content'] + " -" + str(r.json()['author'])
    return response3

def threaded_adding(ids):
    global whos_here_r,whos_here_res
    r = requests.get("https://emeraldchat.com/profile_json?id=" + str(ids),cookies = cookies)
    r = json.loads(r.text)
    whos_here_r.append(r["user"]["display_name"])
    
def matching(dictname,message):
    global whos_here_r,whos_here_res
    keys = list(dictname.keys())
    for i in range(0, len(keys)):
        result = keys[i].match(message)
        if bool(result) == True:
            if dictname == whos_here_res and re_m == whos_here:
                whos_here_r = []
                for i in list_main_dict.keys():threads.append(threading.Thread(target=threaded_adding, args=(i,)))
                for t in threads:t.start()
                for t in threads:t.join()
                threads.clear()
                if len(idle_main_dict.keys()) == 0 : whos_here_res = "I can see " + str(whos_here_r)+" and no lurkers :p"
                elif len(idle_main_dict.keys()) > 0:
                    if len(idle_main_dict.keys()) == 1: whos_here_res = "I can see " + str(whos_here_r)+" and " + str(len(idle_main_dict.keys()))+" person lurking :p"
                    elif len(idle_main_dict.keys()) > 1: whos_here_res = "I can see " + str(whos_here_r)+" and " + str(len(idle_main_dict.keys()))+" peeps lurking :p"
                send_message(fix_message(str(whos_here_res)))
            elif dictname == whos_here_res and re_m == whos_idle:
                whos_here_res = []
                for i in idle_main_dict.keys():threads.append(threading.Thread(target=threaded_adding, args=(i,)))
                for t in threads:t.start()
                for t in threads:t.join()
                threads.clear()
                if len(idle_main_dict.keys()) == 0 : whos_idle_r = "I can see no lurkers as of now"
                elif len(idle_main_dict.keys()) > 0:whos_idle_r = "I can see " + str(whos_here_r)+" lurking"
                send_message(fix_message(str(whos_idle_r)))
            else: send_message(list(dictname.values())[i])
            break
               


def fix_message(messages):
    """Fixes syntactical problems with incomming 
    messages and removes any unwanted chars"""
    message = str(messages)
    chars = ('"[]‘')
    for c in chars : message = message.replace(c, "")
    return (message.replace("'", ''))

def idle_function():
    """Function for moving people 
    between idle and main list with reference
    to time stamps in timeout_control"""
    idle_check_list = list(timeout_control.values())
    for i in range(0, len(idle_check_list)):
        x = idle_check_list[i]
        if (t_start - x) >= 240:
            val = list(timeout_control.keys())[i]
            if val in list_main_dict :
                idle_main_dict[val] = list_main_dict[val]
                del list_main_dict[val]
        elif (t_start - x) < 240:
            val = list(timeout_control.keys())[i]
            if val in idle_main_dict : del idle_main_dict[val]
        i = i+1

def remove_blue():
    """Removes blue from all lists 
    to avoid confusion with people"""
    
    if "Blue" in list_main_dict : del list_main_dict["Blue"]
    if "Blue" in idle_main_dict : del idle_main_dict["Blue"]
    if "Blue" in list(timeout_control.keys()) : del timeout_control["21550262"] 

def mute_func(message,index):
    array = message.split()
    global mute_list
    del array[0:2]
    id = array[0]
    if index == 12:
        if id in mute_list: responses = "I'm already ignoring user  '" + id + " 'o.o"
        else:
            mute_list.append(id)
            new_mute = str(mute_list)
            chars = "[]'\n"
            for c in chars : new_mute = new_mute.replace(c, "")
            muted_contents = repo.get_contents("muted.txt")
            repo.update_file(muted_contents.path, "mute update", str(new_mute), muted_contents.sha, branch="main")
            responses = "Okai I'll ignore user '" + id + "' 0.0"
    elif index == 13:
        if id in mute_list:
            mute_list.remove(id)    
            new_mute = str(mute_list)
            chars = "[]'\n "
            for c in chars : new_mute = new_mute.replace(c, "")
            muted_contents = repo.get_contents("muted.txt")
            repo.update_file(muted_contents.path, "mute update", str(new_mute), muted_contents.sha, branch="main")
            responses = "Okai I'll stop ignoring user '" + id + "' :>"
        else: responses = "I'm already not ignoring user  '" + id + "' o.o"
    send_message(responses)
        
def downvote(user_id,remem,id): req = requests.get("https://www.emeraldchat.com/karma_give?id="+id+"&polarity=-1=HTTP/2", cookies={'remember_token': remem, 'user_id': user_id})

def thread(id):
    banned.add(id)
    for c in cookiejar:
        c = c.split(",")
        user_id = c[1]
        remem = c[0]
        threading.Thread(target=downvote, args=(user_id,remem,id,)).start()


def admin_func(message,id,admin):
    """Function to handle all the admin 
    and mod commands"""
    
    for i in range(0, len(admin_commands)):
        result = admin_commands[i].match(message)
        global greet_status,running,name
        if bool(result) == True:
            if i == 0 :
                greet_status = True
                response = "Okai done ^-^"
                send_message(response)
            elif i == 1:
                if greet_status == True:
                    greet_status = False
                    response = "Okai done ^-^"
                    send_message(response)
                elif greet_status == False:
                    response = "I'm already not greeting o.o"
                    send_message(response)
            elif i == 2 and admin == True:
                response = "Cya :>"
                send_message(response)
                running = False
            elif i == 3 and admin == True:
                response = "List went -poof-"
                send_message(response)
                timeout_control.clear()
                list_main_dict.clear()
                idle_main_dict.clear()
            elif i == 4:
                sr = str(datetime.now() - t).split(":")
                if sr[0] == "0":
                    if str(int(sr[1])+0) == "0" : response = "I just joined -w-"
                    elif (int(sr[1])+0) == 1 : response = "I've been here for just a minute"
                    else : response = "I've been here for only " + str(int(sr[1])+0) + " minutes"
                else:
                    response = "I've been here for " + sr[0] + " hours and " + str(int(sr[1])+0) + " minutes"
                send_message(response)
            elif i == 5:
                greet_timeout = {}
                response = "Just had some memory loss x-x"
                send_message(response)
            elif i == 6:
                l = len(stats_list.keys())
                sr = str(datetime.now() - t).split(":")
                r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
                stats_r = str(len(stats)) + " have entered wfaf and " + str(l) + " unique people have joined in the past " + \
                    sr[0] + " hours and " + sr[1] + \
                    " minutes"", and it is " + \
                    str(r) + " in wfaf"
                send_message(stats_r)
            elif i == 7 and admin == True : send_message(fix_message(str(mute_list)))
            elif i == 8 and admin == True : send_message(str(timeout_control))
            elif i == 9:
                response = "Okai, restarting...."
                send_message(response)
                restart_program()
            elif i == 10 and admin == True:
                if "display_name" in j.keys() : name = fix_name(j["display_name"])
                del timeout_control[name]
                if name in idle_main : idle_main.remove(name)
                elif name in list_main : list_main.remove(name)
                response = "Ahem, aye aye"
                send_message(response)
            elif i == 11 : send_message(ily_r)
            elif i == 12 or i == 13 : mute_func(message, i)
            elif i == 14:
                array = message.split(" ")
                del array [0:2]
                response = "Banning " + fix_name(" ".join(array)) + " by giving -40 karma" 
                thread(str(int(name)))
                send_message(response)
def coin_handling(array):
    """Just as the name suggests,
    handles coins and responses to them"""
    num = array[2]
    if num.isdigit():
        coin_add = int(num)
        coins_contents = repo.get_contents("coins.txt")
        if (coin_add < 101) and (coin_add > -1):
            coin_new = coin_add + int(coins_contents.decoded_content.decode() )
            repo.update_file(coins_contents.path, "coins update", str(coin_new), coins_contents.sha, branch="main")
            if num == "1": coin_confirm = str(int(num) + 0) + " coin added to the fortune well, there are now " + str(coin_new) + " coins in the well, wishing good luck to all :D"
            else: coin_confirm = str(int(num) + 0) + " coins added to the fortune well, there are now " + str(coin_new) + " coins in the well, wishing good luck to all :D"
        elif coin_add > 100: coin_confirm = "Woops too many coins, maybe buy me some chocolates instead? :>"
        send_message(coin_confirm)

def send_feelings(array,index):
    """Handles sending and recieving feelings 
    like hugs and love and what not I will be adding
    because yay feelings"""
    if index != 4:
        del array [0:4]
        name = fix_name(" ".join(array))
        if index == 1: respons = "Sending lotsa love and hugs to " + name+" ❤️❤️"
        elif index == 2: respons = "Sending pats to " + name+" *pat pat*"
        elif index == 3: respons = "Sending hugs to "+name + " (੭｡╹▿╹｡)੭ *intense telekinetic noises*"
        elif index == 5:
            l = list(stats_list.values())
            l = [each_string.lower() for each_string in l]
            n = name.lower()
            if n in l:
                id = list(stats_list.keys())[l.index(n)]
                respons = "ID of " + name + " is " + str(id)
            else : respons = "Im sorry I havent seen anyone with the name " + name + " here"
        elif index == 6:
            id = int(name)
            r = requests.get("https://emeraldchat.com/profile_json?id=" + str(id),cookies = cookies)
            if r.status_code == 200:
                r = json.loads(r.text)
                name = r["user"]["display_name"]
                karma = r["user"]["karma"]
                username = r["user"]["username"]
                gender = r["user"]["gender"]
                created = r["user"]["created_at"].split("T")
                if name or karma or username or gender or created is None:
                    respons = "It appears the following is has either been deleted or doesnt exist, sowwy"
                else : respons = "The account with ID " + str(id) + " has the name " + name + "(" + username + ") with karma:- " + str(karma) + " and gender set to " + gender + " and was created on " + created[0] + " at " + created[1]
            elif r.status_code == 404: respons = "The following account is either deleted or doesnt exist"
            elif r.status_code == 403: respons = "Timeout error, kindly wait for about 15-20 seconds and try again"
            elif r is None : respons = "It appears the following is has either been deleted or doesnt exist, sowwy"
    else: 
        if index == 4:
            del array [0:2]
            name = fix_name(" ".join(array))
            respons = "*bonks "+name + " with a baseball bat~*"
    send_message(respons)


def coins_feelings(message):
    for reg_m in coinsandfeelings:
        result = reg_m.match(message)
        if bool(result) == True:
            index = coinsandfeelings.index(reg_m)
            if index == 0 : coin_handling(message.split(" "))
            else : send_feelings(message.split(" "),index)
            break


"""Connect blue to whatever"""
websocket.enableTrace(False)
ws = websocket.WebSocket()
ws.connect("wss://www.emeraldchat.com/cable",
           cookie=main_cookie,
           subprotocols=["actioncable-v1-json", "actioncable-unsupported"],
           origin="https://www.emeraldchat.com")

ws.send(json.dumps(connect_json))

while running == True:
    try:
        remove_blue()
        idle_function()
        t_start = perf_counter()
        reset_clock = reset_clock + 1
        if reset_clock == 500:
            greet_timeout = {}
            reset_clock = 0
        server_reply = (ws.recv())
        a = json.loads(server_reply)
        whos_here_res ={
            bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
            dice: "Your number is...." + str(random.randint(1,6))
        }
        if ("identifier" in a.keys()) and ("message" in a.keys()):
            b = a["message"]
            greet("user_connected", "add", True)
            greet("typing", "add", False)
            greet("user_disconnected", "remove", False)
            greet("messages", "add", False)
            
            if ("messages" in b.keys()) and ("user" in b.keys()):
                user = b["user"]
                if "id" in user.keys():
                    id = str(user["id"])
                    message = fix_message(str(b["messages"]))
                    if id not in mute_list:
                        coins_feelings(message)
                        matching(response_dict,message)
                        matching(whos_here_res,message)
                    if id in admin : admin_func(message, id, True)
                    elif id in mod : admin_func(message, id, False)

    except websocket.WebSocketConnectionClosedException:reconnect()
    except ConnectionTimeoutError :reconnect()
    except json.JSONDecodeError:continue
    except ValueError:continue
    except IndexError:continue