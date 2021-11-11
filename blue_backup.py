from websocket import create_connection
from concurrent.futures import TimeoutError as ConnectionTimeoutError
import websocket
import random
import time
import json
import datetime
import requests
import re
from datetime import date
import os
import sys
from time import gmtime, strftime
today = date.today()


connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":null}"}
websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("wss://www.emeraldchat.com/cable", cookie="user_id=MjE1NTAyNjI%3D--53715d8c0d5a37453895fbf751e8bc4f9056f2fe",subprotocols=["actioncable-v1-json", "actioncable-unsupported"],origin="https://www.emeraldchat.com",header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"})
print(ws.recv())
ws.send(json.dumps(connect_json))
timeout_control = {}
def connectagain():
    connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":null}"}
    websocket.enableTrace(True)
    ws = websocket.WebSocket()
    ws.connect("wss://www.emeraldchat.com/cable", cookie="user_id=MjE1NTAyNjI%3D--53715d8c0d5a37453895fbf751e8bc4f9056f2fe",subprotocols=["actioncable-v1-json", "actioncable-unsupported"],origin="https://www.emeraldchat.com",header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"})
    print(ws.recv())
    ws.send(json.dumps(connect_json))
running = True
response_kill = False
self_destruct = True
greet_status = True
forbiden_chars = ["\u202e","'",'"',"’"]
replace_txts = []
connection = True
list_main = set()
idle_main = set()
admin = ["18695559","16986137","16521287"]
mod = ["14496406","21847694","20327398","20909209","21964175"]
greet_timeout = {}
chat_status = True
stats_list = set()
stats = []
custom_greet_id = {
    "16986137":"The river of life bubbles when Aqua comes near~ ",
    "21550262" : "Hi, its Blue ^-^",
    "21388579":"Sir This recruit tactically acquired the fig bars sir~",
    "20835136":"Testing, testing, Wan, two, three! ",
    "291734":"Here comes our favorite magical frog! 🐸 ~~.*~",
    "14751444" : "Hamtaro, the karmic wonder, has arrived ·ᴗ·",
    "18695559" : "Your friendly neighbourhood Saturn is here! *~~.",
    "18274541":"A buzzy Bee enters the hive! 🐝 ~~.*~",
   # "18491422" : "Shhhh... The one and only drama queen cat is here *meow* ",
    "18491422" : "And the hot cat arrives on the stage, ladies and germs"
    "18560513" : "SCP-1689 would make for a lot of ... Chipz. ~*",
    "17248098":"The darker the night, the brighter the stars... ~*",
    "20909209" : "A dude? B dude? what dude? which dude? what is A? what is dude? who am i? what is wfaf..... x-x",
    "19422865" : "Twi, the cute pony is here ~*",
    "17979714":"Your local simp (Bri) is here ~*",
    "14648841":"こんにちはねこちゃん",
    "17364255":"Coming hot out of the oven, it's 𝖕𝖎𝖊! 🥧 *~~.",
    "21848509":"Megumin⁩, the arch-wizard magically appears out of thin air 🧙",
    "19259507" : "Greetings cathy cath ~*",
    "20073491" : "Greetings, your highness *bows*",
    "20909261" : "Mecha nurse is here, everyone get ready for your shots 💉 💊 ",
    "22466125" : "Welcome lovely person <3",
    "21842289" : "As dusk appears, darkness takes over the sky... before the last trace of light is gone"
}
whohere_t = 0
starttime = time.time()
t = datetime.datetime.now()
timeout = 10
reset_clock = 0
whos_here = re.compile(r"""(blue who'?’?s here\??)|(blue das crazy\??|(yzarc sad eubl)|(blue who is all here)|(blue who all are there here\??)\s*)""", re.I)
whos_here = whos_here
whos_idle = re.compile(r"""(blue who'?’?s idle\??\s*)|(blue who is all idle\s*)|(blue who is all lurking\s*)|(blue who'?’?s lurking\??\s*)""", re.I)
whos_idle = whos_idle
tldr = re.compile(r"""(blue wfaf)|(blue tldr)|(what is wfaf)|(blue where are we)\s*""", re.I)
high_five = re.compile(r"""(blue )?(high five)\s*""", re.I)
dab = re.compile(r"""blue dab\s*""", re.I)
#hate_myself1 = re.compile(r"""(blue (i hate myself)|(no one likes me))|((i hate myself)|(no one likes me))\s*""", re.I)
hate_myself1 = re.compile(r"""(blue )?(i hate myself)|(no one likes me)\s*""", re.I)

thanks = re.compile(r"""((thanks|thx|thenks|thonks|thank you) blue\s*)|(blue (thanks|thx|thenks|thonks|thank you)\s*)""", re.I)
smile = re.compile(r""":>\s*""", re.I)
hey1 = re.compile(r"""hi blue\s*""", re.I)
kill = re.compile(r"""blue (kill|shoot|murder) me\s*""", re.I)
pats = re.compile(r"""blue send pats\s*""", re.I)
hugs2 = re.compile(r"""blue hug\s*""", re.I)
howdy = re.compile(r"""howdy Blue\??\s*""", re.I)
party = re.compile(r"""blue (lets )?party\s*""", re.I)
menu = re.compile(r"""blue menu\s*""", re.I)
magic_menu = re.compile(r"""blue magic menu\s*""", re.I)
smile_rev = re.compile(r"""<:\s*""", re.I)
heart = re.compile(r"""<3\s*""", re.I)
quote = re.compile(r"""blue (tell me a )?quote\s*""", re.I)
uwu = re.compile(r"""(uwu\s*)|(blue cultural reset\s*)""", re.I)
jok = re.compile(r"""blue (tell me a )?joke\s*""", re.I)
no = re.compile(r"""blue (no|enforce)\s*""", re.I)
dni = re.compile(r"""blue (dni|do not interact)\s*""", re.I)
bored = re.compile(r"""(blue )?im bored\s*""", re.I)
dying = re.compile(r"""(blue )?im dying\s*""", re.I)
enable_greets = re.compile(r"""blue enable greets\s*""", re.I)
disable_greets = re.compile(r"""blue disable greets\s*""", re.I)
self_destruct = re.compile(r"""(blue self destruct)|(blue die)|(blue kys)\s*""", re.I)
clear_userlist = re.compile(r"""blue clear userlist\s*""", re.I)
uptime1 = re.compile(r"""(blue uptime)|(!uptime)\s*""", re.I)
clear_memory = re.compile(r"""blue clear memory\s*""", re.I)
stats1 = re.compile(r"""(blue stats)|(blue tell me the stats)\s*""", re.I)
stats1 = stats1
get_mute = re.compile(r"""(blue get mutelist)|(blue fetch mutelist)\s*""", re.I)
get_timeout_control = re.compile(r"""(blue get timeout_control)|(blue fetch timeout_control)\s*""", re.I)
restart_s = re.compile(r"""((blue|blew) restart)|((blue|blew) reset)\s*""", re.I)
hide = re.compile(r"""blue help me hide\s*""", re.I)
ily = re.compile(r"""blue (ily)|(i love you)\s*""", re.I)
love = re.compile(r"""blue send love\s*""", re.I)

coffee = re.compile(r"""blue serve (coffee|1|caffee)\s*""", re.I)
milk = re.compile(r"""blue serve (milk|2)\s*""", re.I)
water = re.compile(r"""blue serve (water|3)\s*""", re.I)
cookiess = re.compile(r"""blue serve (cookies and milk|a|cookies n milk)\s*""", re.I)
ppizza = re.compile(r"""blue serve (pineapple pizza|b)\s*""", re.I)

im_bored_list=[
    "How about, dance :D",
    "Hmmm maybe sing a song?",
    "Study... maybe... instead of procrastinating heh",
    "Well.... have you been outside lately? How about go for a walk? (if its not an unreasonable time)",
    "I would love to play with you to make you feel less bored but.... Aqua hasnt programmed it yet ;-;",
    "Youtube dot com hehe, best place to cure boredom",
    "How about watching a movie? or binging a tv series? (dont ask for suggestions :> I just stare at binary numbers 24/7)",
    "Sleep",
    "You could go to 1v1 and find someone to talk to? (this is one of the worst advices ive given but yea its a viable option)",
    "Same :)",
    "Ahhhh who isnt",
    "Sameee ~high five~",
    "Ive heard star gazing is lovely, give that a try",
    "Spread love :>"
]

coffee_r = "☕" 
milk_r = "🥛"
water_r = "🥤"
cookies_r = "🍪 🥛 🍪"
pineapple_pizza_r = "🍍 + 🍕"

tldr_r = "You're here because you tried to message someone who didn't accept your friend request. We call this chat WFAF,  Waiting For A Friend. Let's keep it family-friendly!"
high_five_r = "High five ~*"
dab_r = "ヽ( •_)ᕗ"
hate_myself_r =  "I like you, have a cupcake 🧁 ^-^"
thanks_r = "You're welcome :D"
hi_r = "hiiiiii :D"
smile_r = "<:"
#kill_r = "Ahem 🔪 "
kill_r = "Nu, smh"
pats_r = "._.)/(._."
hug_r = "(੭｡╹▿╹｡)੭"
party_r = "partyyy wohooo 🥳"
menu_r = "Rn we have 1) Coffee, 2) Milk, 3) Water"
magic_menu_r = "We have A) Cookies n Milk, B) Pineapple Pizza"
smile_rev_r = ":>"
heart_r = "<3"
dying_r = "Nothing new, now go work smh"
uwu_r = "UwU"
howdy_r = "hewwos"
no_r = "Kindly be nice and keep this family-friendly while you are here, else the wfaf door is always open for you to leave, thanks"
dni_r = "We are not interested, thanks no thanks"
ily_r = "I love you even moreeee"
love_r = "Hey wonderful person, you are amazing and deserve everything you desire and love. Hope the best for you. You have all my love and wishes. Much love ~ Blue :>"
response_dict = {
    tldr : tldr_r,
    high_five : high_five_r,
    dab : dab_r,
    hate_myself1 : hate_myself_r,
    thanks : thanks_r,
    smile : smile_r,
    hey1 : hi_r,
    kill : kill_r,
    pats : pats_r,
    hugs2 : hug_r,
    party : party_r,
    menu : menu_r,
    magic_menu : magic_menu_r,
    smile_rev : smile_rev_r,
    heart : heart_r,
    uwu : uwu_r,
    howdy : howdy_r,
    no : no_r,
    dni : dni_r,
    dying : dying_r,
    love : love_r,

    coffee : coffee_r,
    milk : milk_r,
    water : water_r,

    cookiess : cookies_r,
    ppizza : pineapple_pizza_r,
}
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def send_message(content):
    if response_kill == False :
        message = {"command":"message","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":null}","data":"{\"message\":\"" + content +"\",\"id\":null,\"action\":\"speak\"}"}
        ws.send(json.dumps(message))

def greet(action,result,greet) :
    if (action in b.keys()) and ("user" in b.keys()):
        user = b["user"]
        if "display_name" in user.keys():
            name = user["display_name"]
            for i in range (0 , len(forbiden_chars)):
                name = name.replace(forbiden_chars[i],"")
            if result == "add":
                list_main.add(name)
                for i in range (0 , len(forbiden_chars)):
                    name = name.replace(forbiden_chars[i],"")
                timeout_control[name] = time.perf_counter()
            elif (result == "remove"):
                del timeout_control[name]
                if name in idle_main:
                    idle_main.remove(name)
                elif name in list_main:
                    list_main.remove(name)
            if (greet == True) and ("id" in user) and (action == "user_connected") :
                stats_list.add(name)
                stats.append(name)
                timeout_control[name] = time.perf_counter()
                if (greet_status == True):
                    ids = user["id"]
                    if str(ids) in custom_greet_id.keys():
                        greet = custom_greet_id[str(ids)]
                        send_message(greet)
                    else :
                        if name in greet_timeout.keys():
                            Greet_1 = "Hi, " + name +", retrying won't help, you can try asking 'what is wfaf' for more info :D"
                            Greet_2 = "Hi again, " + name +", try asking 'what is wfaf' for more info :D "
                            if (greet_timeout[name] == "1") :
                                send_message(Greet_1)
                                greet_timeout[name] = "2"
                            elif greet_timeout[name] == "2":
                                send_message(Greet_2)
                                greet_timeout[name] = "3"
                            elif greet_timeout[name] == "3":
                                pass
                        else:
                            Greet_general = "Hi, " + name +", Welcome to WFAF, which stands for Waiting For A Friend, Let's keep it family-friendly, Enjoy your stay :D "
                            send_message(Greet_general)
                            greet_timeout[name] = "1"
                            
def message_reply():
    if ("identifier" in a.keys()) and ("message" in a.keys()) :
        b = a["message"]
        if ("messages" in b.keys()) and ("user" in b.keys()):
            user = b["user"]
            if "id" in user:
                if str(user["id"]) in mute_list:
                    pass
                else:
                    message = str(b["messages"])
                    chars = '"[]‘'
                    for c in chars:
                        message = message.replace(c,"")
                    message = message.replace("'", "")
                    keys = list(response_dict.keys())
                    for i in range (0, len(keys)):
                        re_m = keys[i]
                        result = re_m.match(message)
                        if bool(result) == True:
                            values = list(response_dict.values())
                            send_message(values[i])
                    keys = list(whos_here_res.keys())
                    for i in range(0,len(keys)):
                        re_m = keys[i]
                        result = re_m.match(message)
                        if bool(result) == True:
                            values = list(whos_here_res.values())
                            send_message(values[i])


def log():
    if ("identifier" in a.keys()) and ("message" in a.keys()) :    
        b = a["message"]
        if ("messages" in b.keys()) and ("user" in b.keys()):
            user_arr = b["user"]
            if "display_name" in user_arr.keys():
                name = user_arr["display_name"]
                for i in range (0 , len(forbiden_chars)):
                    name = name.replace(forbiden_chars[i],"")
                d4 = today.strftime("%b-%d-%Y")
                message = str(b["messages"])
                chars = '"[]'
                for c in chars:
                    message = message.replace(c,"")
                try:
                    log = open("log " + d4 + ".txt","a")
                    log.write(name + ":- " + message+ "\n" ) 
                except FileNotFoundError :
                    with open("log " + d4 + ".txt", 'w') as f:
                        f.write(name + ":- " + message + "\n" ) 
def idle_function():
    idle_check_list = list(timeout_control.values())
    for i in range (0,len(idle_check_list)):
        x = idle_check_list[i]
        if (t_start - x) >= 240:
            keys = list(timeout_control.keys())
            val = keys[i]
            for i in range (0 , len(forbiden_chars)):
                val = val.replace(forbiden_chars[i],"")
            if val in list_main:
                list_main.remove(val)
            idle_main.add(val)
        elif (t_start - x) < 240:
            keys = list(timeout_control.keys())
            val = keys[i]
            for i in range (0 , len(forbiden_chars)):
                val = val.replace(forbiden_chars[i],"")
            if val in idle_main:
                idle_main.remove(val)
            
        i = i+1
url = 'https://api.quotable.io/random'
r = requests.get(url)
q = r.json()
response1 = q['content']
response2 = (q['author'])
response3 = " -" + str(response2)
response3 = response1 + response3
while running == True :
    try:
        if "Blue" in list_main:
            list_main.remove("Blue")
        if "Blue" in idle_main:
            list_main.remove("Blue")
        if "Blue" in list(timeout_control.keys()):
            del timeout_control["Blue"]
        idle_function()
        t_start = time.perf_counter()
        r = requests.get("https://icanhazdadjoke.com/slack")
        joke = r.text
        joke = json.loads(joke)
        joke = joke["attachments"]
        joke = joke[0]
        joke = joke["text"]
        reset_clock = reset_clock + 1 
        if reset_clock == 500:
            greet_timeout = {}
            reset_clock = 0 
        t_now = time.perf_counter()
        server_reply = (ws.recv())
        a = json.loads(server_reply)
        if ("identifier" in a.keys()) and ("message" in a.keys()) :    
            b = a["message"]
            mute1 = open("muted.txt","r")
            content = mute1.read()
            mute_list = content.split('\n', 1)[0]
            mute_list = mute_list.split(",")
            mute1.close()
            greet("user_connected","add",True )
            greet("typing","add", False )
            greet("user_disconnected", "remove", False)
            greet("messages", "add" , False)
        url = 'https://api.quotable.io/random'
        r = requests.get(url)
        q = r.json()
        response1 = q['content']
        response2 = (q['author'])
        response3 = " -" + str(response2)
        response3 = response1 + response3
        if len(idle_main) == 0:
            whos_here_r = "I can see " +str(list_main)+" and no lurkers :p"
            whos_idle_r = "I can see no lurkers as of now"
        elif len(idle_main) > 0:
            if len(idle_main) == 1:
                whos_here_r = "I can see " +str(list_main)+" and "+ str(len(idle_main))+" person lurking :p"
            elif len(idle_main) > 1 :
                whos_here_r = "I can see " +str(list_main)+" and "+ str(len(idle_main))+" peeps lurking :p"
            whos_idle_r = "I can see " +str(idle_main)+" lurking"
        whos_here_r = whos_here_r.replace("{","")
        whos_here_r = whos_here_r.replace("}","")
        whos_idle_r = whos_idle_r.replace("{","")
        whos_idle_r = whos_idle_r.replace("}","")
        whos_here_res = {
            whos_here : whos_here_r,
            whos_idle : whos_idle_r,
            jok : joke,
            quote : response3,
            bored : im_bored_list[random.randint(0,len(im_bored_list))]
        }
        log()
        message_reply()
        admin_commands = [
            enable_greets,
            disable_greets,
            self_destruct,
            clear_userlist,
            uptime1,
            clear_memory,
            stats1,
            get_mute,
            get_timeout_control,
            restart_s,
            hide,
            ily
        ]
        if ("identifier" in a.keys()) and ("message" in a.keys()) :    
            b = a["message"]
            if ("messages" in b.keys()) and ("user" in b.keys()):
                j = b["user"]
                if "id" in j.keys() :
                    id = str(j["id"])
                    message = str(b["messages"])
                    chars = ('"[]‘')
                    for c in chars:
                        message = message.replace(c,"")
                    message = message.replace("'" , '')
                    if id in admin:
                        for i in range (0, len(admin_commands)):
                            re_n = admin_commands[i]
                            result = re_n.match(message)
                            if bool(result) == True:
                                if i == 0:
                                    greet_status = True
                                    response = "Okai done ^-^"
                                    send_message(response)
                                if i == 1:
                                    greet_status = False
                                    response = "Okai done ^-^"
                                    send_message(response)
                                if i == 2:
                                    response = "Cya :>"
                                    send_message(response)
                                    running = False
                                if i == 3:
                                    response = "List went -poof-"
                                    send_message(response)
                                    list_main.clear()
                                    idle_main.clear()
                                    timeout_control = {}
                                if i == 4:
                                    uptime = str(datetime.datetime.now() - t)
                                    split2_result =uptime.split(":")
                                    if split2_result[0] == "0":
                                        if str(int(split2_result[1])+0) == "0":
                                            response = "I just joined -w-"
                                        elif (int(split2_result[1])+0) == 1:
                                            response = "I've been here for just a minute"
                                        else:
                                            response = "I've been here for only " + str(int(split2_result[1])+0) +" minutes"
                                    else:
                                        response = "I've been here for " + split2_result[0] + " hours and " + str(int(split2_result[1])+0)  +" minutes"
                                    send_message(response)
                                if i == 5:
                                    greet_timeout= {}
                                    response = "Just had some memory loss x-x"
                                    send_message(response)
                                if i == 6:
                                    l = len(list(stats_list))
                                    uptime = str(datetime.datetime.now() - t)
                                    split2_result =uptime.split(":")
                                    r = time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())
                                    stats_r = str(len(stats)) + " have entered wfaf and " +  str(l) + " unique people have joined in the past " + split2_result[0] + " hours and " + split2_result[1] +" minutes"", and it is " + str(r) + " in wfaf"
                                    send_message(stats_r)
                                if i == 7:
                                    send_message(str(mute_list))
                                if i == 8 :
                                    send_message(str(timeout_control))
                                if i == 9 :
                                    response = "Okai, restarting...."
                                    send_message(response)
                                    restart_program()
                                if i == 10 :
                                    if "display_name" in j.keys():
                                        name = j["display_name"]
                                        for i in range (0 , len(forbiden_chars)):
                                            name = name.replace(forbiden_chars[i],"")
                                    del timeout_control[name]
                                    if name in idle_main:
                                        idle_main.remove(name)
                                    elif name in list_main:
                                        list_main.remove(name)
                                    response = "Ahem, aye aye"
                                    send_message(response)
                                if i == 11 :
                                    send_message(ily_r)


                    elif id in mod:
                        for i in range (0, len(admin_commands)):
                            re_n = admin_commands[i]
                            result = re_n.match(message)
                            if bool(result) == True:
                                if i == 0:
                                    greet_status = True
                                    response = "Okai done ^-^"
                                    send_message(response)
                                if i == 1:
                                    greet_status = False
                                    response = "Okai done ^-^"
                                    send_message(response)
                                    timeout_control = {}
                                if i == 4:
                                    uptime = str(datetime.datetime.now() - t)
                                    split2_result =uptime.split(":")
                                    if split2_result[0] == "0":
                                        if str(int(split2_result[1])+0) == "0":
                                            response = "I just joined -w-"
                                        elif (int(split2_result[1])+0) == 1:
                                            response = "I've been here for just a minute"
                                        else:
                                            response = "I've been here for only " + str(int(split2_result[1])+0) +" minutes"
                                    else:
                                        response = "I've been here for " + split2_result[0] + " hours and " + str(int(split2_result[1])+0)  +" minutes"
                                    send_message(response)
                                if i == 5:
                                    greet_timeout= {}
                                    response = "Just had some memory loss x-x"
                                    send_message(response)
                                if i == 6:
                                    l = len(list(stats_list))
                                    uptime = str(datetime.datetime.now() - t)
                                    split2_result =uptime.split(":")
                                    r = time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())
                                    stats_r = str(len(stats)) + " have entered wfaf and " +  str(l) + " unique people have joined in the past" + split2_result[0] + " hours and " + split2_result[1] +" minutes"", and it is " + str(r) + " in wfaf"
                                    send_message(stats_r)
                    
        timenow = time.time()
        if (int(starttime - timenow) > 20):
            greet_timeout = {}
            starttime = time.time()

        
        dict_serve = {
            "coffee" : "Image: [aW1hZ2UvOTc4NDI1NC9jb2ZmZWUuanBn]" ,
            "milk" : "Image: [aW1hZ2UvOTc4NDI1Mi9taWxrLmpwZWc=]",
            "water" : "Image: [aW1hZ2UvOTc4NDI1My93YXRlci5qcGc=]",
            "doritos" : "Image: [aW1hZ2UvOTc4NDI2OC9pbWFnZXMuanBlZw==]",
            "pineapple pizza" : "Image: [aW1hZ2UvOTc4NDI3Ni9pc3RvY2stNTM3NjQwNzEwLmpwZw==]"
        }
        if ("identifier" in a.keys()) and ("message" in a.keys()) :   
            b = a["message"]
            if ("messages" in b.keys()) and ("user" in b.keys()):
                user = b["user"]
                if "id" in user:
                    if str(user["id"]) in mute_list:
                        pass
                    else:
                        message = str(b["messages"])
                        chars = '[]"‘'
                        for c in chars:
                            message = message.replace(c,"")
                        message = message.replace("'", "")
                        array = message.split()
                        if ((array[0] == "blue") or (array[0] == "Blue")) and (len(array) >2):
                            if (array[1] == "add") and ((array [3] == "coins") or (array[3] == "coin") or (array[4] == "coins") or (array[4] == "coin")):
                                num = array[2]
                                if num.isdigit():
                                    coin_add = int(num)
                                    if (coin_add < 101) and (coin_add > -1):
                                        file1 = open("coins.txt","r")
                                        count_now = file1.read()
                                        first = count_now.split('\n', 1)[0]
                                        coin_new = coin_add + int(first)
                                        file1.close()
                                        file2 = open("coins.txt","w")
                                        file2.write(str(coin_new))
                                        file2.close()
                                        if num == "1":
                                            coin_confirm = str(int(num) + 0) + " coin added to the fortune well, there are now "+ str(coin_new) + " coins in the well, wishing good luck to all :D"
                                            send_message(coin_confirm)
                                            coin_new = 0
                                        else:
                                            coin_confirm = str(int(num) + 0) + " coins added to the fortune well, there are now "+ str(coin_new) + " coins in the well, wishing good luck to all :D"
                                            send_message(coin_confirm)
                                            coin_new = 0
                                    elif coin_add > 100 :
                                        coin_overflow = "Woops too many coins, maybe buy me some chocolates instead? :>"
                                        send_message(coin_overflow)
                            elif (array[1]== "send"):
                                    if (array [2]== "hugs") and (array[3] == "to"):
                                        new_arr = []
                                        for i in range(4,len(array)):
                                            new_arr.append(array[i])
                                        name = ""
                                        for j in range (0,len(new_arr)):
                                            name = name + new_arr[j] + " "
                                            j= j+1
                                        responses = "Sending hugs to "+name+" (੭｡╹▿╹｡)੭ *intense telekinetic noises*"
                                        send_message(responses)
                                    elif (array [2]== "pats") and (array[3] == "to"):
                                        new_arr = []
                                        for i in range(4,len(array)):
                                            new_arr.append(array[i])
                                        name = ""
                                        for j in range (0,len(new_arr)):
                                            name = name + new_arr[j] + " "
                                            j= j+1
                                        responses = "Sending pats to " + name+" *pat pat*"
                                        send_message(responses)
    
                    j = b["user"]
                    if "id" in j.keys() :
                        id = j["id"]
                        ids = str(id)
                        if (ids in admin) or (ids in mod):
                            message = str(b["messages"])
                            chars = '"[]'
                            for c in chars:
                                message = message.replace(c,"")
                            message = message.replace("'", "")
                            array = message.split()
                            if (len(array) > 2 ) and ((array[0] == "blue") or (array[0] == "Blue")) : 
                                if ((array[1] == "mute") or (array[1] == "ignore")):
                                    id_ignored = array[2]
                                    if id_ignored in mute_list:
                                        responses = "I'm already ignoring user  '" + id_ignored +" 'o.o"
                                        send_message(responses)
                                    else:
                                        mute_list.append(id_ignored)
                                        new_mute = str(mute_list)
                                        chars = "[]' "
                                        for c in chars:
                                            new_mute = new_mute.replace(c,"")
                                        new_list_entry = open ("muted.txt","w")
                                        new_list_entry.write(new_mute)
                                        new_list_entry.close()
                                        responses = "Okai I'll ignore user '" + id_ignored +"' 0.0"
                                        send_message(responses)
                                if ((array[1] == "unmute") or (array[1] == "unignore")):
                                    id_ignored = array[2]
                                    mute_list.remove(id_ignored)
                                    new_mute = str(mute_list)
                                    chars = "[]'/n "
                                    for c in chars:
                                        new_mute = new_mute.replace(c,"")
                                    new_list_entry = open ("muted.txt","w")
                                    new_list_entry.write(new_mute)
                                    new_list_entry.close()
                                    responses = "Okai I'll stop ignoring user '" + id_ignored + "' :>"
                                    send_message(responses)

    except websocket.WebSocketConnectionClosedException as e:
        while connection == True :
            connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":null}"}
            websocket.enableTrace(True)
            ws = websocket.WebSocket()
            ws.connect("wss://www.emeraldchat.com/cable", cookie="user_id=MjE1NTAyNjI%3D--53715d8c0d5a37453895fbf751e8bc4f9056f2fe;_prototype_app_session=VTZDMXJMRlNTSHdjM1M2dWMxMkp3VThra3pCT1dpa3F4S3RhZktaRnh4T3RYNy9tV0VvNE51cGkySDhvOG9mR0NtajRmQTdndzlLZUNlTXRwYjlVRDhuckVCdnFhTjZ0ZVV5YlZHaE5yRzdKbVZ5a0RqT0lUOXo0UlZYeWtWSU0wbFJMQ2xZTWgwTnZHdEx4eE9ZU0dlakxtZnd1ZUpCejBEVml0UmllSUNBYjRCMGx3K2NlQ00rRndLS3VONVN3U2ZIdFVxcnV2WnJPUjhyRjVCWVpmUy9oRDhlYWJ2QlMzWmFCaE10SHhxUT0tLUU2WWFsbmh1VUl5OGJHZnlPSEFaYkE9PQ%3D%3D--876c8414f3da49506e6392636364b694344fce8d",subprotocols=["actioncable-v1-json", "actioncable-unsupported"],origin="https://www.emeraldchat.com",header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36" }, timeout = 10000 )
            print(ws.recv())
            if ws.connected == True:
                ws.send(json.dumps(connect_json))
                connection = False
            if ws.connected == False:
                time.sleep(1)
                continue
    except ConnectionTimeoutError as e:
        while connection == True :
            connectagain()
            if ws.connected == True:
                ws.send(json.dumps(connect_json))
                connection = False
            if ws.connected == False:
                time.sleep(1)
                continue
    except ValueError:
        pass
    except IndexError:
        pass
    except KeyError :
        pass
    except :
        pass
