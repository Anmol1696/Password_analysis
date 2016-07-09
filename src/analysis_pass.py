"""
    Contains the main code for analysising the passwords
"""

from src.helping_functions.generic_func import load_file, free_ram

import json
import re

class PassAnalysis:
    """
        All the functions for password analysis
    """
    def __init__(self, init_json_file):
        """
            The init for the class, define all the variables
            init_json_file is the file carrying the information about the required files and words
        """
        self.init_json_file     = init_json_file
        self.all_passwords      = []
        self.common_words       = []
        self.rockyou_list       = []

        self.lower_case         = range(97, 123)
        self.upper_case         = range(65, 91)
        self.numerical          = range(48, 58)
        self.symbol             = range(32, 48) + range(91, 97) + range(58, 65) + range(123, 127)

    def load_init_json(self):
        """
            Called rigth after init
        """
        init_json = json.load(self.init_json_file)
        
        print 'Loading Password list'
        self.all_passwords      = load_file(init_json['password_list_location'])

        print 'Loading rockyou list'
        self.rockyou_list       = load_file(init_json['rockyou_list_location'])

        print 'Loading common_words'
        self.common_words       = load_file(init_json['common_word_list_location'])

        print 'Forming the Variables'
        self.symbol_frequancy   = dict.fromkeys(self.symbol, 0)
        self.symbol_group_length= dict.fromkeys(range(1, 24), 0)

    def __group_pass(self, password):
        """
            group the pass as the group type
            Basically group all the lower_case, upper_case, numbers and symbols as one
        """
        group = dict.fromkeys(['l', 'u', 'n', 's'], [])
        
        group['l'] = re.findall("[a-z]+", password)
        group['u'] = re.findall("[A-Z]+", password)
        group['n'] = re.findall("[0-9]+", password)
        group['s'] = re.findall("[\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\[\\\\\]\^\_\`\:\;\<\=\>\?\@\{\|\}\~]+", password)

        return group


    def _get_len(password):
        """
            return the length of the password
        """

        return len(passwords)

    def _get_case(self, password):
        """
            return the case used as one of ['l', 'u', 'n', 's', 'lu', ....]
        """
        pass_ord = map(ord, password)

        result = ''

        if all(i in self.lower_case for i in pass_ord):
            result += 'l'
        if all(i in self.upper_case for i in pass_ord):
            result += 'u'
        if all(i in self.numerical for i in pass_ord):
            result += 'n'
        if all(i in self.symbol for i in pass_ord):
            result += 's'

        return result

    def _get_frequancy(self, password, case):
        """
            case is the output of __get_case
        """
        pass_ord = map(ord, password)

        if 's' in case:
            # Get symbol frequancy
            for sym in self.symbol:
                if sym in pass_ord:
                    self.symbol_frequancy[sym] += 1
            
            # Get num of symbol
            
