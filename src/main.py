#!/usr/bin/env python3

from qtstrap import *
from main_window import MainWindow


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