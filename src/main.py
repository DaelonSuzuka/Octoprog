#!/usr/bin/env python3

from qt import *
import signal


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


class Application(QApplication):
    def __init__(self) -> None:
        super().__init__()

        self.init_app_info()

        # create window
        self.window = MainWindow()
        self.window.show()

    def init_app_info(self):
        self.setOrganizationName("LDG Electronics")
        self.setOrganizationDomain("LDG Electronics")
        self.setApplicationName("PIC-Multi-Prog")
        self.setApplicationVersion("v0.1")


def run():    
    # Create the Qt Application
    app = Application()

    def ctrlc_handler(sig, frame):
        app.window.close()
        app.shutdown()

    # grab the keyboard interrupt signal 
    signal.signal(signal.SIGINT, ctrlc_handler)

    # Run the main Qt loop
    app.exec_()

if __name__ == "__main__":
    run()