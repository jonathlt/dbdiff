import pg8000.native
import configparser
import logging
import sys
import pathlib
from pathlib import Path, PurePath
from common import csvfile_to_list

logger = logging.getLogger(__name__)

def get_connection(db_alias, ini_file):
    config_object = configparser.ConfigParser()
    try:
        with open(ini_file,"r") as file_object:
            config_object.read_file(file_object)
    except FileNotFoundError:
        print("Problem reading config file. Please check the file exists and is readable.")
        sys.exit(1)
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

def get_database_name(db_alias):
    config_object = configparser.ConfigParser()
    try:
        with open('config.ini',"r") as file_object:
            config_object.read_file(file_object)
    except FileNotFoundError:
        print("Problem reading config.ini file. Please check the file exists and is readable.")
        sys.exit(1)
    return config_object.get(db_alias,"database")

def get_sql(query_name, ini_file):
    sql = None
    config_object = configparser.ConfigParser()
    try:
        with open(ini_file,"r") as file_object:
            config_object.read_file(file_object)
    except FileNotFoundError:
        print("Problem reading config.ini file. Please check the file exists and is readable.")
        sys.exit(1)

    file = config_object.get(query_name, "sqlfile")
    file = pathlib.Path(__file__).parent.resolve() / file

    try:
        with open(Path(file)) as file_object:
            sql = file_object.read()
    except FileNotFoundError:
        print(f"Problem reading SQL file {file}. Please check the file exists and is readable.")
        sys.exit(1)
    logger.debug(f'sql = {sql}')
    return sql

def run_sql(conn, sql, resultkey):
    logger.debug(f"sql {sql}")
    logger.debug(f"resultkey {resultkey}")
    dict = {}
    dict[resultkey] = []
    for row in conn.run(sql):
        row_dict = {}
        index = 0
        for col in conn.columns:
            row_dict[col['name']] = row[index]
            index = index+1
        dict[resultkey].append(row_dict)
    return dict

def get_data(db_alias, queryname, dictkey):
    sql = get_sql(queryname, "config.ini")
    dict = {}
    dict[dictkey] = []
    conn = get_connection(db_alias, "config.ini")
    return run_sql(conn, sql, dictkey)

def build_exclusion_list(object_type):
    exclusion_list = []
    exclusions_dir = Path('exclusions')
    object_path = exclusions_dir / object_type
    if not object_path.exists():
        logger.warning(f"No exclusions found for {object_type}.")
        return exclusion_list
    for exclusions_file in object_path.iterdir():
        exclusion_list.extend(csvfile_to_list(exclusions_file))
    return exclusion_list