from var import *
from time import sleep, strftime, gmtime
from utils import *
import websocket
from cl import cl
def thread_function():
    global seen_data
    cookie = "user_id=MjExNzQ2MDg%3D--a4763efe1b8631066fdee681d54eec7ba278ca9e"
    list_id =  ["48","56","33","39","38","40","34","51","58","57","41","54","37","53","43","42","49","55","59","44","46","36","60","52","32","50","47","35","45"]
    channel_dict = {'48': 'ice squad ❄️', '56': 'noodle squad 🍜 ', '33': 'roleplaying', '39': 'moon squad 🌑', '38': 'sun squad ☀️', '40': 'conspiracy squad 👽', '34': 'VIP ⭐', '51': 'banana squad 🍌', '58': 'sushi squad 🍣', '57': 'pizza squad 🍕', '41': 'film squad 🍿', '54': 'dragon squad 🐉️', '37': 'pie squad 🥧', '53': 'magic squad 🔮️', '43': 'cake squad 🍰', '42': 'love squad 💘', '49': 'strawberry squad 🍓', '55': 'royal squad 👑', '59': 'bomb squad 💣', '44': 'earth squad 🌎', '46': 'water squad 💧', '36': 'brain squad 🧠', '60': 'owl squad 🦉', '52': 'cosmic squad 🌌', '32': 'general', '50': 'apple squad 🍎', '47': 'lightning squad ⚡', '35': 'air squad 🌪️', '45': 'fire squad 🔥'}

    def refresh_seen():
        global seen_data
        with open('seen.json', 'r') as f:
            seen_data = json.loads(f.read())
    refresh_seen()
    def update_seen_json():
        global seen_data
        with open('seen.json', 'w') as f:
            json.dump(seen_data, f)

    def update_seen(name,id,username,room_id):
        time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        id = str(id)
        if id not in seen_data:
            seen_data[id] = {}
            seen_data[id]["channel_name"] = {}
        seen_data[id]["name"] = name
        seen_data[id]["username"] = username
        seen_data[id]["channel_name"][channel_dict[room_id]] = time_stamp
        update_seen_json()

    def connect(n):
        connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n +"\"}"}
        ws.send(json.dumps(connect_json))
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
                        update_seen(name,id,username,room_id)
        except Exception as e:
            print("Error in gc logging %s" % e)
            sleep(5)
            pass