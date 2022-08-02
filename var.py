"""All static and dynamic variables used in the program."""
import datetime
import re
import json
from datetime import datetime
from imgurpython import ImgurClient
import simp

with open("config.json", "r", encoding='utf-8') as f:
    config = json.loads(f.read())
with open('data.json', 'r', encoding='utf-8') as f:
    DATA = json.loads(f.read())
with open('messages.json', 'r', encoding='utf-8') as f:
    SAVED_MESSAGES = json.loads(f.read())
with open('image_cache.json', 'r', encoding='utf-8') as f:
    image_cache = json.loads(f.read())


main_cookie = config["main_cookie"]
client_id = config["imgur_client_id"]
client_secret = config["imgur_client_secret"]

response = simp.simple_image_download

CLIENT = ImgurClient(client_id, client_secret)
ID = 0

delay_handle = {}

# main connecting request json
connect_json = {
    "command": "subscribe",  # Main connecting request json
    "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}"
}
channel_dict = {
    '48': 'ice squad ❄️',
    '56': 'noodle squad 🍜 ',
    '33': 'roleplaying',
    '39': 'moon squad 🌑',
    '38': 'sun squad ☀️',
    '40': 'conspiracy squad 👽',
    '34': 'VIP ⭐',
    '51': 'banana squad 🍌',
    '58': 'sushi squad 🍣',
    '57': 'pizza squad 🍕',
    '41': 'film squad 🍿',
    '54': 'dragon squad 🐉️',
    '37': 'pie squad 🥧',
    '53': 'magic squad 🔮️',
    '43': 'cake squad 🍰',
    '42': 'love squad 💘',
    '49': 'strawberry squad 🍓',
    '55': 'royal squad 👑',
    '59': 'bomb squad 💣',
    '44': 'earth squad 🌎',
    '46': 'water squad 💧',
    '36': 'brain squad 🧠',
    '60': 'owl squad 🦉',
    '52': 'cosmic squad 🌌',
    '32': 'general',
    '50': 'apple squad 🍎',
    '47': 'lightning squad ⚡',
    '35': 'air squad 🌪️',
    '45': 'fire squad 🔥'
}

connect_json_blue = {
    "command": "subscribe",
    "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}"
}
threads = []  # List of threads
PLACEHOLDER_LIST = []
RUNNING = True  # Main while loop control variable
GREET_STATUS = True  # Handles enabling and disabling greetings
ALT_UNIVERSE_TOGGLE = False
SHORTEN_GREET_TOGGLE = True  # Handles enabling and disabling shortened greetings
guessing_game_status = True
chess_game_status = True
insult_control = True
forbiden_chars = [
    "\u202e",
]

bracs = [
    "{",  # Curly brackets to be removed
    "}"
]

MAIN_DICT = {}  # Main list dictionary
IDLE_DICT = {}  # Idle list dictionary
STATS_LIST = {}  # Unique number of people joined stats
stats = []  # Total people joined stats
GREET_TIMEOUT = {}  # Control number of greets and timeout
TIMEOUT_CONTROL = {}  # Control dict for list switch timeout
SPAM_TIMEOUT = {}  # Control dict for spam control
banned = set()  # banned list
STALKING_LOG = {}  # the name suggests
RESET_CLOCK = 0  # reset greet timeout
STARTTIME = datetime.now()  # Script start timestamp
t = datetime.now()  # Current date time
aichatstate = False
SPAM_CHECK_TOGGLE = True
cookies = {"_prototype_app_session": config["prototype_cookie"]}
IMAGE_CACHE = {}

# Response list for im bored phrase
im_bored_list = [
    "How about, dance :D",
    "Hmmm maybe sing a song?",
    "Study... maybe... instead of procrastinating heh",
    "Well.... have you been outside lately? How about go for a walk? (if its not an unreasonable time)",
    "Youtube dot com hehe, best place to cure boredom",
    "How about watching a movie? or binging a tv series? (dont ask for suggestions :> I just stare at binary numbers 24/7)",
    "Sleep",
    "You could go to 1v1 and find someone to talk to? (this is one of the worst advices ive given but yea its a viable option)",
    "Same :)",
    "Ahhhh who isnt",
    "Sameee ~high five~",
    "Ive heard star gazing is lovely, give that a try",
]

# All matching strings
hey1 = re.compile(r"""hi blue(\\n)*\s*""", re.I)
howdy = re.compile(r"""howdy Blue\??\s*""", re.I)
whos_here = re.compile(
    r"""((!u)|(blue (who'?’?s here\??)|(das crazy\??)|(who is (all )?here)|(who all are t?here\??)|(blue where the hoes at\??)))(\\n)*\s*$""",
    re.I)
whos_idle = re.compile(
    r"""(!i)|(blue (who'?’?s idle|lurking)|(who is all idle|lurking)\??)(\\n)*\s*$""",
    re.I)
tldr = re.compile(
    r"""(blue (wfaf|tldr)|(where are we))|(what is wfaf)|(what'?s wfaf)(\\n)*\s*""", re.I)
high_five = re.compile(r"""(blue )?(high five)(\\n)*\s*$""", re.I)
low_five = re.compile(r"""(blue )?(low five)(\\n)*\s*$""", re.I)
dab = re.compile(r"""blue dab(\\n)*\s*$""", re.I)
hate_myself1 = re.compile(
    r"""(blue )?(i hate myself)|(no one likes me)(\\n)*\s*$""", re.I)
thanks = re.compile(
    r"""((thanks|thx|thenks|thonks|thank you) blue)|(blue (thanks|thx|thenks|thonks|thank you))(\\n)*\s*""",
    re.I)
smile = re.compile(r""":>(\\n)*\s*""", re.I)
smile_rev = re.compile(r"""<:(\\n)*\s*$""", re.I)
kill = re.compile(r"""blue (kill|shoot|murder) me(\\n)*\s*$""", re.I)
pats = re.compile(r"""blue send pats(\\n)*\s*$""", re.I)
hugs2 = re.compile(r"""blue hug(\\n)*\s*$""", re.I)
party = re.compile(r"""blue (lets )?party(\\n)*\s*$""", re.I)
menu = re.compile(r"""blue menu(\\n)*\s*$""", re.I)
magic_menu = re.compile(r"""blue magic menu(\\n)*\s*$""", re.I)
heart = re.compile(r"""<3(\\n)*\s*""", re.I)
quote = re.compile(r"""blue (tell me a )?quote(\\n)*\s*$""", re.I)
uwu = re.compile(r"""(uwu\s*)|(blue cultural reset(\\n)*\s*$)""", re.I)
jok = re.compile(r"""blue (tell me a )?joke(\\n)*\s*$""", re.I)
no = re.compile(r"""blue (no|enforce)(\\n)*\s*$""", re.I)
eyes = re.compile(r"""o.(\u200b)?o(\\n)*\s*$""")
dni = re.compile(r"""blue (dni|do not interact)(\\n)*\s*$""", re.I)
bored = re.compile(r"""(blue )?im bored(\\n)*\s*$""", re.I)
dying = re.compile(r"""(blue )?im dying(\\n)*\s*$""", re.I)
enable_greets = re.compile(r"""blue (enable|disable) greets(\\n)*\s*$""", re.I)
disable_greets = re.compile(r"""blue disable greets(\\n)*\s*$""", re.I)
self_destruct = re.compile(
    r"""(blue self destruct)|(blue die)|(blue kys)(\\n)*\s*$""", re.I)
clear_userlist = re.compile(r"""blue clear userlist(\\n)*\s*$""", re.I)
uptime1 = re.compile(r"""(blue uptime)|(!uptime)(\\n)*\s*$""", re.I)
clear_memory = re.compile(r"""blue clear memory(\\n)*\s*$""", re.I)
stats1 = re.compile(r"""(blue (tell me the)? stats)(\\n)*\s*$""", re.I)
get_mute = re.compile(r"""(blue get|fetch mutelist)(\\n)*\s*$""", re.I)
get_timeout_control = re.compile(
    r"""blue (get|fetch) TIMEOUT_CONTROL(\\n)*\s*$""", re.I)
get_admin_list = re.compile(r"""blue (get|fetch) admin_list(\\n)*\s*$""", re.I)
restart_s = re.compile(r"""((blue|blew) restart|reset)(\\n)*\s*$""", re.I)
hideregex = re.compile(r"""blue help me hide(\\n)*\s*$""", re.I)
ily = re.compile(r"""blue i(ly)|( love you)(\\n)*\s*""", re.I)
love = re.compile(r"""blue gift love(\\n)*\s*$""", re.I)
dice = re.compile(r"""blue roll a dice(\\n)*\s*$""", re.I)
mutereg = re.compile(r"""(?:blue|eva) mute ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
unmutereg = re.compile(
    r"""(?:blue|eva) unmute ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
enableai = re.compile(r"""blue enable chat-ai(\\n)*\s*""", re.I)
disableai = re.compile(r"""blue disable chat-ai(\\n)*\s*""", re.I)
setgreet = re.compile(
    r"""blue set greet for ([0-9]+)\s*(:-)?\s*([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getgreet = re.compile(r"""blue get greet of ([0-9]+)(\\n)*\s*""", re.I)
removegreet = re.compile(r"""blue remove greet of ([0-9]+)(\\n)*\s*""", re.I)

stalk = re.compile(r"""(blue start stalking )([0-9]+)(\\n)*\s*""", re.I)
stop_stalk = re.compile(r"""(blue stop stalking )([0-9]+)(\\n)*\s*""", re.I)
get_stalk = re.compile(r"""blue get stalklist(\\n)*\s*""", re.I)
ban = re.compile(r"""blue ban ([0-9]+)(\\n)*\s*""", re.I)
refresh_data = re.compile(r"""blue reload data(\\n)*\s*""", re.I)
refresh_messages = re.compile(r"""blue reload message data(\\n)*\s*""", re.I)
seen_reg = re.compile(r"""blue seen ([^\\]+)(\\n)*\s*""", re.I)

addlandmine = re.compile(
    r"""blue add landmine ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
removelandmine = re.compile(
    r"""blue remove landmine ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getlandmine = re.compile(r"""blue get landmine list(\\n)*\s*""", re.I)

spamtoggle = re.compile(r"""blue spam toggle(\\n)*\s*""", re.I)
getspamstatus = re.compile(r"""blue spam status(\\n)*\s*""", re.I)
altuni = re.compile(r"""blue (alt|alternate) universe(\\n)*\s*""", re.I)

makeknight = re.compile(r"""blue make ([a-z0-9\W ]+|me) a knight(\\n)*\s*""",
                        re.I)
removeknight = re.compile(
    r"""blue remove ([a-z0-9\W ]+|me) from knighthood(\\n)*\s*""", re.I)
toggleshortgreet = re.compile(r"""blue toggle short greets(\\n)*\s*""", re.I)
toggle_insult = re.compile(r"""blue (enable|disable) insults(\\n)*\s*""", re.I)

savenickname = re.compile(
    r"""blue save nickname for ([^""]+) as ([a-z0-9\w ]+)(\\n)*\s*""", re.I)
ai = re.compile(r""">([a-z0-9\W ]+)(\\n)*\s*""", re.I)

consoleinput = re.compile(r""">([a-z0-9\W ]+)(\\n)*\s*""", re.I)
# Menu Items
coffee = re.compile(r"""blue serve (coffee|1|caffee)(\\n)*\s*$""", re.I)
milk = re.compile(r"""blue serve (milk|2)(\\n)*\s*$""", re.I)
water = re.compile(r"""blue serve (water|3)(\\n)*\s*$""", re.I)
cookiess = re.compile(
    r"""blue serve (cookies and milk|a|cookies n milk)(\\n)*\s*$""", re.I)
ppizza = re.compile(r"""blue serve (pineapple pizza|b)(\\n)*\s*$""", re.I)

# feelings regex
coins = re.compile(r"""blue add ([0-9]+)([a-z0-9\W ]*) coins(\\n)*\s*""", re.I)
hug = re.compile(r"""blue (send )?hug(s)? (to )?([a-z0-9\W ]+)(\\n)*\s*""",
                 re.I)
pat = re.compile(r"""blue send pats to ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
loves = re.compile(r"""blue send love to ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
bonk = re.compile(r"""blue bonk ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
get_id = re.compile(r"""(blue )(fetch|get)( id of )([^\\]+)(\\n)*\s*""", re.I)
get_karma = re.compile(r"""blue (fetch|get) details of ([0-9]+)(\\n)*\s*""",
                       re.I)
mod = re.compile(r"""blue (mod|demod) ([0-9]+)(\\n)*\s*""", re.I)

help = re.compile(r"""blue help(\\n)*\s*""", re.I)
help_greetings = re.compile(r"""blue help greetings(\\n)*\s*""", re.I)
help_general = re.compile(r"""blue help general responses(\\n)*\s*""", re.I)
help_sending = re.compile(
    r"""blue help sending (feelings|messages|feelings/messages)(\\n)*\s*""",
    re.I)
help_admin = re.compile(r"""blue help admin commands(\\n)*\s*""", re.I)
save_message = re.compile(
    r"""blue\s+(?:save|leave)\s+a?\s*message\s+for\s+([^""]+)\s*:-?\s*([a-z0-9\W ]+)(\\n)*\s*""", re.I)
serve = re.compile(r"""blue serve ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getmeme = re.compile(r"""blue meme(\\n)*\s*""", re.I)
guessing_game = re.compile(r"""blue start guessing game(\\n)*\s*""", re.I)
guessing = re.compile(r"""([0-9]+)(\\n)*\s*""", re.I)
chess_game = re.compile(r"""blue start chess game against ([0-9]+)(\\n)*\s*""",
                        re.I)
chess_reset = re.compile(r"""!chess reset(\\n)*\s*""", re.I)
chess_get_board = re.compile(r"""!chess get board(\\n)*\s*""", re.I)

list_all = re.compile(r"""!l(\\n)*\s*$""", re.I)
# insult
insult = re.compile(r"""blue insult ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
report_id_cp = re.compile(r"""blue report ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
save_message_r = "Okay message saved for user %s"
# Mene replies
coffee_r = "☕"
milk_r = "🥛"
water_r = "🥤"
cookies_r = "🍪 🥛 🍪"
pineapple_pizza_r = "🍍 + 🍕"

# Other replies
tldr_r = (
    "You're here because you tried to message someone who didn't accept your friend request."
    " We call this chat WFAF,"
    " Waiting For A Friend."
    " Let's keep it family-friendly!"
    " Enjoy your stay uwu")
high_five_r = "High five ~*"
dab_r = "ヽ( •_)ᕗ"
hate_myself_r = "I like you, have a cupcake 🧁 ^-^"
thanks_r = "You're welcome :D"
hi_r = "Hellosss :D"
smile_r = "<:"
kill_r = "Ahem 🔪 "
#kill_r = "Nu, smh"
pats_r = "._.)/(._."
hug_r = "(੭｡╹▿╹｡)੭"
party_r = "partyyy wohooo 🥳"
menu_r = "Rn we have 1) Coffee, 2) Milk, 3) Water"
magic_menu_r = "We have A) Cookies n Milk, B) Pineapple Pizza"
smile_rev_r = ":>"
heart_r = "<3"
dying_r = "Nothing new, now go work smh"
uwu_r = "UwU"
howdy_r = "hewwos"
no_r = ("Kindly be nice and keep this family-friendly while you are here, "
        "else the wfaf door is always open for you to leave, thanks")
eyes_r = "0.0"
dni_r = "We are not interested, thanks no thanks"
ily_r = "I love you even moreeee"
low_five_r = "Even lower five ~*"
love_r = ("Hey wonderful person, "
          "you are amazing and deserve everything you desire and love."
          " Hope the best for you."
          " You have all my love and wishes."
          " Much love ~ blue :>")
jok_r = "placeholder"

help_response = (
    "From the following modules pick one and say blue help (module name) \n"
    "1. General Responses\n"
    "2. Sending Feelings/Messages\n"
    "3. Admin Commands (admin only)\n")

help_greetings_response = "This modules greets people when they enter the chatroom, the greets for someone ae decided on the basis of the state of short-greet toggle and is any custom greet for the person is present ~*"
help_general_response = (
    "This modules contains general responses, such as :- ~*"
    "1. What is WFAF\\n"
    "2. Blue whos here/idle\\n"
    "3. Blue save message for name/id :- message\\n"
    "4. Blue help\n (Get back to the original help message)\\n"
    "The last one you can use to save a message for a person and it will be delivered to them when they enter wfaf next time ^-^ ~*"
)
help_sending_feelings = (
    "This modules contains commands to send feelings/messages to people, such as :- ~*"
    "1. Blue send love to name\n"
    "2. Blue send hugs to name/Blue hug name\n"
    "3. Blue send pats to name/Blue pat name\n"
    "4. Blue bonk name\n")
help_admin_commands = (
    "This modules contains commands to perform admin actions, such as :- ~*"
    "1) Blue stats (Gets stats of entries done while blue was online)\n"
    "2) Blue enable/disable greets\n"
    "3) Blue uptime\n"
    "4) Blue mute/unmute ID\n"
    "5) Blue toggle short greets\n")

# response and string match dictionary
response_dict = {
    tldr: tldr_r,
    high_five: high_five_r,
    dab: dab_r,
    hate_myself1: hate_myself_r,
    thanks: thanks_r,
    smile: smile_r,
    hey1: hi_r,
    kill: kill_r,
    pats: pats_r,
    hugs2: hug_r,
    party: party_r,
    smile_rev: smile_rev_r,
    heart: heart_r,
    uwu: uwu_r,
    howdy: howdy_r,
    no: no_r,
    dni: dni_r,
    dying: dying_r,
    love: love_r,
    low_five: low_five_r,
    jok: jok_r,
    quote: jok_r,
    eyes: eyes_r,
    save_message: save_message_r
}
"""help : help_response,
help_general : help_general_response,
help_sending : help_sending_feelings,
help_admin : help_admin_commands,
help_greetings : help_greetings_response"""

# List containing vars of admin command matches
admin_commands = [
    enable_greets,
    self_destruct,
    clear_userlist,
    uptime1,
    clear_memory,
    stats1,
    get_mute,
    get_timeout_control,
    restart_s,
    hideregex,
    ily,
    mutereg,
    unmutereg,
    ban,
    get_admin_list,
    stalk,
    stop_stalk,
    get_stalk,
    enableai,
    disableai,
    mod,
    refresh_data,
    refresh_messages,
    setgreet,
    getgreet,
    removegreet,
    addlandmine,
    removelandmine,
    getlandmine,
    altuni,
    spamtoggle,
    getspamstatus,
    makeknight,
    removeknight,
    toggleshortgreet,
    savenickname,
    toggle_insult,
    report_id_cp
    ]

# Menu list with images
dict_serve = {
    "coffee":
        "Image: [aW1hZ2UvOTc4NDI1NC9jb2ZmZWUuanBn]",
    "milk":
        "Image: [aW1hZ2UvOTc4NDI1Mi9taWxrLmpwZWc=]",
    "water":
        "Image: [aW1hZ2UvOTc4NDI1My93YXRlci5qcGc=]",
    "doritos":
        "Image: [aW1hZ2UvOTc4NDI2OC9pbWFnZXMuanBlZw==]",
    "pineapple pizza":
        "Image: [aW1hZ2UvOTc4NDI3Ni9pc3RvY2stNTM3NjQwNzEwLmpwZw==]"
}

coinsandfeelings = [
    coins, loves, pat, hug, bonk, get_id, get_karma, seen_reg, serve, getmeme,
    insult
]

cookiejar = [
"d3lkdFdVeERadDdhcVNNRWxSZTV6ZUV6ZEFJZVN6YUFObFRIWnQvRjNRRU1HRU1FbVBUY3k1cHF1UEN0cSsrTEwwNWYzOUcrRGhYazhrQmpSYXNoWUxZVGswcDh2Zys3M3A3Yy9jYW1ZL2svc3BMTGc1aUhmcEkvclFHR3FQTWc0bWw4eWJjWENsUzFPbFRycWlOVVZvWDRkc2JRaW81RmZkZTVqS2UxYjkxSVo2d1NiZFVNZ3FjREx0NEdZcVkwUVZOU0JYNFQ4WVNRaXNFbVdKWnIrQmI1bS9vR1g3NkxWQjJUS20xY01BND0tLTdhZDFNMTRNVWpLdFZodlN3M2hkUXc9PQ%3D%3D--6611abf3314e4cb3e1e989900524ee2b9d6f9484",
"NnpLckg5TXVkWDQ0YlRGejZPdGF4R2phRVBOVjR4SWUzVTBUcjFRQ29hNjFHNmJ0V1F2Q0ZBbW9pRzk2RWI2dkR5bTF5TWFyODVYNVluSzM4Ry9Tekx2THJORkJDRmFxUHVoWXhkY2hRckcydEdyMmtVNDkyeW9IMkU4MjlvNEYrcUlTYmtJaUczVnlIcUw3LzRGaXN2RWQ1dW9XZTVwZXA0MHgvSzdLMEEvb2tnelhaK3EzNHppUFMxME9lL3NVdEZIYTdsYmlzRFBkcFVBUiswbVo0YVplOTl5TCt2VU9JWFF4YXBwMUVpZz0tLXZCa2trTlBEWTAyNzgwSHRDZWRyZFE9PQ%3D%3D--d464042183c36076b49b58e1d4acf9103a7ab2ac",
"Q08renFIb0ZJaC96MTE2UmQ1Y3RrelQ4dmJzVG1ucEh6bWZjdVpYb283VCtUUmw1cllGR3ZrakNwaU5OditNWHZDZk5HL2NiUEJPMTQ5bk14UDRWNzVlR1N1cEhpUHdhbDUrZHYyTGlwUUFJQlNFaUJJTmcrSFMyM3VHWnFMUHAyWjBGbmhpbXBud2RZY3hjbkhIaG9FOXg4QU1oR0FlNVo2Z1ZOYzNQbllELzlWVGJBS3NibVRMUDB4cW9GaW9Wb2laa2RwdFYyRktWYnhJcFFTQW4wejRzdnNMY1p6Nm4xNWlhVlQvL2JSTT0tLTM0S1RkaFNoTnBDODNEckhUVnVhZHc9PQ%3D%3D--fb5d1343bdae07e60f56fdc6a3266cdcf5edd43e",
"QzBUbUlkU3Aya054WDdkcU1CeGFoYzVtOXlUZG1VNzJWeldseHhGbGU4eGxvUFZYT3JQMmtYVjIxTE1MZkZDUW9QOGlNbER5Nm5mcTlOTFAvT2xZcEJzaWU1RFNQT0F0K0tGVEgrQUJINnJDeVgzSmo4N1pIL0RUWUxFc0djeHBLS2VBS3p6SHNaVzA4dnRuK2ZHd25GbzVUWTl3bDlmajQ5di9lOUtwZmlDOWg5NnpPMUtPejNFVk5xMkxTcjR1MzhXb0c1VUlubzY1MFpUYllkakxMMFdPWlRLbGRKVGNHeGJtMlB0K3RkQT0tLWJsbE5OeTBLYXNaWHR4d1ArbkxLeUE9PQ%3D%3D--93d9158a2db3555ca260580d8e706baec68fb871",
"VFhjMHRFaW1XUmlLODVMY0VUTldOUWpZT2JEOVcvUTNwb2o5UGlSR1F5blBWclFaYUJqQ2N4eFIzbUpuZGtudm5PalJvYnFVa0RQa090bDFZTGN1ekJsVEI3Q2gzSEZtdUZUeWs2VDRpUzhjUW9KczBzVktURldOYXg1RlJJTnQ2bnVtTFJsUjh4cmh2TTJEOEFsL1RIMm1wcTV1OHphNytVKzZ0cTJoVnh5cXh0azRVWGxVL1BhVDJET2tQeG5wNG1wc25UQ2szc1c5ZC9WVi90UVFmQ21hSmtXV1A5T2RscHFlVWhTbURiZz0tLThWS1BtQThLKytUVXVQR042VUJSVVE9PQ%3D%3D--7352403adef43366d226528f7215797b88f75cae",
"V3pLL1RtM21aU3E0a0xLZGRRT3JETCs3eTBwVkRvUE5FVkFYR0hoZHVhN1dWSGRwZmlXYjZkK3VHcHg2Q1BqSGV1Qk1Cb2JxVFJpUGdlazJxVU8vMlhQTDFyNmtmNzVGRlNYd1NMT0xDWGN3RTdxTHJ5cEtTaTlwSXdqMGNmOTdZNXBOR1NLRS9NVXVnckh6aU5kYW9lNmwvcy9KdDdMWUNFM3dhZ29uT2kweUIxYXVPbjBjK0YrZ29HUVhGUmVFdHhlOWN3THdkVTFhUHJUZlhub0RqWWJCaTQxV0tiT0ZQWWwxbjRwc08zUT0tLVpNZUhMQTEvZzJMMEpWYlZuNlI4YkE9PQ%3D%3D--a8538a40f9d9f3280abdd888d15cbe34f9c9d972",
"SlRGdnlyWkZ1aWRzcThpeGJFRmVuTGNPR0NoYWNSZVpLb3llM1V0bCsrZVhzZ2RYTHpZczZIVlpIbmszRlRvOXZsUHNXNGQrUDZsZEtsV3lvZXJUNGhGazhJdDFxSm92cXViZDF3dlFRY2cvRkUyM3ZLRFRXTmY2cy9yOFd6ZXhHVTVObmRZRFRUNk9FcjQ4c2JjMEgyZCsxQUdmakhYVi9PZVNrUUdvZlVDR2VhcHdGVEFUekhzSStnSTFjK1d6ejlpQXZZVTkzUW9XMXhuRUkvSU9hcU9PZDBoa1FvK2MvWExKRlI4SVhCUT0tLWcwRS9GZHVvTTd5UFlBNUl2SGxFamc9PQ%3D%3D--2463ef7b670344a6bf1c4c47cd37bab93f3a5759",
"OXgyS1lDaUlJOTZkZnBtZGRJUWpDN1JuSEc5Ymt5ZG45SlcvR0pDSmpWNTlIb0hNU0VsdXZ6Y0ZySlBldGp2cXV5RnpOeWdOOUdNOHVmZ0V4THdIdnFJUmh3aHM2MXYwbTlLVVREYzJWWTU3a0lnUENkdm9nRW5ObmJONTdoaHFXc0o1WUdoQ2ZieFdWN2RVdHFSTVMxckJHMkdtdjd2Q2FBZ3d4QnlwQTVxdjI1RHZyOUloOTFuRlF4VVBvU1hud3NzR0ZTZ2M1S0p4NVQyMkpzNWFONWwxc0M0VkRSTTdyeWRHN1ByL1F6WT0tLVlaRndUSjBRSEsyVnd4YXhEaEgyaGc9PQ%3D%3D--e66bc33d3fb4e92a24767f1275f266104cd4c044",
"eGh3eU5PanRFTnpLQndsckpmQStWTW10cUhtN2k2RElGdWk0Y2tveENrS0ZLbGdHOGVtYTFGQ1UzRlAxUWUzWGhkL01JaUFyVXZSMEFxb0xLdmIxWm9uZlh6NXlxN2gxak1qUXFHVlNIcElWeEZpc1Z2SVBRRjFuMktQWDUzRm5wS0JSTWp6aWErM1Jva3pNUXZQM0JJbXZSM1Q2QWlxYnhITUg1bDdYSlFDN0FLNGxnL25BN2NNZWVObmM4ZWNnL2pqTUpSVjM1MWR2dVI0b2thcmxtcmtvYmRNM0NHd2dPNWFRd0dTSUllYz0tLUlGQXB3YmNzRXhsMDFTNGNuQzBQblE9PQ%3D%3D--b2b3aadd75b532a01493d31837b5bc70621ae5ad",
"Y1B3TmRndk1iK2N3N2pCTFFCU0R5dVM3MnZxYVFyZ1F1VzQzZjNaRHRlbjVwR0x0M3lPQkIzRFA4dG5maWJKZ0N2K043YndvRTczLzFscFZyeVlOTXVjbjJ0bS8vSnhEU21ZZE1EcTB5czZzVlA0WVVHMUhxWkh1VUpnZjVPSXZVdDFpcWxIbDIzblRleXJhYk5UMTl3Qm5KemN3RDBVeHIzdjNvT04rNi9YZ1BJUVdhSzBmcGZFV3hoZzREbUhvWmJwemRUMHdzUHNNRm5HdFRhYWk5eGU4eWl1MTVMekZXaWFpUEt3ZkFwND0tLTAxYUtOR29xbnRPMWhUS3FpQ1BDOFE9PQ%3D%3D--506bb9edaf0d66782694e21041a1dc8bea661d7f",
"bDJDN0c4U01uNVMwck1HNnNMKzJMcTVCdG1lV1Z2LzJxVjdxNDZQWWZGYTIwL2JZS3pubVFXWWViQjgvWEgwUWpldndDRldDK0w4YkQyUFE2UmpOUjZCMDJkQURaVXFtZk13clAwYnJQUXlWSXZFOWlvbHZpVzhpMFlPQytxckRZdCtHSmhEaVhGc2pLdXd2aWQwaTQyZUVoS1h5UWhkQUFuNkpyL0ZMUjMxUmJiZk96bjNKbm9zeDUwZXJtSlZnQXg3RWwyckZqWmpVQThpSzViZTBwUkJLc1NKYTFIaVZUVGpXRW1KU2xYZz0tLURaK2swODdLeWsyZUwrSTBGbGV3eUE9PQ%3D%3D--a7ac5e6d84b2ad64c87faec346724e080e49109e",
"Ti9TSzV3RmhEU0VkUjRyZmV2UG56RzNJcFFDRWkyNWtWaWFLeEF6b21JWldFM2NaNCtPSzhHRzdVY1c2VGZUUlViWkIyUnpNS2NVSElvMlRXcE56b2d5N0Z3eHEwMzRabTdNTmFlTDNpdXF3dHBWYzJsaGYxdzk1SEJHS1RpUUw4OGNoNGNUYm5Eb1drMk80dHRhVURWemMyTkZzMWlOVUs3KzhIK3Q2cDVZWVJ1VmRBYThENFYwQzBGWkpHRzdRaFI4TVMrZFJ1WGNZSW9OMHNlMXZORVNFVWozTmdsNTBiWldWVHB1ajdNZz0tLStCOWhVQ2VaT3pxWFQxY0FueFk2Q1E9PQ%3D%3D--12f7adb80ed911c349b131b932fffe267ccdbfe7",
"blc0OHRSMjVwb0xkdUNFZVZoemY4dlFmMFRjbVJUQTJhSlZhbnhUVWphWS96MjNndzFBY0Y3TU1hMnorYTMxSGlFSk02UjRlcjEyTURKQS9UU2loVS95TDd2Y0J3cGpBV2JlMFh3YUUvK0V1Y0RHZnZpVmNNSjQ5NjB6VU9pN1Q0QWsyLzF5Yjc4U1ZEc3VHcDhRcHNpa1IxRm9QaDNMck5QeEVTZ0F2M1lzR3U1K2FaQ0djekl5TzNqRnIyQjk5V1NlZ0FjT3l4cHo0VjU5cCtqUjRhZHhXQjJuS0hidkNMVkw2b0tscUM0bz0tLXY3KzFhYXF1MXVBeWwwN1VsZ2d2NUE9PQ%3D%3D--9f4df1b4510421e599c78d0c36871c2d2c7abf9f",
"UWNDMWIrYzFDSS9DUjV1RGhkSnBDRkhsaDRZTGo0V2pTb2lsVmtPdVNZVTdwVWlHMzQ1di9MQ1ZZTkNCQit5cWQxTUp3NnhmQTg4TUJvTUlTYlFjSU9MeUcrcFU0SXdacGtWb3ZKRTgyN2RJdXlyZjJ3dUZDN2xTRU9KNUpsR3RuZjlyT0hLTitoZVIycFZMekhFOUtBNmRaaGFpUFFDMDg3ZjUyM2pUOE5GL1RZU2hWRFVJUHdTWnQwVFdWM29DbzV0WVpId1A0RFhwWmwzYUpMMEJaTHd3L1AvOERwRlVGVE5VT005a0RhWT0tLXFMb3NxQTBEUmx4S1FnTnU3OGp6L1E9PQ%3D%3D--aac964503267acbb2a29492c6667874dba507752",
"ZW1NUllMRXp2M0Q0OUdQUTZOR1NKdUoxYjVmQnJ0SFpGcHN4RTVCMUtTUXVSdVFMc0h5OWI2VE1ORzM1clpqYkEzRzRVRkxjZEF4UFFYMjdnOXM1bzF0SGowVnAwNnlQbmdWamNsVHVZeHV0WitwOEtwYSsrdjZ6SnZ5RGVKUk5uL2ZwWitVNURVSFU1K3ZiT3lUcWxHT2o3ZmRzOUptTTlQUEJvUUZqelV6T0xjblNIZTlKdDQ3ZDc4Q1RSL2JzZW5vcldYWm5DNTJ2ZUxDR1BrOTIvc0lsODFScUlsRnNIN1dPUk1TcW1jaz0tLXNtRFVTb1EzSmVhMS9ZYVc2SVVVbXc9PQ%3D%3D--ae3f99e580c36b713e67c0d023215ed9dae4c148",
"SEU2NEFrQWQySzlHY1dzb2JZZUI4aXg1WU9ER08xZTlDNGxOY2cvdnFnMGNZQldwdm8wUm81RnhEVWxHUjR0cDg1L09xTVZnQ1hSQUVQVmZ4V0t0WVIvbHlIdnR1K0FRbE1LQytobVI1cnFRM1ZncFFVN3pWaFVKNm9zeXRnOE5rNnlNWjUzdEhMSjVMVnRZUmV5WGhVR2trQ3NTSG04OE1tcVNGaUFyaGtHaHRNN0tCTlljQVFaVEVWaXBlRnJtSmRYV0NDZ0V5QWhQUEFZVHE0SlpOUXZrVHNZTTN6T1ZyMWtUZU1zQTJGND0tLVJqSFNCUnRhWEFwUTA1anFkZmtxa0E9PQ%3D%3D--16fd8b8fffaad0c52c62ea2dfdcf2bec104cad82",
"ODVqczRjdDJOY054WGhJSHkrMm12cVFPcVpUc2FuSWh0YjNlWUp4K1M1NkM0ekxpREo2UHR5UmpueFFkYXBueGtiRHFXT1p4ak9xb1VnR1N2aDhoc2FYMUo3bTdnUGQvTkJQMG1NZWlpOGt1ODlkMkcrR2s1aGZsZEJuRURSdjd1bFVPSkhGdTh2M2IrNU9qUU1tTmc4QXhnM1Q5Q2RNRTltbGY0QTJ1cHJ3ZklxSjcwTEpzekRTcG5mWUZEUzYwU081TGkvQ05QQzFlSC8ya202c0pDQzhreThNb0FSRE9xakFvZ0I3U0IvST0tLVBzaGJmYlVlRjVPcUhCZUJWakpCVHc9PQ%3D%3D--ba300d6afa8e1ac581ab10ce817de82ef3ef1054",
"TTI5Zk5ESVNNLzlnbnU5TDFwOVh3eWE0a3VwSFVuSmNVUnBXTW9NNVJHZStQdXVUKzlyYitYajlxTGVDS0hWS0I1Y2syNEd3OFIvOWEzaHdPVUFQRm1jZEtZWVZFL1gwVWZDMEdBcXZ5RUhoejFYTlVlNUdtTy9MRVN2R0RHbURGbExDc0FDaktRQUNpRElrV0cxWXNXMmpNR0haWEI5OFRWZzBYNjRHRVo3Q1ZvbnFPOWpyZnZHaThNY3RiUGsvQVF2VW9tVkNWTjFMdXdBVDJweGZrb1ZFSUZVWWlQNVlNbGxmcnJhekNKYz0tLW51Ylp6MndRS0VyMCt2YlpkK0FRR2c9PQ%3D%3D--96cdf0ad430dc72d4af5a0bfb5937a81ab4de8cc",
"em5rSU1CMk5GVG5uK3BDNk1mdVlhZjc0b0k0N1dKM256cHMvSFVDeGo5Y2YzMWhTRThTWkVsaURkSitzaUtJdERER05EYm5VclYyengzYk9ZRno3Q3Z5TXlaYXViYmJEQ1J2OENqa01FWjNWNkVDRTVRR01QenJ2UHNaTjVjUFJlczBjb3VSTGpmM0QyZHp4MEVzcW9Kb3creVdEN0VZNE1kS3c0SWRxbnoyZGRsd2NSRGh3NUMvM3RPTnd1WnpuUWJwNWVmUGt2OHR2U29DWkRYNWdxaXVTOE44VURqSXRrSmI2OTU5NEZKUT0tLXJpdVdmQlp6WnhUeThVS3pFWExVYUE9PQ%3D%3D--e5bce628b85f002940dde766eb85b06020081766",
"MTU1NnFrTjZNU1NJMWhYSUVadHRBT3NSOGlWNll3RWplL3QxTVBxanRKNWxRZEhQcUZnZU5xS3RSWk90QVl2aEU1NElMVEFNUW1yVUJXNzB0Z0MvWUhJMHRpMG5JaWp2S0xqSzhUd3B0cWdLVXhXZzBhUitmSVVybmY5bExLemVOZTBmUGN0TUhkUTZVUEtUMFZLWW41ZnYwY3NmNGR2TWNaTEVvd1I0ZFJZTVI3alVxY0V1bVdwVFNVVkZSM1YrT3lvUnpoOFBRaXgrSjUySERpeHJudkY1SG40dmZLWmdNdXpiTm4xdHhkND0tLUNrendPVFNVR1JkaUwwNjBnYzdkVWc9PQ%3D%3D--a237b059c699d2a1b8ae17330851aacc18466788",
"ZVpMbWVMcDFNUFJiRU1SQWtCZUt1TTAyblBrQVFjdGtPK3ZIM2tJS3hzWElhYi9DUjVWL3hBVjVCeXF2TjFpOTZlTkRYMWZtZ1FrVHIxS3ZETzNkRTNYU2NKcFNWREJlNmx3cThuTGtOUGFNU1lpZXp2d3FFczJEL1V3aEdGMElSbkdLRUNEaWxXTjYxU1lHUGk0VlVPOFpkSElTdXgvV0xmUitNWVFJMXRNbzE5YVJoWjZ1WUFBZlJ1NUF6N2podHhwSUxmNlNkZUVXcTNITzhWY2Q5WnVsYkNySFIzTjBjWWxTVHJIOVpGYz0tLUh1bzQyQUtrOVI2ajZrNE9uZU83eVE9PQ%3D%3D--52d8eee722aa2e0745f7afce696532caeeeedad7",

]

check1 = re.compile(
    r"""Welcome, [^""]+, to WFAF - Waiting For A Friend\.  This is a family-friendly group chat you get sent to when you try to message someone who you've sent a friend request to and they haven't accepted your request\."""
)
check2 = re.compile(
    r"""Hi, [^""]+, retrying wont help, you can try asking what is wfaf for more info :D"""
)
check3 = re.compile(
    r"""Hi again, [^\\]+, try asking what is wfaf for more info :D""")
check4 = re.compile(
    r"""Hello, [^""]+! Welcome to WFAF! Welcome to the place where your dreams will come true~"""
)
check5 = re.compile(
    r"""Hi, [^""]+! I'm afraid they aren't your friend yet, you can always try again!"""
)
check6 = re.compile(
    r"""Hi again, [^""]+, dont feel bad, theyll accept one day\.\.\. hopefully!""")

check_pika = re.compile(
    r"""Welcome [^""]+ to WFAF - Waiting for a Friend\. \s*Say 'pika tldr' for more information!""")
greet_check = [check1, check2, check3, check4, check5, check6, check_pika]

# Some Strings

# Links
karma_url = "https://www.emeraldchat.com/karma_give?id=%s&polarity=-1=HTTP/2"
profile_url = "https://emeraldchat.com/profile_json?id=%d"
jokes_url = "https://icanhazdadjoke.com/slack"
insult_url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
ai_url = "https://api.udit.tk/api/chatbot?message=%s&gender=female&name=blue"

# ws-connection shit
ws_url = "wss://www.emeraldchat.com/cable"
origin = "https://www.emeraldchat.com"
subprots = ["actioncable-v1-json", "actioncable-unsupported"]

# Responses
start_ignoring = "Okai I'll ignore '%s' 0.0"
stop_ignoring = "Okai I'll stop ignoring '%s' :>"
already_ignoring = "I'm already ignoring '%s' o.o"
already_not_ignoring = "'%s' is already not in the mutelist o.o"
stopping_logging = "Stopping logging for account id %d because the account has been deleted and doesnt exist anymore"
logging_text = "Logging at (%s) %s %d %s %s\n"
done = "Okay done ^-^"
already_not_greeting = "I'm already not greeting o.o"
leaving = "Cya :>"
clear_list = "List went -poof-"

just_joined = "I just joined -w-"
here_for_one_min = "I've been here for just a minute"
here_for_x_mins = "I've been here for only %s minutes"
here_for_an_hour = "I've been here for an hour"
here_for_hours_and_mins = "I've been here for %s hours"
memory_loss = "Just had some memory loss x-x"
restarting = "Okai, restarting...."
aye_aye = "Ahem, aye aye"
banning_response = "Banning %s"

waking_stalking = "Okai waking stalk function"
already_stalking = "I'm already stalking ID %s"
already_not_stalking = "I'm already not stalking the person with ID %s"
give_valid_id = "Please give a valid ID UnU"
stopping_stalking = "Alright ill stop stalking %s UnU"
stalking_no_one = "I'm currently stalking no one :>"
stalking_following = "Currently stalking the following IDs:- %s"

adding_one_coin = "%d coin added to the fortune well, there are now %d coins in the well, wishing good luck to all :D"
adding_coins = "%d coins added to the fortune well, there are now %d coins in the well, wishing good luck to all :D"
too_many_coins = "Woops too many coins, maybe buy me some chocolates instead? :>"

sending_love = "Sending lotsa love and hugs to %s ❤️❤️"
sending_pats = "Sending pats to %s *pat pat*"
sending_hugs = "Sending hugs to %s (੭｡╹▿╹｡)੭ *intense telekinetic noises*"
sending_bonks = "*bonks %s with a baseball bat~*"

message_log_text = "%s (%s) :- %s"

blue_greet = "Our favorite Blue greeter is here!"
blue_greet2 = "Welcome, Blue!"
disabling_greet = "Disabling greets uwu"
re_enabling_greet = "Re-enabling greets :D"

details_response = "The account with ID %d has the name %s (#%s) with karma %d and gender set to %s and was created on %s at %s"
details_response_null_gender = "The account with ID %d has the name %s (#%s) with karma %d and was created on %s at %s"
account_deleted = "It appears the following account has either been deleted or doesnt exist, sowwy ;-;"
timeout_error = "Timeout error, kindly wait for about 15-20 seconds and try again"
not_seen = "Im sorry I havent seen anyone with the name %s here"

stats_response = "%d people have entered WFAF and %d unique peple have joined in the past %s hours and %s minutes, and it is %s in WFAF "

dice_statement = "Your number is....%d"

unknown_error = "Unknown error occurred, restarting... ~*"

chatlog_file = "chatlogs.txt"

Greet_1 = "Hi, %s, retrying won't help, you can try asking 'what is wfaf' for more info :D"
Greet_2 = "Hi again, %s, try asking 'what is wfaf' for more info :D "
Greet_general = "Hi, %s, welcome to Waiting For A Friend. You're here because you tried texting someone who's not your friend yet, enjoy your stay :D"

whos_here_response_no_lurkers = "I can see %s and no lurkers at the moment ~*"
whos_here_response_gen1 = "I can see %s and 1 person lurking ~*"
whos_here_response_gen2 = "I can see %s and %d peeps lurking ~*"

whos_lurking_none = "I can see no lurkers as of now"
whos_lurking_gen = "I can see %s lurking"
id_response = "ID of %s is %s"

already_mod = "Id %s is already a moderator"
mod_response = "Id %s is now a moderator"

demod_response = "Id %s is no longer a moderator"
not_mod = "Id %s is not a moderator"

greet_set = "Greet of %s set to %s"
greet_updated = "Greet of %s updated to %s"
greet_response = "Greet of %s is %s"
greet_not_set = "Greet of %s is not set"
greet_removed = "Greet of %s removed"

landmine_added = "Landmine added for word %s"
landmine_removed = "Landmine removed for word %s"
landmine_already_added = "Landmine already exists for word %s"
landmine_not_present = "Landmine not present for word %s"

spam_check_on = "Spam check is now on"
spam_check_off = "Spam check is now off"
repeated_message_warning = "%s has sent a message that is the same as the last few sent by %s, this is a warning"

knight_added = "%s is now a knight ~*"
knight_already_added = "%s is already a knight ~*"
knight_removed = "%s is no longer a knight ~*"
knight_not_added = "%s is already not a knight ~*"

shortened_greet_on = "Short greets are now on"
shortened_greet_off = "Short greets are turned off now"

Greet_1_short = "Hi again, %s, say 'what is wfaf' for more info ~*"
Greet_2_short = "Hello, %s, try asking 'what is wfaf' for more info ~*"
Greet_general_short = "Hi, %s, welcome to WFAF ~*"

nickname_added = "Nickname %s added for %s"
nickname_updated = "Nickname %s updated for %s"
