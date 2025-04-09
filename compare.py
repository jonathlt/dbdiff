from pg_utils import get_data
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
    
option_output = click.option("-o", "--output", "fileobj", type=click.File("w"), default=sys.stdout, help="Output file name")

@click.group()
def comparisons():
    pass

@option_output
@click.command()
def tables(fileobj):
    db1_dict = get_data("database1", "tablesquery", "tables")
    db2_dict = get_data("database2", "tablesquery", "tables")
    added, removed = compare(db1_dict, db2_dict, "tables")
    print_dict_items(fileobj, added, "added")
    print_dict_items(fileobj, removed, "removed")

@option_output
@click.command()
def functions(fileobj):
    db1_dict = get_data("database1", "functionsquery", "functions")
    db2_dict = get_data("database2", "functionsquery", "functions")
    added, removed = compare(db1_dict, db2_dict, "functions")
    print_dict_items(fileobj, added, "added")
    print_dict_items(fileobj, removed, "removed")

comparisons.add_command(tables)
comparisons.add_command(functions)

if __name__ == '__main__':
    setup_logging()
    comparisons()