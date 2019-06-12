# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(742, 736)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.config_button = QtWidgets.QPushButton(self.centralwidget)
        self.config_button.setGeometry(QtCore.QRect(600, 160, 75, 31))
        self.config_button.setObjectName("config_button")
        self.output_button = QtWidgets.QPushButton(self.centralwidget)
        self.output_button.setGeometry(QtCore.QRect(600, 200, 75, 31))
        self.output_button.setObjectName("output_button")
        self.img_directory_button = QtWidgets.QPushButton(self.centralwidget)
        self.img_directory_button.setGeometry(QtCore.QRect(600, 120, 75, 31))
        self.img_directory_button.setObjectName("img_directory_button")
        self.header_label = QtWidgets.QLabel(self.centralwidget)
        self.header_label.setGeometry(QtCore.QRect(200, 0, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.header_label.setFont(font)
        self.header_label.setObjectName("header_label")
        self.subheader_label = QtWidgets.QLabel(self.centralwidget)
        self.subheader_label.setGeometry(QtCore.QRect(30, 30, 691, 41))
        font = QtGui.QFont()
        font.setItalic(True)
        self.subheader_label.setFont(font)
        self.subheader_label.setObjectName("subheader_label")
        self.dir_label = QtWidgets.QLabel(self.centralwidget)
        self.dir_label.setGeometry(QtCore.QRect(30, 120, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dir_label.setFont(font)
        self.dir_label.setObjectName("dir_label")
        self.config_label = QtWidgets.QLabel(self.centralwidget)
        self.config_label.setGeometry(QtCore.QRect(30, 160, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.config_label.setFont(font)
        self.config_label.setObjectName("config_label")
        self.output_label = QtWidgets.QLabel(self.centralwidget)
        self.output_label.setGeometry(QtCore.QRect(30, 200, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.output_label.setFont(font)
        self.output_label.setObjectName("output_label")
        self.preview_label = QtWidgets.QLabel(self.centralwidget)
        self.preview_label.setGeometry(QtCore.QRect(30, 240, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.preview_label.setFont(font)
        self.preview_label.setObjectName("preview_label")
        self.yes_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.yes_radioButton.setGeometry(QtCore.QRect(320, 250, 41, 17))
        self.yes_radioButton.setObjectName("yes_radioButton")
        self.no_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.no_radioButton.setGeometry(QtCore.QRect(390, 250, 41, 17))
        self.no_radioButton.setObjectName("no_radioButton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 80, 801, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.img_dir_text = QtWidgets.QTextEdit(self.centralwidget)
        self.img_dir_text.setGeometry(QtCore.QRect(320, 120, 271, 31))
        self.img_dir_text.setObjectName("img_dir_text")
        self.config_text = QtWidgets.QTextEdit(self.centralwidget)
        self.config_text.setGeometry(QtCore.QRect(320, 160, 271, 31))
        self.config_text.setObjectName("config_text")
        self.output_text = QtWidgets.QTextEdit(self.centralwidget)
        self.output_text.setGeometry(QtCore.QRect(320, 200, 271, 31))
        self.output_text.setObjectName("output_text")
        self.img_dir_help = QtWidgets.QToolButton(self.centralwidget)
        self.img_dir_help.setGeometry(QtCore.QRect(690, 120, 31, 31))
        self.img_dir_help.setObjectName("img_dir_help")
        self.config_help = QtWidgets.QToolButton(self.centralwidget)
        self.config_help.setGeometry(QtCore.QRect(690, 160, 31, 31))
        self.config_help.setObjectName("config_help")
        self.output_help = QtWidgets.QToolButton(self.centralwidget)
        self.output_help.setGeometry(QtCore.QRect(690, 200, 31, 31))
        self.output_help.setObjectName("output_help")
        self.preview_help = QtWidgets.QToolButton(self.centralwidget)
        self.preview_help.setGeometry(QtCore.QRect(690, 240, 31, 31))
        self.preview_help.setObjectName("preview_help")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 290, 781, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(30, 310, 331, 41))
        self.run_button.setObjectName("run_button")
        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(380, 310, 341, 41))
        self.quit_button.setObjectName("quit_button")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 370, 691, 261))
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 650, 691, 41))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 742, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionHelp)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.config_button.setText(_translate("MainWindow", "Select"))
        self.output_button.setText(_translate("MainWindow", "Select"))
        self.img_directory_button.setText(_translate("MainWindow", "Select"))
        self.header_label.setText(_translate("MainWindow", "Autolung - automated lung image analysis"))
        self.subheader_label.setText(_translate("MainWindow", "Written by Gennaro Calendo for the Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University, 2019"))
        self.dir_label.setText(_translate("MainWindow", "Select the folder containing lung images:"))
        self.config_label.setText(_translate("MainWindow", "Select the configuration file for this image set:"))
        self.output_label.setText(_translate("MainWindow", "Select the folder where the results will be saved:"))
        self.preview_label.setText(_translate("MainWindow", "Would you like to save QC images?"))
        self.yes_radioButton.setText(_translate("MainWindow", "Yes"))
        self.no_radioButton.setText(_translate("MainWindow", "No"))
        self.img_dir_help.setText(_translate("MainWindow", "?"))
        self.config_help.setText(_translate("MainWindow", "?"))
        self.output_help.setText(_translate("MainWindow", "?"))
        self.preview_help.setText(_translate("MainWindow", "?"))
        self.run_button.setText(_translate("MainWindow", "Start Analysis"))
        self.quit_button.setText(_translate("MainWindow", "Quit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "About"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionHelp.setText(_translate("MainWindow", "About"))


