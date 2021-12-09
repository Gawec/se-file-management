
# path-changing functions
def find_parent_path(path = '../'):
    '''return path of parent folder of current path'''
    if not path_is_okay(path):
        path = fix_path(path)
        return path
    
    if path == 'D:\\':
        return path
    if path == 'C:\\':
        return path

    path = path.replace('\\', '/')

    split_path = path.split('/')
    folder_list = [x for x in split_path if x != ''] # x is folder name
    parent_path = ''.join(folder + '/' for folder in folder_list[:-1])[:-1]

    if path_is_okay(parent_path):
        return parent_path
    else:
        return fix_path(parent_path)
        

def format_path(path):
    '''removes unnecessary "/" characters and returns a directory path-like string   ||   fixes some mistakes with root folder'''
    if not path_is_okay(path):
        path = fix_path(path)
        return path

    if path == 'D:\\':
        return path
    if path == 'C:\\':
        return path

    path = path.replace('\\', '/')

    split_path = path.split('/')
    folder_list = [x for x in split_path if x != ''] # x is folder name
    formated_path = ''.join(folder + '/' for folder in folder_list)[:-1]

    if path_is_okay(formated_path):
        return formated_path
    else:
        return fix_path(formated_path)

# conversion functions
def convert_to_path(folders_list):
    '''convert list into a directory path-like string separated by "/" '''
    path = ''.join(folder + '/' for folder in folders_list)[:-1]
    return path


def convert_to_folder_list(path):
    '''convert a directory path-like string separated by "/" into a list'''

    split_path = path.split('/')
    folder_list = [x for x in split_path if x != ''] # x is folder name
    return folder_list

# check-it and fix-it functions
def path_is_okay(_path):
    '''checks if some rules are not of paths are not followed'''
    path = _path.upper()
    if path[0] != 'C' and path[0] != 'D':
        print('Error: this path does not seem to be correct. \n Root folder must be "C:\\" or "D:\\"')
        return False

    if path == 'C' or path == 'C:' or path == 'C:/':
        print('Error: this path might cause unexpected behaviour. \n The recommended root folder is "C:\\" or "D:\\"')
        return False

    if path == 'D' or path == 'D:' or path == 'D:/':
        print('Error: this path causes unexpected behaviour. \n The recommended root folder is "C:\\" or "D:\\"')
        return False
    
    if path[1] != ':':
        print('Error: this path does not seem to be correct. \n Root folder must be "C:\\" or "D:\\"')
        return False

    if len(path) >= 4:
        if path[2] != '/' and path[2] != '\\':
            print('Error: this path does not seem to be correct. \n Root folder must be "C:\\" or "D:\\"')
            return False
    return True


def fix_path(_path):
    '''checks if some rules are not of paths are not followed and tries to fix them'''
    unsafe_paths = ['D:', 'D:/', 'C:', 'C:/']
    path = _path.upper()

    # if path is root convert to safe-root
    if path == 'D' or path == 'D:' or path == 'D:/' or path == 'D/' or path == 'D\\':
        return 'D:\\'

    if path == 'C' or path == 'C:' or path == 'C:/' or path == 'C/' or path == 'C\\':
        return 'C:\\'

    # return 'C:\' if root folder is bad
    if path[0] != 'C' and path[0] != 'D':
        return 'C:\\'    
         
    if path[1] != ':':
        return 'C:\\'    

    if len(path) >= 4:
        if path[2] != '/' and path[2] != '\\':
            return 'C:\\'    

    return _path
