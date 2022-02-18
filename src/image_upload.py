from blue import image_cache, response 
from imgurpython.helpers.error import (ImgurClientError,
                                       ImgurClientRateLimitError)
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

def get_image_link(query):
    url =  response().urls(query, 6)
    try:
        return image_upload(query,url[-1])
    except ImgurClientError:
        send_message("Sorry I couldn't find %s" % query)
        pass
    except ImgurClientRateLimitError:
        send_message("Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying")
        pass

def send_pic(query):
    send_message(get_image_link(query))

def get_meme():
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    r = json.loads(r.text)
    link = r["url"]
    image = client.upload_from_url(link)
    link = image["link"].replace("https://","")
    formattedlink = "Image: " + link
    return formattedlink

def get_meme_link():
    try:
        send_message(get_meme())
    except ImgurClientError:
        send_message("Sorry I couldn't find a meme")
        pass
    except ImgurClientRateLimitError:
        send_message("Sorry the rate limit of 50 pics per hour has been exceeded, please wait for a couple of mins before retrying")
        pass
