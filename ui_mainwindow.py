# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1271, 919)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(self.groupBox_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.textBrowser_res = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser_res.setStyleSheet("#textBrowser_res {font-size: 18;}")
        self.textBrowser_res.setObjectName("textBrowser_res")
        self.textBrowser_res_2 = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser_res_2.setStyleSheet("#textBrowser_res {font-size: 18;}")
        self.textBrowser_res_2.setObjectName("textBrowser_res_2")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.textBrowser_score = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_score.setObjectName("textBrowser_score")
        self.gridLayout_3.addWidget(self.textBrowser_score, 1, 0, 1, 1)
        self.gridLayout_3.setRowStretch(0, 7)
        self.gridLayout_3.setRowStretch(1, 2)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.plainTextEdit_que = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_que.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEdit_que.setObjectName("plainTextEdit_que")
        self.gridLayout.addWidget(self.plainTextEdit_que, 0, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 12)
        self.checkBox_saveImg = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_saveImg.setChecked(True)
        self.checkBox_saveImg.setObjectName("checkBox_saveImg")
        self.gridLayout_2.addWidget(self.checkBox_saveImg, 0, 8, 1, 1)
        self.checkBox_logging = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_logging.setChecked(True)
        self.checkBox_logging.setObjectName("checkBox_logging")
        self.gridLayout_2.addWidget(self.checkBox_logging, 0, 7, 1, 1)
        self.checkBox_debug = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.gridLayout_2.addWidget(self.checkBox_debug, 0, 9, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 5, 1, 1)
        self.checkBox_wx = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_wx.setObjectName("checkBox_wx")
        self.gridLayout_2.addWidget(self.checkBox_wx, 0, 6, 1, 1)
        self.pushButton_roi = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_roi.setObjectName("pushButton_roi")
        self.gridLayout_2.addWidget(self.pushButton_roi, 0, 10, 1, 1)
        self.pushButton_pic = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pic.setObjectName("pushButton_pic")
        self.gridLayout_2.addWidget(self.pushButton_pic, 0, 11, 1, 1)
        self.pushButton_planB = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_planB.setObjectName("pushButton_planB")
        self.gridLayout_2.addWidget(self.pushButton_planB, 0, 3, 1, 1)
        self.pushButton_planA = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_planA.setObjectName("pushButton_planA")
        self.gridLayout_2.addWidget(self.pushButton_planA, 0, 2, 1, 1)
        self.pushButton_planC = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_planC.setObjectName("pushButton_planC")
        self.gridLayout_2.addWidget(self.pushButton_planC, 0, 4, 1, 1)
        self.pushButton_simple = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_simple.setObjectName("pushButton_simple")
        self.gridLayout_2.addWidget(self.pushButton_simple, 0, 1, 1, 1)
        self.pushButton_search = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_search.setObjectName("pushButton_search")
        self.gridLayout_2.addWidget(self.pushButton_search, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsettsing = QtWidgets.QAction(MainWindow)
        self.actionsettsing.setObjectName("actionsettsing")
        self.actionroi = QtWidgets.QAction(MainWindow)
        self.actionroi.setObjectName("actionroi")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Result"))
        self.textBrowser_res.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>"))
        self.textBrowser_res_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>"))
        self.checkBox_saveImg.setText(_translate("MainWindow", "save_img"))
        self.checkBox_logging.setText(_translate("MainWindow", "logging"))
        self.checkBox_debug.setText(_translate("MainWindow", "debug"))
        self.checkBox_wx.setText(_translate("MainWindow", "wx"))
        self.pushButton_roi.setText(_translate("MainWindow", "ROI"))
        self.pushButton_pic.setText(_translate("MainWindow", "Pic"))
        self.pushButton_planB.setText(_translate("MainWindow", "Plan B"))
        self.pushButton_planA.setText(_translate("MainWindow", "Plan A"))
        self.pushButton_planC.setText(_translate("MainWindow", "Plan C"))
        self.pushButton_simple.setText(_translate("MainWindow", "Simple"))
        self.pushButton_search.setText(_translate("MainWindow", "Search"))
        self.actionsettsing.setText(_translate("MainWindow", "setting"))
        self.actionroi.setText(_translate("MainWindow", "roi"))

