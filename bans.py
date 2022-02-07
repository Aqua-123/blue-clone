import websocket
import time
import threading
import re
import cl
from unidecode import unidecode
import json
import requests
from github import Github
import datetime
from sys import executable,argv
from os import execl
import os

user = "Aqua-123"
passw = "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"
g = Github(passw)
repo = g.get_user().get_repo("Ban")
contents = repo.get_contents("bannn/Logs.txt")

exempted = [
	23207460,
	16986137,
	22975867
]
print(contents)

list_id =  ["48","56","33","39","38","40","34","51","58","57","41","54","37","53","43","42","49","55","59","44","46","36","60","52","32","50","47","35","45"]
cookies1 = "user_id=MjExNzQ2MDg%3D--a4763efe1b8631066fdee681d54eec7ba278ca9e"
banned = set()
spam_check = {}
connection = True
cookies = [
	"pdVeGU8z0xEWE3AwXLtwYg,MjEzNjU0OTg%3D--22f0619fded0f807a9f6bec0850b50fa5e25f283",
	"wPlIJoPs4CJBiRFiRBI5Hg,MjEzNjU1Mjg%3D--8caad3b6c0d62bf15fa4eabd5a4be98c8881d0d9",
	"nQU9oEUxRM4z63SIhalv7A,MjEzNjU1NDQ%3D--fab39000eef642962df0039babc8ccd00423f77b",
	"-h20PQOizKpllMfHkfTdTQ,MjEzNjU2MTg%3D--287779803c32817c186ef3411bbceb617530d818",
	"Z2hEYzGFNXN_5mlJLxNQ7g,MjEzNjU2Mjc%3D--2d9e9d1d45decc5e62ebd977a6534f95a096fe15",
	"vfxhUamleQGWlQwlg3jy8g,MjEzNjU3MTU%3D--c57d93efdbc6fcab8dee26aa420cd22be614b080",
	"tfkSU6nSC3FGPsh-Ohj3bQ,MjEzNjU4ODA%3D--9533c0c3f24e1474594c9d90d6d0bc56a72f59be",
	"VKF9907M03rH8F_GWy0bRg,MjEzNjU4OTc%3D--42c71fa03d22c6a0662f214c0df83514d2bbb139",
	"ulU86iRKETxIzVlsdJJL6g,MjEzNjU5MDY%3D--fbd6f4345f8bcc829fef2d9ccf82bc7f3eeb0494",
	"8yLj3E9K1VPbDVv97JExrg,MjEzNjU5MjA%3D--d1f2fd73fcb212f69416d31e3389840c5396dfcb",
	"whBt9EGjFgpew7qFxYcEsA,MjEzNjU5Mjk%3D--21f3f34505388ee373020484a3d55f8130562fc4",
	"r2S8TGourJGZyrWFxpnH0Q,MjEzNjU5MzY%3D--3f8c552b1553ed11bc85d95df6b2bc73770f29f4",
	"E7Ot6EAqxsuJXG_ru3ZNaw,MjEzNjU5Njc%3D--5ed9d8dc86d3057ef3de3a6d8ec87c6d8c08d677",
	"fpftMA7Gneh7EqWaFfIhvA,MjEzNjU5OTY%3D--e98b8be80a745a723e229729d24d1924f301f808",
	"od2XycduJCXjEnMvI-F2MQ,MjEzNjYwMDY%3D--12ccd9e5942228b0619dad8026462e40684db06e",
	"op7TQDeEu8uYBrLGzu5sSQ,MjEzNjYwMjU%3D--2d59e0f2d521572207a22c70929fbf1f04b2beb2",
	"X8woOd2h3D5bDXtVZLZGzw,MjEzNjYwNTM%3D--75f559baa47ef1e3c9c0f2fe8a1d90b861dbef7f",
	"OKnqrSUHZqVjBQfcmXq0gQ,MjEzNjYwOTA%3D--54d9af0bfae43010fbb2c8a8a7ec85d79f779c37",
	"g0QR3GzUn9Kz1WwVEEav3A,MjEzNjY2Nzc%3D--680a3871a5461a93be3fa74f98e51e77b59d6fbf",
	"Jq_3qRpe5AHl489oWV-1-A,MjEzNjY3NDU%3D--6a4421fa62199c3a29ccc33261a05de6b3560854",
	"sr4higsfs_F0nweLim0DYw,MjEzNjY3NTc%3D--8417d222c223dd9aadee9924e69e0d6c4f167ffe",
	"bruUIozlXLQ8MeoMAiJneg,MjEzNzA3Mjc%3D--12818a8d4a10225efe9e2be078b4a8874442a4a4",
	"N7aQ3cikb-MjwAEW6DX-8w,MjEzNzA4MTA%3D--38b202cea0084ae79fff84d9d98ca7e28911484f",
	"Q0YV5Z4Thl8MfuFBq4i-eQ,MjEzNzA4NDM%3D--56414bb41c3082b64d07263fec31b384aed098fe",
	"Tt24yftYF9B8aG7xzefSRg,MjEzNzA4NjA%3D--a2d9df9ea0f7265f68ccbab7f0a203baeeca40ad",
	"MiU7Munir06EQ8zWAkUpUw,MjEzNzA4OTM%3D--a80cd9ed407f53b638ad88bce1a4c88b9b56a429",
	"FQlitNwBXoJQOZSKT7bqFA,MjEzNzA5MTU%3D--f59e4a2c013b4380d637e5640bae07d190c9de71",
	"hhoO4V8nN1J4vOMSxCxHDQ,MjEzNzA5NDU%3D--2a41697e2f27507c39b139aaf610edfedaa307b9",
	"zgetfM1ZIxnjH7w6EjvoqQ,MjEzNzA5ODU%3D--1707bc5d04bbdbf292e048b703cf343353aea51c",
	"qcWMS8sLGClA31-qfbBKog,MjEzNzExMDM%3D--8611d01d9d12abc6ac41e38dcb69ff5c7991eb87"
]
def downvote(user_id,remem,id):
	req = requests.get("https://www.emeraldchat.com/karma_give?id="+id+"&polarity=-1=HTTP/2", cookies={'remember_token': remem, 'user_id': user_id})

def thread(id):
	banned.add(id)
	for c in cookies:
		c = c.split(",")
		user_id = c[1]
		remem = c[0]
		threading.Thread(target=downvote, args=(user_id,remem,id,)).start()

restart_program = lambda : execl(executable,executable, * argv)

def connect(n):
	connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n +"\"}"}
	ws.send(json.dumps(connect_json))

def disconnect(n):
	connect_json= {"command":"unsubscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n +"\"}"}
	ws.send(json.dumps(connect_json))

def gitlog(log):
	file = open("Logs.txt","a")
	file.write(log)
	file.close() 
	contents = repo.get_contents("bannn/Logs.txt")
	repo.update_file(contents.path, "ban log", contents.decoded_content.decode() + log, contents.sha, branch="main")
	
websocket.enableTrace(False)
ws = websocket.WebSocket()
ws.connect("wss://www.emeraldchat.com/cable", cookie=cookies1,subprotocols=["actioncable-v1-json", "actioncable-unsupported"],origin="https://www.emeraldchat.com",header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}, timeout = 1000000  )
print(ws.recv())

for i in range (0,len(list_id)):
	n = list_id[i]
	connect(n)
for i in exempted: banned.add(str(i))
def matching(id,name,marker):
	if marker == 2:
		result1 =  word_reg.search(name)
		namedec = unidecode(name).replace("[","").replace("]","")
		result2 = word_reg.search(namedec)
		namereg = re.sub('[\W_]+', '', name)
		result3 = word_reg.search(namedec)
		namesubdec = re.sub('[\W_]+', '', namedec)
		result4 = word_reg.search(namedec)
	elif marker == 1:
		result1 =  name_reg.search(name)
		namedec = unidecode(name)
		result2 = name_reg.search(namedec)
		namereg = re.sub('[\W_]+', '', name)
		result3 = name_reg.search(namedec)
		namesubdec = re.sub('[\W_]+', '', namedec)
		result4 = name_reg.search(namedec)
	if (result1 or result2 or result3 or result4 ) and (id not in banned):
		thread(id)
		log = "banning " + id + " for " + name +    "\n"
		print(log)
		gitlog(log)
cl.cl() 
name_reg = re.compile(r"""\w*(z(i|1|!)o)|rofl x|(BANNER)|(harenoir)|(aqua)|(bresheses)|(Earth diamond)|(Josh x)|(Call me daddy)|(Meine)|(Liebe)|opalchat.?com|(🅾🅿🅰🅻 🅲🅷🅰🆃)|(Gashing Sphere)|(^r$)|(💎)\w*\s*""", re.I)
word_reg = re.compile(r"""\w*(cunt)|(Trysomething(danker)|(lessterrible))|(n+(i|j)+g+g+a+)|(n+x*(i|j|1|l)*gg+[a-z]*r+(s|z)*)|(will rape)|(n+i+gg+o+(z|r|s)+)|(niqqa)|(s+u+k+m+a+d+i+k+)|(sukshit)|(deserve to be raped)|(i wanna rape)|(will|shall|would|should) rape|black (men|cock|d(i|1)ck)|((should be )raped)|(OpalChat.com)|(opalchat.com)|(P𝔸Ｌ𝐂𝐇𝔸TＣom)|(A better Emerald Chat)\w*(\\n)*\s*""", re.I)
while True:
	try:
		server_reply = (ws.recv())
		a = json.loads(server_reply)
		if ("identifier" in a.keys()) and ("message" in a.keys()) :    
			b = a["message"]
			if ("user_connected" in b.keys() or "typing"in b.keys() or "user_disconnected"in b.keys() or "messages"in b.keys()) and ("user" in b.keys()):
				user = b["user"]
				if "display_name" in user.keys():
					name = str(user["display_name"])
					id = str(user["id"])
					matching(id,name,1)
					if "messages" in b.keys() and  "user" in b.keys():
						message = str(b["messages"])
						if "id" in user.keys() : id = str(user["id"])
						if id in spam_check.keys(): spam_check[id].append(time.time())
						else:
							spam_check[id] = []
							spam_check[id].append(time.time())
						matching(id,message.replace("[","").replace("]","").replace("'", "").replace('"',""),2)
		for i in spam_check.keys():
			list1 = list(reversed(spam_check[i]))
			if len(list1) >= 5:
				if list1[0] - list1[4] <3 and  i not in banned:
					thread(i)
					log = "banning " + i + " for spam" + "\n"
					gitlog(log)
			elif len(list1) >= 3 and  list1[0] - list1[2] <1.3 and  i not in banned:
				thread(i)
				log = "banning " + i + " for spam" + "\n"
				gitlog(log)
			else: pass
	except ValueError: pass
