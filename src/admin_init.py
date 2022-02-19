from src.admin import *
from var import *
from src.utils import restart_program

def admin_function_init(i, id , isadmin, result):
    global greet_status, running, name, starttime, aichatstate, greet_timeout, data
    if i == 0:
        greet_status = True 
        response = done
    elif i == 1:
        if greet_status is True:
            greet_status = False
            response = done
        else:
            response = already_not_greeting
    elif i == 2 and isadmin:
        response = leaving
        running = False
    elif i == 3 and isadmin: 
        response = clear_lists()
    elif i == 4:
        response = respond_uptime()
    elif i == 5:
        greet_timeout = {}
        response = done
    elif i == 6:
        response = send_stats()
    elif i == 7 and isadmin:
        response = fix_message(str(data["mutelist"]))
    elif i == 8 and isadmin:
        response = str(timeout_control)
    elif i == 9:
        response = restarting
        restart_program()
    elif i == 10 and isadmin:
        del timeout_control[id]
        if id in list_main_dict :
            del list_main_dict[id]
        if id in idle_main_dict:
            del idle_main_dict[id]
        response = aye_aye
    elif i == 11 and id not in data["mutelist"]:
        response = ily_r
    elif i == 12 or i == 13:
        response = mute_func(result,i)
    elif i == 14 and isadmin:
        id_ban = result.group(1)
        thread(id_ban)
        Thread(target = ban_log, args = (id_ban,id,)).start()
        response = banning_response % id_ban
    elif i == 15:
        response = fix_message(str(data["admin"]))
    elif i == 16:
        response = str(result.group(2))
    elif i == 17:
        response = stop_stalking(str(result.group(2)))
    elif i == 18:
        if not stalking_log:
            response =  stalking_no_one
        else:
            response = stalking_following % fix_message(str(stalking_log.keys()))
    elif i == 19:
        aichatstate = True
        response = done
    elif i == 20:
        aichatstate = False
        response = done
    elif i == 21 and id == "0":
        response = mod_demod(result)
    elif i == 22:
        refresh_data()
        response = done
    elif i == 23 :
        refresh_messages()
        response = done
    elif i == 24 and isadmin:
        response = set_greet(result)
    elif i == 25 and isadmin:
        response = get_greet(result)
    elif i == 26 and isadmin:
        response = remove_greet(result)
    elif i == 27 and isadmin:
        response = add_landmine(result)
    elif i == 28 and isadmin:
        response = remove_landmine(result)
    elif i == 29 and isadmin:
        response = get_landmine()
    elif i == 30 and (id == "0" or id == "16986137"):
        toggle_alt_universe()
        response = done
    elif i == 31 and isadmin:
        response = toggle_spam_check()
    elif i == 32 and isadmin:
        response = get_spam_check_status()
    elif i == 33 and isadmin:
        response = make_knight(result)
    elif i == 34 and isadmin:
        response = remove_knight(result)
    elif i == 35 and isadmin:
        response = toggle_shortened_greet()
    elif i == 36 and isadmin:
        response = save_nickname(result)
    if int(id) != 0:
        send_message(response)
    else: 
        if response:
            print("Admin Command: " + response)

def admin_func(message, id , isadmin):
    global greet_status, running, name, starttime, aichatstate,greet_timeout, data
    for i in range(len(admin_commands)):
        result = admin_commands[i].match(message)
        if result:
            admin_function_init(i, id, isadmin, result) 
