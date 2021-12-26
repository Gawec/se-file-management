# TODO: create proper implementation
from pathlib import Path


class Regex:
    '''class resposible for creating names of files based on their path and regex format'''

    def __init__(self):
        return

    def set_folder_main_path(self, main_path):
        self.main_path = main_path

    def create_name(self, filepath):
        '''Creates file name based on filepath and set regex'''
        path = filepath.replace(self.main_path, '')
        name = ''
        for s in Path(path).parts:
            if s not in path:
                continue
            name += s + "_"
        return name[2:-1]

    def check_if_ignore(self, filepath):
        '''Returns true or false whether a file should be ignored based on regex and its name'''
        return False
