import sys
import os
from colorama import just_fix_windows_console, Fore
just_fix_windows_console()

def print_added(fileobj, text):
    if fileobj == sys.stdout:
        fileobj.write(Fore.GREEN + "+" + text + os.linesep)
    else:
        fileobj.write("+" + text + os.linesep)

def print_removed(fileobj, text):
    if fileobj == sys.stdout:
        fileobj.write(Fore.RED + "-" + text + os.linesep)
    else:
        fileobj.write("-" + text + os.linesep)

def print_dict_items(filename, dict, state):
    for item in dict:
        output = ""
        for k,v in item.items():
            output += f"|{k}:{v}|"
        if state == 'added':
            print_added(filename, output)
        else:
            print_removed(filename, output)