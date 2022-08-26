"""All static and dynamic variables used in the program."""
import datetime
import re
import json
from datetime import datetime
from imgurpython import ImgurClient
import simp

with open("config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.loads(f.read())
with open("messages.json", "r", encoding="utf-8") as f:
    SAVED_MESSAGES = json.loads(f.read())
with open("image_cache.json", "r", encoding="utf-8") as f:
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
    "identifier": '{"channel":"RoomChannel","room_id":null}',
}
channel_dict = {
    "48": "ice squad ❄️",
    "56": "noodle squad 🍜 ",
    "33": "roleplaying",
    "39": "moon squad 🌑",
    "38": "sun squad ☀️",
    "40": "conspiracy squad 👽",
    "34": "VIP ⭐",
    "51": "banana squad 🍌",
    "58": "sushi squad 🍣",
    "57": "pizza squad 🍕",
    "41": "film squad 🍿",
    "54": "dragon squad 🐉️",
    "37": "pie squad 🥧",
    "53": "magic squad 🔮️",
    "43": "cake squad 🍰",
    "42": "love squad 💘",
    "49": "strawberry squad 🍓",
    "55": "royal squad 👑",
    "59": "bomb squad 💣",
    "44": "earth squad 🌎",
    "46": "water squad 💧",
    "36": "brain squad 🧠",
    "60": "owl squad 🦉",
    "52": "cosmic squad 🌌",
    "32": "general",
    "50": "apple squad 🍎",
    "47": "lightning squad ⚡",
    "35": "air squad 🌪️",
    "45": "fire squad 🔥",
}

connect_json_blue = {
    "command": "subscribe",
    "identifier": '{"channel":"RoomChannel","room_id":"blueyblue"}',
}
threads = []  # List of threads
PLACEHOLDER_LIST = []
RUNNING = True  # Main while loop control variable
GREET_STATUS = True  # Handles enabling and disabling greetings
ALT_UNIVERSE_TOGGLE = False
SHORTEN_GREET_TOGGLE = True  # Handles enabling and disabling shortened greetings
guessing_game_status = True
insult_control = True
forbiden_chars = [
    "\u202e",
]

bracs = ["{", "}"]  # Curly brackets to be removed

MAIN_DICT = {}  # Main list dictionary
IDLE_DICT = {}  # Idle list dictionary
STATS_LIST = {}  # Unique number of people joined stats
stats = []  # Total people joined stats
GREET_TIMEOUT = {}  # Control number of greets and timeout
TIMEOUT_CONTROL = {}  # Control dict for list switch timeout
SPAM_TIMEOUT = {}  # Control dict for spam control
banned = set()  # banned list
STALKING_LOG = {}  # the name suggests
spam_control = {}  # spam control dict
RESET_CLOCK = 0  # reset greet timeout
STARTTIME = datetime.now()  # Script start timestamp
t = datetime.now()  # Current date time
SPAM_CHECK_TOGGLE = True
cookies = {
    "_prototype_app_session": config["prototype_cookie"],
    "user_id": "MjUxNjA2MjI=--290f5f3744c733739a2559c2ea238947d672bbc7",
    "cf_clearance": "X1BTFa1LSoIoira.B9EVDY0uTrFCb2.uiCxqi4WIehA-1659206546-0-150",
}
data_csrf = {
    "X-CSRF-Token": "DBAsvol5Bjx3UK0HZskTpsmUGD8BHu8bqVw18yRGZYtVyuc35EfHy60F3s+JrBz9CHCMvBhcxRuczs2ptFS9cA=="
}
head = {
    "Host": "emeraldchat.com",
    "Referer": "https://emeraldchat.com/app",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
}
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
    re.I,
)
whos_idle = re.compile(
    r"""(!i)|(blue (who'?’?s idle|lurking)|(who is all idle|lurking)\??)(\\n)*\s*$""",
    re.I,
)
tldr = re.compile(
    r"""(blue (wfaf|tldr)|(where are we))|(what is wfaf)|(what'?s wfaf)(\\n)*\s*""",
    re.I,
)
high_five = re.compile(r"""(blue )?(high five)(\\n)*\s*$""", re.I)
low_five = re.compile(r"""(blue )?(low five)(\\n)*\s*$""", re.I)
dab = re.compile(r"""blue dab(\\n)*\s*$""", re.I)
hate_myself1 = re.compile(
    r"""(blue )?(i hate myself)|(no one likes me)(\\n)*\s*$""", re.I
)
thanks = re.compile(
    r"""((thanks|thx|thenks|thonks|thank you) blue)|(blue (thanks|thx|thenks|thonks|thank you))(\\n)*\s*""",
    re.I,
)
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
    r"""(blue self destruct)|(blue die)|(blue kys)(\\n)*\s*$""", re.I
)
clear_userlist = re.compile(r"""blue clear userlist(\\n)*\s*$""", re.I)
uptime1 = re.compile(r"""(blue uptime)|(!uptime)(\\n)*\s*$""", re.I)
clear_memory = re.compile(r"""blue clear memory(\\n)*\s*$""", re.I)
stats1 = re.compile(r"""(blue (tell me the)?\s*stats)(\\n)*\s*$""", re.I)
get_mute = re.compile(r"""(blue (get|fetch) mutelist)(\\n)*\s*$""", re.I)
get_timeout_control = re.compile(
    r"""blue (get|fetch) TIMEOUT_CONTROL(\\n)*\s*$""", re.I
)
get_admin_list = re.compile(r"""blue (get|fetch)\s*admin_list(\\n)*\s*$""", re.I)
restart_s = re.compile(r"""((blue|blew) restart|reset)(\\n)*\s*$""", re.I)
hideregex = re.compile(r"""blue help me hide(\\n)*\s*$""", re.I)
ily = re.compile(r"""blue i(ly)|( love you)(\\n)*\s*""", re.I)
love = re.compile(r"""blue gift love(\\n)*\s*$""", re.I)
dice = re.compile(r"""blue roll a dice(\\n)*\s*$""", re.I)
mutereg = re.compile(r"""(?:blue|eva) (?:mute|ignore) ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
unmutereg = re.compile(r"""(?:blue|eva) unmute ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
enableai = re.compile(r"""blue enable chat-ai(\\n)*\s*""", re.I)
disableai = re.compile(r"""blue disable chat-ai(\\n)*\s*""", re.I)
setgreet = re.compile(
    r"""blue set greet for ([0-9]+)\s*(:-)?\s*([a-z0-9\W ]+)(\\n)*\s*""", re.I
)
getgreet = re.compile(r"""blue get greet of ([0-9]+)(\\n)*\s*""", re.I)
removegreet = re.compile(r"""blue remove greet of ([0-9]+)(\\n)*\s*""", re.I)

stalk = re.compile(r"""(blue start stalking )([0-9]+)(\\n)*\s*""", re.I)
stop_stalk = re.compile(r"""(blue stop stalking )([0-9]+)(\\n)*\s*""", re.I)
get_stalk = re.compile(r"""blue get stalklist(\\n)*\s*""", re.I)
ban = re.compile(r"""blue ban ([0-9]+)(\\n)*\s*""", re.I)
refresh_data = re.compile(r"""blue reload data(\\n)*\s*""", re.I)
refresh_messages = re.compile(r"""blue reload message data(\\n)*\s*""", re.I)
seen_reg = re.compile(r"""blue seen ([^\\]+)(\\n)*\s*""", re.I)

addlandmine = re.compile(r"""blue add landmine ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
removelandmine = re.compile(r"""blue remove landmine ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getlandmine = re.compile(r"""blue get landmine list(\\n)*\s*""", re.I)

spamtoggle = re.compile(r"""blue spam toggle(\\n)*\s*""", re.I)
getspamstatus = re.compile(r"""blue spam status(\\n)*\s*""", re.I)
altuni = re.compile(r"""blue (alt|alternate) universe(\\n)*\s*""", re.I)

makeknight = re.compile(r"""blue make ([a-z0-9\W ]+|me) a knight(\\n)*\s*""", re.I)
removeknight = re.compile(
    r"""blue remove ([a-z0-9\W ]+|me) from knighthood(\\n)*\s*""", re.I
)
toggleshortgreet = re.compile(r"""blue toggle short greets(\\n)*\s*""", re.I)
toggle_insult = re.compile(r"""blue (enable|disable) insults(\\n)*\s*""", re.I)

savenickname = re.compile(
    r"""blue save nickname for ([^""]+) as ([a-z0-9\w ]+)(\\n)*\s*""", re.I
)
ai = re.compile(r""">([a-z0-9\W ]+)(\\n)*\s*""", re.I)
sort_admins = re.compile(r"""blue sort adminlist(\\n)*\s*""", re.I)
sort_mutes = re.compile(r"""blue sort mutelist(\\n)*\s*""", re.I)
consoleinput = re.compile(r""">([a-z0-9\W ]+)(\\n)*\s*""", re.I)
# Menu Items
coffee = re.compile(r"""blue serve (coffee|1|caffee)(\\n)*\s*$""", re.I)
milk = re.compile(r"""blue serve (milk|2)(\\n)*\s*$""", re.I)
water = re.compile(r"""blue serve (water|3)(\\n)*\s*$""", re.I)
cookiess = re.compile(
    r"""blue serve (cookies and milk|a|cookies n milk)(\\n)*\s*$""", re.I
)
ppizza = re.compile(r"""blue serve (pineapple pizza|b)(\\n)*\s*$""", re.I)

# feelings regex
coins = re.compile(r"""blue add ([0-9]+)([a-z0-9\W ]*) coins(\\n)*\s*""", re.I)
hug = re.compile(r"""blue (send )?hug(s)? (to )?([a-z0-9\W ]+)(\\n)*\s*""", re.I)
pat = re.compile(r"""blue send pats to ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
loves = re.compile(r"""blue send love to ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
bonk = re.compile(r"""blue bonk ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
get_id = re.compile(r"""(blue )(fetch|get)( id of )([^\\]+)(\\n)*\s*""", re.I)
get_karma = re.compile(r"""blue (fetch|get) details of ([0-9]+)(\\n)*\s*""", re.I)
get_my_details = re.compile(
    r"""blue ((?:(?:fetch|get) my details)|(?:who am i))(\\n)*\s*""", re.I
)
mod = re.compile(r"""blue (mod|demod) ([0-9]+)(\\n)*\s*""", re.I)

help = re.compile(r"""blue help(\\n)*\s*""", re.I)
help_greetings = re.compile(r"""blue help greetings(\\n)*\s*""", re.I)
help_general = re.compile(r"""blue help general responses(\\n)*\s*""", re.I)
help_sending = re.compile(
    r"""blue help sending (feelings|messages|feelings/messages)(\\n)*\s*""", re.I
)
help_admin = re.compile(r"""blue help admin commands(\\n)*\s*""", re.I)
save_message = re.compile(
    r"""blue\s+(?:save|leave)\s+a?\s*message\s+for\s+([^""]+)\s*:-?\s*([a-z0-9\W ]+)(\\n)*\s*""",
    re.I,
)
serve = re.compile(r"""blue serve ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getmeme = re.compile(r"""blue meme(\\n)*\s*""", re.I)
guessing_game = re.compile(r"""blue start guessing game(\\n)*\s*""", re.I)
guessing = re.compile(r"""([0-9]+)(\\n)*\s*""", re.I)
chess_game = re.compile(r"""blue start chess game against ([0-9]+)(\\n)*\s*""", re.I)
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
    " Enjoy your stay uwu"
)
high_five_r = "High five ~*"
dab_r = "ヽ( •_)ᕗ"
hate_myself_r = "I like you, have a cupcake 🧁 ^-^"
thanks_r = "You're welcome :D"
hi_r = "Hellosss :D"
smile_r = "<:"
kill_r = "Ahem 🔪 "
# kill_r = "Nu, smh"
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
no_r = (
    "Kindly be nice and keep this family-friendly while you are here, "
    "else the wfaf door is always open for you to leave, thanks"
)
eyes_r = "0.0"
dni_r = "We are not interested, thanks no thanks"
ily_r = "I love you even moreeee"
low_five_r = "Even lower five ~*"
love_r = (
    "Hey wonderful person, "
    "you are amazing and deserve everything you desire and love."
    " Hope the best for you."
    " You have all my love and wishes."
    " Much love ~ blue :>"
)
jok_r = "placeholder"

help_response = (
    "From the following modules pick one and say blue help (module name) \n"
    "1. General Responses\n"
    "2. Sending Feelings/Messages\n"
    "3. Admin Commands (admin only)\n"
)

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
    "4. Blue bonk name\n"
)
help_admin_commands = (
    "This modules contains commands to perform admin actions, such as :- ~*"
    "1) Blue stats (Gets stats of entries done while blue was online)\n"
    "2) Blue enable/disable greets\n"
    "3) Blue uptime\n"
    "4) Blue mute/unmute ID\n"
    "5) Blue toggle short greets\n"
)

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
    save_message: save_message_r,
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
    report_id_cp,
    sort_admins,
    sort_mutes,
]

# Menu list with images
dict_serve = {
    "coffee": "Image: [aW1hZ2UvOTc4NDI1NC9jb2ZmZWUuanBn]",
    "milk": "Image: [aW1hZ2UvOTc4NDI1Mi9taWxrLmpwZWc=]",
    "water": "Image: [aW1hZ2UvOTc4NDI1My93YXRlci5qcGc=]",
    "doritos": "Image: [aW1hZ2UvOTc4NDI2OC9pbWFnZXMuanBlZw==]",
    "pineapple pizza": "Image: [aW1hZ2UvOTc4NDI3Ni9pc3RvY2stNTM3NjQwNzEwLmpwZw==]",
}

coinsandfeelings = [
    coins,
    loves,
    pat,
    hug,
    bonk,
    get_id,
    get_karma,
    seen_reg,
    serve,
    getmeme,
    insult,
    get_my_details,
]

cookiejar = [
    "WXVqK0QwaGRoTUo2SVVhQVVQbks1ZjdMM3VPUHNNc29QajMvR3YzWUdJbWJnd3ZRL09tY3hPUUk2OS9BSzhiOERNQ1NKUE82RlhFQmhmQzZIeXd1aytORVFLRHN2QUF6aElwMHJuTzg2eGdoWUw4TGgyWHBySTBKQ1FLZDFrTnJiSVdXS04va0Njbk50SDI5V1dUNENMY2UwV3JleWFQN3BxcnJmeGJZWFl0WUZEWEYraHl2bElZNE9uVkdBUjQrYStzcmIvTkpHYVBMWFNZV3lycHVqNjVBazNkd2M3bkhoR3g0ektwOFppND0tLVpsaVJOb0Rla0lXWC92TWFoTkx5dHc9PQ%3D%3D--ff82ed7572c2af28228f2b877a3c41af5fe9f1d5",
    "L2pOejdob1pTY1dpVlUrd0ZBbWoxNm1QblM0QkpMVUZUanAyMGJKeG9iZWFndERBc0tOazVBb2ppVlBZUXdGVnJLUkhVUkg1OVAyL1JHUmRQcG1hUm1XUUMwK3FOQkJOdmdZVWZXL1ZCNTR5MmQ1VW1zR1Z0cnJIemxFdmJsL2o4S2p5MTNVNm1uRTBQOVBsbHdoOWozbTlYZ2lnSHN1VW5PdkFRamJZNlNpazlwWFdwODN3NWgyNHZOY3JNcjQxUWsvdDZIc2tHUUlzVTRaYTdQdUt0VE13UG9OK1NUMHJSYVh2WHZNU2RVbz0tLXQ3b2xsMVhJd3ExWXFHeHhqOGY5TVE9PQ%3D%3D--d036638dfce5bb97ab3ce527c190414b4caed6ef",
    "bWtrRkloMVg3Y0lQMzQ1TnUzQTg2cjd2V1hxYTgzUHVBZEE4R0ZTdXJZazROM2tnS21LSHp6OHRFU21FQ25kTmRheS9tKzRrMmltNCtLTWJaWHJOenhmdUsxS3ZvdHhnVTl1N2VnL3RBeHA4dmFYVnhTVVNEMUh4dUc3RHc4YTJ6OEFOdUc3Y3grWWtia0k4dFdCbThYSDh5cklkanJLSWE0OWhKbktSQXM4YlRDS08wazZSZnFJUkVaYTN6RmtjejAvbjRPVUtFREh1VTZ5bnRXWFNZb2RJbzA5YWg2R2Z6WWdMbWNGVEViST0tLXlKemN2MnBJdmtSTk4xMnBUNUxnUlE9PQ%3D%3D--2061bce6ca506d9350841399700bb15b6abcb86b",
    "UHh5YXlndlZMRG9YMEt4OXZPVGErOUlSQWlETHBaM2hGMVhQL05vZEtMOEx0UGpCb3E0NTBtNm8vYlZ4NWd3NWk1NUtxNnQ1RUd4Zk1RWDZVTGhJNkduS0lFbFFVSEtheHV3U1UvTG92NG9kQmU4S09Iak5ZMGprSndFMVp2Q1FNaTFhN0htVFo2eEQ3dHJPUE5JWDR2bWR0aTl0UEdScTZEWlZpNlp3dWQzTHBRcmtkbWtyUFUrVVpRZjROb05sSW9pTnQ0UlFTbCtSdDNWeXoxUGE3QW9DanVFd25HaWpVTnhkRnZ1aktnST0tLTZqelV3VHVvY0ZLaXd2VVR0QmNjZkE9PQ%3D%3D--b615e0763b18c28b5645c8067fcd8bfa7259cb7f",
    "VzFTRXlDMnpzTnFobUlXOTN3WW91R3JPU21uMkZ5eVNWR0xvNVFjN3hWWmdObmRuTmpTWnNlWC9wN3o4eXg4QVZnRnhvQVhRV21uZVk0LzlSQU9mNHNoUHhDYWlPTWFLZUJPL0pRdThDUmtUbDA2SkRlc3FJaUtRby9rRUUrZlZpM1JzVFcxNnpwcXJ3TDMrN0dFQitaLzBqM253NlNNQWxpdWJGbmhyZnBmUHBHWUNXbndaRkd5QlI2NExmRG9pRzZ0RDRRWXRiUjI3cnNxV1ZnTTFUVGJVRW9DRy9Lc0xDMWtXdTFkbE44az0tLUp6YjBPenVBOVlXQTBhKy9wNDRzbkE9PQ%3D%3D--5a0099b4a7fb1a642de71c14a806509eec0d9c3e",
    "OGdOQTRYTndBZmhuakt6MGh3cDB6VDhVODFXTldENmZUSXRrb0JOOXhXUXRjT3ppZmpOV1kvRVpkMlFtV1pYMmZkK3hwYkd0aHJIM2wzMzJOYk02WmFuUmZDZXlBaDZjZHJqdlZSb0R3U3JkdzhzVGR6TW1LckhmSmZReGovcWZOaDhjUTUvZlpSVW1YaDE4akpYVXY0L01DUHZMQkp2c1Bsc0tzZEJ3bmQ4Y2crMHh0WW56OXEwZ3QyRUpRTHFCc21jZTdJWDJETlliRzhBZVdRT2Q5dC9kT1ZWQ1k5NCszZXd2UjNWME5wbz0tLXNkQ1JlZ1pNNFYzamJyQ0Z3VVB2Vnc9PQ%3D%3D--b9064fb035076217c9a108061fb281cf0d977173",
    "K1BRSldnajR5VW1WVFJaRktLY0ZIWHhJVVBTek05c3lwdnFWNkdRaUc4ZVVuNnlVSlp4bDl1b1NwcyswMVVHQ0RqK0M1ZzN2WWlaSTBRdkEzNGtURTBxbnRIVzkxcGpqSVVuRC9TNktBbnl0Zm5nQktHTWFIeG8xUGlvZXlxcTdWM0NjcThJNnFySjhsNUxaR0diY0ptd3JUY1NpV0U0N2FqTitUNDRrWER2bGZ4VGpNSWdrMTVmeEozbktNejFTK3J5YndOVnI0WHBqTzI5amJqUWlyM2RHWjR4S3luTzc2TmgxZC9YMXIwND0tLWJNcHA2bWo3TUE3b3gxYVV3cE9EaFE9PQ%3D%3D--f9c2af6809d7800e3248d510a407291da5b5b0ca",
    "R2t4L1FuMFRnejdMNkFHZ1lmQlFZOWxvblZvUFljTllwMjZ3Vy9SbEdmZmRZNFRBa0JRbU1CVWNxR3hBbmxEYkh1czBxRWc1dlAzQUR2SFpiUDdvM0RFMUd1SjJ0NHVkSTk5RUcwTFhJU2trb2ZxMzI1RTdEV2JoSGxOdE04VTZmQ0xVVlhXK0FPZEtXaHAvcUhsVy9WMHZOWVhlZGs3QWZIWUZRUkptRGo2dDI3Y2lBSS83OUFOa1hxdE54MlROQUZSeHhpbmh4YjVQMVd0N1FTeTRuV1ZCeTAydnBTclRQcDIzdEhVTG5ZZz0tLWlHaGVIZ2w5RDJMU0ZmMFdSY2FxT0E9PQ%3D%3D--dba536fe6e3ed05cd64580a47e6c3a3ccfc2f116",
    "bXdYWXkxcVNqaW13b1JodkJnRk0rbUU2S3F5NXRyL0pDNTE3NjVHeENSL1B1djJ0bTR5RkZCWlR2am11ZmJPTnZvSEVNUHpYWG54bUVWKzdSSU85eDY3UGRsZWlkSk5iVWFHRzJZY2hqYnFUYmdmSHdvUUMrSlBPcDJpekcwVSt6cDVxc2d6ZFo3Q1BPZFgvWW90allmdDYxdWdRN3BXOEl3dHhqQlRodkJhMkpPa2ZLdjJYTW9uMnpNR1VtV2YvdWNKNnIrK2NVUG01TnpkREE2bVhnOXhUQVNwUVdxTW0zRGcvREU2RDRMVT0tLTZ2Ui9xVUI4c3RpVUpVK2xEdjdja2c9PQ%3D%3D--7e55ce4d3f0a7447e68b45d8383c1fa6650c4aa7",
    "a2hYY1NsT2UxQ0dDZ0k0d2RuQkgwMzJ6Y0l6Vk16eVJ3MSsyNG9RQm01Q2UrS0VXbnN5ai9KWGpua2dOMSs1RFpsMU1TRlcwT3ozNGs4VlRJclZWSnhsQ0hzbVVRNVlRc2J6ZUNZbXVvTk0wZUdBWEtpQzJkMFpSeWUzMXRJVjFWaHI1ZWpQd3ZPd3hLK2xNZVNpNE95c254SXJtUjc4dDR4NHhscmpoQmdKSTljM3l5MEpNVHArbUszMTZ5VFZmYnh0T1R2SzJVL2hvOXhyOEV3cVBuVk9CaUFUSjZ5dDBTajlsRTJjWVY4TT0tLXhQNTd1UU40RUxrRjlVcytFdnBwcHc9PQ%3D%3D--5997c7e45f9d9d9bfdcfe868ebac36fe2e47b349",
    "YloxdGZVMTFyZkFzc1hFMWk2bTFIbHo3RmU2Z0NiMko2RzVtcXpEdEw0ckJ3ZThydlY4Zm54dWxoWVhnSGpXTUFNaGpBejg0Z3lmUC8rUlFBcXVibFVVWStvUm5FZUlYaGxxcGxZODB0UTEwblFSbllLWTVDNmdvOUlabFNvV1EyOGcwU2t5QStsMEJZRjNoSjdCQzV1ajNGenRZZm9yeGtWTytXNmRsR2xWL3dmaGRDQlhCMzF4Zit3ekE4SUowcW8vNGE1QzZQWE5scXhBYm9hMFN5RGppOHdTR2VsMnpPeDRmVXVMYlV6Zz0tLTNHYzdUVTEyTTBhMDZVUUZ6Ri9xcFE9PQ%3D%3D--7f9664d621c4f3a02f8a5f104bb4e017af5f95e5",
    "eUFoYzFhd3hKaHQxSjg3bFdrRVJYR05tVVc1aUQyS0xtaGpWeDdWcysxSURQQ043em4zV1ZuSnBOY2F4RGRDSDdqMGl2TVZFOW9uRTNMN1FLcTRSSGdLSzZKZlNlNUVyL1pCK3BGWDJuS3RXZ0VUMWkyU0NOSTZPeUNocVMzOUFpSnJ5OGk2eXk5QXY5QVZMbkIvTFg3MTRTNzJrZGJIYmxuNElOWjhrSDgrUFRXdGdRemtKL1FheGtXYkl1QlBvUXVrSzRONmEreDl3V2xYYnJ5aG12bVR3R0FZUUkwdER3citVUnhrUGVOWT0tLVBuTEl3bFgrUzU4ekYxM3JyRVJXWnc9PQ%3D%3D--64fbc8eefa7c7a741719946f1a868f9a961046b4",
    "d293S2hRZEhKSmM2Y0xiNFJhQUthWFMzZ20xditRUzNZM1NVU3FERVpQWnRkOWNoT0U5K0lZeEE4Q1ZWOW1hUDFqK2NyTXFMejJKMVR2cWxOZndlMklDUGFsZmhtNUxVK0hwbElUL3FCb084RzZLMnF0ak01NythemZoaGdBQkJ6b0d5c1FqWVVMOUYrOTRTcnNrVEVwZU1WUWRSdUFpaFl3NUErZVZTTFhKako4dFNwd05LdHE4QVFSdmswZ3kvUlpqUUVJNXpPODc3SmY3bVpJVW9BYndscXZtN2RRSEdveXpudHpaQ1M1UT0tLXRxOUpYKzEzTk1uV2dTaFFLK1Y1Nnc9PQ%3D%3D--d7e48e40138d714159e2022638fb5ae6303d6303",
    "ZkNjMzRSY3BuV3loK0x0QStzYWpWK1NvZXpTbTZtODRPM1pkbkhLMnNBT290dnRrZ3IvanRteFZCSWUrSFEycVRLYXcySkxpcis5RWdxbFRjVkhINHdTNzFsc3NRbWZhUWo3K0FXZ0Q5ODNTV3o4cVdDWnlFeWU1UWxpbzlvbEgyYnFmVmRMelIwbk1Zc0RwMXdrM0lEUkZFdWVET0pMT1JDMGZvZDhMV1BDa203clFIRlJyVHRLZ2s2NTl4b3o2TFBCVnpXUkhaWlVtYmRpNC9XaHVTZUhaQnpSZ0ZiZ1RuRlpSZURZSkNYND0tLWZuLzRvdjBrdWp1RmxmRDhnY0hLVHc9PQ%3D%3D--f43eb1fa4ce055ea697369cce80ce24ee7996fef",
    "d1p1bjNqV0JEZHBFZVJnN21VTnV0eTZUbWlwZFU5Q0tjZWFBdlE4Nllpa3FvL3Yyd1VIZUFTRDQvcUhZaU1vemp2SHVubzRRSkU1Q1Q3T1ZkRU94S2V2MFd0Nk1KQmZNNUQxMFlhSmNheWU1Ky8xdUVXM0ZYYnd3VHh0OTlRVk1DRkptMThiTDRjRzZMWFcxU25DL3VyRnA0eHcvTGFJYTFFMTRQRFZFWG9DTnlFQUtWMG10U0V2bFRYVWlZQUM2Z1ppSXFDdHcxVmtMbVkxQnc4RG11MFFuSGlURmVhMW41TTBIaDlTdnpqST0tLTlOWUR4K1RnK2hid2RxOG1LSnZYa2c9PQ%3D%3D--193889aeb7fb1226ccceec762093bef871c20e13",
    "QmEwemZmdXQ5ZlEyaVNkWUQyckZ2SHVYZFBtR3NnMlB2MXZtU0FNdFVLcVFQTlNnRjZuQmJaVGpsOVkzWXJKVXpKNDVKTzhGWGlHaDJueEJaVXNpUlo4SjRSd1BCenJobVVJR1kyb2lkcWVaR0VnbXRRL0x4aW9lbXhyc1lwLzIzMnZCNk9ialhkQ1pqUXBkSTduL1ZNZDE4Z0hCT2NCVmhFU0VhRGdDUFBMUXdvM2p2ai9sVFBTNHhXLzBHOEljaFNySjY2SCs5RytRWnNwd05vS0gzaXdDejg3aUV4bnZlMjZYOTR4dEFIOD0tLVhYVVhobVk0OW1jNURBaVZzeWZtN1E9PQ%3D%3D--f280ba8a558b2b01c8184df7c5bfa97273b59b6d",
    "elJyUkdNNVY1MllTaEtJSlIwVzloTXY1emZRZE9WUU5FdzZCV095Rm9jdXVRZ29rUnVnTXNhWXRXWkNVb20wVXF4akwrZkIyY281SThRU09zbnRmeVF6R2tSYnNlUEU0cWhLaFBrVllOclpKVXlxMUQwNXNrQlc3dTdYcHVNV1lUakJUcTVkS2tFZDJZSWw3WFQ3VGlDZjZCMGxkRWhXV3FUQTQ4RGZ0cWh0eHpYclFNaG5HUWt0QS9pU0ZOU1QyWnBmYkRJK2t3UytwdS8vdUZmdHRELzJvS1RkeVdsc0lZSWQ4TnpJRXhIbz0tLXJja3RHRXNsQWxpNGtTK2w0Ni91MXc9PQ%3D%3D--fa90df9be699a0874c02665771a1a3e14d6cf7a7",
    "M0FPdUVuY3JMWU5RaWVhTTNkMmkyWjRUTVkzaXNKempjTENNSFE1SnlqQ1AvWVNkQ1o5TnRPNFNrYWNtRGNQcGRRRFdVbUJoWGphd01UREwzcVNCR1JzK2U1M25EWTRSMTJubU9ZUllWSm4xUWRPejluQUo3VU9mVm95YjBsc0NuVWdKaG5VNWZXL3JiaWwwVTFnd1ZoZTNtMFB5UzZFdkRSWlRsLysxQi9QZkNXMWFva20wUklyd25tQzdhVFpxZXpCUi9hK3QyT2w4Mi9XOHBMSVl1cnJjbU5jejhrYlRsdWQxTVY4dHptTT0tLWdVYzZVeCtsbGd3dS84QjVrMHFvU3c9PQ%3D%3D--8390466c10f7e6783e739c89784222cda9900481",
    "U0VTUEJYakZ6NXRzeU1ETWV5ajBSQmFxZG1LcWFHcGdXelJtWVZRZlFnS3dBNDlpTkhDM2hNK0NER0E4Wk9BYmEvRStTVHI2U3pSRWY0MkNHVU5nV0xjRUVMenh4T1JXU1FWN2loZk4rZ2JIVk9HOVFINXNuQjYzVEVOWXFWZm5EUGE4S0YyeGJUa29kM2dmMzhWZU9pblliODNIQjI3c2E5R1pCWW1mUUptaDR4SUhoZTQzUEVwYjR6OExGanR5eE1RVnp0NlU4TlFFelltaTg3bWZvK1lydjJkazV5VWR5TFZmYW1jbHlPbz0tLXN4UkVZZjhwVm1kUEZwMVlRbnBDNlE9PQ%3D%3D--30501955e855debe5d397a15cd514f606dd7a4b1",
    "a01sVkxzUlh0RFJ4UTVoNHZlTEJIbEpHNTBFU2srUTkrL2tkVjh6NDlBVHIzMHRzTmhJVDNZVXh6NWhBK2FiWDZyaTd6ZGFUbUR6OTJyM2JpRnVseUlMSFUxOVhNczF3TzZSMGdrMDI5d0FUQ1dVOTE3L0xUSTN2cm40TFlsbHhWSjY0SURQTjhMYUo5MnJjRWFQV3NRWkFvQ3l1V3ZXVHpqUUVCMUJkMXU3dXRDanRFbHJoelJZcUxFbnQ0cU5LTnVFa0tEK3VZa1UzNHdneHhDR2ZaMnB3UTN2Ylh2RkdFd1pvUWlJeFBqZz0tLUt4bS9Tc29vRUExd2lXMTltSzUwemc9PQ%3D%3D--d863b1d9d60ddcc554ec1ff09ba3f1858e631032",
    "VlB0WVZadXdkREpZQkU2M08yUWZZTWFZb0xVODlMaHA3NlBZVG9IbjRRUkZCTUdyN3hDRXdhWjlsYlBJOEFqeFNhVWRpVytkSDRxS3VHRG9Qd2ZVUnc5QysrUEE5VTlGTmJQNXU4N0tQdWIrZTUrRU9zRTBTZXlqWDA0c2RMSW83eVdtYVIwZFo1cXRBTko2RVdqSkZXdkFrNlRXQXhtT1R0em9DQ3FHUTVrVWVuUVhjT0ZFbWkwNjNxcit1eTQ0RWZNTGJKTldLWDA0L2YrWElpMGZ0bkdLVXJYTmhUazFVZ0NEQVM2QUY5ST0tLS9OQitPSEJHazhVYjJBd0tNNnJOaGc9PQ%3D%3D--63e84b0dd7f238839e1b7163f980affbdf242ab5",
    "dmVwcGVjaUE2Ky9PbUhsWi85L0ZOM2VpYjJ6azVGTXVTY0NtS29KbEFOdzY1NVlzR0ZMSGx5eUlRWTBjekF2VE9zNGgwSTYvWGhWMUZDbmV3cVRZeU5RTFBmUXdnY1pJL29NVjVMeVk3RlJPZVN6TmY1Y29wUjJQQXNrWnF3NklkUkdDZkFGQTN0Nml4bFJ3UnltMEhvTllWNGdmUWNXbm9kSnpTbUprd2NBUmkraGpmN1pob1A3Ti92NEd5cy92b1lWMEFMM0lWVitKY1hNYWJLT3VXZ1VDVFNkWll5S0diWlNpOUFVWmhEbz0tLTNEZStSdTE1M3o2bTBSNDlmOTEyYkE9PQ%3D%3D--15dbfa4787824a6d3be796c200e5a20beb4d3b86",
    "bnNUWFExWHZCWVo2VEFhdGRrYTBoeDgxcnN4K0ZkbENMNlJBWEJZaTVPV01oNFBseVkvaDFGWWxVeGh3N1gvVmJQbUhBT0JheEF0ZTZJeExlVTRGT2VNdCtFbVJKUTVUNXlzbnFkS2JlYjRoMEpiVkhwYm5ma3NIL1VrT3hwWk80S0tTUlgxdnBkYXJKZ0VicUNwMGsyMjlrdWdpR2hFMUg1Q1NXcHpHYUtpQzliUDFPVzNETEdjTENkOThKN3EwaEtndVFBc3B1NnNQbEdXOHArRWhEOXpPTnl2aE94b1pjbm1PM1pJV1dJQT0tLVZqM2p2R0ZZcTlaYmM1TS81VGpibFE9PQ%3D%3D--2ea2cc7b3d242d715bfacbbc46e1e5c7e9456840",
    "bWRnOVZTU1ZLWUdhNEI3eVM5cEtKcy9FVUdvTFZ5NmQ5RCtiU1BHdzl4VEE2S0c2cXVaK2VsY284blcwKzRzdTF6ZDVweXIwWWVpc0FhWHBpYlFBOTlDNjJxOUlyTGRPSU5xY0hoVFRzaDFpbFluQjZ4aHRjRmNtUVpJdEl3QUVFVENJMmg5OEZ2THBIdTdoSFovUDBMTjU5UGZjSEMyckpNSzFiRnhvY0NmOHF3eFcrdVdjek5VV2FuRzNNTm1ZNkNPbGkwbHlrUVMyYjcwaGpMS0lMWnFSeWhSNVNUc1pHVmtwVW83MTdrOD0tLW11cVpqb28yZy8zRitNcEJla2pRTnc9PQ%3D%3D--1e7bbcfcc944232511336a22999bfa1d1c8bedef",
    "V0tOTUlXbW52Y2RFSmJOeXM4NGozOWhsL2IrMGpxcSt0VHZObWg1Vm5zdzBRK0RONFdyNkFPRENmQiszZ3BEYWtEajFuR3ZFY3Z0VVZQTzUrU05PVWxmeC9nbHJUeWF6LzNaYlFMd2l0ZXJld3Z2QWJxaWk4WTJwMW5OZUJrbHQyQ29raVhoTVBJMFhnVVpvRzNTKzRMc2JDNE5BRlRqanpiY1Mya1hyamxkR0VXamZHUkRqVXhoc2E3REZxMUg2amhuYTFJR0UwM1lENmlTYUtzQk1QU2VoamI4aWJzcjhiSXRncklOUHpCND0tLVhrTlRSbndXUWxYR2ZnOFByMENRSHc9PQ%3D%3D--37deea19a72d797b3cd53d20edfc79af884aea11",
    "YkFEcVA4M0gvUlE5SnRvT3ZCWnIvdVFPU1RKSDZMa1FNcFBLSHlhc3U2N0dBdTA5Z2IzS3ZXdnRoTzltb1ZLOUxrVUJQZXczc0lWazhHcTYvUUhPc2Nkd2gwRHZPWjVnOXB5UVRBalB1Y3Nvb3d3NlljWFJicFEra1pZdU1XMXlyakNtZ3R1OEVZMWw1T25XYS8xd3dLWEpLd3RJc3k3bm4wV3ZoZzAyR3BaSWY2RTZIVGJGcEFiZzBwTkJXRXJ3Rkl3NEpKMXhWT0cwdnVaRGU0S0s0N1YrVWVPQktscnF5TmNtajY2V0EzUT0tLXAzYzJKMGpvcnhTOXZXcExWK0FRUlE9PQ%3D%3D--3b7829e4e42b56f8b874053f95b95d609c2de834",
    "UXdVNHhGejJaRlEvVFVxUHFhZGc0OTdBelNsMzJJQlFpeGN5eGdwREEzc0lFVk5IRVZrS2R3OU5Id3ZYMmtCamlWUHA4dkJXd3lPbTJ1ZjZZeDVYNVBKV3hNRUdxOFUwcnUya24vKzQwRDFoeit0eU45NEt0eC9Pc0pBOTRuc0VHUUxLMHg0OFJ0NWZFSnd5d0xySjhpNllFUDVIcnNSNnBGdVdHdml0VWp3cVduUDRuaUg0dUs5V2FsRDlpNzZ1WEx4bHorc0kwL092SXVhYXZMNENkVGc0clhvRjYrRzVZYitSNXdTSzdWTT0tLWxuWG5BNTlDVXNTNU42MFMrbFAySEE9PQ%3D%3D--c9c93ee130c9ecb5893fad8f223ad95d3fdaef4f",
]

check1 = re.compile(
    r"""Welcome, [^""]+, to WFAF - Waiting For A Friend\.  This is a family-friendly group chat you get sent to when you try to message someone who you've sent a friend request to and they haven't accepted your request\."""
)
check2 = re.compile(
    r"""Hi, [^""]+, retrying wont help, you can try asking what is wfaf for more info :D"""
)
check3 = re.compile(r"""Hi again, [^\\]+, try asking what is wfaf for more info :D""")
check4 = re.compile(
    r"""Hello, [^""]+! Welcome to WFAF! Welcome to the place where your dreams will come true~"""
)
check5 = re.compile(
    r"""Hi, [^""]+! I'm afraid they aren't your friend yet, you can always try again!"""
)
check6 = re.compile(
    r"""Hi again, [^""]+, dont feel bad, theyll accept one day\.\.\. hopefully!"""
)

check_pika = re.compile(
    r"""Welcome [^""]+ to WFAF - Waiting for a Friend\. \s*Say 'pika tldr' for more information!"""
)
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
restarti1ng = "Okai, restarting...."
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

details_response_alt_null_gen = (
    "You are %s (#%s) with ID %d and karma %d and your account was created on %s at %s"
)
details_response_alt = "You are %s (#%s) with ID %d and karma %d, with your gender set to %s and your account was created on %s at %s"
account_deleted = "It appears the following account has either been deleted or doesnt exist, sowwy ;-;"
timeout_error = "Timeout error, kindly wait for about 15-20 seconds and try again"
not_seen = "Im sorry I havent seen anyone with the name %s here"

stats_response = "%d people have entered WFAF and %d unique peple have joined in the past %s hours and %s minutes, and it is %s in WFAF "

dice_statement = "Your number is....%d"

unknown_error = "Unknown error occurred, restarting... ~*"

chatlog_file = "chatlogs.txt"

Greet_1 = (
    "Hi, %s, retrying won't help, you can try asking 'what is wfaf' for more info :D"
)
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
