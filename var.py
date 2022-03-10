"""All static and dynamic variables used in the program."""
import datetime
import re
import json
from datetime import datetime
from imgurpython import ImgurClient
from simple_image_download import simple_image_download as simp
with open("config.json", "r") as f:
  config = json.loads(f.read())

main_cookie = config["main_cookie"]
client_id = config["imgur_client_id"]
client_secret = config["imgur_client_secret"]

response = simp.simple_image_download

CLIENT = ImgurClient(client_id, client_secret)

with open('data.json', 'r') as f:
    DATA = json.loads(f.read())
with open('messages.json', 'r') as f:
    SAVED_MESSAGES = json.loads(f.read())
with open('seen.json', 'r') as f:
    SEEN_DATA = json.loads(f.read())
with open('image_cache.json', 'r') as f:
    image_cache = json.loads(f.read())


# main connecting request json
connect_json = {
  "command": "subscribe",  # Main connecting request json
  "identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}"
}

connect_json_blue= {"command":"subscribe",
  "identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"blueyblue\"}"}
threads = [] # List of threads 
RUNNING = True  # Main while loop control variable
GREET_STATUS = True  # Handles enabling and disabling greetings
ALT_UNIVERSE_TOGGLE = False
SHORTEN_GREET_TOGGLE = False # Handles enabling and disabling shortened greetings
forbiden_chars = [
  "\u202e",
  #"'",     #Forbidden chars to be removed 
 # '"',
  #"’",
  "\u202e",
  #"'",
]

bracs = [
  "{",    #Curly brackets to be removed
  "}"
]

MAIN_DICT = {} # Main list dictionary 
IDLE_DICT = {} # Idle list dictionary
STATS_LIST = {}  # Unique number of people joined stats
stats = []  # Total people joined stats
GREET_TIMEOUT = {}  # Control number of greets and timeout
TIMEOUT_CONTROL = {}  # Control dict for list switch timeout
SPAM_TIMEOUT = {}  # Control dict for spam control
banned = set() #banned list
STALKING_LOG = {} #the name suggests
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
hey1 = re.compile(r"""hi blue(\\n)*\s*$""", re.I)
howdy = re.compile(r"""howdy Blue\??\s*$""", re.I)
whos_here = re.compile(
  r"""(blue who'?’?s here\??)|(blue das crazy\??|(yzarc sad eubl)|(blue who is all here)|(blue who all are there here\??)|(blue where the hoes at\??)(\\n)*\s*$)""", re.I)
#whos_here = re.compile(r"""blue (who'?s here)|(das crazy)|(who (is all here)|(all are there))|(where the hoes at)\?*(\\n)*\s*$""", re.I)
whos_idle = re.compile(
  r"""(blue who'?’?s idle\??\s*)|(blue who is all idle\s*)|(blue who is all lurking\s*)|(blue who'?’?s lurking\??(\\n)*\s*$)""", re.I)
tldr = re.compile(r"""(blue (wfaf|tldr)|(where are we))|(what is wfaf)(\\n)*\s*$""", re.I)
high_five = re.compile(r"""(blue )?(high five)(\\n)*\s*$""", re.I)
low_five = re.compile(r"""(blue )?(low five)(\\n)*\s*$""", re.I)
dab = re.compile(r"""blue dab(\\n)*\s*$""", re.I)
hate_myself1 = re.compile(r"""(blue )?(i hate myself)|(no one likes me)(\\n)*\s*$""", re.I)
thanks = re.compile(r"""((thanks|thx|thenks|thonks|thank you) blue\s*)|(blue (thanks|thx|thenks|thonks|thank you)(\\n)*\s*)""", re.I)
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
self_destruct = re.compile(r"""(blue self destruct)|(blue die)|(blue kys)(\\n)*\s*$""", re.I)
clear_userlist = re.compile(r"""blue clear userlist(\\n)*\s*$""", re.I)
uptime1 = re.compile(r"""(blue uptime)|(!uptime)(\\n)*\s*$""", re.I)
clear_memory = re.compile(r"""blue clear memory(\\n)*\s*$""", re.I)
stats1 = re.compile(r"""(blue stats)|(blue tell me the stats)(\\n)*\s*$""", re.I)
get_mute = re.compile(r"""(blue get mutelist)|(blue fetch mutelist)(\\n)*\s*$""", re.I)
get_timeout_control = re.compile(r"""blue (get|fetch) TIMEOUT_CONTROL(\\n)*\s*$""", re.I)
get_admin_list = re.compile(r"""blue (get|fetch) admin_list(\\n)*\s*$""", re.I)
restart_s = re.compile(r"""((blue|blew) restart|reset)(\\n)*\s*$""", re.I)
hideregex = re.compile(r"""blue help me hide(\\n)*\s*$""", re.I)
ily = re.compile(r"""blue (ily)|(i love you)(\\n)*\s*""", re.I)
love = re.compile(r"""blue gift love(\\n)*\s*$""", re.I)
dice = re.compile(r"""blue roll a dice(\\n)*\s*$""", re.I)
mutereg = re.compile(r"""blue mute ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
unmutereg = re.compile(r"""blue unmute ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
enableai = re.compile(r"""blue enable chat-ai(\\n)*\s*""", re.I)
disableai = re.compile(r"""blue disable chat-ai(\\n)*\s*""", re.I)
setgreet = re.compile(r"""blue set greet for ([0-9]+)\s*(:-)?\s*([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getgreet = re.compile(r"""blue get greet of ([0-9]+)(\\n)*\s*""", re.I)
removegreet = re.compile(r"""blue remove greet of ([0-9]+)(\\n)*\s*""", re.I)

stalk = re.compile(r"""(blue start stalking )([0-9]+)(\\n)*\s*""", re.I)
stop_stalk = re.compile(r"""(blue stop stalking )([0-9]+)(\\n)*\s*""", re.I)
get_stalk = re.compile(r"""blue get stalklist(\\n)*\s*""", re.I)
ban = re.compile(r"""blue ban ([0-9]+) for ([a-z ]+)(\\n)*\s*""", re.I)
refresh_data = re.compile(r"""blue reload data(\\n)*\s*""", re.I)
refresh_messages =  re.compile(r"""blue reload message data(\\n)*\s*""", re.I)
seen_reg = re.compile(r"""blue seen ([^\\]+)(\\n)*\s*""", re.I)

addlandmine = re.compile(r"""blue add landmine ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
removelandmine = re.compile(r"""blue remove landmine ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getlandmine = re.compile(r"""blue get landmine list(\\n)*\s*""", re.I)

spamtoggle = re.compile(r"""blue spam toggle(\\n)*\s*""", re.I)
getspamstatus = re.compile(r"""blue spam status(\\n)*\s*""", re.I)
altuni = re.compile(r"""blue (alt|alternate) universe(\\n)*\s*""", re.I)

makeknight = re.compile(r"""blue make ([a-z0-9\W ]+|me) a knight(\\n)*\s*""", re.I)
removeknight = re.compile(r"""blue remove ([a-z0-9\W ]+|me) from knighthood(\\n)*\s*""", re.I)
toggleshortgreet = re.compile(r"""blue toggle short greets(\\n)*\s*""", re.I)

savenickname = re.compile(r"""blue save nickname for ([^""]+) as ([a-z0-9\w ]+)(\\n)*\s*""", re.I)
ai = re.compile(r""">[a-z0-9\W ]+(\\n)*\s*""", re.I)

consoleinput = re.compile(r""">([a-z0-9\W ]+)(\\n)*\s*""", re.I)
# Menu Items
coffee = re.compile(r"""blue serve (coffee|1|caffee)(\\n)*\s*$""", re.I)
milk = re.compile(r"""blue serve (milk|2)(\\n)*\s*$""", re.I)
water = re.compile(r"""blue serve (water|3)(\\n)*\s*$""", re.I)
cookiess = re.compile(r"""blue serve (cookies and milk|a|cookies n milk)(\\n)*\s*$""", re.I)
ppizza = re.compile(r"""blue serve (pineapple pizza|b)(\\n)*\s*$""", re.I)

#feelings regex
coins = re.compile(r"""blue add ([0-9]+)([a-z0-9\W ]*) coins(\\n)*\s*""", re.I)
hug = re.compile(r"""blue (send )?hug(s)? (to )?([a-z0-9\W ]+)(\\n)*\s*""", re.I)
pat = re.compile(r"""blue send pats to ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
loves = re.compile(r"""blue send love to ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
bonk = re.compile(r"""blue bonk ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
get_id = re.compile(r"""(blue )(fetch|get)( id of )([^\\]+)(\\n)*\s*""", re.I)
get_karma = re.compile(r"""blue (fetch|get) details of ([0-9]+)(\\n)*\s*""", re.I)
mod = re.compile(r"""blue (mod|demod) ([0-9]+)(\\n)*\s*""", re.I)

help = re.compile(r"""blue help(\\n)*\s*""", re.I)
help_greetings = re.compile(r"""blue help greetings(\\n)*\s*""", re.I)
help_general = re.compile(r"""blue help general responses(\\n)*\s*""", re.I)
help_sending = re.compile(r"""blue help sending (feelings|messages|feelings/messages)(\\n)*\s*""", re.I)
help_admin = re.compile(r"""blue help admin commands(\\n)*\s*""", re.I)
save_message = re.compile(r"""blue save ?a? message for ([^""]+) :- ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
serve = re.compile(r"""blue serve ([a-z0-9\W ]+)(\\n)*\s*""", re.I)
getmeme = re.compile(r"""blue meme(\\n)*\s*""", re.I)
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
  "The last one you can use to save a message for a person and it will be delivered to them when they enter wfaf next time ^-^ ~*")
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
  smile_rev: smile_rev_r,
  heart: heart_r,
  uwu: uwu_r,
  howdy: howdy_r,
  no: no_r,
  dni: dni_r,
  dying: dying_r,
  love: love_r,
  low_five: low_five_r,
  jok : jok_r,
  quote: jok_r,
  eyes:eyes_r,
  save_message: save_message_r

}
"""help : help_response,
help_general : help_general_response,
help_sending : help_sending_feelings,
help_admin : help_admin_commands,
help_greetings : help_greetings_response"""

#List containing vars of admin command matches
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
  savenickname
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
  bonk,
  get_id,
  get_karma,
  seen_reg,
  serve,
  getmeme
]


cookiejar = [
	"TEN4OVZDZWsrT2ExOVcxQ1pUdmZkc2xtYUVjV2dMK2JBeFB3YkJsRzY0cGFTTmdhL3lIZEEyOWpGRnR0djhXVjNXRGZNRDNtQnczUFZ2NzVPMmREVU44Rmo3clNVR2N5SVhCWStSNzlsWFk2TkVzOFdEbkR4Y1BmMkkvQSttWFRETkNkdGhHaDJZTmR5Qmc3a09FNFFuaHoybVNJell3SDdGM1JQUk5yZCtLbmVMT0ZUVkZzYWxxSTg0SWtoSnJkVmcyL05DQlBwZG5XQ0I3TWxQbzdRdEtLdmszaVR6OVpOSVFZdWFmaXJLRT0tLW5CMXZtWlhpN2xJYnVEY0lBR2xMT2c9PQ%3D%3D--2e94ff98e2180cfac2d585d7b7973cf9dceaa4c2",
	"NzcyU2p2UVBHWWxlNW1QSEVyWVc0OGE3OFZaZG1KaW42MzlXb2dFOVN4QUY0d1lJNHV3TXNTSFVxamhUQ0tnbEZ2MUpleGlkL0xqU04vbW0wdXlEbU1Yd3A1Y1A1S2xabFo0cHFydzBqU2xnWDFHUFVLMEJheWJPaERQQVFicVJUMVFNZE5PVy9yVXBKczhqNHJSZU1SRTEwMFVJeHR0bHNGejlCMWdySnRVejJuLytFdzVNYWNBV2ZlNlowdjZrUm03UURSNlFVVDU1ZUQ5Y1pzeEhZcWViMyttU1hHTkQySVBQblRmM00yZz0tLVJ2TmFLcXg1UWRWSHBFRVAxUEljN0E9PQ%3D%3D--b827f6fe322e6aea7f500a7f5170852560101bab",
	"VlNzYVdXaitFaTlkelArSFNNMmlIbU1qZk14R1lWTmZYSzl3UlZlQ3R0N3l3Y3BzeXBkMmc2cUxjdytpVDUvOFpocUEyQW0vZ3M0bks1RzA5c1p4U01xKzRtc2tWZ09IaGcybW5MTkU5cW9xbnhZU0t4VjFVbjZVRmVjLy9xMXRrVGlUYUlyTXNINW1nT0Z4NEEyeTd6SnduUk0xMyt1QUMrOWhZSjloNSt4VkthSjN0SVFGTGdDRFRScDlwVUZEZHNtZklOQnhOTWJkdGZXUXFZcXp5SVBoMFdsYmYzWU1Lcnl6YzFQMGNsOD0tLTRuQ0dGYTB2YWhUdVR1cnRUQ0s1Nnc9PQ%3D%3D--fb4a9a3449e56daaef747cdb1fc2da27855075a2",
	"TW0xeGl1MjNoeDBldTQwS1ZzaFczYnd0QWQ4L2VaMnRyS1ZRdFVsb3RwWTBZYzFORUpiTlduc2xiNERZczlERDdzVXlJb2VxSmFIaktNeWRWQkdqVzU2V0JoY1M4Wk1MeFBPRkFVTURDOW1Sc2tYVUpMcCtxZUtsUVFrN2pjZTdtWW05dW5sYmFtVDJGdzd1c0huL0poRnVuVE1udDA0ZlhVelhMdlhVaUFEdVFCd1NQdEFUVDZJb3R0bEdhbUQvQTYyZWg2NXcvOXI5NUtnZWRTMHlVM0ZoRDlSMWdOR0JRMDRmbkswbFIrbz0tLVcvcWVZaVBlMEM3L3RNcUVaNEUwb1E9PQ%3D%3D--87dbde2084ddc10776e5db17abe2a0a15c248bf6",
	"MVpwVlZNWCsvMlppdm1Od2FRYXpBTnlvTXRrd2o0SDFwTFBsNkVIY2lkanU5WjBzKzlleWtDQkp4QlZpcmJjNnhMM3d5VDNCVWJZUG0xL1d4bDlHZ3NvYTdhbzJxL2d6ZHJsQVN5Y3JtYTlnSTFLaW5iU3lsL1RVaXRBQ0FtKzhjWlFTN09IUFl6RmltWXZUUDl4bXJhRWxnZ2lSeFFBdkZOQUJqMWc4cDYvUzBKUzZQdVozdlBtdW9vTlNvK3NvOStQT25UV1ZYSUgrMWN5VDVZNWFtNWs2Z2NmaWVSM0R0NFNpSndydUNsbz0tLS8xTHRmZ0crSHJhZ2g5UWhFZkluZnc9PQ%3D%3D--9c9ca2a44a64ac60a45dd23a032d14f8ffb4ca77",
	"dEhkWUMxaXR0NndmRnpLdUtSSjRpUTZPbXlNenNUekNNWmszQnI4dVUyUk5XRXU2d0NUMnFlb0U3SGlDbERpWGdBOFhqMi9ZTUU1bzYvSENSb3g3VzNYdllsOTM2YXFPOEU4VGlBVzg2M0w2Um9Ga0VaUXRJWU5la0w0YllMU29yeExIY1pFaVJmQTJUK2t3RFZ0YjZLL2lROXFGMEJHNkxvYnI3MmFsd29xdUZvaWxzTXl0THRCRTRLNEZ4NjZQNkFUQm54dmxvVUZTQTFUdDZpbWh2Ymdadk8zSFo4ME9kRUJEOUpMd2ZyRT0tLVhaS3FMQktvdlRiUHF2RWIrT1RycGc9PQ%3D%3D--62f6c70bd13fb118f7e65ece36b7e3735c0e61dc",
	"aG1LL282Y1pHQ2R2OHlRaVlpdDV4eFkxcHIrZ0l2RE9JSkhnWUpIblhLK0NqRlhpRnhLL1l1cG9aVDlDS3RROHRZcVV4TUtVWDNxZEMwRVI5UXByOE13WStVWUhsdFBOb2FQRm9pWDBuWWhHbm5EZTI0ZGUyRFE0dkF4SFIxcGMzb2JPSUpGU2dwV1huMzNuVVRHUUw1YnlNMmsySW1WeHVJTEM3ZndpSlR2WlNzQmJLaXpJdkRFOGZYWFdZcWpnQUp5T0JlVkw5VERCMm0vcGpZaG55ZnBRc2drWTlGU293Y0NXaklpcnVxQT0tLUpmMC9JQytGSk1KcTlFb3psYVpJQkE9PQ%3D%3D--be889684d75af24c9a62e182ebe8a5ac9655c81c",
	"QXdOcXdodEY4aW13QitKTzkzVW10L2RCYlY2Yjlvenh3cjlrNWNxdDVyNDVNRmQ4dkErK2lOSVBJWThVUTdnQ09paVRSSE9HR1h5eXA1MG9yR1NlSHJtQUNkWkF0czluQXlIM1BGeHAxQk9PbFpvMzNTQXpIUlpKbGZjTEFhL2xLWUVXS2F3Z0krNjdoL1c3alJ6RzZkYThkUzR5dFhqbGJ2VDJ2UWsxN0N1bkxzREkzblJSUCtPZCs2NkJXWTlQNmcvS09zUC94M0FGQXE3NjFUSlV1TUFQYVNaRWlCcFlFQWNFcUFrRHN3Yz0tLU9oVVBPcmJ2UGxSM3Brb1VFUGsxZ2c9PQ%3D%3D--2ceb6dd7b82b9f7a849a56eeba2777be6da64d8a",
	"Z2p4eS94UEFyV3lZaWNHSjdPK04rMUFRNHp5V1FDL3hZYjM0TkVGYlErQWwvV3VIZ1o2NnY0SW5BRS9FV0Q3WnBjOCtDUDBaRDhnYTJkSlhlQWRUbXNyNE1kSE5BUUw5MWlzTjk3TDJyUnUxdTduVjVGMlZKVGVNQ3VVWmtyWERtRC9rMFB3T1YvUFNWY1dSRGVZUWFDRHB6YnNSejMzVnNtTHhhTC84TGdGK041Y3FJNGZ1bDBSV2FocTYyMjU1bEpjeWZTeTZFQWsxREVRK2JRazBCZEsrN3ZWeFVHOXN1VThFcjFuQW9oRT0tLUpNbTZZNXQ3S3VpQmtsUUVIaVgxcVE9PQ%3D%3D--0ca975caeb1e8838d93671fdcbf78076977a1874",
	"S3VmdC9jTXhuUUpoNXphUk91Y3I4cTVlNjlQYm5ZYkFTclVpallNUmJTZTRqOHI1ckRTaFZ0azd2TkRCWEx4aitXZHJMcFoyaEJCQ0hZOUp3ZmVGOTF2SnBJek4wZUh1ODFJM0JueDhXMndHQXArejVGU2VlcTVvNW9yanV2R3FjTXQwOUVQNGtuS2t1cHc2bzByZmlTNCtXK0R2T0tUbERJYUZ2b3BpTlZRQWFCUjlhczB3M0NGY3Y1R2FSU0ZpbzZybnBJUGt0dmR0eDAzKzNJRkxBVU54RVBWQ2VFMEhSdE43VTFiektpOD0tLVdrV2RoSHdHYzdGdXlFRzJOb0tJYVE9PQ%3D%3D--a2880521f93abd24968a34d8f701561d969287e9",
	"SEJZNTdWRGplNG9OOGRoRk5VaTM5cVBQQlZqVzduM1ZHLzU2ejNORFFUbTRReFJ2cFJVd1pzaUw2cVMyRzgyRTlJOWliL2g3dklaVXRUenkvSEJFbE9aaE90SHkxaGhHVkp2amJhSTRVVjVOc0szVXE1M095RmxQYTB6dE5EZjBqdE12S3NsbjU2T1o4M0RkbGVWMmtweHNyMU9YMUtOL243blhJVy9vY2NFb1VIRWZrTVAzbUxlRmRISHVqOStPMFg2d3hjaXRQVE9jZy85Z3E1bTVJbkxUbm4wMDlQTDFYTStDQklaVkxXMD0tLU9XOVA4NFBIcmVVSVFnaDloQnF6cXc9PQ%3D%3D--2224e9289512edaf8e7662087e496ffc5bfea05d",
	"RGhJdE9KcVYwQTRrTDgzTFU1aDJaUHJQancvQmJRMjlOVnc1ZzVYUU1XMjc1UDV2Qlc1NHJjOTY1b05tMWg0WHI4UFJSenBjSU9jcGIva0swMWRwWWtlUzcwbGdhNjF6dXVoR1prdk9lK1hkRkl1QURnS3gxY2RtYm9HdkY5MXlvZnhWRGtPZlB1bE5ZOHFUZlZvZ014eStLdTQ2Und3YWI1MXZpL3laM0wxcU04RkMvcFh1MUprb2owNTMwSFlRZ3hvL3BpNzFvL1NrRTVjbytQMU1BVmIzZ2R1ZFJHYUxTZkdxL2tUVXJrTT0tLWcweUNDTmR5elFMYjBGVktNK2VRbFE9PQ%3D%3D--2eb2273b202a32f3d083a306b16f5b0b08f0bf5a",
	"dmwzYmZPRTBFaktHRmEvbzZ6ei8ySVlOZm96R2R0SGVnbGVtaHlGUTFTZlYzSlFLbWl4Vys3emQ0eTJyMlVQSEdNUVcxUjMwbzFLQm5ka2tZbnJ6by9UazhvSmV3N0srMU1CN29VRHBNRnVOU1BPTkwwMW9WdXZsRnhBbHp6eGJHb25xNnlxSVpiMlZnWE9OcW5KSnI5anA3M0xsakVQR3ZRR1FiT2w2blFBS0Vodk5aSlJDWWwxMit3NlpzY05FWU1aV3I2VWszcEhva0xEa0VWZmR5QXg2dlc0ODhiWkFMTDR6NDloNGFoST0tLUNwcVExajkwTi9LaGovcU9iYW1LN3c9PQ%3D%3D--144e29055d51cd1eecc1cf0d5727b0fc259d2461",
	"cHhYOHF4RU9XelNpMi9wSWxJMFV6TnJqaXh2Y3ZrL09hRnBrNldaZE1uaFlnVkpNL04xc1V3aFFpcWpzb3hpNmpkZ0J0Vy8rOHNJZDRxdDNnN3IyTWFmd2JJNCtqNnhXSGU2YnVYVTFXTmhhQkFWZ3pUVW9mTVVlbU1WMjFiZmhsNmNzdHhNTGNpRXNWVnB4K1lRd3JmUWVnSnBCU0xYSVRJVXN2RnpLTUFOaFZxUWNqdnJrbjB1RWpsNWZUSm8wWlJxWmxvTlBoZXcvT1RVZldtTy9ZbE1SWW1mLzc3MDc3ckVGbE1DeDRLbz0tLWU3cUc4RDRoMTZGWHFwL2dBWEtzRXc9PQ%3D%3D--b10c124e6d650942b88592824bb2701bc3542be1",
	"SWJ2eDVUeWFMdUpINjFObkx5ME45RGhxLzB5ajZraktuWjNrVTFBZzNOU1Rkb2JzSWo1U3QrZSs0Ym9ROUNYaUpZWXVweStwWDVpNG5xKzljUUxZK3BpWnluOHA1dkdCNTFGL1MwOGtlYnFudXdaMHltMkRUVDhXQVB6clhCUlQrdTRlVEs5a0l1SEJ4T013ckdPMitTQm1JV2FDOXJMQXNlSThEc045UHU4ZUFHSFA0L3crUU15cWM0eU1WUjVLbW1jcVhGUGFRUEpOb2FHbm9TQ3diY2FyOTAxSlhwM1pNWHpWN1FwaWRIUT0tLVdDMm0wcHZVQVpocDRYVGV0ai9rd0E9PQ%3D%3D--383fc252e7b6690a901ac816c11ed0e7e943e7fc",
	"NFVROUxKV2NMcXhqem9NaDl0RGZPUnh2Y3VmWG9RampxS0ozZEFDVlI4alU0a1dhcnp4dUtmTEs4Ykl2RGVobHU0cWFWaklqUlJqcUgrdnFwaDY1Yjl2NHdlTVNYbWNZcU5acnZUUVUrd1JNenVvMkdrNkd0ckduY0NKT3RiMndqazh3dzQxaWFJaUpTZkdqcG9IWC9yTGFnbHVzNXNlZjA2ajVKOWF6SkpiNWtGUG9rdk81SXlXWnU3MmRYZnZZcXB2Tk9NVlU0TXJQVzdpc2VpcUpPWDZWQ0tvMDZYMkZ0bmVPL0owZ3oyTT0tLTkrUzZzbEhXT2hrYndXSGMrYzVVZ0E9PQ%3D%3D--1746da44fdf60e16025dcaf713f5857a78a68121",
	"dG9BbU5VQ0VuT1RidWxNNEwycTBWZzFHM2F3RXpHaWZPVENIRitWNENKZHcxS0tUb2FEa1RDczVQRXBRMXl3bjhyVytjMXJjdGZTSy83dXpoalR1MDVJSWZsOW1jU1MzOURRbk5YMUVLNTc3Qm0zejREenZjckxuWEE4c1o3MFFZdTJ5V2NqWnFlR1pwVXRDN2JrYVhyOXZiZkJLMWxkMFNhY3ZsZStHNjl1dy96ZVNYcm1iQWEyaFd6bjQ2a1d2YkJpWklnNXU0LzR4Q1lwZVZXaUt3VE1zTWV3UlRtazlodnRNcTF4N3JWVT0tLVg3K2dXL3lTQklVRlA5d0NZdkFxOEE9PQ%3D%3D--78d811526e998d213c62489fdb668cebfaee8728",
	"ZFlPNFh0VDRyVUdwL0NibFFmUW9RTlpLOHd3MDk2OUl5MWR0NDM4aWpMNmphQ0VFWHNLZ25zY3FyWDh2eGpSUS9RdkZTRkJaREwrK0o3alI1UWxzUkIzWWkrbEl0S3doWThObzdySE1ZT1BxK2FoYXJ0YitVTHlJYWpVTWtKOGU0TS8wTllQdnBhUzhVWkdlbVZXakZLZmZwUktsZmJlYmorVXIwQnRWMTNNZGM4TDJWUVNJSE4yZEsvbm5Teko0a3k2Q0VBVStmZzRkM09JSmVGN1pJN1BwU3o2bFBrdGhLTExzM1plcVc3RT0tLU5aMHJURlhtaGNWbmF6eTg2OTVNZUE9PQ%3D%3D--5393ecf35e73d92a971975b80996185f18077668",
	"SC9sRGdtaUhmL1ZqSGZsS21rcmQ3S0F2MU9UODdHcHkwRXFURXp5RG9NaklmTFM0NHY0WkdINHJ1RS9CVTZmN3JTRjEyVDh5dXFTQjhNVTBLUTJHVU9NS2V6Y1lZMmN2eGczc083Ylg3V2ttcFN1cUxCZGpTTWFIZ0l5eDl5d2FaRThYdkxvOXBsS01OWUZSS2gvU0o2ZFRuN2hVM0V3bnN5UTdJbFNUTGxHNWhSelRkakZlQVo2TzZSckQ1bFNVTWtzbnUvbFd2eGtFdWRUSE9zWTQydFNHcDJ3SjY3dldvWG5kQmZXellFaz0tLXhrQTUzMmdReU5iV2k0dWVrWlB2RFE9PQ%3D%3D--33666b8414bd968d7d0467fccc823fc12b3b85a0",
	"bWU3VXZPU3hQdlZtai9OYWRHbVRNMUdGc3F6K0M4WjEwNlZlUzBQak1JZ3kxTVZQaDJvaEVUVElSTVdvaXhpZWhSRHdCWDhmbWpCTWNKcXBkcHh5dnFaMGFJN2wrNk5RMTlyc2dRVHNUaEFVYzR2YUp5aTRjMnNNTWRVbVZiQXBwMWVnZ2d6ZnVvM05VL1M4aGExMGNIWHZGQzk5UG8xS1lXNG9YNHlhK3Y4QlMwdFkwSGN4L1ZXeFQzOGtONGhIU1NaUE1ZTVRWNGEzeDNZUmRENFhSL2pwM3MrcVNVVHJxZkdBYlROOEQ2bz0tLWxkQXlGUWlKMmdVWEora3ZzYnlYWWc9PQ%3D%3D--3ceb710afcdbb4e813eb9bda84abe98fd3bd45bf",
	"amU2VjIyUHBGdVplMW5Ha08vQy9UenQxcktpQ2o3aTN1UDNocXVsVlNJalNmMCtRM3NFNWN2c1J2d3crUWFPMVdvZ2FFOHJ3RkNQWTdXbUxjTXZITXhEZGs1Y2xyVGFiWWpvdFlEenUxclhEUm4vcHBBalpoeGI3NTZTU0RxeEYzRGhMaW9IcVdKcCt3QTY1Z1QwZm9nQXArNGdKa3JpcHlPQk44L3hnUDgxc2VCRzlhajlmenljZndtTmFhZ3BEc0lOK2ZOYy8rN09NWEJ2NzdrQVZTSVIyZGU3YnlvVnAxV0hpdUhyNHRyaz0tLUp2M1NsaFJVajlnYjE0dUZVM2NsM1E9PQ%3D%3D--3ac451540678d7b260602c6db72aa22132cea377",
	"QlMrNWtDeVQ2TkxSQmR3M3ZtNmF6YlhkYzQycTkrNmMycStBQWRseDBUeEV4RE1qYUJLQ0xCRVFIellDbDZuS21jT0xrUGF4Z0RVNGJobzNDSVYvdGhSSVI4Rk0zdDlXd3BabjdGL3p0bVJ0eThuUFNjdzduVE9FdTI2dGpXWXNOUGsrc3dqbkJPMFJlVTJqbUd6UHp5K0NCSmNPdmE1VnVSMXowK2ZBLzBlMEtaeS9UbEZSOVVZK21jdUxlTlZXYmZxckFJYVpvdHJnMlJveGc3blVJMGdPa2NkeUlaMEdTMXY5cTFpckkvVT0tLUduazVvL2MraVZWWTAzU3V5NXB5NVE9PQ%3D%3D--63c4fe77f92f85eec1c5fef6351f6c4e354663d8",
	"TittbEcxckZHUDJTY2RUQzJhSkVzYWRTY2MvWHZEZmYvZC8zQ0VxV3R1Mkd1WjFVWlkrem9Ra1lRbURhWkJMU2haTWRqQjVOUkd5bUtSdnJzMFdJdmV6dXhYZ1FwRTFGQUVNYy8zTU5kR2Y4QjV5cjFmQmE4MzZVTlhXQ3RtenJCM2pCckEzREpLenlSZlZCWjhpTjJFRFVGZ08zbCtGNmFveHZIakkyVmFtanQrUzdBWVBOYkpsVmIxNzhtSWVHK1h5cVhDbng4amF4UkM3cTB6aVJQbGkwZ2ZSbnpITm9SVEkxVzNUa0hkZz0tLXZEc3BxWGduR281MCsrUituY3pFdFE9PQ%3D%3D--bc9f42e77a2dd35dbade73b4159d7845d32bc65c",
	"TlpabUxCTDhLMXVwYXZpSHBnYnI1dExDZG5pcWRpMm1KeGxmL0N4bHdGREFMTk1JY3BaTG1TWlpQa2REUXpZQTFCNXlkYXpkOFRUUGU2YUt0alkzcjJtUnZTbk5hbDVLMURSOVJOVktaVURaYVpYcHdqMGpMbXMyVFNSd1ZlSFhiU1p1TmZGdk1vV21jdCtJbzVLYlNGZHhWdGdSMVdUczJjb1BlenlDbjNxUlJVbmdJdWtZMzhtak04cnBtVWNNZ2lSMy9sTGNmaFF5VXh2MTdyQzMrbFJoYkJlZTlxMS80UVNiZ1ZYWmxNbz0tLUpNRExHU09JTkoxTmNhWmFJT0duNEE9PQ%3D%3D--29c4ec75f15e3e30e5996ab6cb36f83b862623ce",
	"emdKUnJkU1hCVkFmeWhuVFdGMGVpQ0d6K3RGWi9ybkJPaGpYRVg2V2Joc1M3Tm1PZzFLblFJaElqK1JnWjE1VHpVdGhUcTZQUTVpMmF0YnBvSS81ckVJTjBQQS9JeUxvRERTa0gremMyY3lOdXYzbTZoT1VnS1lMd1l4a0hJMlpuc2xwMGZYaHVQNFlIbHVCMENWZUNuaElDczl2ekd4TjJMWEhUbnJQMlRMd1NFUnhNZXhNQk5ONzFNN3lnc2d2SEV2REE2amFJa0JBTUUzVlBzN2N4ZzZ3UnVxdzVGRk9tWktScWZMS1E0Zz0tLUdSOVJxeGFWWlVhdVh4eVErRnpRL1E9PQ%3D%3D--3e179942a059d116ae9978614c2f6f6a69a04bcb",
	"bmluckZwR2d2bEQwcEt6SGIwY2V6eUtnL1h6QmNnYWZRei9kdlRlTHZqTjlDL1djMlBpR1h5Y0ZEazRUUzMzM3FjRk5SaHN2R3Bja2F3NVhWRS9LTktjcTFEM2VzcHVMKzQzMUx1LzJaNmRFUThvZGFpWFJ3M3Bmb243d0g4WDAzVHNFMTR4SFlOSGhONVFTRTF4NUo2bE0zU2tCNWI0TTVDdGk2a0daRC9ubTVrOFNrS1dsSHBldVhyd0Y2YXpzMi9wNmpxYlA5Y0FyREk0blQydFV1QlhRNytRYjlHZHo5Z2JxSVI3M3RYQT0tLWhkV0hRZXpDdE5rMEhGeFNBNGgzZnc9PQ%3D%3D--d7b7303c9935a71efa4693d3bff05e521586b7d1",
	"a1IwN0p2M1lQOWFVZVEwUHpWZkJ5OU51Tkx0bjRxZ0tRUTdmT2JPYVZ5ZjV4RTdENHdPTW56UUpGTk9vcmdPZ3hvOTRTMG45REhKQmVuWkVwenRlL05DM1VFNXF1VVh3b1RhaFdjWHp1QndCR1ppK3lIR2pFazVCUkp0d25OWDZweFBmSVVnaHhjU3FPUDVnTnhacExrQU1STmZLeFZvZFozaVowTFpHWDlBMUNiS05XYTRNdmJnWDVPV2VhL0xGK2MvNWhYK3FhanhuT0FtRzhBZXdodk9qY2NIZmlrZHZaMVRpTXRmYy9nMD0tLW92a3VkS3pNTlE0T3A4OXdoRkVGc0E9PQ%3D%3D--b516eea6ee314eb25e8de664076615e6d1c3a411",
	"RHp1Y3ZuVHhIQy9ZYXBQeERncVdhcXFZMUQyNVNlSlliOHFJSmJ2U2ZNSkw4SDRiaEV4akNqbXJKY3RMN0hoRTdGT2tRZmxPRjJvdFVIdmM3TnFkcCt2SWFIcGMybkEyeTFUeVVBQmNIUStQY0JwWWpuVHlwbndaWGdxb0cvZHJhTVNPVHBNekNyMG5rT1ZmaTJVeWxDc1Q2RzlCTUZrc0tWMWluYVNYT3BtOVhYN1dkTHJGMEczSVdFOVh4L3ZJdENTRnI0SS8rd1BmUFVlKzhRTWY4UktScEFidHpNTmkvclZRWmNUTDViaz0tLVh5ZnRITWw1ODlJaldhb01nWEZSQkE9PQ%3D%3D--a65a87e9600c00ce5edaa37b7c02c39cda8356f6",
	"QnZFdmpjdVNGeXo2bWdPc216UW5KUThKcWdwZ0xFMWdYY1prcVArNGNGRC9ySW5nUWhseWRsZGk3d3V2K3ZvcitqdVFLZkdFc2pkQ3FjV1ZaVnN4U0wySlZabXV5NHc1OVEvamozb3RtTlR2NVZOSFZpNnY2N0hGVEp0VlNrNnNsU3hJNXlWQmFlbU5YNmZYeHdId3owdEFaTFgzWkZqdHFMUVdtNHlvZDhzbUtOQkFiMy9aTW1IblBhNTlJSUFhcG9HVDlYSmNkN1FYRGxNMEx5VFhkZE96djQ1aUVQU00reVpCeGEyNFY4ST0tLUFPK1dlNmxXWjhnNDR5cXJzVk84YWc9PQ%3D%3D--4edd357855db3999879cd7cc24d9f42420d8eaa3",
	"djdLdUNTTnZ6cTJtQkh2Ulppcnl2S3hsUlVtQWN0N2RlN2J4ZU1SVDJocHIzRE4xVHFBbjdjVFdIWFpCL1gwUnl3RFRLbDdLckFxMTNSYkxBaFJBUkU1Q3kyWVQ4L2NLT2dNNmhoblUwMnp0Q3RUNTQ1Zmtsd2lQck80czFUL3IrODgvbW1DUUFDcU12N0ovaDNuNFFiTkJhQlhwOVdvbnFlaHJ3SXByZU82WmQxWGNZbE5FV1hxUW1rM29LMUNQdVN1dms3UWRJYy9GYU1iYjlrZDkzaUFHUVBjWHRVOFRaOStJdjdSSGwyRT0tLWg4Sm9rSW91dTNNamd2UFpxa1BDNkE9PQ%3D%3D--7620ec2438ae158bac5b1d1bad4faf34041cad37",
	"WjJlOFBNN0VnRXVRQTlIWlZIRHNlS0Z2aVNKYVVqQUtMTmF4MHJJQVBtWlFUZ1JtV1BzZStEYlp2YUcyL1FCTndLelNJR3JWMHN3cFZDODJWYXJMOUhKOFlLRkl3RXdtTE9FZmlEamRyU09tbEJTc3NuQ3RsT0ZnWUpZR3VKMlF1b2dSN0JIS0p4eGJFcWFUYXh4cXpDR3hoYnNpYW1ZR3g0LzNUM0o4anlORFIvY0ZONGNHNjNIWXVXUkFBU29uZGRuTU1mT3dTTkJuVHNlUWk2ZHdWUTJCdXllY3lkZmpFdk1zdXNJOGN6ST0tLTQwWlV0K21vQVd1VldTckxueU0yMUE9PQ%3D%3D--2cf55bfda859bd21f7350753ffa78d895fcedbe6",
	"a3NtZW1CTE9OWkVQRGJ0Qjg4Nlp3U0NnR0ZQQnQ5K0FuOFlhdFp2ZkllVkJXdXJjUDVYSU9XZUNpV2tZQ0d5S1ZhSWJlRWMwNHBMTEprdnIwMkV2U0gwWHVKQ3lJRTZncHlxZ3N1ZWhEcUgwKzRkbjhwYmI5dU9PNk9ZMVlSMXIzejhlb1JSSUx6cHI0anh1SVV6U2ZuVktvbDJHdVUrTEZ5ZUhLZlZQM2FUUWxXdkRQWFVscjdITEFkTzFRYXBZeFdzZjd2elRnRWUyR0kwU0o4cFhQVy84TkNYa2N6NEdxY1VEOVRsQ2ZLQT0tLVhyQm1WKzRRUG02YzRVWXkzQmRMUmc9PQ%3D%3D--c9c55e26bc7d187f051f7d21039076f561935225",
	"a3Z5cmRqaCt0dk1tSXpqcWs1SUVaQm5YaXVwaEV6alU3czlZTkQwN0ZxaEswOEJMaUZwbmtLdzg2Uk0xdUZVbXM5VEgvTDNzVWZiQlNaTlZmUEEvRWZmTzBQWnNlbDlhZklVdDl6SDZtNnptaXBVVzlFL1RxMHBDMWYwUGJGa0NqUnRqODRoK2NHQ3h3aVNIc3pZSzlncHhudXZJUGpOTUZlaDVaTS8wQTFsUDlPWDNvcEI5VmNFZnZnaEJ2YXM0RjJLRzNLdWtCaytadWN0SzEyRTJubSt4eEJXdlhXcDlndk1WY083K0JXND0tLWtIbTYxQVpZV3p4M0pUTnY2VXdaUkE9PQ%3D%3D--10a94e3cdcbdbadc05d654797e75028517fd3ed4",
	"eTRSVU1HcTNuLzN4b1drNlIzS0pxTXRpWnlpWUFHcitKNmFOWElSc2FmZmVYdThUTmJQK1pEbStsbEZsRngyZEFjYkk1N1BYd0dtdjk3NVFpaHZaU3NOaklZMGRXRUVSKzNJczV3V3dENDg2emovSzc5ZU5adlpPNXNyMXVBaXNQVjhHNnNCSmdWWERpR0xWQzVrS2VyZzJ2d0Q1MUJFaTFTOHQyc01qQjg1eDBWUFI3aFllZnMwa1JSNll2Y1pOMldxN01jbXZBVnJpR1JKUWtSMmp0RGtmZ0FFeGpBZ0NqSFRaYk41bUNWUT0tLWcwY3JST1ZBVXBsbTFhTHVzcWx4REE9PQ%3D%3D--f92108b0e45fdd1860ba85f308decd2334e9583c",
	"L2Vaa01sUHJ3cWloamljdENGUElSUlYzV1Rkbmh2bWMrZDhOL3ZsVXhPZkxTS2J5aURBWU5kZXl2ak9TU1NCM1E4R3ZxWk5yYXc3dFd5aU14YmN3YU9UelB5N01aMTJqdG9PVFlyVEUybWpoc2NRVTNVYXJDYnlvdlV1aWI0cVE2YVMvSzZxYmQvYkoxd1NaTUZCalNWWklzamx0QXBPVDMrT3ZYMDZtQm5pV0tDVjlKTjlxSDZZYWpBRVJxZFlEQW5xaHRsREZoVlJaZDY2czFDdk9jSGhIczJlM1JiQTd3SEprTUxYQzd2TT0tLUdRdUV1bTFRNFA0d3FUTUdJZE5CNWc9PQ%3D%3D--7deba08c45c24b00c604f6f89ec2c5b45b7dcb88",
	"K2VjUDJLajd4SGlCTk9OS1ZKOXN0enZtZXhvTTVmYUYyMFJxZEx0ZlRsWS9TSWM4YkNkcVJFaWd5NXFBckRNS2RzUzNybGpNU0RUMXB2ZG10NUVmWjJScktVa0I1bDY0Z3RUcWZnaUUzdDFFQWY1R1BLYW96am0wLzZqTmplTlc3UE5jWWlQS29xQmpzMWdUMWgyN1NpdDZXeTBIRlJ3bmkvWmtGalV3YVVkWHZzUVFNNXMwUTc0eXpPVkk2MXR4WGJwRkJUclNYRFAwVC9QYURLVnhkKzJiWGZRTnJGcnkzOGVxZ0tWdXBKaz0tLWwzRVp3NHhvcDVKRTJyMGY1NHBDL1E9PQ%3D%3D--1450888afc7cc44781d6ce2690c889f09bd9c46e",
	"MTA3cjJialloM0dZQWtkdjR6Ny9uanVRL2N2QURwc3J6cnUrTHFLNSs4M25sTUluNnM0U2JhTC9PampTenM2VDczdDJTWEVIREVlc3JrTlRIQ1NNdVRkZ2hDQWM3c0pxMEdONEwxMXQ5Vlo0dm94alpMakVMRWIwZ0RMY2dlUUlCRDYrN2pIQXYzWXl6NC9UY0lWOUpJQXI0R3l1YVhTT05LM2ZoaGFwNmpVL2s3STJVcUg0UTRNR3ZhcGFKQ1hCZGM0ZmxOWE0rWEM5SVZTQ01mc0R6ME1WSk5PSnBLcU96eWdtN3ZpTkxEND0tLUNrWmFDTWRnQmU5bkFVaFFjZGtOaGc9PQ%3D%3D--de792b4c303594010bfc08150b392ae0ad28659a",
	"dWIxTUo4eU93QTl6aWRnL084SGd6d0REWWdTdXJxUGtPTitaQU9rNWVvV01GcTE1VFAwZHIzVUw1c0d6OTg0dW1PZFZ4TmRiQVJBdTdOUmVDV2J1WjZ3ZU95VWhINWdWa1N0cGlieTgwTlh6R20vVThxejc1SG9TUWl1MUtEcWp5VlpaSUFOSWhyakFsMERKaEppOGVreklGMUdBb0ZDZEJJQmd0YXBQaENxUTlqeXZHK2lVa0N3ZG1GWXk1UzRJK21YcEtnOWR3cDVTWXJybkdsT3BmSGxNRklDb2lJSDJtQkh2a0R6K0xSMD0tLThZTzlQR1V1TUxwQ1p1YThTMzVRZUE9PQ%3D%3D--8096447e5f486861df27621bf291fa6a594bdf44",
	"eXp6cngxYXU0VkdsUDZFU3FZS0YwSTA4TW44WWVQTVB4ak9uWE9rbTlPQjRMSHNob1FndnlvTmJ3K1BYQmY0ZFkzS1dqVmR3dElVYmQ1bVRSTFJXL1VDYUNPYmsrU1FCcmYzVWRjMXBWYnVNQ1hPWDFLWWR2djNVMVVmOTdKbUxHaWd3WDdYV3RWR3pFM2FBdmh0eHFMNk9JZGVQWmZYWlhXK1ZuaEQ1Z3lqV0xpeFcxaWdKMWd1OE55Mkd3ZFFvZGlBZnVwSTVlU01JZk12Qkg0VFVoamluNmJ5a1drU1lSRE13dXhHNm45VT0tLXRMd2hXTTlsTnpiV1EyTVRSUVNNV0E9PQ%3D%3D--520c8ad282645df83d2541850dda78c00cd1f8f8",
	"djNDd3BJT2k1TmJ5ZTcvb20wM2JsZW5MNTVxdXRoMW0xV0FFTitsbVIvMmpMRFdscFV3RUphc2ZEYldpUXR5L0FIb2grby9seFJydVYzaTJKN2JRdzFBSlpTdW1nM3NIYW5KQ2toYTJMNU1BNTErMTdqMHJBSzNtV3dEQ0FiV3BPU3o0bzBGMlhqM3NEbEJyWmJLd2ZxK0dzUEFjN2dQZ3ZZSytycEtNcmorMVcxbTFJYmFodmlYVjAvTldMTklVTnAvaG03K0J0T2V2a1RFMHVQaGU2TVNJSkZNN3dnQk5YdTc3SHF4UmlwMD0tLU9jQXhLK25xVWY0QVJqUE9MaFVQRVE9PQ%3D%3D--5ba91d3993d698cbbbabfc1359125ed2e3130718"

]

check1 = re.compile(r"""Welcome, [^""]+, to WFAF - Waiting For A Friend. This is a family-friendly group chat you get sent to when you try to message someone who youve sent a friend request to and they havent accepted your request.""")
check2 = re.compile(r"""Hi, [^""]+, retrying wont help, you can try asking what is wfaf for more info :D""")
check3 = re.compile(r"""Hi again, [^\\]+, try asking what is wfaf for more info :D""")
check4 = re.compile(r"""Hello, [^""]+! Welcome to the place where your dreams used to come true!~""")
check5 = re.compile(r"""Hi, [^""]+! Im afraid they arent your friend yet, you can always try again!""")
check6 = re.compile(r"""Hi again, [^""]+, dont feel bad, theyll accept one day... hopefully!""")

greet_check= [
  check1,
  check2,
  check3,
  check4,
  check5,
  check6
]

#Some Strings

#Links
karma_url = "https://www.emeraldchat.com/karma_give?id=%s&polarity=-1=HTTP/2"
profile_url = "https://emeraldchat.com/profile_json?id=%d" 
jokes_url = "https://icanhazdadjoke.com/slack"

#ws-connection shit
ws_url = "wss://www.emeraldchat.com/cable"
origin = "https://www.emeraldchat.com"
subprots = ["actioncable-v1-json", "actioncable-unsupported"]

#Responses
start_ignoring = "Okai I'll ignore user '%s' 0.0"
stop_ignoring = "Okai I'll stop ignoring user '%s' :>"
already_ignoring = "I'm already ignoring user '%s' o.o"
already_not_ignoring = "I'm already not ignoring user  '%s' o.o"
stopping_logging = "Stopping logging for account id %d because the account has been deleted and doesnt exist anymore"
logging_text = "Logging at (%s) %s %d %s %s\n"
done = "Okay done ^-^"
already_not_greeting = "I'm already not greeting o.o"
leaving = "Cya :>"
clear_list = "List went -poof-"

just_joined = "I just joined -w-"
here_for_one_min = "I've been here for just a minute"
here_for_x_mins = "I've been here for only %s minutes"
here_for_hours_and_mins = "I've been here for %s hours and %s minutes"
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
