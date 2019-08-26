# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window_about(object):
    def setupUi(self, window_about):
        window_about.setObjectName("window_about")
        window_about.resize(391, 172)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(window_about.sizePolicy().hasHeightForWidth())
        window_about.setSizePolicy(sizePolicy)
        window_about.setWindowTitle("About MChat")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/MChat.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        window_about.setWindowIcon(icon)
        window_about.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(window_about)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(window_about)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../icons/qt.gif"))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(window_about)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setText("<html><head/><body><p>MChat</p><p>is a little chat program for ethernet network.</p><p>Developed by Marco Valaguzza (C) 2019</p><p>with Phyton and QT library</p></body></html>")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(window_about)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1, QtCore.Qt.AlignRight)

        self.retranslateUi(window_about)
        self.buttonBox.accepted.connect(window_about.accept)
        self.buttonBox.rejected.connect(window_about.reject)
        QtCore.QMetaObject.connectSlotsByName(window_about)

    def retranslateUi(self, window_about):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window_about = QtWidgets.QDialog()
    ui = Ui_window_about()
    ui.setupUi(window_about)
    window_about.show()
    sys.exit(app.exec_())

