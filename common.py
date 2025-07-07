from csv import DictReader
import sys
import os
import click

def remove_key_and_value(list, key):
    for item in list:
        item.pop(key, None)

def update_value(list, key, value):
    for item in list:
        item[key] = value

def csvfile_to_list(csvfile):
    list_of_dict = []
    with open(csvfile, 'r') as data:
        dict_reader = DictReader(data)
        list_of_dict = list(dict_reader)
    return list_of_dict

def print_added(fileobj, text):
    if fileobj == sys.stdout:
        fileobj.write(click.style("+" + text + os.linesep, fg='green'))
    else:
        fileobj.write("+" + text + os.linesep)

def print_removed(fileobj, text):
    if fileobj == sys.stdout:
        fileobj.write(click.style("-" + text + os.linesep, fg='red'))
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