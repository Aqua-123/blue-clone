import re
import time
import datetime
from datetime import date,datetime
from github import Github

main_cookie = "user_id=MjE1NTAyNjI%3D--53715d8c0d5a37453895fbf751e8bc4f9056f2fe"
#Getting info from github shiz 
user = "Aqua-123"
passw = "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"
g = Github(passw)
repo = g.get_user().get_repo("blue-clone")
coins_contents = repo.get_contents("coins.txt")
muted_contents = repo.get_contents("muted.txt")
mute_list = muted_contents.decoded_content.decode().strip().split(",")

# main connecting request json
connect_json = {
    "command": "subscribe",  # Main connecting request json
    "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}"
}
    
threads = [] # List of threads 
running = True  # Main while loop control variable
response_kill = False  # Handles response enabling and disabling
greet_status = True  # Handles enabling and disabling greetings
connection = True  # Control checking of connection timeout

admin = [
    "18695559",
    "16986137",
    "16521287",  # Admin ids
    "22466125",
    "22716229",
    "22783061",
    "11427049"
]

mod = [
    "14496406",
    "21847694",
    "20327398",  # Mod ids
    "20909209",
    "21964175"
]

forbiden_chars = [
    "\u202e",
    "'",         #Forbidden chars to be removed 
    '"',
    "’",
    "'"
]

bracs = [
    "{",        #Curly brackets to be removed
    "}"
]

list_main = set()  # Main list
list_main_dict = {} # Main list dictionary 
idle_main = set()  # Idle list
idle_main_dict = {} # Idle list dictionary
stats_list = set()  # Unique number of people joined stats
id_list = set() #ID list 
stats = []  # Total people joined stats
greet_timeout = {}  # Control number of greets and timeout
timeout_control = {}  # Control dict for list switch timeout

whohere_t = 0  # timestamp for whos here
reset_clock = 0  # reset greet timeout
starttime = time.time()  # Script start timestamp
t = datetime.now()  # Current date time
today = date.today()
greet_status = True

cookies = {"_prototype_app_session":"OHVTZXhlYmpOUStPbU1KNTFaVUVlM1c0cktnYnN1MWN4eFN1akxwMElZWjRiZVNSSGVOUWZwajJ1V1NFMytrbm9tL3NFTE9rQk9HZnJLWUJsNTlXM0JOWG9hZE9yZjNmamkyM29Pd0JqU01YZVlpWkd2WlhBR3hVZGJHbGRtRG5HemtvL29xZm9kVExlODJSKzNiV1YxcHV2TUY1c0RPQXRUbkluelhJbmdPekZXcWUzZzNldnFPK1ZjRkhMN0xLa3A2WDkxemtvaTlDemZmTkJvT0RlUzJhczBkYnJBR3dVbEQyTWtIN3l4TT0tLUxQeW9UcHZtdUJWbEVjQXMwRmYxUnc9PQ%3D%3D--83ddb608f55747654feca4873dff6895e55b263e"}
# Custom greets
custom_greet_id = {
    "16986137": "The river of life bubbles when Aqua comes near~ ",
    "21550262": "Hi, its Blue ^-^",
    "21388579": "Sir This recruit tactically acquired the fig bars sir~",
    "20835136": "Testing, testing, Wan, two, three! ",
    "291734": "Here comes our favorite magical frog! 🐸 ~~.*~",
    "14751444": "Hamtaro, the karmic wonder, has arrived ·ᴗ·",
    "18695559": "Your friendly neighbourhood Saturn is here! *~~.",
    "18274541": "A buzzy Bee enters the hive! 🐝 ~~.*~",
    "18491422": "Shhhh... The one and only drama queen cat is here *meow* ",
    "18560513": "SCP-1689 would make for a lot of ... Chipz. ~*",
    "17248098": "The darker the night, the brighter the stars... ~*",
    "20909209": "A dude? B dude? what dude? which dude? what is A? what is dude? who am i? what is wfaf..... x-x",
    "19422865": "Twi, the cute pony is here ~*",
    "17979714": "Your local simp (Bri) is here ~*",
    "14648841": "こんにちはねこちゃん",
    "17364255": "Coming hot out of the oven, it's 𝖕𝖎𝖊! 🥧 *~~.",
    "21848509": "Megumin, the arch-wizard magically appears out of thin air 🧙",
    "19259507": "Greetings cathy cath ~*",
    "20073491": "Greetings, your highness *bows*",
    "20909261": "Mecha nurse is here, everyone get ready for your shots 💉 💊 ",
    "22466125": "Welcome lovely person <3",
    "21842289": "As dusk appears, darkness takes over the sky... before the last trace of light is gone",
    "11427049": "Personal pizzas all around! Harenoir has arisen from the void!",
    "16008266": "The most radiant & shining greeter has arrived! <3"
}

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
hey1 = re.compile(r"""hi blue\s*$""", re.I)
howdy = re.compile(r"""howdy Blue\??\s*$""", re.I)
whos_here = re.compile(
    r"""(blue who'?’?s here\??)|(blue das crazy\??|(yzarc sad eubl)|(blue who is all here)|(blue who all are there here\??)|(blue where the hoes at\??)\s*$)""", re.I)
whos_here = whos_here
whos_idle = re.compile(
    r"""(blue who'?’?s idle\??\s*)|(blue who is all idle\s*)|(blue who is all lurking\s*)|(blue who'?’?s lurking\??\s*$)""", re.I)
whos_idle = whos_idle
tldr = re.compile(r"""(blue (wfaf|tldr)|(where are we))|(what is wfaf)\s*$""", re.I)
high_five = re.compile(r"""(blue )?(high five)\s*$""", re.I)
low_five = re.compile(r"""(blue )?(low five)\s*$""", re.I)
dab = re.compile(r"""blue dab\s*$""", re.I)
hate_myself1 = re.compile(r"""(blue )?(i hate myself)|(no one likes me)\s*$""", re.I)
thanks = re.compile(r"""((thanks|thx|thenks|thonks|thank you) blue\s*)|(blue (thanks|thx|thenks|thonks|thank you)\s*)""", re.I)
smile = re.compile(r""":>\s*""", re.I)
smile_rev = re.compile(r"""<:\s*$""", re.I)
kill = re.compile(r"""blue (kill|shoot|murder) me\s*$""", re.I)
pats = re.compile(r"""blue send pats\s*$""", re.I)
hugs2 = re.compile(r"""blue hug\s*$""", re.I)
party = re.compile(r"""blue (lets )?party\s*$""", re.I)
menu = re.compile(r"""blue menu\s*$""", re.I)
magic_menu = re.compile(r"""blue magic menu\s*$""", re.I)
heart = re.compile(r"""<3\s*""", re.I)
quote = re.compile(r"""blue (tell me a )?quote\s*$""", re.I)
uwu = re.compile(r"""(uwu\s*)|(blue cultural reset\s*$)""", re.I)
jok = re.compile(r"""blue (tell me a )?joke\s*$""", re.I)
no = re.compile(r"""blue (no|enforce)\s*$""", re.I)
dni = re.compile(r"""blue (dni|do not interact)\s*$""", re.I)
bored = re.compile(r"""(blue )?im bored\s*$""", re.I)
dying = re.compile(r"""(blue )?im dying\s*$""", re.I)
enable_greets = re.compile(r"""blue enable greets\s*$""", re.I)
disable_greets = re.compile(r"""blue disable greets\s*$""", re.I)
self_destruct = re.compile(r"""(blue self destruct)|(blue die)|(blue kys)\s*$""", re.I)
clear_userlist = re.compile(r"""blue clear userlist\s*$""", re.I)
uptime1 = re.compile(r"""(blue uptime)|(!uptime)\s*$""", re.I)
clear_memory = re.compile(r"""blue clear memory\s*$""", re.I)
stats1 = re.compile(r"""(blue stats)|(blue tell me the stats)\s*$""", re.I)
get_mute = re.compile(r"""(blue get mutelist)|(blue fetch mutelist)\s*$""", re.I)
get_timeout_control = re.compile(r"""blue (get|fetch) timeout_control\s*$""", re.I)
restart_s = re.compile(r"""((blue|blew) restart|reset)\s*$""", re.I)
hide = re.compile(r"""blue help me hide\s*$""", re.I)
ily = re.compile(r"""blue (ily)|(i love you)\s*""", re.I)
love = re.compile(r"""blue gift love\s*$""", re.I)
dice = re.compile(r"""blue roll a dice\s*$""", re.I)
mutereg = re.compile(r"""blue mute [^""]+\s*""", re.I)
unmutereg = re.compile(r"""blue unmute [^""]+\s*""", re.I)

# Menu Items
coffee = re.compile(r"""blue serve (coffee|1|caffee)\s*$""", re.I)
milk = re.compile(r"""blue serve (milk|2)\s*$""", re.I)
water = re.compile(r"""blue serve (water|3)\s*$""", re.I)
cookiess = re.compile(r"""blue serve (cookies and milk|a|cookies n milk)\s*$""", re.I)
ppizza = re.compile(r"""blue serve (pineapple pizza|b)\s*$""", re.I)

#feelings regex
coins = re.compile(r"""blue add [0-9]+( [^""]+)? coins\s*""", re.I)
hug = re.compile(r"""blue send hug(s)? to [^""]+\s*""", re.I)
pat = re.compile(r"""blue send pats to [^""]+\s*""", re.I)
loves = re.compile(r"""blue send love to [^""]+\s*""", re.I)
bonk = re.compile(r"""blue bonk [^""]+\s*""", re.I)

# Mene replies
coffee_r = "☕"
milk_r = "🥛"
water_r = "🥤"
cookies_r = "🍪 🥛 🍪"
pineapple_pizza_r = "🍍 + 🍕"


# Other replies
tldr_r = (
    "You're here because you tried to message someone who didn't accept your friend request."
    "We call this chat WFAF,"
    "Waiting For A Friend."
    " Let's keep it family-friendly!"
)
high_five_r = "High five ~*"
dab_r = "ヽ( •_)ᕗ"
hate_myself_r = "I like you, have a cupcake 🧁 ^-^"
thanks_r = "You're welcome :D"
hi_r = "hiiiiii :D"
smile_r = "<:"
#kill_r = "Ahem 🔪 "
kill_r = "Nu, smh"
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
dni_r = "We are not interested, thanks no thanks"
ily_r = "I love you even moreeee"
low_five_r = "Even lower five ~*"
love_r = (
    "Hey wonderful person, "
    "you are amazing and deserve everything you desire and love."
    " Hope the best for you."
    " You have all my love and wishes."
    " Much love ~ Blue :>"
)

#response and string match dictionary
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
    menu: menu_r,
    magic_menu: magic_menu_r,
    smile_rev: smile_rev_r,
    heart: heart_r,
    uwu: uwu_r,
    howdy: howdy_r,
    no: no_r,
    dni: dni_r,
    dying: dying_r,
    love: love_r,
    low_five: low_five_r,
    coffee: coffee_r,
    milk: milk_r,
    water: water_r,
    cookiess: cookies_r,
    ppizza: pineapple_pizza_r,
}

#List containing vars of admin command matches
admin_commands = [
    enable_greets,
    disable_greets,
    self_destruct,
    clear_userlist,
    uptime1,
    clear_memory,
    stats1,
    get_mute,
    get_timeout_control,
    restart_s,
    hide,
    ily,
    mutereg,
    unmutereg
]

#Menu list with images
dict_serve = {
    "coffee": "Image: [aW1hZ2UvOTc4NDI1NC9jb2ZmZWUuanBn]",
    "milk": "Image: [aW1hZ2UvOTc4NDI1Mi9taWxrLmpwZWc=]",
    "water": "Image: [aW1hZ2UvOTc4NDI1My93YXRlci5qcGc=]",
    "doritos": "Image: [aW1hZ2UvOTc4NDI2OC9pbWFnZXMuanBlZw==]",
    "pineapple pizza": "Image: [aW1hZ2UvOTc4NDI3Ni9pc3RvY2stNTM3NjQwNzEwLmpwZw==]"
}

coinsandfeelings = [
    coins,
    loves,
    pat,
    hug,
    bonk
]
