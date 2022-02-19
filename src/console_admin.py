from var import *
from src.ws import send_message
from src.admin_init import *
from src.general_responses import *
from src.feelings_init import *

def console_input():
    while True:
        text = input()
        name = "Console Admin"
        if consoleinput.match(text):
            content = consoleinput.match(text).group(1)
            send_message(content)
        else:
            whos_here_r = whos_idle_r = []
            whos_here_res = { 
                whos_here: whos_here_r,
                whos_idle: whos_idle_r,
                bored: im_bored_list[random.randint(0, len(im_bored_list)-1)],
                dice: dice_statement % random.randint(1, 6)
            }
            admin_func(text, 0, True)
            matching(fix_name(name),response_dict, text, True, False)
            matching(fix_name(name),whos_here_res, text, True, True)
            coins_feelings(text, id, True)
