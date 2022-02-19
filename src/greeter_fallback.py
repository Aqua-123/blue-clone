from src.ws import send_message
from var import *

def dis_en_greets(id):
    global greet_status
    if id == "16008266" and greet_status == True:
        send_message(disabling_greet)
        greet_status = False
    elif id == "20909261" and greet_status == False:
        send_message(re_enabling_greet)
        greet_status = True

def check_greeters(message, id):
    global greet_status,data
    found = False
    if id in data["greeter_fallback"]:
        for reg_m in greet_check:
            result = reg_m.search(message)
            if message in data["custom_greet"].values() or result or message == blue_greet:
                dis_en_greets(id)
                found = True
                break
        if found is False:
            for reg_m in data["custom_greet"].values():
                reg = re.compile(r"" + reg_m + r"", re.I)
                result = reg.search(message)
                if result:
                    dis_en_greets(id)
                    break