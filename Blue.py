from websocket import create_connection
from concurrent.futures import TimeoutError as ConnectionTimeoutError
import websocket
import random
import json
import requests
import re
from datetime import date,datetime
import datetime
from os import execl
import os
from sys import executable,argv
from time import gmtime, strftime,sleep,perf_counter
from github import Github
from vars import *
import threading
from timeit import default_timer as timer
import cleverbotfree
os.system("playwright install")
#Restarts the current program.
restart_program = lambda : execl(executable,executable, * argv)
name = " "
channel_id = "null"
starttime = t
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

    Greet_1 = "Hi, " + name + ", retrying won't help, you can try asking 'what is wfaf' for more info :D"
    Greet_2 = "Hi again, " + name + ", try asking 'what is wfaf' for more info :D "
    Greet_general = ("Hi, " + name + ", Welcome to WFAF, which stands for Waiting For A Friend, to which you were sent when you tried texting someone who hasn't accepted/declined your friend request, Enjoy your stay :D ")
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
            name,id = fix_name(user["display_name"]),user["id"]
            if result == "add":
                list_main.add(name)
                stats_list[id] = list_main_dict[id] =  name
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
                if (greet_status == True) and str(user["id"]) != "20909261" and str(user["id"]) != "20909232":
                    if str(user["id"]) in custom_greet_id.keys() : send_message(custom_greet_id[str(user["id"])])
                    else : send_greet(name)
                        
def get_joke():
    """Fetches jokes from API mentioned
    and returns it as value of var joke"""
    r = requests.get("https://icanhazdadjoke.com/slack")
    joke = json.loads(r.text)["attachments"][0]["text"]
    send_message(joke)
    
def get_quote():
    """Fetches quotes from the API mentioned 
    and returns it as value of var response3"""
    r = requests.get('https://api.quotable.io/random')
    content = str(r.json()['content'])
    author = "~ by " + str(r.json()['author'])
    send_message(content)
    time.sleep(0.2)
    send_message(author)
    
def threaded_adding(ids):
    global whos_here_r,whos_here_res
    r = requests.get("https://emeraldchat.com/profile_json?id=" + str(ids),cookies = cookies)
    r = json.loads(r.text)
    whos_here_r.append(r["user"]["display_name"])
    
def matching(dictname,message):
    global whos_here_r,whos_here_res
    keys = list(dictname.keys())
    for i in range(0, len(keys)):
        re_m = keys[i]
        result = re_m.match(message)
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
            elif dictname== response_dict and re_m == jok: threading.Thread(target=get_joke).start()
            elif dictname == response_dict and re_m == quote: threading.Thread(target=get_quote).start()
            else: send_message(list(dictname.values())[i])
            break

def fix_message(messages):
    """Fixes syntactical problems with incomming 
    messages and removes any unwanted chars"""
    message = str(messages)
    chars = ('"[]‘')
    for c in chars : message = message.replace(c, "")
    return (message.replace("'", '').replace("\n", "").strip())

def idle_function():
    """Function for moving people 
    between idle and main list with reference
    to time stamps in timeout_control"""
    idle_check_list = list(timeout_control.values())
    for i in range(0, len(idle_check_list)):
        x = idle_check_list[i]
        if (t_start - x) >= 240:
            val = list(timeout_control.keys())[i]
            if val in list_main_dict:
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
def update_git(mute_list):
    new_mute = str(mute_list)
    chars = "[]'\n"
    for c in chars : new_mute = new_mute.replace(c, "")
    muted_contents = repo.get_contents("muted.txt")
    repo.update_file(muted_contents.path, "mute update", str(new_mute), muted_contents.sha, branch="main")
    
def mute_func(message,index):
    array = message.split()
    global mute_list
    del array[0:2]
    id = array[0]
    if index == 12:
        if id in mute_list: responses = "I'm already ignoring user  '" + id + " 'o.o"
        else:
            mute_list.append(id)
            update_git(mute_list)
            responses = "Okai I'll ignore user '" + id + "' 0.0"
    elif index == 13:
        if id in mute_list:
            mute_list.remove(id)    
            update_git(mute_list)
            responses = "Okai I'll stop ignoring user '" + id + "' :>"
        else: responses = "I'm already not ignoring user  '" + id + "' o.o"
    send_message(responses)
        
def downvote(user_id,remem,id): requests.get("https://www.emeraldchat.com/karma_give?id="+str(id)+"&polarity=-1=HTTP/2", cookies={'remember_token': remem, 'user_id': user_id})

def ban_log(banned_id, admin_id):
    r = requests.get("https://emeraldchat.com/profile_json?id=" + str(id),cookies = cookies)
    admin_name = json.loads(r.text)["user"]["display_name"]
    banned_logs = repo.get_contents("logs.txt")
    log = admin_name + "(" + str(admin_id) + ")"  " banned " +str(banned_id) + "\n"
    repo.update_file(banned_logs.path, "ban-log", banned_logs.decoded_content.decode() + log, banned_logs.sha, branch="main")

def thread(id):
    banned.add(id)
    for c in cookiejar:
        c = c.split(",")
        user_id = c[1]
        remem = c[0]
        threading.Thread(target=downvote, args=(user_id,remem,id,)).start()
        
def stalker(id,time_now):
    filename = str(id) + ".txt"
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir": contents.extend(repo.get_contents(file_content.path))
        else: all_files.append(str(file_content).replace('ContentFile(path="','').replace('")',''))
    git_prefix = 'stalker-logs/'
    git_file = git_prefix + filename
    if git_file in all_files:
        logs = repo.get_contents(git_file)
        log = logs.decoded_content.decode()
        repo.update_file(logs.path, "stalker-log", log, logs.sha, branch="main")
    else: repo.create_file(git_file, "committing files", "", branch="main")
    while stalking_log[id][1] == True:
        r = requests.get("https://emeraldchat.com/profile_json?id=" + str(id),cookies = cookies)
        print(r.status_code)
        if r.status_code == 200:
            r = json.loads(r.text)
            name, karma,username, gender,created = r["user"]["display_name"],r["user"]["karma"], r["user"]["username"],r["user"]["gender"],r["user"]["created_at"].split("T")
            logs = repo.get_contents(git_file)
            log = logs.decoded_content.decode()
            time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
            text = "Logging at (" + str(time) + ") " + name + " " + str(karma) + " " + username + " " + gender + "\n"
            log = log + text
            repo.update_file(git_file, "committing files", log,logs.sha, branch="main")
        elif r.status_code == 404 or r is None:
            send_message("Stopping logging for account id " + str(id) + " because the account has been deleted and doesnt exist anymore")
            break
        elif timer() - time_now >= 3600:
            send_message("Stalking session of ID " + str(id)) 
            break
        else: pass
        sleep(15)
        
def admin_func(message,id,isadmin):
    """Function to handle all the admin 
    and mod commands"""
    
    for i in range(0, len(admin_commands)):
        result = admin_commands[i].match(message)
        global greet_status,running,name,starttime,aichatstate
        if bool(result) == True:
            if i == 0 :
                greet_status,response = True,"Okai done ^-^"
                send_message(response)
            elif i == 1:
                if greet_status == True:
                    greet_status,response = False,"Okai done ^-^"
                    send_message(response)
                elif greet_status == False:
                    response = "I'm already not greeting o.o"
                    send_message(response)
            elif i == 2 and isadmin == True:
                response = "Cya :>"
                send_message(response)
                running = False
            elif i == 3 and isadmin == True:
                response = "List went -poof-"
                send_message(response)
                timeout_control.clear()
                list_main_dict.clear()
                idle_main_dict.clear()
            elif i == 4:
                sr = str(datetime.now() - starttime).split(":")
                if sr[0] == "0":
                    if str(int(sr[1])+0) == "0" : response = "I just joined -w-"
                    elif (int(sr[1])+0) == 1 : response = "I've been here for just a minute"
                    else : response = "I've been here for only " + str(int(sr[1])+0) + " minutes"
                else: response = "I've been here for " + sr[0] + " hours and " + str(int(sr[1])+0) + " minutes"
                send_message(response)
            elif i == 5:
                greet_timeout,response = {},"Just had some memory loss x-x"
                send_message(response)
            elif i == 6:
                l, sr, r= len(stats_list.keys()),str(datetime.now() - starttime).split(":"),strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
                stats_r = str(len(stats)) + " have entered wfaf and " + str(l) + " unique people have joined in the past " + sr[0] + " hours and " + sr[1] + " minutes"", and it is " + str(r) + " in wfaf"
                send_message(stats_r)
            elif i == 7 and isadmin == True : send_message(fix_message(str(mute_list)))
            elif i == 8 and isadmin == True : send_message(str(timeout_control))
            elif i == 9:
                response = "Okai, restarting...."
                send_message(response)
                restart_program()
            elif i == 10 and isadmin == True:
                if "display_name" in j.keys() : name = fix_name(j["display_name"])
                del timeout_control[name]
                if name in idle_main : idle_main.remove(name)
                elif name in list_main : list_main.remove(name)
                response = "Ahem, aye aye"
                send_message(response)
            elif i == 11 and id not in mute_list: send_message(ily_r)
            elif i == 12 or i == 13 : mute_func(message, i)
            elif i == 14:
                array = message.split(" ")
                del array [0:2]
                response = "Banning " + fix_name(" ".join(array))  
                thread(fix_name(" ".join(array)) )
                threading.Thread(target=ban_log, args=(fix_name(" ".join(array)),id,)).start()
                send_message(response)
            elif i == 15 :
                response = str(admin).replace('"',"").replace("[", "").replace("]", "")
                send_message(response)
            elif i == 16:
                id = str(result.group(2))
                print(id)
                if id.isdigit():
                    if id not in stalking_log.keys():
                        t = threading.Thread(target=stalker, args=(id,timer(),) )
                        stalking_log[id] = [t, True]
                        t.start()
                        send_message("Okai waking stalk function")
                    else: send_message("I'm already stalking ID " + id)
                else: send_message("Please give a valid ID UnU")
            elif i ==17 :
                id = str(result.group(2))
                if id in stalking_log.keys():
                    stalking_log[id][1] = False
                    del stalking_log[id]
                    send_message("Alright ill stop stalking " + id + " UnU")
                else: send_message("I'm already not stalking the person with ID " + id)
            elif i == 18:
                list1 = list(stalking_log.keys())
                if not list1: response = "I'm currently stalking no one :>"
                else: response = "Currently stalking the following IDs:- " +fix_message(str(list1))
                send_message(response)
            elif i == 19:
                aichatstate = True
                send_message("Okai done")
            elif i == 20:
                aichatstate = False
                send_message("Okai done")
def coin_handling(array):
    """Just as the name suggests,
    handles coins and responses to them"""
    num = array[2]
    if array[2].isdigit():
        coin_add = int(array[2])
        coins_contents = repo.get_contents("coins.txt")
        if (coin_add < 101) and (coin_add > -1):
            coin_new = coin_add + int(coins_contents.decoded_content.decode() )
            repo.update_file(coins_contents.path, "coins update", str(coin_new), coins_contents.sha, branch="main")
            if num == "1": coin_confirm = str(int(num) + 0) + " coin added to the fortune well, there are now " + str(coin_new) + " coins in the well, wishing good luck to all :D"
            else: coin_confirm = str(int(num) + 0) + " coins added to the fortune well, there are now " + str(coin_new) + " coins in the well, wishing good luck to all :D"
        elif coin_add > 100: coin_confirm = "Woops too many coins, maybe buy me some chocolates instead? :>"
        send_message(coin_confirm)
respons = ""

def send_feelings(array,index,id,result):
    """Handles sending and recieving feelings 
    like hugs and love and what not I will be adding
    because yay feelings"""
    global respons
    if index != 4:
        del array [0:4]
        name = result.group(1)
        if index == 1: respons = "Sending lotsa love and hugs to " + name+" ❤️❤️"
        elif index == 2: respons = "Sending pats to " + name+" *pat pat*"
        elif index == 3: respons = "Sending hugs to "+name + " (੭｡╹▿╹｡)੭ *intense telekinetic noises*"
        elif index == 5:
            name = result.group(4)
            l = list(stats_list.values())
            n = 0
            for re_m in l:
                reg = re.compile(r"" + re_m+ "\\n*", re.I)
                result = reg.search(name)
                if result is not None:
                    respons = "ID of " + name + " is " + str(list(stats_list.keys())[l.index(re_m)])
                    break
                else: n+=1
            if n == len(stats_list.values()): response = "Im sorry I havent seen anyone with the name "+name+" here"
        elif index == 6 and id in admin:
            name = result.group(2)
            if name.isdigit():
                id = int(name)
                r = requests.get("https://emeraldchat.com/profile_json?id=" + str(id),cookies = cookies)
                if r.status_code == 200:
                    r = json.loads(r.text)
                    name, karma,username, gender,created = r["user"]["display_name"],r["user"]["karma"], r["user"]["username"],r["user"]["gender"],r["user"]["created_at"].split("T")
                    if gender is None: respons = "The account with ID " + str(id) + " has the name " + name + "(" + username + ") with karma:- " + str(karma)  + " and was created on " + created[0] + " at " + created[1]
                    else:respons = "The account with ID " + str(id) + " has the name " + name + "(" + username + ") with karma:- " + str(karma) + " and gender set to " + gender + " and was created on " + created[0] + " at " + created[1]
                elif r.status_code == 404: respons = "The following account is either deleted or doesnt exist"
                elif r.status_code == 403: respons = "Timeout error, kindly wait for about 15-20 seconds and try again"
                elif r is None : respons = "It appears the following account has either been deleted or doesnt exist, sowwy ;-;"
            else: respons = "Please provide with a valid ID :>"
        send_message(respons)
    else: 
        if index == 4:
            del array [0:2]
            name = fix_name(" ".join(array))
            respons = "*bonks "+name + " with a baseball bat~*"
        send_message(respons)
        
def chat(user_input):
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        bot = c_b.single_exchange(user_input)
        send_message(bot)
        c_b.close()

def dis_en_greets(id):
    global greet_status
    if id == "16008266"and greet_status == True:
        send_message("Disabling greets uwu")
        greet_status = False
    elif id == "20909261" and greet_status == False:
        send_message("Re-enabling greets :D")
        greet_status = True

def check_greeters(message,id):
    global greet_status
    if (id == "16008266" or id == "20909261"):
        for reg_m in greet_check:
            result = reg_m.search(message)
            if message in custom_greet_id.values() or  bool(result) == True or message == "Our favorite Blue greeter is here!" : dis_en_greets(id)
        for reg_m in custom_greet_id.values():
            reg = re.compile(r"" + reg_m+ r"", re.I)
            pattern = reg_m + "\s*"
            result = reg.search(message)
            result1 = re.match(pattern,message)
            if result is not None : dis_en_greets(id)
                
def coins_feelings(message,id):
    for reg_m in coinsandfeelings:
        result = reg_m.match(message)
        if bool(result) == True:
            index = coinsandfeelings.index(reg_m)
            if index == 0 : coin_handling(message.split(" "))
            else : send_feelings(message.split(" "),index,id,result)
            break

def log_chats(message,user_id):
    name = fix_name(user["display_name"])
    log = fix_message(name + "(" + str(user_id) + ") :-" + message) + "\n" 
    file = open("chatlogs.txt","a")
    file.write(log)
    file.close()
    
def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")
    
def push_logs():
    file = open("chatlogs.txt","r")
    contents1 = file.readlines()
    file.close()
    file = open("chatlogs.txt","w")
    file.close()
    date = datetime.today().strftime('%d-%m-%Y')
    filename = "log (" + date + ").txt"
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir": contents.extend(repo.get_contents(file_content.path))
        else: all_files.append(str(file_content).replace('ContentFile(path="','').replace('")',''))
    git_prefix = 'wfaf-logs/'
    git_file = git_prefix + filename
    if git_file in all_files:
        logs = repo.get_contents(git_file)
        log = logs.decoded_content.decode()
        for i in contents1: log = log + i 
        repo.update_file(logs.path, "chat-log", log, logs.sha, branch="main")
    else:
        log = ""
        for i in contents1: log = log + i
        repo.create_file(git_file, "committing files", log, branch="main")

"""Connect blue to whatever"""
websocket.enableTrace(False)
ws = websocket.WebSocket()
ws.connect("wss://www.emeraldchat.com/cable",
           cookie=main_cookie,
           subprotocols=["actioncable-v1-json", "actioncable-unsupported"],
           origin="https://www.emeraldchat.com")
ws.send(json.dumps(connect_json))
start = timer()
while running == True:
    try:
        remove_blue()
        idle_function()
        t_start = perf_counter()
        reset_clock = reset_clock + 1
        if reset_clock == 500:
            greet_timeout , reset_clock ={}, 0
        if timer() - start>= 20 and os.stat("chatlogs.txt").st_size != 0:
            push_logs()
            start = timer()
        server_reply = (ws.recv())
        a = json.loads(server_reply)
        whos_here_r = whos_idle_r = []
        whos_here_res ={
            whos_here: whos_here_r,
            whos_idle: whos_idle_r,
            bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
            dice: "Your number is...." + str(random.randint(1,6))
        }
        if (len(list_main_dict.keys())+ len(idle_main_dict.keys())) <= 4:
            n = random.randint(0,100000)
            if n % 987 == 0: threading.Thread(target= singing).start()
        if ("identifier" in a.keys()) and ("message" in a.keys()):
            b = a["message"]
            threading.Thread(target=greet, args=("user_connected","add",True,)).start()
            threading.Thread(target=greet, args=("typing","add",False,)).start()
            threading.Thread(target=greet, args=("user_disconnected","remove",False,)).start()
            threading.Thread(target=greet, args=("messages","add",False,)).start()
            if ("messages" in b.keys()) and ("user" in b.keys()):
                user = b["user"]
                if "id" in user.keys():
                    id = str(user["id"])
                    message = fix_message(str(b["messages"]))
                    if aichatstate == True:
                        result = ai.match(message)
                        if result: threading.Thread(target=chat, args=(message,)).start()
                    threading.Thread(target=check_greeters, args=(str(b["messages"]),id,)).start()
                    threading.Thread(target=log_chats, args=(message,id,)).start()
                    if id not in mute_list:
                        coins_feelings(message,id)
                        matching(response_dict,message)
                        matching(whos_here_res,message)
                    if id in admin : admin_func(message, id, True)
                    elif id in mod : admin_func(message, id, False)

    except : 
        send_message("Unknown error occurred, restarting... ~*")
        restart_program()
