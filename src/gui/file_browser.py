import os

import PySimpleGUI as sg

# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)
folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

def add_files_in_folder(dirname):  # is parent necessary?
    treedata = sg.TreeData()
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
            treedata.Insert('', fullname, f, values=[], icon=folder_icon)
        else:
            treedata.Insert('', fullname, f, values=[
                            os.stat(fullname).st_size], icon=file_icon)

    return treedata

def find_files_in_folder(dirname, find):
    treedata = sg.TreeData()
    files = os.listdir(dirname)
    for f in files:
        if f == find:
            fullname = os.path.join(dirname, f)
            if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
                treedata.Insert('', fullname, f, values=[], icon=folder_icon)
            else:
                treedata.Insert('', fullname, f, values=[
                            os.stat(fullname).st_size], icon=file_icon)

    return treedata

def exclude_files_in_folder(dirname, find):
    treedata = sg.TreeData()
    files = os.listdir(dirname)
    for f in files:
        if f != find:
            fullname = os.path.join(dirname, f)
            if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
                treedata.Insert('', fullname, f, values=[], icon=folder_icon)
            else:
                treedata.Insert('', fullname, f, values=[
                            os.stat(fullname).st_size], icon=file_icon)

    return treedata

def window_open(window, path, filtr_active, exclude_active, filtr):
    # global window   # should try to change this, heard this isn't good

    if filtr_active == False and exclude_active == False:
        treedata = add_files_in_folder(path)
    elif filtr_active == True:
        treedata = find_files_in_folder(path, filtr)
    else:
        treedata = exclude_files_in_folder(path,filtr)

    layout = [[sg.Button('Up', s=(5)), sg.Button('Back',  s=(5)), sg.Button('Next',  s=(5)),
               sg.Input(path,
                        key='-path-',
                        expand_x=True,
                        tooltip='Displays current directory. You can input path to a directory and go to it using the Browse button.',
                        size=(80)),
               sg.Button('Browse',  s=(10))],
              [
               sg.Input(filtr,
                        key='-filterBar-',
                        expand_x=True,
                        tooltip='You can input phrase for which the program will filter in the directory',
                        size=(30)),
               sg.Button('Filter',  s=(10)),sg.Button('Exclude',  s=(10))
              ],
              [sg.Tree(data=treedata,
                       headings=['Size'],
                       auto_size_columns=True,
                       num_rows=20,
                       row_height=25,
                       col0_width=70,
                       def_col_width=5,
                       key='-TREE-',
                       show_expanded=False,
                       enable_events=True,
                       expand_x=True),
               ],
              [sg.Button('Exit', s=(10)), sg.Button('Open',  s=(10)), sg.Button('Flatten',  s=(10)), sg.Button('Enter-key', bind_return_key = True, visible = False)]]

    window[0] = sg.Window('File Browser', layout, finalize = True)
    window[0]['-TREE-'].bind('<Double-Button-1>', '_double_clicked')
    window[0]['-TREE-'].bind('<Return>', 'Open')

def window_refresh(window, path = '_empty_', filtr_active = False, exclude_active = False, filtr = ''):  # path = os.getcwd() doesn't work propertly it returns the initial working dir from when the app started
    if path == '_empty_' or not os.path.exists(path):
        path = os.getcwd()

    window[0].close()
    window_open(window, path, filtr_active, exclude_active, filtr)
