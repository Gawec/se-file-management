from PyQt5.QtWidgets import QApplication
from gui_qt.gui import Window

if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()