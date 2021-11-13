'''
    Creates folder, which includes many files under many subdirectories,
    the purpose is to have a script for testing target algorithm.
'''

import os
import random
import string
import shutil

'''
    presets for creating subdirectories
    folder_path             - main folder path, path is taken from the path where code is executed!
    leyer_depth             - how many subdirectories there should be
    elements_per_directory  - how many files should be inside folder
    folders_per_directory   - how many folders should be inside folder
    random_name             - should folders and files have random name or special label
'''
settings = {
    "folder_path": "test",
    "layer_depth": 3,
    "elements_per_directory": 8,
    "folder_per_directory": 2,
    "random_name": False
}


def generate_name():
    '''random names generator, name has 8 letters/digits'''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def check_if_folder_exists():
    '''checks if the folder exists and asks user whether should it be deleted or not'''
    if os.path.isdir(settings["folder_path"]):
        print("Test folder already exists, should it be deleted? y/n")
        while True:
            decision = input()
            if decision == "y":
                shutil.rmtree(settings["folder_path"])
                print("Deleting folder...")
                break
            elif decision == "n":
                print("If so I can't do much, please change setting folder_path.")
                return False
            else:
                print("please write 'y' or 'n'")
    return True


def folder_setup_rec(layer_depth=0, folder_names_arr=[]):
    if settings["layer_depth"] < layer_depth:
        return
    current_path = settings["folder_path"] + \
        ''.join(['/'+s for s in folder_names_arr])
    for i in range(settings["elements_per_directory"]):
        random_name = generate_name()
        label = f"file_{layer_depth}_{i}"
        name = random_name if settings["random_name"] else label
        with open(f"{current_path}/{name}", 'w') as f:
            f.write(label)

    if settings["layer_depth"] == layer_depth:
        return
    for i in range(settings["folder_per_directory"]):
        random_name = generate_name()
        label = f"folder_{layer_depth}_{i}"
        name = random_name if settings["random_name"] else label
        new_paths = folder_names_arr.copy()
        new_paths.append(name)
        os.mkdir(f"{current_path}/{name}")
        folder_setup_rec(layer_depth+1, new_paths)


def main():
    # check if the folder already exists
    if not check_if_folder_exists():
        return

    # create main folder
    os.mkdir(settings["folder_path"])

    # recursively create subfiles and subdirectories
    folder_setup_rec()
    print("Done")


if __name__ == "__main__":
    main()
