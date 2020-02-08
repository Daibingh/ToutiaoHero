# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'roi.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ROI(object):
    def setupUi(self, ROI):
        ROI.setObjectName("ROI")
        ROI.resize(483, 577)
        self.gridLayout = QtWidgets.QGridLayout(ROI)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(ROI)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ROI)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(ROI)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 20))
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        spacerItem = QtWidgets.QSpacerItem(278, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 10)

        self.retranslateUi(ROI)
        QtCore.QMetaObject.connectSlotsByName(ROI)

    def retranslateUi(self, ROI):
        _translate = QtCore.QCoreApplication.translate
        ROI.setWindowTitle(_translate("ROI", "Form"))
        self.label.setText(_translate("ROI", "xywh"))

