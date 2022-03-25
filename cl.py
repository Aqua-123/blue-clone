import websocket
import json



def cl():
    def connect(n):
        connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n +"\"}"}
        ws.send(json.dumps(connect_json))
    def disconnect(n):
        connect_json= {"command":"unsubscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n +"\"}"}
        ws.send(json.dumps(connect_json))
    list_id =  ["48","56","33","39","38","40","34","51","58","57","41","54","37","53","43","42","49","55","59","44","46","36","60","52","32","50","47","35","45"]
    websocket.enableTrace(False)
    ws = websocket.WebSocket()
    ws.connect("wss://www.emeraldchat.com/cable", cookie="user_id=MjExNzQ2MDg%3D--a4763efe1b8631066fdee681d54eec7ba278ca9e",subprotocols=["actioncable-v1-json", "actioncable-unsupported"],origin="https://www.emeraldchat.com",header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}, timeout = 1000000  )
    print(ws.recv())
    for i in range (0,len(list_id)):
        n = list_id[i]
        connect(n)
    for i in range (0,len(list_id)):
        n = list_id[i]
        disconnect(n)

