import pg8000.native
import configparser
from pathlib import Path
from colorama import just_fix_windows_console, Fore
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

def get_table_dict(db_alias):
    table_sql = get_sql("tablesquery", "config.ini")
    table_dict = {}
    table_dict["tables"] = []
    conn = get_connection(db_alias, "config.ini")
    for row in conn.run(table_sql):
        row_dict = {}
        index = 0
        for col in conn.columns:
            row_dict[col['name']] = row[index]
            index = index+1
        table_dict["tables"].append(row_dict)
    return table_dict

def compare(dict1, dict2):
    added = []
    removed = []
    for item in dict1['tables']:
        if item not in dict2['tables']:
            removed.append(item)

    for item in dict2['tables']:
        if item not in dict1['tables']:
            added.append(item)
    return added, removed
    
def print_added(text):
    print(Fore.GREEN + "+" + text)

def print_removed(text):
    print(Fore.RED + "-" + text)

db1_dict = get_table_dict("database1")
db2_dict = get_table_dict("database2")

added, removed = compare(db1_dict, db2_dict)
for item in added:
    print_added(f"|table_catalog:{item['table_catalog']}|table_schema:{item['table_schema']}|table name:{item['table_name']}|")
for item in removed:
    print_removed(f"|table_catalog:{item['table_catalog']}|table_schema:{item['table_schema']}|table name:{item['table_name']}|")
