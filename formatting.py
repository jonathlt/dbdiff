from common import write_dict_to_csv, write_dict_to_json
import click
import sys
import os

def print_added(fileobj, text_output, output_format, dict):
    if fileobj == sys.stdout:
        fileobj.write(click.style("not in database1" + text_output + os.linesep, fg='green'))
    else:
        if output_format == 'json':
            write_dict_to_json(fileobj, dict, "added")
        else:
            write_dict_to_csv(fileobj, dict, "added")

def print_removed(fileobj, text_output, output_format, dict):
    if fileobj == sys.stdout:
        fileobj.write(click.style("not in database2" + text_output + os.linesep, fg='red'))
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