import pg8000.native
import configparser
from pathlib import Path
from colorama import just_fix_windows_console, Fore
import click
import sys
import os
just_fix_windows_console()

def get_connection(db_alias, ini_file):
    config_object = configparser.ConfigParser()
    with open(ini_file,"r") as file_object:
        config_object.read_file(file_object)
    port=config_object.get(db_alias,"port")
    user=config_object.get(db_alias,"user")
    host=config_object.get(db_alias,"host")
    password=config_object.get(db_alias,"password")
    database=config_object.get(db_alias,"database")
    return pg8000.native.Connection(user=user, 
                                    host=host, 
                                    port=port, 
                                    password=password, 
                                    database=database)

def get_sql(query_name, ini_file):
    sql = None
    config_object = configparser.ConfigParser()
    with open(ini_file,"r") as file_object:
        config_object.read_file(file_object)
    file=config_object.get(query_name, "sqlfile")
    with open(Path(file)) as file_object:
        sql = file_object.read()
    return sql

def get_dict(db_alias, queryname, dictkey):
    sql = get_sql(queryname, "config.ini")
    dict = {}
    dict[dictkey] = []
    conn = get_connection(db_alias, "config.ini")
    for row in conn.run(sql):
        row_dict = {}
        index = 0
        for col in conn.columns:
            row_dict[col['name']] = row[index]
            index = index+1
        dict[dictkey].append(row_dict)
    return dict

def compare(dict1, dict2, dictkey):
    added = []
    removed = []
    for item in dict1[dictkey]:
        if item not in dict2[dictkey]:
            removed.append(item)

    for item in dict2[dictkey]:
        if item not in dict1[dictkey]:
            added.append(item)
    return added, removed
    
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

option_output = click.option("-o", "--output", "fileobj", type=click.File("w"), default=sys.stdout, help="Output file name")

@click.group()
def comparisons():
    pass

@option_output
@click.command()
def tables(fileobj):

    db1_dict = get_dict("database1", "tablesquery", "tables")
    db2_dict = get_dict("database2", "tablesquery", "tables")

    added, removed = compare(db1_dict, db2_dict, "tables")
    print_dict_items(fileobj, added, "added")
    print_dict_items(fileobj, removed, "removed")

@option_output
@click.command()
def functions(fileobj):
    db1_dict = get_dict("database1", "functionsquery", "functions")
    db2_dict = get_dict("database2", "functionsquery", "functions")

    added, removed = compare(db1_dict, db2_dict, "functions")
    print_dict_items(fileobj, added, "added")
    print_dict_items(fileobj, removed, "removed")

comparisons.add_command(tables)
comparisons.add_command(functions)

if __name__ == '__main__':
    comparisons()