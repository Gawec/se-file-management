import os
import random
import shutil

'''
    examplary config needed to be passed to alg to perform its task
    {
        folder_input        - name of the input folder (str)
        folder_output       - folder to which files will be moved (str)
        log_filename        - log filename (str)
        folder2_enable      - if True, files will be divided to two folders (bool)
        folder2_output      - second folder to which files will be put (str)
        folders_ratio       - number between 0 and 1 expressing file ratio folder1/folder2 (float)
        random_seed         - seed for random file creation (int)
        ignore_file_regex   - string regex of files, that should be ignored (str/None)
    }
'''

DEFAULT_CONFIG = {
    "folder_input": "test",
    "folder_output": "test_out",
    "log_filename": "test_log",
    "folder2_enable": False,  # TODO: enable to test
    "folder2_output": "test_out2",
    "folders_ratio": 0.3,
    "random_seed": 2137,
    "ignore_file_regex": None
}


class Flatter:
    '''
    algorithm responsible for flattening complex folders into flatten based on config
    '''

    def __init__(self, config=DEFAULT_CONFIG):
        self.conf = config
        self.regex = None

    def set_regex(self, regex):
        self.regex = regex

    def run_flatten(self):
        if self.regex is None:
            raise Exception("No regex specified!")
        
        
