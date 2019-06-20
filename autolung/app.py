"""Main app and GUI

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Controls the main app and gui for the autloung program
"""
import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from main_window import Ui_MainWindow
from load_images import collect
from load_config import load_settings
from export import write_output
from processing import process_img
from measure import measure_all
from metadata import extract_metadata


class Stream(QObject):
    """create Stream class for displaying stdout in MainWindow"""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
    
    def flush(self):
        pass


class ProcessingThread(QThread):
    """Create separate processing thread for main analysis function"""
    progress_update = pyqtSignal(int)

    def __init__(self, imgs_dir, conf_file, prv_choice, outdir):
        QThread.__init__(self)
        self.image_directory = imgs_dir
        self.configuration_file = conf_file
        self.preview_yesNo = prv_choice
        self.output_directory = outdir

    def __del__(self):
        self.wait()

    def process_all(self, images, preview, **parameters):
        """Process images in pipeline"""
        data = []
        num_images = len(images)
        for i, img in enumerate(images, start=1):
            img_name = Path(img).name

            print(f"Processing image {i}/{num_images}...")
            print(f"{img_name}...")
            p = process_img(img, preview, **parameters)
            print(f"Measuring airspace statistics on {img_name}...")
            d = measure_all(p, **parameters)
            print(f"Extracting metadata from {img_name}...")
            md = extract_metadata(img, **parameters)
            print("Done.\n")

            results = {**md, **d}
            data.append(results)

            self.progress_update.emit(i)

        return data

    def run(self):
        """Main image processing pipeline, run when new thread starts"""
        params = load_settings(self.configuration_file)
        images = collect(self.image_directory)
        data = self.process_all(images, self.preview_yesNo, **params)
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
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionHelp.triggered.connect(self.aboutText)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setValue(0)
        self.ui.img_dir_help.clicked.connect(self.imgHelp)
        self.ui.config_help.clicked.connect(self.configHelp)
        self.ui.output_help.clicked.connect(self.outHelp)
        self.ui.preview_help.clicked.connect(self.previewHelp)

        sys.stdout = Stream(newText=self.onUpdateText)

    def imgHelp(self):
        """return message box with help about selecting an image directory"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Image Directory Help")
        msg.setText("Select the directory containing the images to be analyzed")
        msg.setDetailedText("Select the path to the directory containing the images you wish to process.\n\nNOTE: all images must be in .tif format - images in other formats will be ignored.")
        msg.exec()

    def configHelp(self):
        """Return message box with help about config files"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Configuration File Help")
        msg.setText("Select the configuration file for this image set")
        msg.setDetailedText("Select the configuration file for the given image set.\n\nConfiguration files are saved as .ini files and can be edited in NotePad. See the autolung protocol for more details about the construction of configuration files.")
        msg.exec()

    def outHelp(self):
        """Return message box with help about selecting an output directory"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Ouput Directory Help")
        msg.setText("Select the location to save the results")
        msg.setDetailedText("Select to location to save the processing results.\n\nResults are saved as time-stamped .xlsx files in the selected location. See the autoloung protocol for information about the structure of the results file.")
        msg.exec()
    
    def previewHelp(self):
        """Return message box with information on preview QC images"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("QC Image Help")
        msg.setText("Select whether or not you would like to save QC images")
        msg.setDetailedText("If 'Yes' then a four panel image showing the grayscale, thresholded, filled, and labelled images will be saved in the same directory as the images to be processed in a new folder named 'QC'. QC images can be used to check the quality of the processing steps.")
        msg.exec()
    
    def aboutText(self):
        """Return message box with program information"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Autolung")
        msg.setDetailedText("(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University")
        msg.exec()

    def onUpdateText(self, text):
        """redirect stdout to QTextEdit"""
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
        N = len(collect(self.img_dir))  # number of images to be processed
        self.ui.progressBar.setMaximum(N)

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
        """Message box to be displayed once processing is finished"""
        QMessageBox.information(self, "Success!", "Finished Processing!")
    
    def updateProgressBar(self, value):
        """Updates the progressbar"""
        self.ui.progressBar.setValue(value)
    
    def startAnalysis(self):
        """Open a new window and thread to begin image processing if all selections have been made"""
        if self.img_dir and self.config_file and self.out_dir:
            self.processing_thread = ProcessingThread(self.img_dir, self.config_file, self.preview_choice, self.out_dir)
            self.processing_thread.progress_update.connect(self.updateProgressBar)
            self.processing_thread.finished.connect(self.done)
            self.processing_thread.start()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Input Error")
            msg.setText("Missing at least one input parameter!")
            msg.setInformativeText("Check above settings before starting analysis")
            msg.exec()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    app.setWindowIcon(QtGui.QIcon("../docs/autolung_icon.ico"))

    application = MainWindow()
    application.show()

    sys.exit(app.exec())