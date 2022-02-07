from var import *
import websocket
import json
from utils import *

def connect():
    global ws
    websocket.enableTrace(False)
    ws = websocket.WebSocket()
    ws.connect(ws_url, cookie=main_cookie, subprotocols=subprots, origin=origin)
    ws.send(json.dumps(connect_json))
    ws.send(json.dumps(connect_json_blue))

def send_message(content):
    message = {
        "command": "message",
        "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
        "data": "{\"message\":\"" + fix_message(content) + "\",\"id\":null,\"action\":\"speak\"}"}
    message_alt = {"command":"message","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}","data":"{\"message\":\""+fix_message(content) + "\",\"id\":\"blueyblue\",\"action\":\"speak\"}"}
    if alt_unverse_toggle is True:
        ws.send(json.dumps(message_alt))
    else:
        ws.send(json.dumps(message))
