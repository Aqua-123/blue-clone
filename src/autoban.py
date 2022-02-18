from blue import data 
from admin import thread
from time import perf_counter
from var import *
def landmine_checker(message,id):
    for word in data["landmine_words"]:
        regex1 = re.compile(r"%s"% word, re.I)
        if regex1.search(message):
           thread(id)
           break

def spam_controlling(id):
    global spam_timeout
    if id in spam_timeout:
        spam_timeout[id].append(perf_counter())
    else:
        spam_timeout[id] = [perf_counter()]

def spam_checker():
    for id in spam_timeout:
        if id not in banned:
            if len(spam_timeout[id]) >= 3 and spam_timeout[id][-1] - spam_timeout[id][-3] < 1.3:
                    thread(id)
                    break
            elif len(spam_timeout[id]) >= 5 and spam_timeout[id][-1] - spam_timeout[id][-5] < 3:
                    thread(id)
                    break