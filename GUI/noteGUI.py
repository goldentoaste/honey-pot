# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PythonProject\stickyMarkdown\GUI\note.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Note(object):
    def setupUi(self, Note):
        Note.setObjectName("Note")
        Note.resize(788, 462)
        self.verticalLayout = QtWidgets.QVBoxLayout(Note)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Note)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet("QFrame{\n"
"    background: #f0f000;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newNoteButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newNoteButton.sizePolicy().hasHeightForWidth())
        self.newNoteButton.setSizePolicy(sizePolicy)
        self.newNoteButton.setMaximumSize(QtCore.QSize(35, 35))
        self.newNoteButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:\\PythonProject\\stickyMarkdown\\GUI\\add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newNoteButton.setIcon(icon)
        self.newNoteButton.setIconSize(QtCore.QSize(20, 20))
        self.newNoteButton.setFlat(True)
        self.newNoteButton.setObjectName("newNoteButton")
        self.horizontalLayout.addWidget(self.newNoteButton)
        self.pinButton = QtWidgets.QPushButton(self.frame)
        self.pinButton.setMaximumSize(QtCore.QSize(35, 35))
        self.pinButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("D:\\PythonProject\\stickyMarkdown\\GUI\\pin.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pinButton.setIcon(icon1)
        self.pinButton.setIconSize(QtCore.QSize(20, 20))
        self.pinButton.setFlat(True)
        self.pinButton.setObjectName("pinButton")
        self.horizontalLayout.addWidget(self.pinButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.minimizeButton = QtWidgets.QPushButton(self.frame)
        self.minimizeButton.setMaximumSize(QtCore.QSize(35, 35))
        self.minimizeButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("D:\\PythonProject\\stickyMarkdown\\GUI\\minimize.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimizeButton.setIcon(icon2)
        self.minimizeButton.setIconSize(QtCore.QSize(20, 20))
        self.minimizeButton.setFlat(True)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)
        self.closeButton = QtWidgets.QPushButton(self.frame)
        self.closeButton.setMaximumSize(QtCore.QSize(35, 35))
        self.closeButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("D:\\PythonProject\\stickyMarkdown\\GUI\\close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon3)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(True)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.editLabel = QtWidgets.QLabel(Note)
        self.editLabel.setObjectName("editLabel")
        self.verticalLayout_3.addWidget(self.editLabel)
        self.editor = QtWidgets.QTextEdit(Note)
        self.editor.setStyleSheet("QTextEdit, QTextBrowser{\n"
"\n"
"border:1px solid #000000;\n"
"}")
        self.editor.setObjectName("editor")
        self.verticalLayout_3.addWidget(self.editor)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.previewLabel = QtWidgets.QLabel(Note)
        self.previewLabel.setObjectName("previewLabel")
        self.verticalLayout_2.addWidget(self.previewLabel)
        self.preview = QtWidgets.QTextBrowser(Note)
        self.preview.setStyleSheet("QTextEdit{\n"
"\n"
"border:1px solid #000000;\n"
"}")
        self.preview.setOpenExternalLinks(True)
        self.preview.setObjectName("preview")
        self.verticalLayout_2.addWidget(self.preview)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Note)
        QtCore.QMetaObject.connectSlotsByName(Note)

    def retranslateUi(self, Note):
        _translate = QtCore.QCoreApplication.translate
        Note.setWindowTitle(_translate("Note", "Form"))
        self.editLabel.setText(_translate("Note", "Edit Markdown"))
        self.previewLabel.setText(_translate("Note", "Preview"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Note = QtWidgets.QWidget()
    ui = Ui_Note()
    ui.setupUi(Note)
    Note.show()
    sys.exit(app.exec_())
