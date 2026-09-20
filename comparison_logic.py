from common import csv_file_to_list
from formatting import print_dict_items
from pg_utils import get_data
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def compare(dict1, dict2, dict_key):
    added = []
    removed = []
    for item in dict1[dict_key]:
        if item not in dict2[dict_key]:
            removed.append(item)

    for item in dict2[dict_key]:
        if item not in dict1[dict_key]:
            added.append(item)
    return added, removed

def build_exclusion_list(object_type):
    exclusion_list = []
    exclusions_dir = Path('exclusions')
    object_path = exclusions_dir / object_type
    if not object_path.exists():
        logger.warning(f"No exclusions found for {object_type}.")
        return exclusion_list
    for exclusions_file in object_path.iterdir():
        exclusion_list.extend(csv_file_to_list(exclusions_file))
    return exclusion_list

def exclusions(dict1, dict2, dict_key):
    exclusion_list = build_exclusion_list(dict_key)
    dict1[dict_key] = [func for func in dict1[dict_key] if func not in exclusion_list]
    dict2[dict_key] = [func for func in dict2[dict_key] if func not in exclusion_list]
    return dict1, dict2 
    
def process_comparison(fileobj, output_format, query, key):
    db1_dict = get_data("database1", query, key)
    db2_dict = get_data("database2", query, key)
    db1_dict, db2_dict = exclusions(db1_dict, db2_dict, key)
    added, removed = compare(db1_dict, db2_dict, key)
    print_dict_items(fileobj, added, removed, output_format)