import os
import sys

import PySimpleGUI as sg
from PyQt5.QtWidgets import QApplication

from gui.file_browser import window_refresh
from gui.flatter_gui import Window
from gui.path_functions import find_parent_path, format_path
from gui.path_navigation import Navigator

# Application setup
# DarkBlue12 DarkBlue13 DarkGrey8 DarkGrey10 DarkGrey14
#Default1 for system default theme to be same as pyqt5 for now
sg.change_look_and_feel('Default1')
# event_log = Navigator()
nav = Navigator()
window = [sg.Window('File Browser')]


def main():
    while True:
        starting_path = sg.popup_get_folder('Folder to display', history=True, history_setting_filename='search_history')
    
        if starting_path == sg.WIN_CLOSED:
            print('Exiting application... [user canceled]')
            sys.exit(0)
        
        if os.path.exists(format_path(starting_path)):
            break
        else:
            sg.popup_ok('The path does not seem to exist!', 'Please try again.')




    path = format_path(starting_path)

    # if not os.path.exists(path):
    #     print('\n Path does not exist! Exiting application... \n')
    #     sys.exit(0)

    nav.append_path(path)
    os.chdir(path)
    window_refresh(window)

    while True:  # Event Loop
        event, values = window[0].read()


        if event in (sg.WIN_CLOSED, 'Exit'):
            print('Exiting application... [user canceled]')
            break


        if event == 'Next':  # navigating forwards on the path stack
            path = nav.forward()
            os.chdir(path)
            window_refresh(window)


        if event == 'Back':  # navigating backwards on the path stack
            path = nav.backward()
            os.chdir(path)
            window_refresh(window)


        if event == 'Up':
            path = find_parent_path(path)
            if os.path.isdir(path):
                nav.new_direction(path)  # adding path to top of stack
                os.chdir(path)
                window_refresh(window)
            else:
                print('\n Path is not a directory! Reverting to last correct path... \n')
                path = os.getcwd()


        if event in ('Browse', 'Enter-key'):
            backup_path = os.getcwd()
            path = format_path(values['-path-'])

            try:
                if os.path.isdir(path):
                    os.chdir(path)
                    path = os.getcwd()
                    nav.new_direction(path)  # adding path to top of stack
                    window_refresh(window)
                else:
                    print('\n Path is not a directory! Reverting to last correct path... \n')
                    sg.popup_ok('Path is not a directory!', 'Reverting to last correct path...')
                    path = os.getcwd()
                    window_refresh(window)
            except:
                print('You do not have the permission to access this folder!')
                sg.popup_ok('You do not have the permission to access this folder!', 'Aborting action...', keep_on_top=True)
                os.chdir(backup_path)
                window_refresh(window)

        if event == 'Filter':
            path = os.getcwd()
            filtr = values['-filterBar-']

            try:
                nav.new_direction(path)  # adding path to top of stack
                window_refresh(window,path,True,filtr)
            except:
                print('You do not have the permission to access this folder!')
                sg.popup_ok('You do not have the permission to access this folder!', 'Aborting action...', keep_on_top=True)
                os.chdir(backup_path)
                window_refresh(window)

        if event in ('Open', '-TREE-_double_clicked', '-TREE-Open') :
            backup_path = os.getcwd()

            try:
                selected = format_path(values["-TREE-"][0])
            except IndexError:
                print('Nothing was selected. Canceling action...')
            else:
                try:    
                    if os.path.isdir(selected):
                        path = selected
                        nav.new_direction(path)  # adding path to top of stack
                        os.chdir(path)
                        window_refresh(window, path)
                    else:
                        os.startfile(selected)
                except PermissionError:
                    print('You do not have the permission to access this folder!')
                    sg.popup_ok('You do not have the permission to access this folder!', 'Aborting action...', keep_on_top=True)

                    os.chdir(backup_path)
                    window_refresh(window)
  
  
        if event == 'Flatten':

            app = QApplication([])
            win = Window()
            win.show()
            app.exec_()


    window[0].close()


if __name__ == "__main__":
    main()

        # if event == '-TREE-':  # my previous take at double-click
        #     # can't register quick double-clicks... dunno why
        #     if event_log.get_current_path() == values['-TREE-'][0]:
        #         selected = format_path(values["-TREE-"][0])
        #         if os.path.isdir(selected):
        #             path = selected
        #             nav.new_direction(path)  # adding path to top of stack
        #             os.chdir(path)
        #             window_refresh(window, path)
        #         else:
        #             os.startfile(selected)
        #     else:
        #         event_log.new_direction(values['-TREE-'][0])
