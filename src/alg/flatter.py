from os import listdir, mkdir
from os.path import join as os_join, isfile, isdir
import random
import time
from regex import Regex
from shutil import move, rmtree

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
    "folder2_enable": True,
    "folders_ratio": 0.3,
    "random_seed": 2137,
    "file_rename_regex": None,
    "ignore_file_regex": None
}


class Flatter:
    '''
    algorithm responsible for flattening complex folders into flatten based on config
    '''

    def __init__(self, config=DEFAULT_CONFIG):
        self.conf = config

    def set_regex(self, regex):
        self.regex = regex

    def __move_and_log(self, input_file):
        out_filename = self.regex.create_name(input_file)

        folder1_prob = 1.0
        target_path1 = self.conf["folder_output"]
        target_path2 = None
        if self.conf["folder2_enable"]:
            folder1_prob = random.random()
            target_path1 = os_join(self.conf["folder_output"], "1")
            target_path2 = os_join(self.conf["folder_output"], "2")

        out_path = None
        if folder1_prob > self.conf["folders_ratio"]:
            out_path = os_join(target_path1, out_filename)
        else:
            out_path = os_join(target_path2, out_filename)

        move(input_file, out_path)
        self.log.write(f"{input_file} moved_to_==> {out_path}\n")

    def __simulate_move(self, input_file):
        out_filename = self.regex.create_name(input_file)

        folder1_prob = 1.0
        target_path1 = self.conf["folder_output"]
        target_path2 = None
        if self.conf["folder2_enable"]:
            folder1_prob = random.random()
            target_path1 = os_join(self.conf["folder_output"], "1")
            target_path2 = os_join(self.conf["folder_output"], "2")

        out_path = None
        if folder1_prob > self.conf["folders_ratio"]:
            out_path = os_join(target_path1, out_filename)
        else:
            out_path = os_join(target_path2, out_filename)

        self.sim_arr.append((input_file, out_path))

    def __flatten_recur(self, input_path, action=None):
        dirs = listdir(input_path)
        files = [f for f in dirs if isfile(os_join(input_path, f))]
        folders = [f for f in dirs if isdir(os_join(input_path, f))]
        for f in files:
            if self.regex.check_if_ignore(f):
                continue
            full_path = os_join(input_path, f)
            action(full_path)

        for f in folders:
            full_path = os_join(input_path, f)
            self.__flatten_recur(full_path, action)
            # rmtree(full_path)

    def simulate_flatten(self):
        if self.regex is None:
            raise Exception("No regex specified!")

        if self.conf["folder2_enable"]:
            random.seed(self.conf["random_seed"])

        self.sim_arr = []
        self.__flatten_recur(self.conf["folder_input"], self.__simulate_move)
        return self.sim_arr

    def run_flatten(self):
        if self.regex is None:
            raise Exception("No regex specified!")
        
        mkdir(self.conf["folder_output"])
        if self.conf["folder2_enable"]:
            random.seed(self.conf["random_seed"])
            mkdir(os_join(self.conf["folder_output"], "1"))
            mkdir(os_join(self.conf["folder_output"], "2"))

        self.log = open(os_join(self.conf["folder_output"], "move_report.log"), "w")

        self.__flatten_recur(self.conf["folder_input"], self.__move_and_log)
        # rmtree(self.conf["folder_input"])
        self.log.close()

    def retrieve_from_log(self, log_name):
        dest_src = []
        with open(log_name, 'r') as log:
            for line in log:
                dest, source = line.split(" moved_to_==> ")
                source = source[:-1]
                dest_src.append(tuple((dest, source)))
        failed_files = []
        for file in dest_src:
            try:
                move(file[1], file[0])
            except:
                failed_files.append(file[0])
        return failed_files


if __name__ == "__main__":
    ftt = Flatter()
    ftt.set_regex(Regex())
    ftt.run_flatten()
    # print(ftt.retrieve_from_log("test_log_1637710061.4046867.log"))
    # print(ftt.simulate_flatten())
