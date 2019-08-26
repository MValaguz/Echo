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
        window_about.resize(384, 178)
        window_about.setWindowTitle("About MChat")
        self.buttonBox = QtWidgets.QDialogButtonBox(window_about)
        self.buttonBox.setGeometry(QtCore.QRect(290, 130, 75, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(window_about)
        self.label.setGeometry(QtCore.QRect(10, 10, 100, 118))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../icons/qt.gif"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(window_about)
        self.label_2.setGeometry(QtCore.QRect(120, 30, 214, 88))
        self.label_2.setText("<html><head/><body><p>MChat</p><p>is a little chat program for ethernet network.</p><p>Developed by Marco Valaguzza (C) 2019</p><p>with Phyton and QT library</p></body></html>")
        self.label_2.setObjectName("label_2")

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

