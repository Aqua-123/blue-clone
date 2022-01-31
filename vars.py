import datetime
import re
import time
from datetime import date, datetime

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
  "11427049",
  "21550262",
  "14267520"
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
  "'",     #Forbidden chars to be removed 
  '"',
  "’",
  "'"
]

bracs = [
  "{",    #Curly brackets to be removed
  "}"
]

fallback_check = [
	"20909261",
	"16008266"
]

greet_exempt = [
	"20909261",
	"20909232"
]
list_main = set()  # Main list
list_main_dict = {} # Main list dictionary 
idle_main = set()  # Idle list
idle_main_dict = {} # Idle list dictionary
stats_list = {}  # Unique number of people joined stats
id_list = set() #ID list 
whos_here_r = []
stats = []  # Total people joined stats
greet_timeout = {}  # Control number of greets and timeout
timeout_control = {}  # Control dict for list switch timeout
banned = set()
stalking_log = {}
whohere_t = 0  # timestamp for whos here
reset_clock = 0  # reset greet timeout
starttime = time.time()  # Script start timestamp
t = datetime.now()  # Current date time
today = date.today()
greet_status = True
aichatstate = False
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
  "16008266": "The most radiant & shining greeter has arrived! <3",
  "22975867":"The earth shalt trem'r at which hour the sphere rolls to the did grind "
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
hey1 = re.compile(r"""hi blue(\\n)*\s*$""", re.I)
howdy = re.compile(r"""howdy Blue\??\s*$""", re.I)
whos_here = re.compile(
  r"""(blue who'?’?s here\??)|(blue das crazy\??|(yzarc sad eubl)|(blue who is all here)|(blue who all are there here\??)|(blue where the hoes at\??)(\\n)*\s*$)""", re.I)
whos_here = whos_here
whos_idle = re.compile(
  r"""(blue who'?’?s idle\??\s*)|(blue who is all idle\s*)|(blue who is all lurking\s*)|(blue who'?’?s lurking\??(\\n)*\s*$)""", re.I)
whos_idle = whos_idle
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
dni = re.compile(r"""blue (dni|do not interact)(\\n)*\s*$""", re.I)
bored = re.compile(r"""(blue )?im bored(\\n)*\s*$""", re.I)
dying = re.compile(r"""(blue )?im dying(\\n)*\s*$""", re.I)
enable_greets = re.compile(r"""blue enable greets(\\n)*\s*$""", re.I)
disable_greets = re.compile(r"""blue disable greets(\\n)*\s*$""", re.I)
self_destruct = re.compile(r"""(blue self destruct)|(blue die)|(blue kys)(\\n)*\s*$""", re.I)
clear_userlist = re.compile(r"""blue clear userlist(\\n)*\s*$""", re.I)
uptime1 = re.compile(r"""(blue uptime)|(!uptime)(\\n)*\s*$""", re.I)
clear_memory = re.compile(r"""blue clear memory(\\n)*\s*$""", re.I)
stats1 = re.compile(r"""(blue stats)|(blue tell me the stats)(\\n)*\s*$""", re.I)
get_mute = re.compile(r"""(blue get mutelist)|(blue fetch mutelist)(\\n)*\s*$""", re.I)
get_timeout_control = re.compile(r"""blue (get|fetch) timeout_control(\\n)*\s*$""", re.I)
get_admin_list = re.compile(r"""blue (get|fetch) admin_list(\\n)*\s*$""", re.I)
restart_s = re.compile(r"""((blue|blew) restart|reset)(\\n)*\s*$""", re.I)
hide = re.compile(r"""blue help me hide(\\n)*\s*$""", re.I)
ily = re.compile(r"""blue (ily)|(i love you)(\\n)*\s*""", re.I)
love = re.compile(r"""blue gift love(\\n)*\s*$""", re.I)
dice = re.compile(r"""blue roll a dice(\\n)*\s*$""", re.I)
mutereg = re.compile(r"""blue mute ([^""]+)(\\n)*\s*""", re.I)
unmutereg = re.compile(r"""blue unmute [^""]+(\\n)*\s*""", re.I)
enableai = re.compile(r"""blue enable chat-ai(\\n)*\s*""", re.I)
disableai = re.compile(r"""blue disable chat-ai(\\n)*\s*""", re.I)

stalk = re.compile(r"""(blue start stalking )([0-9]+)(\\n)*\s*""", re.I)
stop_stalk = re.compile(r"""(blue stop stalking )([0-9]+)(\\n)*\s*""", re.I)
get_stalk = re.compile(r"""blue get stalklist(\\n)*\s*""", re.I)
ban = re.compile(r"""blue ban ([0-9]+)(\\n)*\s*""", re.I)

ai = re.compile(r""">[^""]+(\\n)*\s*""", re.I)
# Menu Items
coffee = re.compile(r"""blue serve (coffee|1|caffee)(\\n)*\s*$""", re.I)
milk = re.compile(r"""blue serve (milk|2)(\\n)*\s*$""", re.I)
water = re.compile(r"""blue serve (water|3)(\\n)*\s*$""", re.I)
cookiess = re.compile(r"""blue serve (cookies and milk|a|cookies n milk)(\\n)*\s*$""", re.I)
ppizza = re.compile(r"""blue serve (pineapple pizza|b)(\\n)*\s*$""", re.I)

#feelings regex
coins = re.compile(r"""blue add ([0-9]+)( [^""]+)? coins(\\n)*\s*""", re.I)
hug = re.compile(r"""blue send hug(s)? to ([^""]+)(\\n)*\s*""", re.I)
pat = re.compile(r"""blue send pats to ([^""]+)(\\n)*\s*""", re.I)
loves = re.compile(r"""blue send love to ([^""]+)(\\n)*\s*""", re.I)
bonk = re.compile(r"""blue bonk ([^""]+)(\\n)*\s*""", re.I)
get_id = re.compile(r"""(blue )(fetch|get)( id of )([^""]+)(\\n)*\s*""", re.I)
get_karma = re.compile(r"""blue (fetch|get) details of ([^""]+)(\\n)*\s*""", re.I)
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
jok_r = "placeholder"
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
  jok : jok_r,
  quote: jok_r
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
  unmutereg,
  ban,
  get_admin_list,
  stalk,
  stop_stalk,
  get_stalk,
  enableai,
  disableai
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
  get_karma
]


cookiejar= [
  "xSVbOxLCnlTTFeauJd5uJA,MjE4NzA2NDQ%3D--bb9b6f95d04f3fef6eabd6a4017334ab857db974",
  "N7RFTEQW3EzUwDorc5Wz_Q,MjE4NzA2NTM%3D--0718c0f094f71439315a9b128f0f302de1fd96d4",
  "NVRCb9M44uLRyAlo8yfgJw,MjE4NzA2NjE%3D--2d60a92c557ae7fe41dc104eba77472f6a7d419d",
  "ovlhF6XEj5PFvP4qE7qS9A,MjE4NzA2NzY%3D--d5200f1ea1b9dfaa0525b69cf19da50407c01b2a",
  "-6nPAoiXGz3mfpCyw24fWA,MjE4NzA3MDM%3D--cb0d4c773267f1b9b61f98cf175f68b6e434a0c7",
  "VEwTHg6Co4xCBOe-JYSaRg,MjE4NzA3MTk%3D--72af0a6a29671e63615b40f8a0472ebc8832bf06",
  "9IqALEksUGTAiCdDgTbB0A,MjE4NzA3MzY%3D--7338b57b479d30aae6ae8d608633aa33b9569ee5",
  "hAlY3rO0ZUXuy4_93NDAjA,MjE4NzA3NDg%3D--57c8af98b1595b65db4c3a7d9be994d97ec51b26",
  "-q5dfVL6JOJei3UO5laWdw,MjE4NzA3NjI%3D--18add85e2a8bd5a48de270c1e4ae49c96a43a552",
  "xW1WH-eQxo6G1nIj1ZSD3A,MjE4NzA3NzQ%3D--45ef842272ecfbf469884187072e4bea8ea5c33b",
  "Oilbh8oa3lX4BLHLp3cjHw,MjE4NzA3OTU%3D--3bb3a416a06d09cfc5181521b2e1e53867b253fe",
  "UbdV_vLU3EGx5oFE1dB8WQ,MjE5MzM3MDM%3D--ec92a4db3b00710b2e60d6682bb4854eabe03374",
  "Jh3sWxqICCy4MZUdYiPDYw,MjE5MzM3MTU%3D--4f39ad6955240c42dd8254ba07bf5a66a88596e9",
  "igCLMb72JOatS_JNHyrq6Q,MjE5MzM3Mjg%3D--77a6f2f1cbec1645015f4b7cf2cad9fba46cb817",
  "3I86oEZjWw1FOJvx8EBzeA,MjE5MzM3Mzc%3D--84282b5e9800e694b3fcebe0563213d1ddd55a5e",
  "rPyOAJrPPK5F0wH5UvkD1g,MjE5MzM3NDQ%3D--a0f7bd8c01607798b52892b54501a8d878c08894",
  "yOkgE9S4ZWuoeRBCCUpeng,MjE5MzM3NTg%3D--335b1126639d33c3a1635292925ca102f9c901dc",
  "FgZ2cjYRIS8l7PURhHWMWw,MjE5MzM3NzY%3D--b240b615808b7b755787d5e4084281f87a53bb44",
  "XWxLIQP0jGbhzm6Mb4zFng,MjE5MzM3ODY%3D--a3bce059930616dbad2044625a79b8225b959208",
  "WT5q0j8tu1SEvIJuvBuQFw,MjE5MzM4MDQ%3D--5d6971bcdbd71cb3bbbed778b22240c018126f48",
  "h03mkf9bjJgi9vQ71FrvIg,MjE5MzM4MDk%3D--66d3cfddbc5dafd8446d1b34612d86e88539cd22",
  "ZF35vAdhC5nzgH0R6_nTXA,MjE5MzM4MjE%3D--cf5504472c4844b5e2600735502ae97f7381a4b1",
  "7woyqOmFoEKjLuni2udZOg,MjE5MzM4Mjk%3D--342c28a1b657dd8fccc2781399070f7873a8f34f",
  "vH6ZN8uWaQnzR1F4g-OqzQ,MjE5MzM4MzY%3D--4dc0f4f6312e47d9dfe1f0e191d3674aff55c6c2",
  "qxdqE3U53gkgBXYkpdCQmg,MjE5MzM4NDQ%3D--d9d8471a6d1ef4fde09021e9b09d12194e79c94e",
  "c2eszxaU-fUZl7ZirU2kpQ,MjE5MzM4NTQ%3D--48025eebe0849cb1927ae648d0b25c253473d81a",
  "eKWJZKuBFUqK8OTFQPqB2Q,MjE5MzM4NjM%3D--1c685045691d613a650ebf375482268f731d43f7",
  "XhLuDkaYH8kAm7R2KG8Pbg,MjE5MzM4NzI%3D--bd7765eb2c2cf9131b6f6a5e8b60fd8bc3afcc7c",
  "ShVeHeP3DkGoKjhwFyqhuQ,MjE5MzM4ODI%3D--6702e861e5f6a92680add55a9a84160bd38a3dfa",
  "X8LCHmlNnlcCMsatzf2k7A,MjE5MzM4OTk%3D--07539bb53cfd0a2b2b268e391b81f37d05b4e1f1",
  "C0eQwOTd5WSJGMk1sHkaGA,MjE5MzM5MTA%3D--3bbdec9856cd24e9f21a9d11ccb95aeb457e1fad",
  "Eu7ZpPJ3Tpr_PFAl9dPAZg,MjE5MzM5MjA%3D--6830d44ef2d66d4c97fb4a296856280fce2f0d86",
  "a-JBW9TihxpIbQlkg6A7Aw,MjE5MzM5Mjg%3D--07472d182ba153be5179562b1907fc2c7a863bea",
  "Kn7RX-nHCuOeNkWbrcUuxw,MjE5MzM5MzQ%3D--5964e91497f859b80bd604f9442525ac6b9ff52f",
  "Q5xg8ySgcc8jC_NZIap-FQ,MjE5MzM5NDg%3D--3e9c6523d9e1d4bfb2ade428ac4081769c7405a9",
  "HiV7ZBBCe5rWRKvZ-z_nsQ,MjE5MzM5NTg%3D--dce19aa5e45553c6eea57b8fec85236c916a719d",
  "f7s1C2KU_KibOgbRholSRQ,MjE5MzM5NjU%3D--3d2cc01c0eae1761ca3a3bdbdba43359cdf3227a",
  "R-msa0hvlVvI_YT4OPNs1A,MjE5MzM5NzA%3D--1108fad75234ed9811072f09d944c6ff2057fa4d",
  "NSsmftg-q3bJtt_bqkMfmQ,MjE5MzM5ODM%3D--f5967bb49452e11bdec6c05020c7dcc0ae622a3d",
  "bLYhibkpw5Ryi_uP94WO7w,MjE5MzQwMDQ%3D--15986d86145d4343082463cd90cc947cd1bece19",
  "5MvA5aDeV73f8ple9U5IDQ,MjE5MzQwMTQ%3D--fdc25e39782a302b6953917e9b225fc6cf6c3b64"
]
check1 = re.compile(r"""Welcome, [^""]+, to WFAF - Waiting For A Friend. This is a family-friendly group chat you get sent to when you try to message someone who you've sent a friend request to and they haven't accepted your request.\s*""")
check2 = re.compile(r"""Hi, [^""]+, retrying won't help, you can try asking 'what is wfaf' for more info :D\s*""")
check3 = re.compile(r"""Hi again, [^""]+, try asking 'what is wfaf' for more info :D\s*""")
check4 = re.compile(r"""Hello, [^""]+! Welcome to WFAF! - Waiting for a Friend! The place where your dreams used to come true~\s*""")
check5 = re.compile(r"""Hi, [^""]+! I'm afraid they aren't your friend yet, you can always try again!\s*""")
check6 = re.compile(r"""Hi again, [^""]+, don't feel bad, they'll accept one day... hopefully!\s*""")
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
here_for_hours_and_mins = "I've been here for %s hours and %d minutes"
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
Greet_general = "Hi, %s, Welcome to WFAF, which stands for Waiting For A Friend, to which you were sent when you tried texting someone who hasn't accepted/declined your friend request, Enjoy your stay :D "

whos_here_response_no_lurkers = "I can see %s and no lurkers at the moment ~*"
whos_here_response_gen1 = "I can see %s and 1 person lurking ~*"
whos_here_response_gen2 = "I can see %s and %d peeps lurking ~*"

whos_lurking_none = "I can see no lurkers as of now"
whos_lurking_gen = "I can see %s lurking"
id_response = "ID of %s is %s"
