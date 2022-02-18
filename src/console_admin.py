from var import *
from ws import send_message
from admin_init import *
from general_responses import *
from feelings_init import *

def console_input():
    while True:
        text = input()
        name = "Console Admin"
        if consoleinput.match(text):
            content = consoleinput.match(text).group(1)
            send_message(content)
        else:
            admin_func(text, 0, True)
            matching(fix_name(name),response_dict, text, True)
            matching(fix_name(name),whos_here_res, text, True)
            coins_feelings(text, id, True)
