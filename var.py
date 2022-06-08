"""All static and dynamic variables used in the program."""
import datetime
import re
import json
from datetime import datetime
from imgurpython import ImgurClient

from simple_image_download import simple_image_download as simp

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
SHORTEN_GREET_TOGGLE = False  # Handles enabling and disabling shortened greetings
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
    r"""((!u)|(blue (who'?’?s here\??)|(das crazy\??)|(who is all here)|(who all are t?here\??)|(blue where the hoes at\??)))(\\n)*\s*$""",
    re.I)
whos_idle = re.compile(
    r"""(!i)|(blue (who'?’?s idle|lurking)|(who is all idle|lurking)\??)(\\n)*\s*$""",
    re.I)
tldr = re.compile(
    r"""(blue (wfaf|tldr)|(where are we))|(what is wfaf)(\\n)*\s*$""", re.I)
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
    "dWVoUTRkYytLTkNyK2lXMlBiSnhTU2NMUk5QOUl5S1p3NzY2QjJDTEl5eDlFc3dyNWxyaG5uaGZTa2ZrRENiZTV4ZWVsam51K0Y1WGl1K1BVbWZkbVVVMFNicmF2N0J3ZzdFT2lKWWdjZ2liWktlV3RRcFlMQjVoYldDcm9QYUdPNUlxeHI0T1dEb0hEaVhhRzJzWnFDRE5LcXlQUHZvYUF0MlFXQnVOSG0zUDdFTFU4T1diMmExb2dDcUpxcTZmT25VQmdtL3RlNmlwa09aMUFLaUZPL3kzQkEwN004b3BFL2tmQ3BJeUVRcz0tLXpodkUzV3Z1UWdMdTNjYzQxdzJOV2c9PQ%3D%3D--74000c4cf0a353c18c0bddb68de1e7b30ba72f41",
    "SVZ0TEpzWWJMdlAzUVdMazVkQThDUWFyWWlNUm5ZaFV5WWF0bG5OT2JiY2tzK0FuMjlyMy9ENlRPdDVQSzlGMmh3VE1XU3gwMWhxbTFKOTRlb04xazNYaW15N2VndytERU9jSXFuR0p1VFRsTWUwTVVpOHhyNE5TKzhBUC9TV21MbHEvQXpZRkluaFRxeUx6azZlQytRYWkxVmdURHdLdkRyN2ZHbDlZczdqVkRHYTkwNk1lK2FDcForMGFxbGVuNSsvZGtqN0YwTUNDS0VvZ01hcERZMTNFSk4wVHNzWDlNK3BEZkJtaTBUOD0tLVlId0ptWER4K204a2dyZC8rOFh3L0E9PQ%3D%3D--6921f5f0c8ba1e70367488378e996fdc12645c2c",
    "eUVtdUtVdnIzcmIreFZuWHAyZmxoOFRSR1B2dUxjYklCSGZMbkE0RHhyd3VQU1UzQnJObmo3bE41RmRtZU5aUHpSQVR0MVpZTXVEcngrVXpxQ3ZhR2FxeUNLaEx0QSswSHp4VlJ5Rld2Y0RmbmxoVUU2aHRVMkFJQWpHeWlwN01UeW5ER1hOTXc1enM2RFMvUmZqNkhMR2U1QUtZVDFoeGI2MzQyNVg3MTdQNmx2RDk3bHRoWEpUQStuSnVhdVlZdkwwVW85ekZtR2Jhbkp3UmUyMTBWRWdyMEZ4OVZyWEVxZUtkY3RVbjdubz0tLXZ4clAzb2NndGNXaWR6eHNqWnBJd3c9PQ%3D%3D--b95f9cf81d9c3fc06a45bb17c812c707ecb14a21",
    "TUFSYVZrdTFmYnBveXlrU1RRSGlqMkwyQ0pQZkx3WFpGTFd4VHNTQ3Y3OTVLQlVJd293R1lCb0JucGFDaGdLYkR1MWtvdUM3ejA0dVZEenRScHNvS3ZOYmE5dVZPZTdoTVY2Kzlmc0xScTUrNXJ5SDJxOGlhME1Ja2pveUFETjR5QmF0MHpQVHppOURaNXZKcW80Ym1kaXRFd2xUb1ArcXR1UTdNMkd6QVFiMTYwNkkzelpBNE80UURINWN5MTEyOW4wUWRtZUVaZDVOZi95c01xb2hBOFVrZEhxZUhYNlJMNlc5anRZN240WT0tLUdjUWhrV0ViZmJUVGhsMkgwTFhLdHc9PQ%3D%3D--c8a58f7a5157b942697868d5551bea9faa5e85fd",
    "c3JqTlQ1c0hJaEFGcTcxSDhNYjFWY1grNEc0NndjdERhWHl6eEJCQTArc3NBZkV1UFg3UDB5dzNBaGZFSjNoTHpiQXlpQWF4dk1SZzZkUHZLajlFL3pqMTA2R0hPelk4OTR4dS9nU0RlZFRsRFBiai9ONUVQWEl6SUJ0SzV0dUtqYlBRTEpxa0t5Rk1jRENPSThSVVNhSjEwUlJYK1ZLd2RJVGkrb3Rob3pYT1dqY3hicHdHUXFrM1E1TVNhS0JNTWJOM3JaMnVadkVxRncxc1JWMGRqbHNaSDQwTDNaOHFkTElpeitSR3k3RT0tLWZkQjJyc3hsZEl6OWVGWURMRm13Ymc9PQ%3D%3D--254bcff4a97ef18d0d861ce55d00ea66fe401a64",
    "aENJdTNDNm9ETHVMVmdQaVNLWXQ4STA4LzNmeXU0aHJmV1ZSNTBDdGErQjFMUSsrME9VeEdyYm0wOU8xNE85MVhYdGx5RmdMUnpLRXNPZEJpNEdZMmRJU2NqMVBVdTBWNzJhY3hLbUZLWmFOVDlhb2dpRHlKS3JYaVkyRlg5TFF0N2tUOGtvS2lnWjZNTHpTa3hOS2VvaFRMK210U1Q4a1QwbHdQUzI3Y2JURW5zRy9NVkFOQmI1ZUcwYTVjU0VkVWpaT3FtSXFqbU1hMzZsa2J0SjRmdytWNXVySVk3MnpmUHNBak9sd1ByST0tLWEyT0VONzR2c01YUTRLMzFNTmNaM1E9PQ%3D%3D--7425c67f456dcd366ddd67ffe064b875d90873ab",
    "U0ZnWWNSVFg5aFlXQlA0TGlGd1NqbmR3R0tuaEw0Zyt0aEFiKzcwU253QVNkbWM5UlBCdU9tMy9kSW1ndzV2N0VWT1Z6Y3FXV1NaRkkzZk41dXhSLzRZUWttVitEVUdhNzVLNWMwWUtmQUlSSFd3azlreDhaQzhKSXNMM1dUQWFqdVpnMTRXWk5Tb0V0ak1ibnNWbUZUNnMyRWFPN0JJejNnRnNTOU9HdjBWQjJlTTlMV2NCREE1dzVFalR0VytRejQ3QkNKZHpPS2tSVGhWbUtJVlllYUdxS3JUMEdORFlSRks2T0sxL3A3bz0tLTkrSXdrWHZoYklyVm44QnNrU2FmeGc9PQ%3D%3D--f01c207da05527bb476262e87da02772c9c5b14f",
    "dXVFSEdMVCsxQWRRano2VjZSQ2QxblpYNHZ2NFlKclRvZ0g4cTlMRTZlMkRnRWZEVEdBMDk3bFhmRVNEbjF4dlhsaWRUWDNBM1dVOVFSTURkMmduSm94ZmhVM2Q2ZjUvWWpnd2pRM1VOdU1lTmJ6THU1eU90WXZqSzZRZ1ZoRkE1REk0WktiZ2gzL0VKUkJqWFo1blFXRmUzK0VLYVFEZEI3SFdLQ0RXemo4TVVrQm9xYktZZllmZHpZRFk4MmdPOWJ5a3A3NnBOZEVPU0VZbUNLQUZJZUNkOFdveTMzUFlianZuZm9qbks0TT0tLTRIMmNJL3pQcGl1ZGlYU1pJRXZ6U1E9PQ%3D%3D--638f1b2d9804b57ee0d7e4004b85a7f4adeb1ead",
    "WnA4VC9CQnhKVXNITWdURVp1UHovNEcxVS81WkdTZ3ZYK3lua09DbFVrNUJCcVVRbEFiMGh6UkVlcEFIMXkzOThZQTRXazdnSU4rWFNldzJadFhYdGJ6c1MwYk0xTkFMekgvVXBjTSs3L2d2SmRnRlVKTXlDeTRxTDR6MmdrUGRYUHFDejN0ZTFNcWhsVHhvRUNFaUtxN000czlyWTV6NXhHRG52NmhFb2xmQTBRRHNyV0NTWUtvc2tDR0Izc0J1OFdDZzJDdjJOWGtlKzIyVDBGK09TL2U1ZWtWc1pvcHo3T3dXWUp0bU5qST0tLXpCdlFRdkwzTkhFc05UY1VQUGVrRkE9PQ%3D%3D--c706cd3151dfc8afff284528ee7b9ae1935cb35c",
    "UE56TG5zWXVvSTZZS2FXMDZ6UHZ4ZFVNNFo5YWRvMWMzWXZ1MWFZSEJFS3RJOFg3c0pMaWN0ZGRFVnpya0pkTkhYbVE5ckRHYlpIN2ZUWG1ucG8rVnBNV1BrWkhhSHpSMGJPZ0JMbm51ZGVvUnQyOUk1UjNPeU9ROWZpTFRobGlFM0huWnhxT21acmxzNElJNmF5WFpZcUZ6dTFWdVJvY3BmMCs2UmU5aElOM24xV3ZpNk9KSjlHeEVvVXErTjRRQTYzZWtqQW1OTGRvYnE0MWtDRlZjUHNLOXQ0MitFemNNWi9NN2trcEdRdz0tLWtPTzF0TUJ4R3lzOHp5NDNGL0M1cXc9PQ%3D%3D--3adb0cff795e8b2f993c3f1be5877e212c9d4612",
    "c1Z1c21oRzhIano4K25Ma2ZET3d6Rk12TXVRcmNqNDFFbnV6N25FUkM4d0ljSm9QVVA4UllGbVpla05OT0tOaGN1WlhaNEhOSTgvZXROejBBNFd1bXo4V2p4QkQ2S0U5aE4wbGM4eGJZblNHSTBkcFRSLzRnblBVVzR5YVg2dll5dkJCcVk1VmJxWnJ1Zk4zYkl2R1k4Wis4OHpPa3dZNU5kbFp0OEpzU0NzTHRMOHFwQUJMZEtiMythM1I4c3M2dG9rc2FlU2VhQStkTklFOHBScEt6RndwWUhYQmUvMEF2U0JjdXNuWE9qST0tLXJaaEpZTFdtQTZQZWV6Ri9La1BxZ0E9PQ%3D%3D--37d7c45fc83c60f2779bdec98afecd460d460619",
    "NVZjYnN6Zm5UVUcyT0hmWWJKK2VvVUgxM3lGd3NMUlRGcE1lT1BNckV1WUZ6ZjJFSjF2d0pWZWNEZFRPQjBoeVJHVXA2RXRoRm1MYWNtWDFwbWFQNGR5NlMza2p1RmU3dXRzVllFdUUzdGNHdCs4MDBFdG50dktVY2RXcXpyR1hCMllUY01Mc2pHMFBYOTZPd2FYdWc3OTZFdHBXOHI3T1lmWlArWlZLQlI1bEUvY3pmZnZESS9hTFhEZktlUG8yQ2JhbUpZaXJwUFJDNGFBaS9ZU3YzVTJPaWh6WDB0RnVKK0lZTFg2cEhIST0tLWw0Zmxta2U4Qm9lOHh4TVc5MlBDRGc9PQ%3D%3D--b8175233ca1f3443b768d1cdfc94afd3359a48a3",
    "RjVFbVhTRFJmL2hGbG9RVzdHMUJlOHpuRFV2dEJzSEd5UTBmbTR0RU56bW5JRkhKZFNCODNBS1JJQ3p2dWM5eEdVcDRRRm1DNU8ydGNKRDJTUHVSaGl1OU5aM0xSc0pMYjdRUy9xZXlWRmQvQ2dzZmhFcFc4V3JCK0pFYi9scmRoUUFBOUl5TzY5UXdoM0dLYnIzSTFLK1lydnpiRlMvbUgrMUtoK2huWWo5OFkxaENRTWtTZlAxTTg2SjlVeU9acTJHR1ljZ0FXa3pUem80V3FUL1liVGdtM1czOXBxbzNqc0V5clVOMjR6bz0tLWFWaEltTHVUMVdjSktUZFIra2ppMEE9PQ%3D%3D--566efc0ed1a5503f6219fa16529ba4addc49b95e",
    "OER2UFpTWVQ4bVJNc1dHWWQ2Y2RUZ1VFZ2hxSTJCMUlyVDZ4TGt5Mml1a1E3aVdvVmJmaVQ0MUM5WG45UDhQY09uV0k1YXZKeENiUS9tSGNBTGd2MS96ZUQxR256WHkzSEZMMGtkSUpab0I2dTRvbWZWRGkyMkcrUjd2eDJyalNDYmJlR0lOYi9ZakFtS1FxSUozb200RG9hNWlKVTZTa0VRczhkRWJZVklYT3RnYkFsMFRkajNGczdhQ3l3bHJMWFNHdUxWdVc4N0xPMEYwL0xMeWRYTlFUQlZoZCtIMjUyMGl4eDFuNnIydz0tLXl4eFBkSlRhL0NtQ1crV2JDOW9uRkE9PQ%3D%3D--247e90c473a12124266c4da85787e6bc368bdeae",
    "U0t3aDRHTVplbGd4UC9kMVArUWJIdTF3Ykp2NlFvQnNTblpUd25QZExvWXQ0QWR3bVhpbXF2NERtK3lnSUlXZmZjT2JiUWJaRjJyMHBqTVlnQ21RUjV1Q3JTbGRUZmxYanYrRHdNa1JjOWJtWG1TV1RhNlJlWlBKV3l3aStQeVJBR1NSV0ZjWjJ0THR2L05GNjhPM1lYeGMwWEJzbU1TT21HM0dnSThYZm8zNkdSNndTWTFRckVJQU9ocFBVQkF0TkdQaytnR1ZydXFqMEhRQnROUjQvQ1M4UVg5ZjJ2L3NiVEdKbjB2TC9maz0tLVVaMUtlMG9nT3dIcVlRSEptdHRpTXc9PQ%3D%3D--e9d3b32697f8786d46dbdcabf110d6b950f39579",
    "YnoyUncyb3VYSWYwRkU1Q0JPUXNYa1B5RW0zbnhyU0x4N3VVcG9wdlQzWE04Q25xR1RyRFE4cDhoSGFQeDVPV242YlZPTEk0a2dRalBXQ2lEUDRmSm5FVjRYN3FaR05GeFNKYmFKY2dpREQrZnlaNEwvRVM2R0M0QTdIV3htdWhmRzhmUXJURmxkS3llNTg3QnpUMEpQb01rblBFck96K01HTFprZlV1Z0xwV3ZlVDdZMHZHSU5mRStSMXlROG9QaTF3RVVzSVpsS0xCb1MxUG5WWUZ4OVViVGEwTmdTRFRzMHR5NXZpcCtJST0tLXpBRC9XRWNObnZFdnBTdHl2U2VKWkE9PQ%3D%3D--ac9f75a5957d3d15cbd27d6b2a12cee687e55238"
    "U3BpTnFINXlURG1yekFvS3paMTBjOWxPQkEwVVV6N25mMHZINk5acDNRamFNRU0yLzY3b2w4R05qN3Iwa1dkeUxPdDZQU1lya3pCN2RNaEhlOGd3QmRvLytkdlVRYXFvb1J3T3RNVndNbnl5Y2w0TEE0MmoycnhsbUwyRjZrbmVvcUhsMll6VENsRTZMT3FqbGVaemJ5ZjdNWUFUL2c1aE9DdGE4NWhhV1ZReFFmN3dqNjNWTW1jUXdXamdadUpPYWxEcEhlSTZYZ1YrQ3dCMytEcUZtZE9NRHdvazZKTGpxaTdLUkNSUHhGTT0tLS82QWVBK2J4dGt4VktZd2E2TlZkR1E9PQ%3D%3D--6af4b89a45169abff3a04e7c1106b4966208a3d5",
    "c3BKL1ZyL1NlVWNWMUdLYXFKVVNVbG1laDlHeU8ybEpnSjVEK08wcEVJZ3ZXbGxxVDczbkZvWVcxWnlVRjR0eHRxd1oyRVd0Q2M3a2YvSjhiRnlFU3hxMTE3aTdrcmNrWGt4ZHl2RWVIb3JaMUZ4NndUVUJtL1ZhREc1WVdBSCsvSTZGR3lOYXh4YmxVMUFLYmppWEFScWp3R0pUYksyelVITHhNT0hVaG4yd2JsbVpNcDZJbVA3ZFJPY1RlSm9GbkM0TXdmWWkvWTBrckN2MXE5blFENHlpTnBFbUxqbGRqaUFkK2JRSXR4QT0tLW5qN2dyd0IxS0dua1dJS3JBWmRsWmc9PQ%3D%3D--3561e872213b8f17f5981fca0b53afee3f5af050",
    "MGdSQTZyM2trQmlCUXdvc2pkeFhzMGg5QTFGSlhjbVhaZU5GUWpLaVBGNHF5bTd5b1RQai80enk0eitvLzlZZ09najRBd1djQkFFb05vYTV5VWwxalpITk9SOHVod1NUWXZ3aVc4NEwwYkNwczJEMVBXSHUxNFIvL0tvb0ZjYmJiMi85cUNDVUx1SG9ibyswbXhCTGVLVzl1cUlTU08ydG9TSW80MVphR29rbXNwWlJPZkt3ZXF2amU5dTlQS0YyWVB4OWM1QXVIM0pzdlk2ZTZZdTkxMUoxZU9rOEMwNndlenRPYnlTMHpLdz0tLW4rTW5qN2wxYWtKTzVHeWphRVNBTmc9PQ%3D%3D--a01e4ff2cad68709b926499a85477e7901660ad1"

]

check1 = re.compile(
    r"""Welcome, [^""]+, to WFAF - Waiting For A Friend. This is a family-friendly group chat you get sent to when you try to message someone who youve sent a friend request to and they havent accepted your request."""
)
check2 = re.compile(
    r"""Hi, [^""]+, retrying wont help, you can try asking what is wfaf for more info :D"""
)
check3 = re.compile(
    r"""Hi again, [^\\]+, try asking what is wfaf for more info :D""")
check4 = re.compile(
    r"""Hello, [^""]+! Welcome to the place where your dreams used to come true!~"""
)
check5 = re.compile(
    r"""Hi, [^""]+! Im afraid they arent your friend yet, you can always try again!"""
)
check6 = re.compile(
    r"""Hi again, [^""]+, dont feel bad, theyll accept one day... hopefully!""")

greet_check = [check1, check2, check3, check4, check5, check6]

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
