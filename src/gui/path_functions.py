import os
from sys import platform

# path-changing functions
def find_parent_path(path = os.getcwd()):
    '''return path of parent folder of current path   ||   should be used in conjunction with os.chdir() so the <cwd> is always the one displayed'''
    
    current_working_path = os.getcwd()

    try:
        os.chdir(path)
        os.chdir(os.pardir)
        path = os.getcwd()
    except:
        print('\n Error occured during path manipulation! \n')
        path = '.'

    os.chdir(current_working_path)
    return path
        

def format_path(path = ''):
    '''removes unnecessary "/" characters and returns a directory path-like string   ||   fixes some mistakes with root folder'''

    if path == '' or path == '/' or path == '\\': # get root directory of <cwd>
        print ('\n Error occured! Path is blank. \n')
        return find_root()
    
    if path == '.': # get <cwd> as absolute path
        return os.getcwd()

    if path == '..': # get parent folder of <cwd> as absolute path
        return find_parent_path('.')

    if platform == 'win32' and len(path) < 4: # append ':/' to single letter path for win32 platform
        return fix_root(path)

    folder_list = convert_to_folder_list(path)
    path = convert_to_path(folder_list)
        
    path = os.path.normpath(path) # getting rid of '/..' and '/.' in a way that makes sense
    path = path.replace('\\', '/') # cuz of linux

    if platform == "linux" or platform == "linux2":
        path = "/" + path

    return path
    
# conversion functions
def convert_to_path(folders_list):
    '''convert list into a directory path-like string separated by "/" '''

    path = ''.join(folder + '/' for folder in folders_list)[:-1]

    return path


def convert_to_folder_list(path):
    '''convert a directory path-like string separated by "/" into a list'''

    path = path.replace('\\', '/')
    split_path = path.split('/')
    folder_list = [x.strip() for x in split_path if x != ''] # x is folder name

    return folder_list



# check-it and fix-it functions
def path_is_okay(path):
    '''checks if some rules are not of paths are not followed  ||  NOT USED ANYMORE'''
    # deprecated
    return os.path.exists(path)

    
def fix_root(_path):
    '''appends ':/' to single letter paths'''
    path = _path.upper()
    if os.path.exists(path):
        return path

    # Some hardcoding just in case

    if path[0].isalpha(): # win32
        if len(path) == 1: 
            print ('function returned a possible root path for given disc letter...')
            return path + ':/'
        elif len(path) == 2:
            if path[1] == ':': # win32
                return path + '/'
        elif len(path) == 3:
            if path[1:3] in (':/', ':\\'): # win32
                return path
            
    print ('function returned root directory of current working folder due to error...')
    return find_root()


def find_root():
    path = os.getcwd()
    parent_path = find_parent_path(path)

    while parent_path != path:
        path = parent_path
        parent_path = find_parent_path(path)

    return path