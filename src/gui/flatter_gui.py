import os
import sys

from alg.flatter import Flatter
from alg.regex import Regex
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QFileDialog, QFormLayout,
                             QGridLayout, QHBoxLayout, QInputDialog, QLabel,
                             QLineEdit, QMainWindow, QMessageBox,
                             QPlainTextEdit, QPushButton, QSpinBox, QTabWidget,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout,
                             QWidget)

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Flatter')

        self.tabs = QTabWidget()

        self.ftt = Flatter()
        self.regex = Regex()
        self.ftt.set_regex(self.regex)
        self.simulation = None

        self.dimmableWidgets1 = []
        self.createTab1()
        self.tabs.addTab(self.tab_1, "Flatten")

        self.createMenu()

    def createMenu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("Flatter")
        self.fileMenu.addAction('Close', self.close)

    def __update_simulation(self):
        if self.ftt.conf["folder_input"] != "" and self.ftt.conf["folder_output"] != "":
            try:
                self.simulation = self.ftt.simulate_flatten()
                self.__target_tree_fill(self.targetTree)
                self.run_flatter.setEnabled(True)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(
                    "Wrong target or source folder selected!\n\n" + str(e))
                msg.setWindowTitle("Error")
                msg.exec_()

    def __source_tree_fill(self, tree, path):
        for element in os.listdir(path):
            path_info = os.path.join(path, element)
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                self.__source_tree_fill(parent_itm, path_info)
                parent_itm.setIcon(0, QIcon('./assets/folder.ico'))
            else:
                parent_itm.setIcon(0, QIcon('./assets/file.ico'))

    def __target_tree_fill(self, tree):
        tree.clear()
        log = QTreeWidgetItem(tree, ["move_report.log"])
        log.setIcon(0, QIcon('assets/file.ico'))
        if self.ftt.conf["folder2_enable"]:
            folder_1 = QTreeWidgetItem(tree, ["1"])
            folder_1.setIcon(0, QIcon('assets/folder.ico'))
            for f in self.simulation[1][0]:
                file_1 = QTreeWidgetItem(folder_1, [f])
                file_1.setIcon(0, QIcon('assets/file.ico'))

            folder_2 = QTreeWidgetItem(tree, ["2"])
            folder_2.setIcon(0, QIcon('assets/folder.ico'))
            for f in self.simulation[1][1]:
                file_2 = QTreeWidgetItem(folder_2, [f])
                file_2.setIcon(0, QIcon('assets/file.ico'))
        else:
            for f in self.simulation[1][0]:
                file = QTreeWidgetItem(tree, [f])
                file.setIcon(0, QIcon('assets/file.ico'))

    def __on_select_source(self):
        folderName = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folderName == '':
            return
        self.ftt.conf["folder_input"] = folderName
        self.sourceTree.clear()
        self.__source_tree_fill(self.sourceTree, folderName)
        self.__update_simulation()

    def __on_select_target(self):
        folderName = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.ftt.conf["folder_output"] = folderName
        self.__update_simulation()

    def __on_checkbox(self):
        for w in self.dimmableWidgets1:
            w.setEnabled(self.checkbox_folder2.isChecked())
        self.ftt.conf["folder2_enable"] = self.checkbox_folder2.isChecked()
        self.__update_simulation()

    def __on_change_ratio(self):
        if self.ratio_input.text() != '':
            self.ftt.conf["folders_ratio"] = 0.01 * \
                float(self.ratio_input.text())
            self.__update_simulation()

    def __on_change_seed(self):
        if self.seed_input.text():
            self.ftt.conf["random_seed"] = 0.01 * float(self.seed_input.text())
            self.__update_simulation()

    def __on_run_flatter(self):
        msg = QMessageBox()
        try:
            self.ftt.run_flatten()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Success")
            msg.setInformativeText(
                "Flattened folder!\n\n")
            msg.setWindowTitle("Success")
            msg.exec_()
        except Exception as e:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(
                "Failed to run flatter!\n\n" + str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def createTab1(self):
        self.tab_1 = QWidget()
        outer_layout = QVBoxLayout()

        options_layout = QFormLayout()

        # Button for selecting target folder
        open_source_folder = QPushButton(self.tab_1)
        open_source_folder.setText("Select")
        open_source_folder.clicked.connect(self.__on_select_source)
        options_layout.addRow("Source Folder", open_source_folder)

        # Button for selecting source folder
        open_target_folder = QPushButton(self.tab_1)
        open_target_folder.setText("Select")
        open_target_folder.clicked.connect(self.__on_select_target)
        options_layout.addRow("Target Folder", open_target_folder)

        # Checkbox for enabling two folders output
        self.checkbox_folder2 = QCheckBox()
        self.checkbox_folder2.stateChanged.connect(self.__on_checkbox)
        options_layout.addRow("Split to two folders", self.checkbox_folder2)

        # Folders ratio input field
        self.ratio_input = QLineEdit()
        ratio_validator = QRegExpValidator(
            QRegExp("[0-9]{2}"), self.ratio_input)
        self.ratio_input.setValidator(ratio_validator)
        self.ratio_input.setEnabled(False)
        self.ratio_input.setText(str(self.ftt.conf["folders_ratio"]))
        self.ratio_input.textChanged.connect(self.__on_change_ratio)
        self.dimmableWidgets1.append(self.ratio_input)
        options_layout.addRow("Folder ratio in %", self.ratio_input)

        # Random seed input field
        self.seed_input = QLineEdit()
        seed_validator = QRegExpValidator(QRegExp("[0-9]{4}"), self.seed_input)
        self.seed_input.setValidator(seed_validator)
        self.seed_input.setEnabled(False)
        self.seed_input.setText(str(self.ftt.conf["random_seed"]))
        self.seed_input.textChanged.connect(self.__on_change_seed)
        self.dimmableWidgets1.append(self.seed_input)
        options_layout.addRow("Seed for RNG", self.seed_input)

        outer_layout.addLayout(options_layout)

        # folder trees
        trees_layout = QHBoxLayout()

        self.sourceTree = QTreeWidget()
        self.sourceTree.setHeaderLabel("Source Folder")
        trees_layout.addWidget(self.sourceTree)

        self.targetTree = QTreeWidget()
        self.targetTree.setHeaderLabel("Simulated Target Folder")
        trees_layout.addWidget(self.targetTree)

        outer_layout.addLayout(trees_layout)

        # execute button
        execute_layout = QVBoxLayout()

        self.run_flatter = QPushButton(self.tab_1)
        self.run_flatter.setText("Run Flatter")
        self.run_flatter.clicked.connect(self.__on_run_flatter)
        self.run_flatter.setEnabled(False)
        execute_layout.addWidget(self.run_flatter)

        outer_layout.addLayout(execute_layout)

        self.tab_1.setLayout(outer_layout)

        self.setCentralWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()