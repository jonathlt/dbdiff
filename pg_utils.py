import pg8000.native
import configparser
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

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