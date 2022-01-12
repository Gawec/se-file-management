# TODO: create proper implementation
from fnmatch import fnmatch
from pathlib import Path


class Regex:
    """class resposible for creating names of files based on their path and regex format"""

    def __init__(self):
        self.accept_pattern = ["*.txt"]
        return

    def set_folder_main_path(self, main_path):
        self.main_path = main_path

    def create_name(self, filepath):
        """Creates file name based on filepath and set regex"""
        path = filepath.replace(self.main_path, "")
        name = ""
        for s in Path(path).parts:
            if s not in path:
                continue
            name += s + "_"
        return name[2:-1]

    def set_accept_pattern(self, pattern):
        self.accept_pattern = pattern.split(",")

    def check_if_accept(self, filepath, ignore=False):
        """Returns true or false whether a file should be ignored based on regex and its name"""
        for pattern in self.accept_pattern:
            if fnmatch(filepath, pattern):
                return not ignore

        return ignore
