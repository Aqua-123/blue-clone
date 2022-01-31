import datetime
import json
import os
import random
import re
from concurrent.futures import TimeoutError as ConnectionTimeoutError
from datetime import date, datetime
from os import execl
from sys import argv, executable
from threading import Thread
from time import gmtime, perf_counter, sleep, strftime
from timeit import default_timer as timer

import cleverbotfree
import requests
import websocket
from github import Github
from websocket import create_connection

from vars import *

# Restarts the current program.
def restart_program(): return execl(executable, executable, * argv)
name = " "
starttime = t

def reconnect():
	while connection:
		websocket.enableTrace(False)
		ws = websocket.WebSocket()
		ws.connect(ws_url,cookie=main_cookie, subprotocols=subprots, origin=origin)
		if ws.connected:
			ws.send(json.dumps(connect_json))
			connection = False
		if not ws.connected: sleep(1)


def fix_name(name):
	for chars in forbiden_chars: return name.replace(chars, "")


def send_message(content):
	"""Function for sending messages
	with the argument of content of text"""
	if response_kill == False:
		message = {
			"command": "message",
			"identifier": "{\"channel\":\"RoomChannel\",\"room_id\":null}",
			"data": "{\"message\":\"" + content + "\",\"id\":null,\"action\":\"speak\"}"}
		ws.send(json.dumps(message))


def greet_text(count, name):
	"""Control which message is to be
	send with context to the greet control"""

	if count == 1: return Greet_1%name
	elif count == 2: return Greet_2%name
	elif count == 3: return Greet_general%name


def send_greet(name):
	"""Checks which greet is to be sent 
	with reference to the saved greet_timeout
	stamps in the dictionary"""
	if name in greet_timeout.keys():
		if greet_timeout[name] == "1":
			send_message(greet_text(1, name))
			greet_timeout[name] = "2"
		elif greet_timeout[name] == "2":
			send_message(greet_text(2, name))
			greet_timeout[name] = "3"
		elif greet_timeout[name] == "3": pass
	else:
		send_message(greet_text(3, name))
		greet_timeout[name] = "1"

def list_removal(id):
	if id in timeout_control.keys(): del timeout_control[id]
	if id in list_main_dict.keys(): del list_main_dict[id]
	if id in idle_main_dict.keys(): del idle_main_dict[id]

def greet(action, result, greet):
	"""Function to do greetings and handling of 
	main, idle and stats lists"""
	if (action in b.keys()) and ("user" in b.keys()):
		user = b["user"]
		if "display_name" in user.keys():
			name, id = fix_name(user["display_name"]), user["id"]
			if result == "add":
				list_main.add(name)
				stats_list[id] = list_main_dict[id] = name
				timeout_control[id] = perf_counter()
			elif result == "remove": list_removal(id)
			if (greet == True) and ("id" in user) and (action == "user_connected"):
				stats.append(name)
				timeout_control[id] = perf_counter()
				if (greet_status == True) and str(user["id"]) not in greet_exempt:
					if str(user["id"]) in custom_greet_id.keys():
						send_message(custom_greet_id[str(user["id"])])
					else: send_greet(name)


def get_joke():
	"""Fetches jokes from API mentioned
	and returns it as value of var joke"""
	r = requests.get("https://icanhazdadjoke.com/slack")
	joke = json.loads(r.text)["attachments"][0]["text"]
	send_message(joke)


def get_quote():
	"""Fetches quotes from the API mentioned 
	and returns it as value of var response3"""
	r = requests.get('https://api.quotable.io/random')
	content = str(r.json()['content'])
	author = "~ by " + str(r.json()['author'])
	send_message(content)
	time.sleep(0.2)
	send_message(author)


def threaded_adding(id):
	global whos_here_r, whos_here_res
	r = requests.get(profile_url%id, cookies=cookies)
	r = json.loads(r.text)
	whos_here_r.append(r["user"]["display_name"])

def reply_whos_here():
	whos_here_r = []
	for i in list_main_dict.keys():threads.append(Thread(target=threaded_adding, args=(i,)))
	for t in threads: t.start()
	for t in threads: t.join()
	threads.clear()
	idle_len = len(idle_main_dict.keys())
	whos_here_r = str(whos_here_r)
	if idle_len== 0:response = whos_here_response_no_lurkers%whos_here_r
	elif idle_len > 0:
		if idle_len == 1:response = whos_here_response_gen1%whos_here_r
		elif idle_len > 1: response = whos_here_response_gen2%(whos_here_r,idle_len)
	send_message(fix_message(response))
 
def replying_whos_idle():
	whos_here_res = []
	for i in idle_main_dict.keys(): threads.append(Thread(target=threaded_adding, args=(i,)))
	for t in threads: t.start()
	for t in threads: t.join()
	threads.clear()
	if len(idle_main_dict.keys()) == 0: response = whos_lurking_none
	elif len(idle_main_dict.keys()) > 0:response = whos_lurking_gen%str(whos_here_res)
	send_message(fix_message(response))
 
def matching(dictname, message):
	global whos_here_r, whos_here_res
	keys = list(dictname.keys())
	for i in range(0, len(keys)):
		re_m = keys[i]
		result = re_m.match(message)
		if bool(result) == True:
			if dictname == whos_here_res and re_m == whos_here: reply_whos_here()
			elif dictname == whos_here_res and re_m == whos_idle:replying_whos_idle()
			elif dictname == response_dict and re_m == jok: Thread(target=get_joke).start()
			elif dictname == response_dict and re_m == quote: Thread(target=get_quote).start()
			else: send_message(list(dictname.values())[i])
			break

def fix_message(messages):
	"""Fixes syntactical problems with incomming 
	messages and removes any unwanted chars"""
	chars = ('"[]‘')
	for c in chars: message = message.replace(c, "")
	return (message.replace("'", '').replace("\n", "").strip())


def idle_function():
	"""Function for moving people 
	between idle and main list with reference
	to time stamps in timeout_control"""
	idle_check_list = list(timeout_control.values())
	for i in range(0, len(idle_check_list)):
		x = idle_check_list[i]
		if (t_start - x) >= 240:
			val = list(timeout_control.keys())[i]
			if val in list_main_dict:
				idle_main_dict[val] = list_main_dict[val]
				del list_main_dict[val]
		elif (t_start - x) < 240:
			val = list(timeout_control.keys())[i]
			if val in idle_main_dict: del idle_main_dict[val]


def remove_blue():
	"""Removes blue from all lists 
	to avoid confusion with people"""

	if "Blue" in list_main_dict: del list_main_dict["21550262"]
	if "Blue" in idle_main_dict: del idle_main_dict["21550262"]
	if "Blue" in list(timeout_control.keys()): del timeout_control["21550262"]


def update_git(mute_list):
	new_mute = str(mute_list)
	chars = "[]'\n"
	for c in chars: new_mute.replace(c, "")
	muted_contents = repo.get_contents("muted.txt")
	repo.update_file(muted_contents.path, "mute update", str(new_mute), muted_contents.sha, branch="main")


def mute_func(result, index):
	id = result.group(1)
	if index == 12:
		if id in mute_list: responses = already_ignoring
		else:
			mute_list.append(id)
			update_git(mute_list)
			response = start_ignoring%id
	elif index == 13:
		if id in mute_list:
			mute_list.remove(id)
			update_git(mute_list)
			response = stop_ignoring%id
		else: response = already_not_ignoring%id
	send_message(response)

def downvote(user_id, remem, id): requests.get(karma_url%id, cookies={'remember_token': remem, 'user_id': user_id})


def ban_log(banned_id, admin_id):
	r = requests.get(profile_url%id, cookies=cookies)
	admin_name = json.loads(r.text)["user"]["display_name"]
	banned_logs = repo.get_contents("logs.txt")
	log = admin_name + "(" + str(admin_id) + \
		")"  " banned " + str(banned_id) + "\n"
	repo.update_file(banned_logs.path, "ban-log",
					 banned_logs.decoded_content.decode() + log, banned_logs.sha, branch="main")


def thread(id):
	banned.add(id)
	for c in cookiejar:
		c = c.split(",")
		Thread(target=downvote, args=(c[1], c[0], id,)).start()


def stalker(id, time_now):
	filename = str(id) + ".txt"
	all_files = []
	contents = repo.get_contents("")
	while contents:
		file_content = contents.pop(0)
		if file_content.type == "dir": contents.extend(repo.get_contents(file_content.path))
		else: all_files.append(str(file_content).replace('ContentFile(path="', '').replace('")', ''))
	git_prefix = 'stalker-logs/'
	git_file = git_prefix + filename
	if git_file in all_files:
		logs = repo.get_contents(git_file)
		log = logs.decoded_content.decode()
		repo.update_file(logs.path, "stalker-log",log, logs.sha, branch="main")
	else: repo.create_file(git_file, "committing files", "", branch="main")
	while stalking_log[id][1] == True:
		r = requests.get(profile_url%id, cookies=cookies)
		if r.status_code == 200:
			r = json.loads(r.text)
			name, karma, username, gender, created = r["user"]["display_name"], r["user"][
				"karma"], r["user"]["username"], r["user"]["gender"], r["user"]["created_at"].split("T")
			logs = repo.get_contents(git_file)
			log = logs.decoded_content.decode()
			time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
			text = logging_text%(str(time),name,karma,username,gender)
			log = log + text
			repo.update_file(git_file, "committing files",log, logs.sha, branch="main")
		elif r.status_code == 404 or r is None:
			send_message(stopping_logging%id)
			break
		elif timer() - time_now >= 3600:
			send_message("Stalking session of ID " + str(id))
			break
		else: pass
		sleep(15)
  
def clear_lists():
	send_message(clear_list)
	timeout_control.clear()
	list_main_dict.clear()
	idle_main_dict.clear()

def respond_uptime():
	sr = str(datetime.now() - starttime).split(":")
	if sr[0] == "0":
		if str(int(sr[1])+0) == "0": send_message(just_joined)
		elif (int(sr[1])+0) == 1:send_message(here_for_one_min)
		else: send_message(here_for_x_mins%int(sr[1])+0)
	else: send_message(here_for_hours_and_mins%(sr[0],int(sr[1])+0))
 
def send_stats():
	sr, r =  str(datetime.now() - starttime).split(":"), strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
	response = stats_response%(len(stats),len(stats_list.keys()),sr[0],sr[1],str(r))
	send_message(stats_r)
 
def start_stalking(id):
	if id.isdigit():
		if id not in stalking_log.keys():
			t = Thread(target=stalker, args=(id, timer(),))
			stalking_log[id] = [t, True]
			t.start()
			send_message(waking_stalking)
		else: send_message(already_stalking%id)
	else: send_message(give_valid_id)
 
def stop_stalking(id):
	if id in stalking_log.keys():
		stalking_log[id][1] = False
		del stalking_log[id]
		send_message(stopping_stalking%id)
	else: send_message(already_not_stalking%id)
 
def admin_func_init(i, id , isadmin, result):
	if i == 0:
		greet_status = True
		send_message(done)
	elif i == 1:
		if greet_status == True:
			greet_status = False
			send_message(done)
		elif greet_status == False: send_message(already_not_greeting)
	elif i == 2 and isadmin == True:
		send_message(cya)
		running = False
	elif i == 3 and isadmin == True: clear_lists()
	elif i == 4: respond_uptime()
	elif i == 5:
		greet_timeout = {}
		send_message(memory_loss)
	elif i == 6: send_stats
	elif i == 7 and isadmin == True: send_message(fix_message(str(mute_list)))
	elif i == 8 and isadmin == True: send_message(str(timeout_control))
	elif i == 9:
		send_message(restarting)
		restart_program()
	elif i == 10 and isadmin == True:
		if "display_name" in j.keys(): name = fix_name(j["display_name"])
		del timeout_control[name]
		if name in idle_main: idle_main.remove(name)
		elif name in list_main: list_main.remove(name)
		send_message(aye_aye)
	elif i == 11 and id not in mute_list: send_message(ily_r)
	elif i == 12 or i == 13: mute_func(result, i)
	elif i == 14:
		id_ban = result.group(1)
		thread(id_ban)
		Thread(target=ban_log, args=(id_ban, id,)).start()
		send_message(banning_response%id_ban)
	elif i == 15:
		response = str(admin).replace('"', "").replace("[", "").replace("]", "")
		send_message(response)
	elif i == 16: start_stalking(str(result.group(2)))
	elif i == 17: stop_stalking(str(result.group(2)))
	elif i == 18:
		list1 = list(stalking_log.keys())
		if not list1: send_message(stalking_no_one)
		else: send_message(stalking_following%fix_message(str(list1)))
	elif i == 19:
		aichatstate = True
		send_message(done)
	elif i == 20:
		aichatstate = False
		send_message(done)
 
def admin_func(message, id, isadmin):
	"""Function to handle all the admin 
	and mod commands"""

	for i in range(0, len(admin_commands)):
		result = admin_commands[i].match(message)
		global greet_status, running, name, starttime, aichatstate
		if bool(result) == True: 
			admin_func_init(i, id, isadmin, result)
			break


def coin_handling(result):
	"""Just as the name suggests,
	handles coins and responses to them"""
	num = result.group(1)
	if num.isdigit():
		coin_add = int(num)
		coins_contents = repo.get_contents("coins.txt")
		if (coin_add < 101) and (coin_add > -1):
			coin_new = coin_add + int(coins_contents.decoded_content.decode())
			repo.update_file(coins_contents.path, "coins update", str(
				coin_new), coins_contents.sha, branch="main")
			if num == "1": send_message(adding_one_coin%(int(num) + 0,coin_new))
			else: send_message(adding_coins%(int(num) + 0,coin_new))
		elif coin_add > 100: send_message(too_many_coins)

def send_feelings(index, id, result):
	"""Handles sending and recieving feelings 
	like hugs and love and what not I will be adding
	because yay feelings"""
	response = ""
	name = result.group(1)
	if index == 1: response = sending_love%name
	elif index == 2: response = sending_pats%name
	elif index == 3: response = sending_hugs%name
	if index == 4: response = sending_bonks%name
	elif index == 5:
		name = result.group(4)
		l = list(stats_list.values())
		n = 0
		for re_m in l:
			reg = re.compile(r"" + re_m + "\\n*", re.I)
			result = reg.search(name)
			if result is not None: 
				id_response%(name,list(stats_list.keys())[l.index(re_m)])
				break
			else: n += 1
		if n == len(stats_list.values()): response = not_seen%name
	elif index == 6 and id in admin:
		name = result.group(2)
		id = int(name)
		r = requests.get(profile_url%id, cookies=cookies)
		if r.status_code == 200:
			r = json.loads(r.text)
			name, karma, username, gender, created = r["user"]["display_name"], r["user"]["karma"], r["user"]["username"], r["user"]["gender"], r["user"]["created_at"].split("T")
			if gender is None:details_response_null_gender%(id,name,username,karma,created[0],created[1])
			else: response = details_response%(id,name,username,karma,gender,created[0],created[1])
		elif r.status_code == 404 or i is None: response = account_deleted
		elif r.status_code == 403: response = timeout_error
	send_message(response)


def chat(user_input):
	with cleverbotfree.sync_playwright() as p_w:
		c_b = cleverbotfree.Cleverbot(p_w)
		bot = c_b.single_exchange(user_input)
		send_message(bot)
		c_b.close()


def dis_en_greets(id):
	global greet_status
	if id == "16008266" and greet_status == True:
		send_message(disabling_greet)
		greet_status = False
	elif id == "20909261" and greet_status == False:
		send_message(re_enabling_greet)
		greet_status = True


def check_greeters(message, id):
	global greet_status
	if id in fallback_check:
		for reg_m in greet_check:
			result = reg_m.search(message)
			if message in custom_greet_id.values() or result or message == blue_greet: dis_en_greets(id)
		for reg_m in custom_greet_id.values():
			reg = re.compile(r"" + reg_m + r"", re.I)
			pattern = reg_m + "\s*"
			result = reg.search(message)
			result1 = re.match(pattern, message)
			if result: dis_en_greets(id)

def coins_feelings(message, id):
	for reg_m in coinsandfeelings:
		result = reg_m.match(message)
		if bool(result) == True:
			index = coinsandfeelings.index(reg_m)
			if index == 0: coin_handling(result)
			else: send_feelings(index, id, result)
			break


def log_chats(message, user_id):
	name = fix_name(user["display_name"])
	log = fix_message(message_log_text%(name,user_id,message)) + "\n"
	file = open("chatlogs.txt", "a")
	file.write(log)
	file.close()


def singing():
	send_message("*Sings ~*")
	sleep(2)
	send_message("la la lalla ~*")

def push_logs():
	file = open(chatlog_file, "r")
	contents1 = file.readlines()
	file.close()
	file = open(chatlog_file, "w")
	file.close()
	date = datetime.today().strftime('%d-%m-%Y')
	filename = "log (%s).txt"%date
	all_files = []
	contents = repo.get_contents("")
	while contents:
		file_content = contents.pop(0)
		if file_content.type == "dir": contents.extend(repo.get_contents(file_content.path))
		else: all_files.append(str(file_content).replace('ContentFile(path="', '').replace('")', ''))
	git_prefix = 'wfaf-logs/'
	git_file = git_prefix + filename
	if git_file in all_files:
		logs = repo.get_contents(git_file)
		log = logs.decoded_content.decode()
		for i in contents1: log += i
		repo.update_file(logs.path, "chat-log", log, logs.sha, branch="main")
	else:
		log = ""
		for i in contents1: log += i
		repo.create_file(git_file, "committing files", log, branch="main")

def check_singing():
	len_main = len(list_main_dict.keys()) 
	len_idle =  len(idle_main_dict.keys())
	if (len_main + len_idle) <= 4 and random.randint(0, 1000000) % 9387 == 0: Thread(target=singing).start()

def clocking():
	if reset_clock == 500: greet_timeout, reset_clock = {}, 0
	if timer() - start >= 20 and os.stat("chatlogs.txt").st_size != 0:
		push_logs()
		start = timer()
  
"""Connect blue to whatever"""
websocket.enableTrace(False)
ws = websocket.WebSocket()
ws.connect(ws_url,cookie=main_cookie,subprotocols=subprots,origin=origin)
ws.send(json.dumps(connect_json))
start = timer()
while running == True:
	try:
		remove_blue()
		idle_function()
		t_start = perf_counter()
		reset_clock = reset_clock + 1
		clocking()
		check_singing()
		server_reply = (ws.recv())
		a = json.loads(server_reply)
		whos_here_r = whos_idle_r = []
		whos_here_res = {
			whos_here: whos_here_r,
			whos_idle: whos_idle_r,
			bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
			dice: dice_statement%random.randint(1, 6)
		}
		if ("identifier" in a.keys()) and ("message" in a.keys()):
			b = a["message"]
			Thread(target=greet, args=("user_connected", "add", True,)).start()
			Thread(target=greet, args=("typing", "add", False,)).start()
			Thread(target=greet, args=("user_disconnected", "remove", False,)).start()
			Thread(target=greet, args=("messages", "add", False,)).start()
			if ("messages" in b.keys()) and ("user" in b.keys()):
				user = b["user"]
				if "id" in user.keys():
					id = str(user["id"])
					message = fix_message(str(b["messages"]))
					# if aichatstate == True:
					#   result = ai.match(message)
					#  if result: Thread(target=chat, args=(message,)).start()
					Thread(target=check_greeters, args=(b["messages"], id,)).start()
					Thread(target=log_chats,args=(message,id,)).start()
					if id not in mute_list:
						coins_feelings(message, id)
						matching(response_dict, message)
						matching(whos_here_res, message)
					if id in admin: admin_func(message, id, True)
					elif id in mod: admin_func(message, id, False)
	except ValueError:
		send_message(unknown_error)
		restart_program()