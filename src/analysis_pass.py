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

        lower_case         = range(97, 123)
        upper_case         = range(65, 91)
        numerical          = range(48, 58)
        symbol             = range(32, 48) + range(91, 97) + range(58, 65) + range(123, 127)

        self.ascii_nums      = {'l' : lower_case, 'u' : upper_case, 'n' : numerical, 's' : symbol}

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
        self.frequancy = {}
        for i in 'luns':
            self.frequancy[i]   = dict.fromkeys(self.ascii_nums[i], 0)
        
        self.group_length       = dict.fromkeys(['luns', dict.fromkeys(range(1, 24), 0))
        
        self.group_num          = dict.fromkeys(['luns'], dict.fromkeys(range(1, 10), 0))
        
        self.case_position      = dict.fromkeys(['luns']dict.fromkeys(['s', 'm', 'e', 'se'], 0))

        # Variables for the repetations, first element is count second is list of the repeated words
        self.password_repetation        = {'count' : 0, 'repeated_words' : []}
        self.rockyou_repetation         = {'count' : 0, 'repeated_words' : []}
        self.rockyou_part_repetation    = {'count' : 0, 'repeated_words' : []}
        self.common_word_repetation     = {'count' : 0, 'repeated_words' : dict.fromkeys(self.common_words, 0)}

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

    def __position(password, pass_ord, pass_group, type_position):
        """
            Get the position of the first element of the group
            Gives the position of uppercase, numeric and symbols only
            's' -> start, 'm' -> middle, 'e' -> end, 'se' -> start and end
        """
        start   = pass_ord[0]
        end     = pass_ord[-1]
        result  = ''

        if start in self.ascii_nums[type_position]:
            result += 's'
        if end in self.ascii_nums[type_position]:
            result += 'e'

        if not result and pass_group[type_position]:
            result = 'm'

        return result

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

        for case in 'luns':
            if all(i in self.ascii_nums[case] for i in pass_ord):
                result += case

        return result

    def get_frequancy(self, password, case):
        """
            case is the output of __get_case
        """
        pass_ord    = map(ord, password)
        pass_group  = __group_pass(password)

        for case_type in case:
            # Get frequancy
            for sym in self.ascii_nums[case_type]:
                if sym in pass_ord:
                    self.frequancy[case_type][sym] += 1
            
            # Get max size of group
            self.group_length[case_type][max(map(len, pass_group[case_type]))] += 1
            # Get the number of groups
            self.group_num[case_type][len(pass_group[case_type])] += 1
            # Get Position of the elements
            pos = __position(password, pass_ord, pass_group, case_type)
            self.case_position[case_type][pos] += 1

    def get_repetations(self):
        """
            From all the passwords, get the number of repetation passwords
        """
        self.set_all_passwords = list(set(self.all_passwords))

        free_ram()
        for password in self.set_all_passwords:
            if self.all_passwords.count(password) != 1:
                self.password_repetation['count'] += 1
                self.password_repetation['repeated_words'].append(password)
            if self.rockyou_list.count(password) != 0:
                self.rockyou_repetation['count'] += 1
                self.rocktou_repetation['repeated_words'].append(password)

            for word in self.common_words:
                if word in password.lower():
                    self.common_words_repetation['count'] += 1
                    self.common_words_repetation['repeated_words'][word] += 1
