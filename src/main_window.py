from qt import *
import sys
import subprocess
from subprocess import Popen, PIPE
from shutil import which


processor_list = [
    # K42 F
    '18F24K42',
    '18F25K42',
    '18F26K42',
    '18F27K42',
    '18F45K42',
    '18F46K42',
    '18F47K42',
    '18F55K42',
    '18F56K42',
    '18F57K42',
    # K42 LF
    '18LF24K42',
    '18LF25K42',
    '18LF26K42',
    '18LF27K42',
    '18LF45K42',
    '18LF46K42',
    '18LF47K42',
    '18LF55K42',
    '18LF56K42',
    '18LF57K42',
    # Q43
    '18F24Q43',
    '18F25Q43',
    '18F26Q43',
    '18F27Q43',
    '18F45Q43',
    '18F46Q43',
    '18F47Q43',
    '18F55Q43',
    '18F56Q43',
    '18F57Q43',
]


programmer_list = {
    'PICkit4': {
        'command':'ipecmd',
        'target': '-P',
        'source': '-F',
        'flags': [
            '-TPPK4'
            '-M'
        ]
    }, 
    'ICD-U80': {
        'command':'ccsloader',
        'target': '-DEVICE=PIC',
        'source': '-WRITE=',
        'flags': [
            '-AREAS=ALL',
            '-POWER=TARGET'
        ],
    },
}


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("PIC-Multi-Prog")

        self.load_settings()
        
        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.processors = PersistentListWidget('processor_selection', items=processor_list)
        self.processors.itemSelectionChanged.connect(lambda: self.target.setText(self.processors.selected_items()[0]))

        self.programmers = PersistentComboBox('programmer_selection', items=programmer_list)

        self.upload = QPushButton('Upload', clicked=self.start_upload)

        self.filename = QLabel(QSettings().value('filename', ''))
        self.open_file = QPushButton('Open File', clicked=self.open_file_dialog)

        self.target = QLabel(self.processors.selected_items()[0])

        self.tabs = PersistentTabWidget('tabs')

        self.output = QTextEdit(readOnly=True)

        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(QLabel('Select Processor:'))
                    layout.add(self.processors)
                with layout.vbox(5) as layout:
                    layout.add(QLabel('Select Programmer:'))
                    layout.add(self.programmers)
                    with layout.hbox() as layout:
                        layout.add(self.open_file)
                        layout.add(QLabel(), 1)
                    with layout.hbox() as layout:
                        layout.add(QLabel('Filename:'))
                        layout.add(self.filename)
                        layout.add(QLabel(), 1)
                    with layout.hbox() as layout:
                        layout.add(QLabel('Target:'))
                        layout.add(self.target)
                        layout.add(QLabel(), 1)
                    layout.add(self.output, 1)
                    with layout.hbox() as layout:
                        layout.add(QLabel(), 1)
                        layout.add(self.upload)

    def open_file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', self.filename.text(), "Hex files (*.hex)")
        if fname:
            self.filename.setText(fname)
            QSettings().setValue('filename', fname)

    def start_upload(self):
        processor = self.processors.selected_items()[0]
        programmer = programmer_list[self.programmers.currentText()]
        hexfile = self.filename.text()
        
        if hexfile == '':
            return

        cmd = [
            programmer['command'],
            programmer['target'] + processor,
            programmer['source'] + hexfile
        ]

        for flag in programmer['flags']:
            cmd.append(flag)

        print(" ".join(cmd))

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)
        
    def save_settings(self):
        QSettings().setValue("window_geometry", self.saveGeometry())
        QSettings().setValue("window_state", self.saveState())

    def load_settings(self):
        if QSettings().value("window_geometry") is not None:
            self.restoreGeometry(QSettings().value("window_geometry"))
        if QSettings().value("window_state") is not None:
            self.restoreState(QSettings().value("window_state"))
