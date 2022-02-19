from pathlib import Path
from var import *
from src.utils import fix_message, fix_name
from time import strftime, gmtime, sleep
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

from cl import *
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
