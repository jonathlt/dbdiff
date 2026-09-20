from common import write_dict_to_csv, write_dict_to_html
import click
import sys
import os

def format_output(fileobj, dict_added, dict_removed, output_format):

    if output_format == 'text':
        for item in dict_added:
            output = ""
            for k,v in item.items():
                output += f"|{k}:{v}|"
            fileobj.write(click.style("added" + output + os.linesep, fg='green'))
        for item in dict_removed:
            output = ""
            for k,v in item.items():
                output += f"|{k}:{v}|"  
            fileobj.write(click.style("removed" + output + os.linesep, fg='red'))

    elif output_format == 'csv':
        for item in dict_added:
          item["operation"] = "added"
        for item in dict_removed:
          item["operation"] = "removed"
        merged_dict = dict_added + dict_removed
        write_dict_to_csv(fileobj, merged_dict)

    elif output_format == 'html':
        for item in dict_added:
          item["operation"] = "added"
        for item in dict_removed:
          item["operation"] = "removed"
        merged_dict = dict_added + dict_removed
        write_dict_to_html(fileobj, merged_dict)        
     

def print_dict_items(filename, dict_added, dict_removed, output_format):
    format_output(filename, dict_added,dict_removed, output_format)