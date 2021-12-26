from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QCheckBox, QFileDialog, QFormLayout, QGridLayout, QHBoxLayout, QInputDialog, QVBoxLayout, QLineEdit, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox, QTabWidget, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Flatter')

        self.tabs = QTabWidget()

        self.dimmableWidgets1 = []
        self.createTab1()
        self.tabs.addTab(self.tab_1, "Flatten")

        self.createMenu()

    def createMenu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("Flatter")
        self.fileMenu.addAction('Close', self.close)

    def on_tab_1_button_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select an image file",  "Initial file name", "*.png;*.jpg;*.jpeg")
        self.tab_1_pixmap = QPixmap(fileName)
        self.tab_1.resize(self.tab_1_pixmap.width(),
                          self.tab_1_pixmap.height())
        self.tab_1_label.setPixmap(self.tab_1_pixmap)

    def _dimm1(self):
        for w in self.dimmableWidgets1:
            w.setEnabled(self.checkbox_folder2.isChecked())

    def createTab1(self):
        self.tab_1 = QWidget()
        outer_layout = QVBoxLayout()

        options_layout = QFormLayout()

        # Button for selecting target folder
        open_source_folder = QPushButton(self.tab_1)
        open_source_folder.setText("Select")
        # self.tab_1_button.clicked.connect(self.on_tab_1_button_clicked)
        options_layout.addRow("Source Folder", open_source_folder)

        # Button for selecting source folder
        open_target_folder = QPushButton(self.tab_1)
        open_target_folder.setText("Select")
        # self.tab_1_button.clicked.connect(self.on_tab_1_button_clicked)
        options_layout.addRow("Target Folder", open_target_folder)

        # Checkbox for enabling two folders output
        self.checkbox_folder2 = QCheckBox()
        self.checkbox_folder2.stateChanged.connect(self._dimm1)
        options_layout.addRow("Split to two folders", self.checkbox_folder2)

        # Folders ratio input field
        self.ratio_input = QLineEdit()
        ratio_validator = QRegExpValidator(
            QRegExp("[0-9]{2}"), self.ratio_input)
        self.ratio_input.setValidator(ratio_validator)
        self.ratio_input.setEnabled(False)
        self.dimmableWidgets1.append(self.ratio_input)
        options_layout.addRow("Folder ratio in %", self.ratio_input)

        # Random seed input field
        self.seed_input = QLineEdit()
        seed_validator = QRegExpValidator(QRegExp("[0-9]{4}"), self.seed_input)
        self.seed_input.setValidator(seed_validator)
        self.seed_input.setEnabled(False)
        self.dimmableWidgets1.append(self.seed_input)
        options_layout.addRow("Seed for RNG", self.seed_input)

        outer_layout.addLayout(options_layout)

        self.tab_1.setLayout(outer_layout)

        self.setCentralWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()
