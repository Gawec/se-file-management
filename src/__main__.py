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
sg.change_look_and_feel('DarkGrey14')
event_log = Navigator()
nav = Navigator()
window = [sg.Window('File Browser')]


def main():
    starting_path = sg.popup_get_folder(
        'Folder to display', history=True, history_setting_filename='search_history', initial_folder='/')
    path = format_path(starting_path)

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
            # adding event to event_log cuz of 'double-click'
            event_log.new_direction(event)

            path = nav.forward()
            os.chdir(path)
            window_refresh(window, path)

        if event == 'Back':  # navigating backwards on the path stack
            event_log.new_direction(event)  # cuz of 'double-click'

            path = nav.backward()
            os.chdir(path)
            window_refresh(window, path)

        if event == 'Up':
            event_log.new_direction(event)  # adding event to event_log

            path = find_parent_path(path)
            if os.path.isdir(path):
                nav.new_direction(path)  # adding path to top of stack
                os.chdir(path)
                window_refresh(window, path)
            else:
                print('\n Path is not a directory! Reverting to last correct path... \n')
                path = os.getcwd()

        if event == 'Browse':
            event_log.new_direction(event)  # cuz of 'double-click'

            path = format_path(values['-path-'])
            if os.path.isdir(path):
                os.chdir(path)
                path = os.getcwd()
                nav.new_direction(path)  # adding path to top of stack
                window_refresh(window, path)
            else:
                print('\n Path is not a directory! Reverting to last correct path... \n')
                path = os.getcwd()

        if event == 'Open':
            event_log.new_direction(event)  # adding event to event_log

            selected = format_path(values["-TREE-"][0])
            if os.path.isdir(selected):
                path = selected
                nav.new_direction(path)  # adding path to top of stack
                os.chdir(path)
                window_refresh(window, path)
            else:
                os.startfile(selected)

        if event == 'Flatten':
            event_log.new_direction(event)  # adding event to event_log

            app = QApplication([])
            win = Window()
            win.show()
            app.exec_()

        # TODO: implement proper doubleclick

        if event == '-TREE-':  # my take at double-click
            # can't register quick double-clicks... dunno why
            if event_log.get_current_path() == values['-TREE-'][0]:
                selected = format_path(values["-TREE-"][0])
                if os.path.isdir(selected):
                    path = selected
                    nav.new_direction(path)  # adding path to top of stack
                    os.chdir(path)
                    window_refresh(window, path)
                else:
                    os.startfile(selected)
            else:
                event_log.new_direction(values['-TREE-'][0])

    window[0].close()


if __name__ == "__main__":
    main()
