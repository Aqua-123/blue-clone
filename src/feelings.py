from blue import image_cache
from var import *
from data_handing import *
import requests

def image_upload(query,urly):
    global client
    found = False
    if query in image_cache:
        return image_cache[query][1]
    for i in image_cache:
        if image_cache[i][0] == urly:
            found = True
            print(image_cache[i][1])
            return image_cache[i][1]
            
    if found is False:
        image = client.upload_from_url(urly)
        link = image["link"].replace("https://","")
        formattedlink = "Image: " + link
        image_cache[query] = [urly,formattedlink]
        update_image_cache()
        refresh_image_cache()
        return formattedlink
    
def coin_handling(result):
    global data
    num = result.group(1)
    coin_add = int(num)
    if (coin_add <= 100) and (coin_add >= 1):
        data["coins"] = coin_add + data["coins"]
        update_data_json()
        if num == "1":
            return adding_one_coin % (coin_add + 0, data["coins"])
        else:
            return adding_coins % (coin_add + 0, data["coins"])
    elif coin_add > 100:
        return too_many_coins

def get_id(result):
    String = result.group(4) 
    id = return_id(String)
    if id is False:
        return not_seen % String
    else:
        if type(id) is not dict:
            return id_response % (String,id)
        else:
            if len(id) ==1:
                return id_response % (String,list(id.keys())[0])
            elif len(id) == 0:
                return not_seen % String
            else:
                return fix_message("I have seen the following users with the name %s :- %s. Specify the ID correspnding to their name"% (String, fix_message(str(id)).replace("{", "").replace("}", "")))
        
def get_details(result):
    id = int(result.group(2))
    r = requests.get(profile_url % id, cookies = cookies)
    if r.status_code == 200:
        r = json.loads(r.text)["user"]
        name = r["display_name"]
        karma = r["karma"]
        username = r["username"]
        gender = r["gender"]
        created = r["created_at"].split("T")
        if gender is None:
            response = details_response_null_gender%(id,name,username,created[0],created[1])
        else:
            response = details_response % (id, name, username, karma, gender, created[0], created[1])
    elif r.status_code == 404 or id is None:
        response = account_deleted
    elif r.status_code == 403:
        response = timeout_error
    return response