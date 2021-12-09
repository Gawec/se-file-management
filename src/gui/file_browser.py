import sys
import os
import PySimpleGUI as sg
import path_functions as pf
from path_navigation import Navigator
from icons import folder_icon, file_icon

starting_path = sg.popup_get_folder('Folder to display', history=True, history_setting_filename='search_history', initial_folder='This PC')
starting_path = pf.format_path(starting_path)   # just in case of random ///////////   or    D:/    or    D:

event_log = Navigator()
nav = Navigator()
nav.append_path(starting_path)

if not starting_path:
    sys.exit(0)

treedata = sg.TreeData()



def add_files_in_folder(parent, dirname):
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
            treedata.Insert(parent, fullname, f, values=[], icon=folder_icon)
        #add_files_in_folder(fullname, fullname)
        else:
            treedata.Insert(parent, fullname, f, values=[
                os.stat(fullname).st_size], icon=file_icon)


def window_refresh():
    global window   # should try to change this, heard this isn't good
    layout = [[sg.Input(starting_path, 
                        key='-path-', 
                        expand_x=True, 
                        tooltip='Displays current directory. You can input path to a directory and go to it using the Browse button.'), 
                        sg.Button('Browse'), sg.Button('Back'), sg.Button('Next')],
              [sg.Tree(data=treedata,
                       headings=['Size', ],
                       auto_size_columns=True, # should try {expand_x = True} instead
                       num_rows=20,
                       col0_width=40,
                       key='-TREE-',
                       show_expanded=False,
                       enable_events=True),
               ],
              [sg.Button('Open'), sg.Button('Up'), sg.Button('Cancel')]]
    window = sg.Window('File Browser', layout)

add_files_in_folder('', starting_path)
window_refresh()

while True:  # Event Loop
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == 'Next':  # navigating forwards on the path stack
        path = nav.forward()
        event_log.new_direction(event) # adding event to event_log

        treedata = sg.TreeData()
        add_files_in_folder('', path)
        starting_path = path
        window_refresh()

    if event == 'Back': # navigating backwards on the path stack
        path = nav.backward()
        event_log.new_direction(event) # adding event to event_log
        
        treedata = sg.TreeData()
        add_files_in_folder('', path)
        starting_path = path
        window_refresh()

    if event == 'Browse': # implemented browse feature
        path = pf.format_path (values['-path-'])

        event_log.new_direction(event) # adding event to event_log
        nav.new_direction(path) # adding path to top of stack

        treedata = sg.TreeData()
        add_files_in_folder('', path)
        starting_path = path
        window_refresh()

    # TODO: implement opening files through doubleclick

    if event == 'Open':
        event_log.new_direction(event)  # adding event to event_log
        selected = ((values["-TREE-"][0]).replace('/', '\\')) 

        if os.path.isdir(selected):
            nav.new_direction(selected) # adding path to top of stack
            treedata = sg.TreeData()
            add_files_in_folder('', selected)
            window_refresh()
            starting_path=selected
        else:
            os.startfile(selected)

    if event == 'Up':
        event_log.new_direction(event) # adding event to event_log
        nav.new_direction(starting_path) # adding path to top of stack
        path = pf.find_parent_path(starting_path) # did this to fix folder_up() 

        treedata = sg.TreeData()
        add_files_in_folder('', path)  # changed os.path.dirname(starting_path) to path
        starting_path = path # just in case
        window_refresh()

    if event == '-TREE-': # my take at double-click 
        if event_log.get_current_path() == values['-TREE-'][0]:   # can't register quick double-clicks
            selected = ((values["-TREE-"][0])).replace('/', '\\')  
            if os.path.isdir(selected):
                nav.new_direction(selected) # adding path to top of stack

                treedata = sg.TreeData()
                add_files_in_folder('', selected)
                starting_path = selected
                window_refresh() 
            else:
                os.startfile(selected)
        else:
            event_log.new_direction(values['-TREE-'][0])



window.close()

'''
maybe make this a function:

        treedata = sg.TreeData()
        add_files_in_folder('', path)
        starting_path = path
        window_refresh() # need to change this to a function that refreshes the window and not creates a new one
'''