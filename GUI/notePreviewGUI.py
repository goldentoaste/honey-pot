# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PythonProject\stickyMarkdown\GUI\notePreview.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotePreview(object):
    def setupUi(self, NotePreview):
        NotePreview.setObjectName("NotePreview")
        NotePreview.resize(340, 140)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NotePreview.sizePolicy().hasHeightForWidth())
        NotePreview.setSizePolicy(sizePolicy)
        NotePreview.setMinimumSize(QtCore.QSize(340, 140))
        NotePreview.setAutoFillBackground(False)
        NotePreview.setStyleSheet("QWidget#NotePreview{\n"
"    background-color:     #FAF0C8;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(NotePreview)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TimeLabel = QtWidgets.QLabel(NotePreview)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimeLabel.sizePolicy().hasHeightForWidth())
        self.TimeLabel.setSizePolicy(sizePolicy)
        self.TimeLabel.setStyleSheet("")
        self.TimeLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.TimeLabel.setObjectName("TimeLabel")
        self.verticalLayout.addWidget(self.TimeLabel)
        self.textBrowser = QtWidgets.QTextBrowser(NotePreview)
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(NotePreview)
        QtCore.QMetaObject.connectSlotsByName(NotePreview)

    def retranslateUi(self, NotePreview):
        _translate = QtCore.QCoreApplication.translate
        NotePreview.setWindowTitle(_translate("NotePreview", "Form"))
        self.TimeLabel.setText(_translate("NotePreview", "Insert Date/Time"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NotePreview = QtWidgets.QWidget()
    ui = Ui_NotePreview()
    ui.setupUi(NotePreview)
    NotePreview.show()
    sys.exit(app.exec_())
