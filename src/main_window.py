from qtstrap import *
from shutil import which
import os
from pathlib import Path
from programmer_data import processor_list, programmer_list


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAcceptDrops(True)
        
        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.target = QLabel('')

        def update_selected_processor():
            selection = self.processors.selected_items()
            if selection:
                self.target.setText(selection[0])
            else:
                self.target.setText('')

        self.processors = PersistentListWidget('processor', items=processor_list, changed=update_selected_processor)
        update_selected_processor()
        
        self.programmers = PersistentComboBox('programmer', items=programmer_list)
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