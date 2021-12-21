import sys
import os
import PySimpleGUI as sg
import path_functions as pf
from path_navigation import Navigator
from icons import folder_icon, file_icon

def add_files_in_folder(dirname): # is parent necessary?
    treedata = sg.TreeData()
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
            treedata.Insert('', fullname, f, values=[], icon=folder_icon)
        else:
            treedata.Insert('', fullname, f, values=[os.stat(fullname).st_size], icon=file_icon)

    return treedata


def window_open(window, path):
    # global window   # should try to change this, heard this isn't good

    treedata = add_files_in_folder(path)

    layout = [[ sg.Button('Up', s = (5)), sg.Button('Back',  s = (5)), sg.Button('Next',  s = (5)), 
                sg.Input(path, 
                        key='-path-', 
                        expand_x=True, 
                        tooltip='Displays current directory. You can input path to a directory and go to it using the Browse button.',
                        size=(80)), 
                sg.Button('Browse',  s = (10))],
              [sg.Tree(data=treedata,
                       headings=['Size'],
                       auto_size_columns=True,
                       num_rows=20,
                       row_height = 25,
                       col0_width=70,
                       def_col_width=5, 
                       key='-TREE-',
                       show_expanded=False,
                       enable_events=True,
                       expand_x=True),
               ],
              [sg.Button('Open',  s = (10)), sg.Button('Cancel', s = (10))]]

    window[0] = sg.Window('File Browser', layout)


def window_refresh(window, path = os.getcwd()):
    
    window[0].close()
    window_open(window, path)
    

# app setup 

sg.change_look_and_feel('DarkGrey14')   # DarkBlue12 DarkBlue13 DarkGrey8 DarkGrey10 DarkGrey14    these ones, I like  ||  change or delete if you want to

event_log = Navigator()
nav = Navigator()
window = [sg.Window('File Browser')]


# app starts here
starting_path = sg.popup_get_folder('Folder to display', history=True, history_setting_filename='search_history', initial_folder='/')
path = pf.format_path(starting_path)

if not os.path.exists(path):
    print('\n Path does not exist! Exiting application... \n')
    sys.exit(0)

nav.append_path(path)
os.chdir(path)
window_refresh(window, path)



while True:  # Event Loop
    event, values = window[0].read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break


    if event == 'Next':  # navigating forwards on the path stack
        event_log.new_direction(event) # adding event to event_log cuz of 'double-click'

        path = nav.forward()
        os.chdir(path)
        window_refresh(window, path)


    if event == 'Back': # navigating backwards on the path stack
        event_log.new_direction(event) # cuz of 'double-click'

        path = nav.backward()
        os.chdir(path)
        window_refresh(window, path)


    if event == 'Up':
        event_log.new_direction(event) # adding event to event_log

        path = pf.find_parent_path(path)
        if os.path.isdir(path):
            nav.new_direction(path) # adding path to top of stack
            os.chdir(path)
            window_refresh(window, path)
        else:
            print('\n Path is not a directory! Reverting to last correct path... \n')
            path = os.getcwd()


    if event == 'Browse': 
        event_log.new_direction(event) # cuz of 'double-click'

        path = pf.format_path(values['-path-'])
        if os.path.isdir(path):
            os.chdir(path)
            path = os.getcwd()
            nav.new_direction(path) # adding path to top of stack
            window_refresh(window, path)
        else:
            print('\n Path is not a directory! Reverting to last correct path... \n')
            path = os.getcwd()


    if event == 'Open':
        event_log.new_direction(event)  # adding event to event_log

        selected = pf.format_path(values["-TREE-"][0]) 
        if os.path.isdir(selected):
            path = selected
            nav.new_direction(path) # adding path to top of stack
            os.chdir(path)
            window_refresh(window, path)
        else:
            os.startfile(selected)


    # TODO: implement proper doubleclick

    if event == '-TREE-': # my take at double-click 
        if event_log.get_current_path() == values['-TREE-'][0]:   # can't register quick double-clicks... dunno why
            selected = pf.format_path(values["-TREE-"][0])
            if os.path.isdir(selected):
                path = selected
                nav.new_direction(path) # adding path to top of stack
                os.chdir(path)
                window_refresh(window, path)
            else:
                os.startfile(selected)
        else:
            event_log.new_direction(values['-TREE-'][0])



window[0].close()

