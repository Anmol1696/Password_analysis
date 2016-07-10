"""
    All the helping functions that will be used
"""

import os
import sys
import time
import json

def free_ram():
    """
        just cleans the ram from the caches
    """
    print 'Freeing Ram..'
    os.system('echo 1 > /proc/sys/vm/drop_caches')
    time.sleep(1)
    
    return 0

def load_file(file_name):
    """
        Load txt file into the variable, txt file is a list
    """
    file_open = open(file_name, 'r')
    all_lines = file_open.readlines()
    file_open.close()

    free_ram()
    variable = [line.split('\n')[0] for line in all_lines]
    free_ram()

    return variable

def dump_json_file(json_file_name, open_type, dict_data):
    """
        Dump the json data into the file
        open_type is 'w'or 'a'
    """
    free_ram()
    with open(json_file_name, open_type) as json_file:
        json.dump(dict_data, json_file)
    free_ram()

def clean_dict_tree(dict_data, default_value, dict_keys='luns'):
    """
        this will propogate through the dict and at the lowest level, clean the dict i.e. remove the keys with the default values
    """
    for key in dict_keys:
        for child_key, value in dict_data[key].iteritems():
            if value == default_value:
                dict_data[key].__delitem__(child_key)

        if dict_data[key]:
            dict_data.__delitem__(key)
    
    return dict_data
