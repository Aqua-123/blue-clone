
from var import *
from blue import seen_data, data
from data_handing import refresh_seen
from time import strftime, gmtime
from utils import fix_message, fix_name

def send_seen(id):
    refresh_seen()
    r = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    name = seen_data[id]["name"]
    username = seen_data[id]["username"]
    if "WFAF" in seen_data[id]["channel_name"]:
        lastseen_list = {}
        for key in seen_data[id]["channel_name"]:
            date = seen_data[id]["channel_name"][key]
            lastseen_list[date] = key
        date = max(lastseen_list)
        channel_name = lastseen_list[date]
        if channel_name == "WFAF":
            date = seen_data[id]["channel_name"]["WFAF"].split(" ")[0]
            month = date.split("-")[1]
            day = date.split("-")[2]
            deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
            if deltatime.days == 0:
                if deltatime.seconds//3600 == 0:
                    if deltatime.seconds//60%60 == 0:
                        response = "%s (#%s) was last seen today just now in WFAF" % (name, username)
                    else:
                        response = "%s (#%s) was last seen today %s mins ago in WFAF" % (name, username, deltatime.seconds//60%60)
                else:
                    response = "%s (#%s) was last seen today %s hours and %s mins ago in WFAF" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60)
            elif deltatime.seconds//3600 == 1: 
                response = "%s (#%s) was last seen yesterday %s hours and %s mins ago in WFAF" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60)
            else:
                if deltatime.seconds//3600 == 0:
                    response = "%s (#%s) was last seen on %s %s %s mins ago in WFAF" % (name, username, day, month, deltatime.seconds//60%60)
                else:
                    response = "%s ($%s) was last seen on %s %s %s hours and %s mins ago in WFAF" % (name, username, day, month, deltatime.seconds//3600, deltatime.seconds//60%60)
        else:
            date_wfaf = seen_data[id]["channel_name"]["WFAF"].split(" ")[0]
            month_wfaf = date_wfaf.split("-")[1]
            day_wfaf = date_wfaf.split("-")[2]
            date_channel = seen_data[id]["channel_name"][channel_name].split(" ")[0]
            month_channel = date_channel.split("-")[1]
            day_channel = date_channel.split("-")[2]
            deltatime_wfaf = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"]["WFAF"], "%Y-%m-%d %H:%M:%S")
            deltatime_channel = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(seen_data[id]["channel_name"][channel_name], "%Y-%m-%d %H:%M:%S")
            if deltatime_wfaf.days == 0:
                if deltatime_wfaf.seconds//3600 == 0:
                    if deltatime_wfaf.seconds//60%60 == 0:
                        response_wfaf = "%s (#%s) was last seen today just now in WFAF" % (name, username)
                    else:
                        response_wfaf = "%s (#%s) was last seen today %s mins ago in WFAF" % (name, username, deltatime_wfaf.seconds//60%60)
                else:
                    response_wfaf = "%s (#%s) was last seen today %s hours and %s mins ago in WFAF" % (name, username, deltatime_wfaf.seconds//3600, deltatime_wfaf.seconds//60%60)
            elif deltatime_wfaf.seconds//3600 == 1:
                response_wfaf = "%s (#%s) was last seen yesterday %s hours and %s mins ago in WFAF" % (name, username, deltatime_wfaf.seconds//3600, deltatime_wfaf.seconds//60%60)
            else:
                if deltatime_wfaf.seconds//3600 == 0:
                    response_wfaf = "%s (#%s) was last seen on %s %s %s mins ago in WFAF" % (name, username, day_wfaf, month_wfaf, deltatime_wfaf.seconds//60%60)
                else:
                    response_wfaf = "%s ($%s) was last seen on %s %s %s hours and %s mins ago in WFAF" % (name, username, day_wfaf, month_wfaf, deltatime_wfaf.seconds//3600, deltatime_wfaf.seconds//60%60)

            if deltatime_channel.days == 0:
                if deltatime_channel.seconds//3600 == 0:
                    if deltatime_channel.seconds//60%60 == 0:
                        response_channel = " but was more recently seen today just now in %s" % (channel_name)
                    else:
                        response_channel = " but was more recently seen today %s mins ago in %s" % (deltatime_channel.seconds//60%60, channel_name)
                else:
                    response_channel = " but was more recently seen today %s hours and %s mins ago in %s" % (deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            elif deltatime_channel.seconds//3600 == 1:
                response_channel = " but was more recently seen yesterday %s hours and %s mins ago in %s" % (deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            else:
                if deltatime_channel.seconds//3600 == 0:
                    response_channel = " but was more recently seen on %s %s %s mins ago in %s" % (day_channel, month_channel, deltatime_channel.seconds//60%60, channel_name)
                else:
                    response_channel = " but was more recently seen on %s %s %s hours and %s mins ago in %s" % (day_channel, month_channel, deltatime_channel.seconds//3600, deltatime_channel.seconds//60%60, channel_name)
            response = response_wfaf + response_channel

    else:
        lastseen_list = {}
        for key in seen_data[id]["channel_name"]:
            date = seen_data[id]["channel_name"][key]
            lastseen_list[date] = key
        date = max(lastseen_list)
        month = date.split("-")[1]
        day =  date.split("-")[2]
        channel = lastseen_list[date]
        time = seen_data[id]["channel_name"][channel].split(" ")[1]
        deltatime = datetime.strptime(r, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        if deltatime.days == 0:
            if deltatime.seconds//3600 == 0:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen today %s mins ago in %s" % (name, username, deltatime.seconds//60%60, channel)
            else:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen today %s hours and %s mins ago in %s" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60, channel)
        elif deltatime.seconds//3600 == 1:
            response = "I dont remember seeing %s (#%s) in WFAF but they were last seen yesterday %s hours and %s mins ago in %s" % (name, username, deltatime.seconds//3600, deltatime.seconds//60%60, channel)
        else:
            if deltatime.seconds//3600 == 0:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen on %s %s %s mins ago in %s" % (name, username, day, month, deltatime.seconds//60%60, channel)
            else:
                response = "I dont remember seeing %s (#%s) in WFAF but they were last seen on %s %s %s hours and %s mins ago in %s" % (name, username, day, month, deltatime.seconds//3600, deltatime.seconds//60%60, channel)
    return fix_message(response)

def get_seen(result):
    refresh_seen()
    string = result.group(1)
    if string.isnumeric():
        id = string
        print(id)
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
            regex1 = re.compile(r'%s' % fix_name(string), re.IGNORECASE)    
            if regex1.search(name) or regex1.search(username):
                possibles[id] = name
            else: n += 1
        for id in data["nickname"]:
            for nickname in data["nickname"][id]:
                regex2 = re.compile(string, re.IGNORECASE)
                n+=1
                if regex2.search(nickname):
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
