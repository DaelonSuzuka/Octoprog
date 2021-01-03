from qt import *
from shutil import which
import os
from pathlib import Path


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
            '-TPPK4',
            '-M'
        ],
        'garbage': [
            'log.*',
            'MPLABXLog.xml',
            'MPLABXLog.xml*',
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
        'garbage': []
    },
}


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("PIC-Multi-Prog")

        self.setAcceptDrops(True)

        self.load_settings()
        
        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.target = QLabel('')

        def update_selected_processor():
            selection = self.processors.selected_items()
            if selection:
                self.target.setText(selection[0])
            else:
                self.target.setText('')

        self.processors = PersistentListWidget('processors', items=processor_list, changed=update_selected_processor)
        update_selected_processor()
        
        self.programmers = PersistentComboBox('programmers', items=programmer_list)
        self.upload = QPushButton('Upload', clicked=self.start_upload)
        self.filename = QLabel(QSettings().value('filename', ''))
        self.open_file = QPushButton('Open File', clicked=self.open_file_dialog)
        self.output = QTextEdit(readOnly=True)

        self.status = QLabel('Ready')
        self.worker = QProcess(self)
        self.worker.readyReadStandardOutput.connect(lambda: self.output.append(str(self.worker.readAll(), 'utf-8')))
        
        self.worker.finished.connect(self.upload_finished)

        self.widgets = [
            self.processors,
            self.programmers,
            self.upload,
            self.open_file,
        ]

        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(QLabel('Select Processor:'))
                    layout.add(self.processors)
                with layout.vbox(5) as layout:
                    with layout.hbox(align='left') as layout:
                        layout.add(QLabel('Programmer:'))
                        layout.add(self.programmers)
                    with layout.hbox(align='left') as layout:
                        layout.add(QLabel('Filename:'))
                        layout.add(self.filename)
                        layout.add(self.open_file)
                    with layout.hbox(align='left') as layout:
                        layout.add(QLabel('Target:'))
                        layout.add(self.target)
                    layout.add(QLabel())
                    with layout.hbox(align='left') as layout:
                        layout.add(self.upload)
                    with layout.hbox(align='left') as layout:
                        layout.add(QLabel('Status:'))
                        layout.add(self.status)
                    layout.add(QLabel())
                    layout.add(QLabel('Output:'),)
                    layout.add(self.output, 1)

    def open_file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', self.filename.text(), "Hex files (*.hex)")
        if fname:
            self.filename.setText(fname)
            QSettings().setValue('filename', fname)

    def start_upload(self):
        processor = self.target.text()
        if processor == '':
            self.output.setText('Please select a target processor.')
            return

        hexfile = self.filename.text()
        if hexfile == '':
            self.output.setText('Please select a hex file.')
            return

        programmer = programmer_list[self.programmers.currentText()]
        if which(programmer['command']) == None:
            self.output.setText('Programmer software not found.')
            return

        self.status.setText('Uploading')
        self.lock()

        command = [
            programmer['command'],
            programmer['target'] + processor,
            programmer['source'] + hexfile
        ]

        for flag in programmer['flags']:
            command.append(flag)

        self.output.clear()
        self.output.append(" ".join(command))
        self.worker.start(" ".join(command))

    def upload_finished(self, exit_code):
        if exit_code == 0:
            self.status.setText('Success')
        else:
            self.status.setText('Failed')

        programmer = programmer_list[self.programmers.currentText()]
        for file in programmer['garbage']:
            if '*' in file:
                for f in Path().glob(file):
                    if os.path.isfile(f):
                        os.remove(f)
            else:
                if os.path.isfile(file):
                    os.remove(file)
        
        self.unlock()

    def lock(self):
        for widget in self.widgets:
            widget.setEnabled(False)

    def unlock(self):
        for widget in self.widgets:
            widget.setEnabled(True)

    def dragEnterEvent(self, event):
        prefix = 'file:///'
        strip = len(prefix)
        
        if event.mimeData().hasUrls():
            if len(event.mimeData().urls()) != 1:
                event.ignore()
                return

            text = event.mimeData().text()
            if text[-4:] != '.hex':
                event.ignore()
                return

            if text[:strip] != prefix:
                event.ignore()
                return

            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        prefix = 'file:///'
        strip = len(prefix)

        filename = event.mimeData().text()[strip:]
        if os.path.isfile(filename):
            self.filename.setText(filename)

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
