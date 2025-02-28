# pylint: disable-all
from var import *
from sys import argv, executable
from os import execl
from time import gmtime, strftime
from cairosvg import svg2png
import chess
import os


def fix_message(message):
    chars = ('"[]‘')
    for c in chars:
        message = message.replace(c, "")
    for c in forbiden_chars:
        message = message.replace(c, "")
    message = message.replace(".", ".​")
    return message


def fix_name(name):
    for chars in forbiden_chars:
        name.replace(chars, '')
    return name


def restart_program():
    execl(executable, executable, *argv)


def format_out_list(input_list):
    return ", ".join(input_list)


def curly_replace(text):
    return text.replace("{", "").replace("}", "")


def is_creator(id):
    if id in ("0", "14267520", "24039236"):
        return True


def image_to_link(image):
    link = image["link"].replace("https://", "")
    link = "Image: " + link
    return link


def return_datestring(deltatimedays, date_channel):

    if deltatimedays == 0:
        return ""
    elif deltatimedays == 1:
        return "a day and "
    return "{} days and ".format(deltatimedays)


def board_to_svg(board):
    return chess.svg.board(board)


def svg_to_png(svg):
    return svg2png(bytestring=svg, write_to='output.png')


def chess_imgur():
    link = CLIENT.upload_from_path("output.png")
    os.remove("output.png")
    return link


def return_deltatime(timestamp):
    timestamp = str(timestamp)
    current_time = strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())
    return datetime.strptime(current_time,
                             "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(
                                 timestamp, "%Y-%m-%d %H:%M:%S")

def join_list(list):
    return ", ".join(list)

def process_input_name(input_name):
    input_name = input_name.replace("\n", "").strip()
    me_regex = re.compile(r"m\s*e(\\n)*\b", re.I)
    input_name = re.sub(me_regex, "you", input_name)
    myself_regex = re.compile(r"my\s*self\s*(\\n)*\b", re.I)
    input_name = re.sub(myself_regex, "you", input_name)
    my_regex = re.compile(r"my\s*(\\n)*\b", re.I)
    input_name = re.sub(my_regex, "your", input_name)
    return input_name