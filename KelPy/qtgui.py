# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\chet_\Documents\GUI\KelPy.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
#
# Last edited: 8/1/23 - Chet Russell


from PyQt5 import QtCore, QtGui, QtWidgets

import os

import core

# Use a dict to sort the values needed?


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(313, 437)
        MainWindow.setMinimumSize(QtCore.QSize(313, 437))
        MainWindow.setMaximumSize(QtCore.QSize(313, 437))
        MainWindow.setDocumentMode(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Tab 1
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab_0")

        self.imageFolder_label_0 = QtWidgets.QLabel(self.tab)
        self.imageFolder_label_0.setGeometry(QtCore.QRect(50, 10, 71, 16))
        self.imageFolder_label_0.setObjectName("imageFolder_label_0")

        self.downloadFolder_label_0 = QtWidgets.QLabel(self.tab)
        self.downloadFolder_label_0.setGeometry(QtCore.QRect(50, 50, 71, 16))
        self.downloadFolder_label_0.setObjectName("downloadFolder_label_0")

        self.imageFolder_select_0 = QtWidgets.QPushButton(self.tab)
        self.imageFolder_select_0.setGeometry(QtCore.QRect(140, 10, 75, 21))
        self.imageFolder_select_0.setObjectName("imageFolder_select_0")
        self.imageFolder_select_0.clicked.connect(self.image_dir_select_0)
        self.imageFolder_0 = ""

        self.downloadFolder_select_0 = QtWidgets.QPushButton(self.tab)
        self.downloadFolder_select_0.setGeometry(QtCore.QRect(140, 50, 75, 21))
        self.downloadFolder_select_0.setObjectName("downloadFolder_select_0")
        self.downloadFolder_select_0.clicked.connect(self.download_dir_select_0)
        self.downloadFolder_0 = ""

        self.resultsFolder_name_label_0 = QtWidgets.QLabel(self.tab)
        self.resultsFolder_name_label_0.setGeometry(QtCore.QRect(20, 90, 101, 16))
        self.resultsFolder_name_label_0.setObjectName("resultsFolder_name_label_0")

        self.resultsFolder_name_0 = QtWidgets.QLineEdit(self.tab)
        self.resultsFolder_name_0.setGeometry(QtCore.QRect(140, 90, 113, 21))
        self.resultsFolder_name_0.setObjectName("resultsFolder_name_0")

        self.pixelBuff_label_0 = QtWidgets.QLabel(self.tab)
        self.pixelBuff_label_0.setGeometry(QtCore.QRect(60, 130, 61, 16))
        self.pixelBuff_label_0.setObjectName("pixelBuff_label_0")

        self.pixelBuff_select_0 = QtWidgets.QSpinBox(self.tab)
        self.pixelBuff_select_0.setGeometry(QtCore.QRect(140, 130, 42, 21))
        self.pixelBuff_select_0.setMaximum(10)
        self.pixelBuff_select_0.setMaximum(10)
        self.pixelBuff_select_0.setValue(5)

        self.quality_label_0 = QtWidgets.QLabel(self.tab)
        self.quality_label_0.setGeometry(QtCore.QRect(80, 170, 41, 16))
        self.quality_label_0.setObjectName("quality_label_0")

        self.quality_select_0 = QtWidgets.QComboBox(self.tab)
        self.quality_select_0.setGeometry(QtCore.QRect(140, 170, 61, 21))
        self.quality_select_0.setEditable(False)
        self.quality_select_0.setObjectName("quality_select_0")
        self.quality_select_0.addItem("")
        self.quality_select_0.addItem("")
        self.quality_select_0.addItem("")
        self.quality_select_0.addItem("")
        self.quality_select_0.addItem("")

        self.crop_label_0 = QtWidgets.QLabel(self.tab)
        self.crop_label_0.setGeometry(QtCore.QRect(90, 210, 31, 20))
        self.crop_label_0.setObjectName("crop_label_0")

        self.crop_select_0 = QtWidgets.QSpinBox(self.tab)
        self.crop_select_0.setGeometry(QtCore.QRect(140, 210, 42, 21))
        self.crop_select_0.setMaximum(5)
        self.crop_select_0.setObjectName("crop_select_0")

        self.specClass_label_0 = QtWidgets.QLabel(self.tab)
        self.specClass_label_0.setGeometry(QtCore.QRect(10, 250, 111, 20))
        self.specClass_label_0.setObjectName("specClass_label_0")

        self.specClass_select_0 = QtWidgets.QComboBox(self.tab)
        self.specClass_select_0.setGeometry(QtCore.QRect(140, 250, 51, 22))
        self.specClass_select_0.setObjectName("specClass_select_0")
        self.specClass_select_0.addItem("")
        self.specClass_select_0.addItem("")
        self.specClass_select_0.setItemText(1, "")

        self.run_0 = QtWidgets.QPushButton(self.tab)
        self.run_0.setGeometry(QtCore.QRect(100, 290, 91, 31))
        self.run_0.setObjectName("run_0")
        self.run_0.clicked.connect(self.run_main)

        self.progressBar_0 = QtWidgets.QProgressBar(self.tab)
        self.progressBar_0.setGeometry(QtCore.QRect(30, 340, 231, 23))
        self.progressBar_0.setProperty("value", 0)
        self.progressBar_0.setTextVisible(True)
        self.progressBar_0.setObjectName("progressBar_0")

        self.tabWidget.addTab(self.tab, "")

        # Tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_1")

        self.imageFolder_label_1 = QtWidgets.QLabel(self.tab_2)
        self.imageFolder_label_1.setGeometry(QtCore.QRect(50, 10, 71, 16))
        self.imageFolder_label_1.setObjectName("imageFolder_label_1")

        self.imageFolder_select_1 = QtWidgets.QPushButton(self.tab_2)
        self.imageFolder_select_1.setGeometry(QtCore.QRect(140, 10, 75, 21))
        self.imageFolder_select_1.setObjectName("imageFolder_select_1")
        self.imageFolder_select_1.clicked.connect(self.image_dir_select_1)
        self.imageFolder_1 = ""

        self.downloadFolder_label_1 = QtWidgets.QLabel(self.tab_2)
        self.downloadFolder_label_1.setGeometry(QtCore.QRect(50, 50, 71, 16))
        self.downloadFolder_label_1.setObjectName("downloadFolder_label_1")

        self.downloadFolder_select_1 = QtWidgets.QPushButton(self.tab_2)
        self.downloadFolder_select_1.setGeometry(QtCore.QRect(140, 50, 75, 21))
        self.downloadFolder_select_1.setObjectName("downloadFolder_select_1")
        self.downloadFolder_select_1.clicked.connect(self.download_dir_select_1)
        self.downloadFolder_1 = ""

        self.resultsFolder_name_label_1 = QtWidgets.QLabel(self.tab_2)
        self.resultsFolder_name_label_1.setGeometry(QtCore.QRect(20, 90, 101, 16))
        self.resultsFolder_name_label_1.setObjectName("resultsFolder_name_label_1")

        self.resultsFolder_name_1 = QtWidgets.QLineEdit(self.tab_2)
        self.resultsFolder_name_1.setGeometry(QtCore.QRect(140, 90, 113, 21))
        self.resultsFolder_name_1.setObjectName("resultsFolder_name_1")

        self.pixelBuff_label_1 = QtWidgets.QLabel(self.tab_2)
        self.pixelBuff_label_1.setGeometry(QtCore.QRect(60, 130, 61, 16))
        self.pixelBuff_label_1.setObjectName("pixelBuff_label_1")

        self.pixelBuff_select_1 = QtWidgets.QSpinBox(self.tab_2)
        self.pixelBuff_select_1.setGeometry(QtCore.QRect(140, 130, 42, 21))
        self.pixelBuff_select_1.setMaximum(10)
        self.pixelBuff_select_1.setObjectName("pixelBuff_select_1")
        self.pixelBuff_select_1.setValue(5)

        self.quality_label_1 = QtWidgets.QLabel(self.tab_2)
        self.quality_label_1.setGeometry(QtCore.QRect(80, 170, 41, 16))
        self.quality_label_1.setObjectName("quality_label_1")

        self.quality_select_1 = QtWidgets.QComboBox(self.tab_2)
        self.quality_select_1.setGeometry(QtCore.QRect(140, 170, 61, 21))
        self.quality_select_1.setEditable(False)
        self.quality_select_1.setObjectName("quality_select_1")
        self.quality_select_1.addItem("")
        self.quality_select_1.addItem("")
        self.quality_select_1.addItem("")
        self.quality_select_1.addItem("")
        self.quality_select_1.addItem("")

        self.crop_label_1 = QtWidgets.QLabel(self.tab_2)
        self.crop_label_1.setGeometry(QtCore.QRect(90, 210, 31, 20))
        self.crop_label_1.setObjectName("crop_label_0")

        self.crop_select_1 = QtWidgets.QSpinBox(self.tab_2)
        self.crop_select_1.setGeometry(QtCore.QRect(140, 210, 42, 21))
        self.crop_select_1.setMaximum(5)
        self.crop_select_1.setObjectName("crop_select_0")

        self.featAlg_label = QtWidgets.QLabel(self.tab_2)
        self.featAlg_label.setGeometry(QtCore.QRect(30, 250, 91, 20))
        self.featAlg_label.setObjectName("featAlg_label")

        self.featAlg_select = QtWidgets.QComboBox(self.tab_2)
        self.featAlg_select.setGeometry(QtCore.QRect(140, 250, 51, 22))
        self.featAlg_select.setObjectName("featAlg_select")
        self.featAlg_select.addItem("")
        self.featAlg_select.addItem("")
        self.featAlg_select.addItem("")
        self.featAlg_select.addItem("")

        self.run_1 = QtWidgets.QPushButton(self.tab_2)
        self.run_1.setGeometry(QtCore.QRect(100, 290, 91, 31))
        self.run_1.setObjectName("run_1")
        self.run_1.clicked.connect(self.run_ortho)

        self.progressBar_1 = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar_1.setGeometry(QtCore.QRect(30, 340, 231, 23))
        self.progressBar_1.setProperty("value", 0)
        self.progressBar_1.setObjectName("progressBar_1")

        self.tabWidget.addTab(self.tab_2, "")

        # Tab 3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.orthofile_label = QtWidgets.QLabel(self.tab_3)
        self.orthofile_label.setGeometry(QtCore.QRect(30, 10, 81, 16))
        self.orthofile_label.setObjectName("orthofile_label")

        self.orthofile_select = QtWidgets.QPushButton(self.tab_3)
        self.orthofile_select.setGeometry(QtCore.QRect(140, 10, 75, 21))
        self.orthofile_select.setObjectName("orthofile_select")
        self.orthofile_select.clicked.connect(self.ortho_file_select_0)
        self.ortho_file_0 = ""

        self.resultsFolder_label_0 = QtWidgets.QLabel(self.tab_3)
        self.resultsFolder_label_0.setGeometry(QtCore.QRect(40, 50, 71, 16))
        self.resultsFolder_label_0.setObjectName("resultsFolder_label_0")

        self.resultsFolder_select_0 = QtWidgets.QPushButton(self.tab_3)
        self.resultsFolder_select_0.setGeometry(QtCore.QRect(140, 50, 75, 21))
        self.resultsFolder_select_0.setObjectName("resultsFolder_select_0")
        self.resultsFolder_select_0.clicked.connect(self.results_dir_0)
        self.resultsFolder_0 = ""

        self.gsd_label = QtWidgets.QLabel(self.tab_3)
        self.gsd_label.setGeometry(QtCore.QRect(10, 90, 181, 16))
        self.gsd_label.setObjectName("gsd_label")

        self.gsd_select = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.gsd_select.setGeometry(QtCore.QRect(200, 90, 62, 16))
        self.gsd_select.setObjectName("gsd_select")

        self.specClass_label_1 = QtWidgets.QLabel(self.tab_3)
        self.specClass_label_1.setGeometry(QtCore.QRect(10, 130, 111, 16))
        self.specClass_label_1.setObjectName("specClass_label_1")

        self.specClass_select_1 = QtWidgets.QComboBox(self.tab_3)
        self.specClass_select_1.setGeometry(QtCore.QRect(140, 130, 51, 22))
        self.specClass_select_1.setObjectName("specClass_select_1")
        self.specClass_select_1.addItem("")
        self.specClass_select_1.addItem("")
        self.specClass_select_1.setItemText(1, "")

        self.run_2 = QtWidgets.QPushButton(self.tab_3)
        self.run_2.setGeometry(QtCore.QRect(100, 290, 91, 31))
        self.run_2.setObjectName("run_2")
        self.run_2.clicked.connect(self.run_seg)

        self.progressBar_2 = QtWidgets.QProgressBar(self.tab_3)
        self.progressBar_2.setGeometry(QtCore.QRect(30, 340, 231, 23))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")

        self.tabWidget.addTab(self.tab_3, "")

        # Tab 4
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.ortho1_label = QtWidgets.QLabel(self.tab_4)
        self.ortho1_label.setGeometry(QtCore.QRect(40, 10, 81, 16))
        self.ortho1_label.setObjectName("ortho1_label")

        self.ortho1_select = QtWidgets.QPushButton(self.tab_4)
        self.ortho1_select.setGeometry(QtCore.QRect(140, 10, 75, 21))
        self.ortho1_select.setObjectName("ortho1_select")
        self.ortho1_select.clicked.connect(self.ortho_file_select_1)
        self.ortho_file_1 = ""

        self.ortho2_label = QtWidgets.QLabel(self.tab_4)
        self.ortho2_label.setGeometry(QtCore.QRect(40, 50, 81, 16))
        self.ortho2_label.setObjectName("ortho2_label")

        self.ortho2_select = QtWidgets.QPushButton(self.tab_4)
        self.ortho2_select.setGeometry(QtCore.QRect(140, 50, 75, 21))
        self.ortho2_select.setObjectName("ortho2_select")
        self.ortho2_select.clicked.connect(self.ortho_file_select_2)
        self.ortho_file_2 = ""

        self.resultsFolder_label_1 = QtWidgets.QLabel(self.tab_4)
        self.resultsFolder_label_1.setGeometry(QtCore.QRect(40, 90, 71, 16))
        self.resultsFolder_label_1.setObjectName("resultsFolder_label_1")

        self.resultsFolder_select_1 = QtWidgets.QPushButton(self.tab_4)
        self.resultsFolder_select_1.setGeometry(QtCore.QRect(140, 90, 75, 21))
        self.resultsFolder_select_1.setObjectName("resultsFolder_select_1")
        self.resultsFolder_select_1.clicked.connect(self.results_dir_1)
        self.resultsFolder_1 = ""

        self.resultName = QtWidgets.QLineEdit(self.tab_4)
        self.resultName.setGeometry(QtCore.QRect(140, 140, 113, 21))
        self.resultName.setObjectName("resultName")

        self.resultName_label = QtWidgets.QLabel(self.tab_4)
        self.resultName_label.setGeometry(QtCore.QRect(50, 140, 71, 16))
        self.resultName_label.setObjectName("resultName_label")

        self.run_3 = QtWidgets.QPushButton(self.tab_4)
        self.run_3.setGeometry(QtCore.QRect(100, 290, 91, 31))
        self.run_3.setObjectName("run3")
        self.run_3.clicked.connect(self.run_merge)

        self.progressBar_3 = QtWidgets.QProgressBar(self.tab_4)
        self.progressBar_3.setGeometry(QtCore.QRect(30, 340, 231, 23))
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setObjectName("progressBar_3")

        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KelPy"))
        self.imageFolder_label_0.setText(_translate("MainWindow", "Image Folder:"))
        self.downloadFolder_label_0.setText(_translate("MainWindow", "Download To:"))
        self.imageFolder_select_0.setText(_translate("MainWindow", "Select"))
        self.downloadFolder_select_0.setText(_translate("MainWindow", "Select"))
        self.resultsFolder_name_label_0.setText(
            _translate("MainWindow", "Results Folder Name:")
        )
        self.pixelBuff_label_0.setText(_translate("MainWindow", "Pixel Buffer:"))
        self.quality_label_0.setText(_translate("MainWindow", "Quality:"))
        self.quality_select_0.setCurrentText(_translate("MainWindow", "high"))
        self.quality_select_0.setItemText(0, _translate("MainWindow", "high"))
        self.quality_select_0.setItemText(1, _translate("MainWindow", "ultra"))
        self.quality_select_0.setItemText(2, _translate("MainWindow", "medium"))
        self.quality_select_0.setItemText(3, _translate("MainWindow", "low"))
        self.quality_select_0.setItemText(4, _translate("MainWindow", "lowest"))
        self.crop_label_0.setText(_translate("MainWindow", "Crop:"))
        self.specClass_label_0.setText(
            _translate("MainWindow", "Species Classification:")
        )
        self.specClass_select_0.setItemText(0, _translate("MainWindow", "False"))
        self.specClass_select_0.setItemText(1, _translate("MainWindow", "True"))
        self.run_0.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Main")
        )
        self.imageFolder_label_1.setText(_translate("MainWindow", "Image Folder:"))
        self.imageFolder_select_1.setText(_translate("MainWindow", "Select"))
        self.downloadFolder_label_1.setText(_translate("MainWindow", "Download To:"))
        self.downloadFolder_select_1.setText(_translate("MainWindow", "Select"))
        self.resultsFolder_name_label_1.setText(
            _translate("MainWindow", "Results Folder Name:")
        )
        self.pixelBuff_label_1.setText(_translate("MainWindow", "Pixel Buffer:"))
        self.quality_label_1.setText(_translate("MainWindow", "Quality:"))
        self.quality_select_1.setCurrentText(_translate("MainWindow", "high"))
        self.quality_select_1.setItemText(0, _translate("MainWindow", "high"))
        self.quality_select_1.setItemText(1, _translate("MainWindow", "ultra"))
        self.quality_select_1.setItemText(2, _translate("MainWindow", "medium"))
        self.quality_select_1.setItemText(3, _translate("MainWindow", "low"))
        self.quality_select_1.setItemText(4, _translate("MainWindow", "lowest"))
        self.crop_label_1.setText(_translate("MainWindow", "Crop:"))
        self.featAlg_label.setText(_translate("MainWindow", "Feature Algorithm:"))
        self.featAlg_select.setItemText(0, _translate("MainWindow", "sift"))
        self.featAlg_select.setItemText(1, _translate("MainWindow", "akaze"))
        self.featAlg_select.setItemText(2, _translate("MainWindow", "hahog"))
        self.featAlg_select.setItemText(3, _translate("MainWindow", "orb"))
        self.run_1.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            _translate("MainWindow", "Orthorectification"),
        )
        self.orthofile_label.setText(_translate("MainWindow", "Orthomosaic File:"))
        self.orthofile_select.setText(_translate("MainWindow", "Select"))
        self.resultsFolder_label_0.setText(_translate("MainWindow", "Results Folder:"))
        self.resultsFolder_select_0.setText(_translate("MainWindow", "Select"))
        self.gsd_label.setText(
            _translate("MainWindow", "GSD (Ground-sample distance) in cm:")
        )
        self.specClass_label_1.setText(
            _translate("MainWindow", "Species Classification:")
        )
        self.specClass_select_1.setItemText(0, _translate("MainWindow", "False"))
        self.specClass_select_1.setItemText(1, _translate("MainWindow", "True"))
        self.run_2.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            _translate("MainWindow", "Identification"),
        )
        self.ortho1_label.setText(_translate("MainWindow", "Orthomosaic 1:"))
        self.ortho1_select.setText(_translate("MainWindow", "Select"))
        self.ortho2_label.setText(_translate("MainWindow", "Orthomosaic 2:"))
        self.ortho2_select.setText(_translate("MainWindow", "Select"))
        self.resultsFolder_label_1.setText(_translate("MainWindow", "Results Folder:"))
        self.resultsFolder_select_1.setText(_translate("MainWindow", "Select"))
        self.resultName_label.setText(_translate("MainWindow", "Result Name:"))
        self.run_3.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Merge")
        )

    def run_main(self):
        print("Running all")
        d = {
            "image_folder": self.imageFolder_0,
            "download_folder": self.downloadFolder_0,
            "results": self.resultsFolder_name_0.text(),
            "pixelbuff": self.pixelBuff_select_0.value(),
            "quality": self.quality_select_0.currentText(),
            "crop": self.crop_select_0.value(),
            "spec_class": self.specClass_select_0.currentText(),
        }
        if d.get("spec_class") == "False":
            d.update({"spec_class" : False})
        else:
            d.update({"spec_class" : True})
        print(d)
        final_folder = d.get("download_folder") + "/" + d.get("results")
        os.mkdir(final_folder)
        core.orthorec(imgdir=d.get("image_folder"), dwndir=final_folder, quality=d.get("quality"), crop=d.get("crop"), kmz=False, ft="sift", exif=True, pb=d.get("pixelbuff"))
        print("Orthorectification done")
        value = core.calculate_gsd(final_folder + "/report.pdf")
        core.seg(ortho=final_folder + "/odm_orthophoto.tif", komp=final_folder, gsd=value, spec=d.get("spec_class"))
        print("Done.")

    def run_ortho(self):
        print("Running ortho")
        d = {
            "image_folder": self.imageFolder_1,
            "download_folder": self.downloadFolder_1,
            "results": self.resultsFolder_name_1.text(),
            "pixelbuff": self.pixelBuff_select_1.value(),
            "quality": self.quality_select_1.currentText(),
            "crop": self.crop_select_1.value(),
            "feat_alg": self.featAlg_select.currentText(),
        }
        print(d)
        final_folder = d.get("download_folder") + "/" + d.get("results")
        os.mkdir(final_folder)
        core.orthorec(imgdir=d.get("image_folder"), dwndir=final_folder, quality=d.get("quality"), crop=d.get("crop"), kmz=False, ft=d.get("feat_alg"), exif=True, pb=d.get("pixelbuff"))
        print("Orthorectification done")


    def run_seg(self):
        print("Running segmentation")
        d = {
            "ortho_file": self.ortho_file_0[0],
            "results_folder": self.resultsFolder_0,
            "GSD" : self.gsd_select.value(),
            "spec_class": self.specClass_select_0.currentText(),
        }
        if d.get("spec_class") == "False":
            d.update({"spec_class" : False})
        else:
            d.update({"spec_class" : True})
        print(d)
        core.seg(ortho=d.get("ortho_file"), komp=d.get("results_folder"), gsd=d.get("GSD"), spec=d.get("spec_class"))
        print("Segmentation done")


    def run_merge(self):
        print("Running merge")
        d = {
            "ortho_1": self.ortho_file_1[0],
            "ortho_2": self.ortho_file_2[0],
            "results_folder" : self.resultsFolder_1,
            "results_name": self.resultName.text(),
        }
        print(d)
        core.merge_orthos(o1=d.get("ortho_1"), o2=d.get("ortho_2"), dir=d.get("results_folder"), name=d.get("results_name"))
        print("Merge done")

    def image_dir_select_0(self):
        self.imageFolder_0 = str(
            QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        )
        print(self.imageFolder_0)

    def download_dir_select_0(self):
        self.downloadFolder_0 = str(
            QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        )
        print(self.downloadFolder_0)

    def image_dir_select_1(self):
        self.imageFolder_1 = str(
            QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        )
        print(self.imageFolder_1)

    def download_dir_select_1(self):
        self.downloadFolder_1 = str(
            QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        )
        print(self.downloadFolder_1)

    def results_dir_0(self):
        self.resultsFolder_0 = str(
            QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        )
        print(self.resultsFolder_0)

    def results_dir_1(self):
        self.resultsFolder_1 = str(
            QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        )
        print(self.resultsFolder_1)

    def ortho_file_select_0(self):
        self.ortho_file_0 = QtWidgets.QFileDialog.getOpenFileName(None, "Select File")
        print(self.ortho_file_0[0])

    def ortho_file_select_1(self):
        self.ortho_file_1 = QtWidgets.QFileDialog.getOpenFileName(None, "Select File")
        print(self.ortho_file_1[0])

    def ortho_file_select_2(self):
        self.ortho_file_2 = QtWidgets.QFileDialog.getOpenFileName(None, "Select File")
        print(self.ortho_file_2[0])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
