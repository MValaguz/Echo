# Form implementation generated from reading ui file 'program_info_ui.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Program_info(object):
    def setupUi(self, Program_info):
        Program_info.setObjectName("Program_info")
        Program_info.resize(458, 144)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons:Echo.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Program_info.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Program_info)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=Program_info)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=Program_info)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Program_info)
        QtCore.QMetaObject.connectSlotsByName(Program_info)

    def retranslateUi(self, Program_info):
        _translate = QtCore.QCoreApplication.translate
        Program_info.setWindowTitle(_translate("Program_info", "Program Info"))
        self.label.setText(_translate("Program_info", "<html><head/><body><p><img src=\"icons:python.gif\"/><img src=\"icons:qt.gif\"/></p></body></html>"))
        self.label_2.setText(_translate("Program_info", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Echo</span></p><p><span style=\" font-size:10pt;\">© 2019-2025</span></p><p><span style=\" font-size:10pt;\">Developed by </span><span style=\" font-size:10pt; font-weight:600;\">Marco Valaguzza</span><span style=\" font-size:10pt;\"> (Italy) </span></p><p><span style=\" font-size:10pt;\">with Python 3.13 and QT6</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Program_info = QtWidgets.QDialog()
    ui = Ui_Program_info()
    ui.setupUi(Program_info)
    Program_info.show()
    sys.exit(app.exec())
