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


class Application(BaseApplication):
    def __init__(self) -> None:
        super().__init__()

        self.init_app_info()

        # create window
        self.window = MainWindow()
        self.window.show()

    def init_app_info(self):
        self.setOrganizationName("LDG Electronics")
        self.setOrganizationDomain("LDG Electronics")
        self.setApplicationName("Octoprog")
        self.setApplicationVersion("v1.0")


def run():    
    # Create the Qt Application
    app = Application()

    # Run the main Qt loop
    app.exec_()

if __name__ == "__main__":
    run()