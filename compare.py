import click
import sys
import logging
from comparison_logic import process_comparison

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(filename='comparison.log', level=logging.DEBUG)

option_output = click.option("-o", "--output", "fileobj", type=click.File("w"), default=sys.stdout, help="Output file name")
option_output_format = click.option("-f", "--output_format", "output_format", type=click.Choice(['csv', 'json'], case_sensitive=False), default='csv', help="Output format: csv or json")

@click.group()
def comparisons():
    pass

commands = {
    "tables": {
        "query": "tables_query",
        "key": "tables"
    },
    "tables_rowcount": {
        "query": "tables_rowcount_query",
        "key": "tables_rowcount"
    },
    "functions": {
        "query": "functions_query",
        "key": "functions"
    }
}

def build_comparison_command(command_name, command_info):
    @option_output
    @option_output_format
    @click.command(name=command_name)
    def command(fileobj, output_format):
        process_comparison(fileobj, output_format, command_info["query"], command_info["key"])
    return command

for command_name, command_info in commands.items():
    command = build_comparison_command(command_name, command_info)
    comparisons.add_command(command)

def main():
    setup_logging()
    comparisons()

if __name__ == '__main__':
    # this is a test comment for code pipeline  testing   
    main()