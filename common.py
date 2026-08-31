from csv import DictReader, DictWriter
import sys
import os
import click
import json

def add_column_to_dict(dict, key, value):
    for item in dict:
        item[key] = value
    return dict

def write_dict_to_csv(fileobj, dict, operation):
    dict = add_column_to_dict(dict, "operation", operation)
    with open(fileobj.name, 'w', newline='') as csv_file:
        writer = DictWriter(csv_file, fieldnames=dict[0].keys())
        writer.writeheader()
        writer.writerows(dict)

def write_dict_to_json(fileobj, dict, operation):
    dict = add_column_to_dict(dict, "operation", operation)
    with open(fileobj.name, 'w') as json_file:
        json.dump(dict, json_file, indent=4)

def remove_key_and_value(list, key):
    for item in list:
        item.pop(key, None)

def update_value(list, key, value):
    for item in list:
        item[key] = value

def csv_file_to_list(csv_file):
    list_of_dict = []
    with open(csv_file, 'r') as data:
        dict_reader = DictReader(data)
        list_of_dict = list(dict_reader)
    return list_of_dict

def print_added(fileobj, text_output, output_format, dict):
    if fileobj == sys.stdout:
        fileobj.write(click.style("+" + text_output + os.linesep, fg='green'))
    else:
        if output_format == 'json':
            write_dict_to_json(fileobj, dict, "added")
        else:
            write_dict_to_csv(fileobj, dict, "added")

def print_removed(fileobj, text_output, output_format, dict):
    if fileobj == sys.stdout:
        fileobj.write(click.style("-" + text_output + os.linesep, fg='red'))
    else:
        if output_format == 'json':
            write_dict_to_json(fileobj, dict, "removed")
        else:
            write_dict_to_csv(fileobj, dict, "removed")

def print_dict_items(filename, dict, state, output_format):
    for item in dict:
        output = ""
        for k,v in item.items():
            output += f"|{k}:{v}|"
        if state == 'added':
            print_added(filename, output, output_format, dict)
        else:
            print_removed(filename, output, output_format, dict)