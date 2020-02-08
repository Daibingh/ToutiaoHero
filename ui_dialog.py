# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_roi = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_roi.setObjectName("lineEdit_roi")
        self.horizontalLayout.addWidget(self.lineEdit_roi)
        self.checkBox_wx = QtWidgets.QCheckBox(Dialog)
        self.checkBox_wx.setObjectName("checkBox_wx")
        self.horizontalLayout.addWidget(self.checkBox_wx)
        self.checkBox_logging = QtWidgets.QCheckBox(Dialog)
        self.checkBox_logging.setChecked(True)
        self.checkBox_logging.setTristate(False)
        self.checkBox_logging.setObjectName("checkBox_logging")
        self.horizontalLayout.addWidget(self.checkBox_logging)
        self.checkBox_saveimg = QtWidgets.QCheckBox(Dialog)
        self.checkBox_saveimg.setChecked(True)
        self.checkBox_saveimg.setObjectName("checkBox_saveimg")
        self.horizontalLayout.addWidget(self.checkBox_saveimg)
        self.checkBox_debug = QtWidgets.QCheckBox(Dialog)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.horizontalLayout.addWidget(self.checkBox_debug)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "roi"))
        self.checkBox_wx.setText(_translate("Dialog", "use_wx"))
        self.checkBox_logging.setText(_translate("Dialog", "logging"))
        self.checkBox_saveimg.setText(_translate("Dialog", "save_img"))
        self.checkBox_debug.setText(_translate("Dialog", "debug"))

