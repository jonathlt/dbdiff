from pg_utils import get_data, build_exclusion_list, get_database_name
from common import print_dict_items
import click
import sys
import logging

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(filename='comparison.log', level=logging.DEBUG)

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

def exclusions(dict1, dict2, dictkey):
    exclusion_list = build_exclusion_list(dictkey)
    dict1[dictkey] = [func for func in dict1[dictkey] if func not in exclusion_list]
    dict2[dictkey] = [func for func in dict2[dictkey] if func not in exclusion_list]
    return dict1, dict2 
    
option_output = click.option("-o", "--output", "fileobj", type=click.File("w"), default=sys.stdout, help="Output file name")
option_outputformat = click.option("-f", "--outputformat", "outputformat", type=click.Choice(['csv', 'json'], case_sensitive=False), default='csv', help="Output format: csv or json")

@click.group()
def comparisons():
    pass

@option_output
@option_outputformat
@click.command()
def tables(fileobj, outputformat):
    db1_dict = get_data("database1", "tablesquery", "tables")
    db2_dict = get_data("database2", "tablesquery", "tables")
    db1_dict, db2_dict = exclusions(db1_dict, db2_dict, "tables")
    added, removed = compare(db1_dict, db2_dict, "tables")
    print_dict_items(fileobj, added, "added", outputformat)
    print_dict_items(fileobj, removed, "removed", outputformat)

@option_output
@option_outputformat
@click.command()
def tablesrowcount(fileobj, outputformat):
    db1_dict = get_data("database1", "tablesrowcountquery", "tablesrowcount")
    db2_dict = get_data("database2", "tablesrowcountquery", "tablesrowcount")
    db1_dict, db2_dict = exclusions(db1_dict, db2_dict, "tablesrowcount")
    added, removed = compare(db1_dict, db2_dict, "tablesrowcount")
    print_dict_items(fileobj, added, "added", outputformat)
    print_dict_items(fileobj, removed, "removed", outputformat)

@option_output
@option_outputformat
@click.command()
def functions(fileobj, outputformat):
    db1_dict = get_data("database1", "functionsquery", "functions")
    db2_dict = get_data("database2", "functionsquery", "functions")
    db1_dict, db2_dict = exclusions(db1_dict, db2_dict, "functions")
    added, removed = compare(db1_dict, db2_dict, "functions")
    print_dict_items(fileobj, added, "added", outputformat)
    print_dict_items(fileobj, removed, "removed", outputformat)

comparisons.add_command(tables)
comparisons.add_command(functions)
comparisons.add_command(tablesrowcount)

def main():
    setup_logging()
    comparisons()

if __name__ == '__main__':
    # this is a test comment for code pipeline testing
    main()