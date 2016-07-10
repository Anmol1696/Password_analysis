"""
    Contains the main code for analysising the passwords
"""

from src.helping_functions.generic_func import load_file, free_ram
from src.helping_functions.generic_func import dump_json_file

import json
import re
import sys
import time

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

        # All the passwords with which we faced a problem
        self.troubling_passwords = []

        lower_case         = range(97, 123)
        upper_case         = range(65, 91)
        numerical          = range(48, 58)
        symbol             = range(32, 48) + range(91, 97) + range(58, 65) + range(123, 127)

        self.ascii_nums      = {'l' : lower_case, 'u' : upper_case, 'n' : numerical, 's' : symbol}

    def load_init_json(self):
        """
            Called rigth after init
            'l' -> lower_csae, ''
        """
        with open(self.init_json_file) as json_open:
            init_json = json.load(json_open)

        del(json_open)
        
        self.json_dump_folder = init_json['json_dump_folder']

        print 'Loading Password list'
        self.all_passwords      = load_file(init_json['password_list_location'])

        print 'Loading rockyou list'
        self.rockyou_list       = load_file(init_json['rockyou_list_location'])

        print 'Loading common_words'
        self.common_words       = load_file(init_json['common_word_list_location'])

        print 'Forming the Variables'
        self.pass_length        = dict.fromkeys(range(30), 0)

        self.frequancy = {}

        # The dictionary inside a dictionary is defined seperately else the variable does not work
        for i in 'luns':
            self.frequancy[i]           = {}
        
        self.group_length               = dict.fromkeys('luns', None)
        for temp in 'luns':
            self.group_length[temp]     = {}
        
        self.group_num                  = dict.fromkeys('luns', None)
        for temp in 'luns':
            self.group_num[temp]        = {}
        
        self.case_position              = dict.fromkeys('luns', None)
        for temp in 'luns':
            self.case_position[temp]    = {}

        # Variables for the repetations, first element is count second is list of the repeated words
        self.password_repetation        = {'count' : 0, 'repeated_words' : {}}
        self.rockyou_repetation         = {'count' : 0, 'repeated_words' : {}}
        self.common_word_repetation     = {'count' : 0, 'repeated_words' : dict.fromkeys(self.common_words, 0)}

        return 0

    def __group_pass(self, password):
        """
            group the pass as the group type
            Basically group all the lower_case, upper_case, numbers and symbols as one
        """
        group = dict.fromkeys(['l', 'u', 'n', 's'], [])
        
        group['l'] = re.findall("[a-z]+", password)
        group['u'] = re.findall("[A-Z]+", password)
        group['n'] = re.findall("[0-9]+", password)
        group['s'] = re.findall("[\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\[\]\^\_\`\:\;\<\=\>\?\@\{\|\}\~]+", password)

        return group

    def __position(self, password, pass_ord, pass_group, type_position):
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

    def _get_len(self, password):
        """
            return the length of the password
        """
        try:
            self.pass_length[len(password)] += 1
        except:
            self.pass_length[len(password)] = 1

    def _get_case(self, password):
        """
            return the case used as one of ['l', 'u', 'n', 's', 'lu', ....]
        """
        pass_ord = map(ord, password)

        result = ''

        for pass_element in pass_ord:
            for case in 'luns':
                if pass_element in self.ascii_nums[case] and case not in result:
                    result += case
                    continue

        return result

    def _get_frequancy(self, password, case):
        """
            case is the output of __get_case
        """
        pass_ord    = map(ord, password)
        pass_group  = self.__group_pass(password)
        
        for case_type in case:
            # Get frequancy
            for sym in self.ascii_nums[case_type]:
                sym_count_pass = pass_ord.count(sym)
                if sym_count_pass != 0:
                    try:
                        self.frequancy[case_type][chr(sym)] += sym_count_pass
                    except:
                        self.frequancy[case_type][chr(sym)] = sym_count_pass
            
            # Get max size of group
            try:
                self.group_length[case_type][max(map(len, pass_group[case_type]))] += 1
            except: 
                self.group_length[case_type][max(map(len, pass_group[case_type]))] = 1

            # Get the number of groups
            try:
                self.group_num[case_type][len(pass_group[case_type])] += 1
            except: 
                self.group_num[case_type][len(pass_group[case_type])] = 1
    
            # Get Position of the elements
            pos = self.__position(password, pass_ord, pass_group, case_type)

            try:
                self.case_position[case_type][pos] += 1
            except:
                self.case_position[case_type][pos] = 1

    def get_repetations(self):
        """
            From all the passwords, get the number of repetation passwords
        """
        self.set_all_passwords = list(set(self.all_passwords))

        free_ram()
        print 'Starting the repetation check....'
        
        for password in self.set_all_passwords:
            all_passwords_count = self.all_passwords.count(password)
            rockyou_list_count  = self.rockyou_list.count(password)

            if all_passwords_count != 1:
                self.password_repetation['count'] += 1
                self.password_repetation['repeated_words'][password] = all_passwords_count
            
            if rockyou_list_count != 0:
                self.rockyou_repetation['count'] += 1
                self.rockyou_repetation['repeated_words'][password] = rockyou_list_count

            for word in self.common_words:
                if word in password.lower():
                    self.common_word_repetation['count'] += 1
                    self.common_word_repetation['repeated_words'][word] += 1
        free_ram()

        return 0

    def dump_all_variables_to_json(self):
        """
            json dump folder is the location where all the self variables will be dumped as json files
            dump_json_file from the helping functions will e used to perform the dumping
        """
        # Club some variables into one
        repetation = {
            'password_repetation'       : self.password_repetation, 
            'rockyou_repetation'        : self.rockyou_repetation, 
            'common_words_repetation'   : self.common_word_repetation
        }

        analysis = {
            'pass_length'   : self.pass_length,
            'frequancy'     : self.frequancy, 
            'group_length'  : self.group_length, 
            'group_num'     : self.group_num, 
            'case_position' : self.case_position
        }

        file_name_data = {
            'repetation'            : repetation,
            'analysis'              : analysis,
            'troubling_passwords'   : self.troubling_passwords
        }

        for file_name, data in file_name_data.iteritems():
            dump_json_file(str(self.json_dump_folder) + '/' + file_name + '.json', 'w', data)

        return 0

    def get_full_analysis(self):
        """
            This is the main function that calls all the functions and forms the analysis
        """
        print 'Starting the analysis'
        
        for password in self.all_passwords: 
            self._get_len(password)
            case = self._get_case(password)
            try:
                self._get_frequancy(password, case)
            except:
                self.troubling_passwords.append(password)

        self.get_repetations()

        return 0

if __name__ == '__main__':
    start = time.time()
    free_ram()
    
    try:
        init_json_file = sys.argv[1]
    except:
        print sys.argv
        print 'Init json file not mentioned'
        pass
    
    password_obj = PassAnalysis(init_json_file)
    password_obj.load_init_json()
    password_obj.get_full_analysis()
    password_obj.dump_all_variables_to_json()
    
    start = time.stop()
    free_ram()

    print 'Time taken -> ', (stop - start)/60, 'mins'
