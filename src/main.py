#!/usr/bin/env python3

from qtstrap import *
from main_window import MainWindow


try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PySide2.QtWinExtras import QtWin
    myappid = 'LDG.Octoprog.1.0'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def run():    
    # Create the Qt Application
    app = BaseApplication()

    # create window
    window = MainWindow()
    window.show()

    # Run the main Qt loop
    app.exec_()

if __name__ == "__main__":
    run()