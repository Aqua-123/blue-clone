# pylint: disable-all
from var import *
from sys import argv, executable
from os import execl
from time import gmtime, perf_counter, sleep, strftime
from cairosvg import svg2png
import chess
import os
def fix_message(message):
    chars = ('"[]‘')
    for c in chars:
        message = message.replace(c, "")
    for c in forbiden_chars:
        message = message.replace(c, "")
    message = message.replace(".",".​")
    return message

def fix_name(name):
    for chars in forbiden_chars:
        name.replace(chars, '')
    return name

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    execl(executable, executable, *argv)

def format_out_list(input_list):
    return ", ".join(input_list)

def curly_replace(text):
    return text.replace("{","").replace("}","")

def is_creator(id):
    if id in ("0", "14267520"):
        return True
        
def image_to_link(image):
    link = image["link"].replace("https://", "")
    link = "Image: " + link
    return link

def return_datestring(deltatimedays,date_channel):
    match deltatimedays:
        case 0: return "today"
        case 1: return "yesterday"
        case _: return  "on " + date_channel.split("-")[2] + " " + datetime.strptime(date_channel.split("-")[1], "%m").strftime("%b") + ","

def board_to_svg(board):
    return chess.svg.board(board)

def svg_to_png(svg):
    return svg2png(bytestring=svg,write_to='output.png')

def chess_imgur():
    link = CLIENT.upload_from_path("output.png")
    os.remove("output.png")
    return link

def return_deltatime(timestamp, current_time=strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmtime())):
    return datetime.strptime(current_time, "%a, %d %b %Y %I:%M:%S %p %Z") - datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")