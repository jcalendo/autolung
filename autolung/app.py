"""Main app and GUI

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Controls the main app and gui for the autloung program
"""
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from main_window import Ui_MainWindow

from processing import process_all
from load_images import collect
from load_config import load_settings
from export import write_output


class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class ProcessingThread(QThread):
    def __init__(self, imgs_dir, conf_file, prv_choice, outdir):
        QThread.__init__(self)
        self.image_directory = imgs_dir
        self.configuration_file = conf_file
        self.preview_yesNo = prv_choice
        self.output_directory = outdir

    def __del__(self):
        self.wait()

    def run(self):
        """Main image processing pipeline, run when new thread starts"""
        params = load_settings(self.configuration_file)
        images = collect(self.image_directory)
        data = process_all(images, self.preview_yesNo, **params)
        write_output(data, self.output_directory)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Autolung")

        self.img_dir = ""
        self.config_file = ""
        self.out_dir = ""
        self.preview_choice = ""
        self.ui.img_directory_button.clicked.connect(self.getImageDirectory)
        self.ui.config_button.clicked.connect(self.getConfigFile)
        self.ui.output_button.clicked.connect(self.getOutDir)
        self.ui.yes_radioButton.toggled.connect(lambda: self.btnState(self.ui.yes_radioButton))
        self.ui.no_radioButton.toggled.connect(lambda: self.btnState(self.ui.no_radioButton))
        self.ui.run_button.clicked.connect(self.startAnalysis)
        self.ui.quit_button.clicked.connect(self.close)

        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        cursor = self.ui.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textBrowser.setTextCursor(cursor)
        self.ui.textBrowser.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def getImageDirectory(self):
        """Select the images directory and set text in img_dir text field"""
        self.img_dir = str(QFileDialog.getExistingDirectory(self, "Select Image Directory"))
        self.ui.img_dir_text.setText(self.img_dir)

    def getConfigFile(self):
        """Select the config file and set text in congfig text field"""
        self.config_file, _ = QFileDialog.getOpenFileName(self, "Select Config File")
        self.ui.config_text.setText(str(self.config_file))

    def getOutDir(self):
        """Select the output directory and set the text label"""
        self.out_dir = str(QFileDialog.getExistingDirectory(self, "Select Save Location"))
        self.ui.output_text.setText(self.out_dir)

    def btnState(self, btn):
        """Get the value of the preview selection from the radio buttons"""
        if btn.text() == "Yes":
            if btn.isChecked() == True:
                self.preview_choice = btn.text()
        
        if btn.text() == "No":
            if btn.isChecked() == True:
                self.preview_choice = btn.text()
    
    def done(self):
        QMessageBox.information(self, "Success!", "Finished Processing!")
    
    def startAnalysis(self):
        """Open a new window and thread to begin image processing"""
        self.processing_thread = ProcessingThread(self.img_dir, self.config_file, self.preview_choice, self.out_dir)
        self.processing_thread.finished.connect(self.done)
        self.processing_thread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')

    application = MainWindow()
    application.show()

    sys.exit(app.exec())