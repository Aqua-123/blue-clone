from var import *
import requests
from ws import send_message
from time import sleep
import json
import random
from threading import Thread

def get_jokes():
    r = requests.get(jokes_url)
    if r.status_code == 200:
        joke = json.loads(r.text)["attachments"][0]["text"]
        return joke
    else:
        return "Error: " + str(r.status_code)

def get_quote(console):
    r = requests.get('https://api.quotable.io/random')
    content = str(r.json()['content'])
    author = "~ by " + str(r.json()['author'])
    if console is not True:
        send_message(content)
        sleep(0.2)
        send_message(author)
    else:
        print("Console:- %s"%content)
        sleep(0.2)
        print("Console:- %s"%author)

def singing():
    send_message("*Sings ~*")
    sleep(2)
    send_message("la la lalla ~*")


def check_singing():
    l = len(timeout_control)
    if l <= 4 and random.randint(0, 100000) % 93870 == 0:
        Thread(target=singing).start()
