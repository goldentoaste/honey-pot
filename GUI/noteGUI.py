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
        self.horizontalLayout.setContentsMargins(2, 2, 2, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newNoteButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newNoteButton.sizePolicy().hasHeightForWidth())
        self.newNoteButton.setSizePolicy(sizePolicy)
        self.newNoteButton.setMaximumSize(QtCore.QSize(35, 35))
        self.newNoteButton.setStyleSheet("QPushButton:hover:!pressed{\n"
"    border: 1px solid #000000;\n"
"}")
        self.newNoteButton.setText("")
        self.newNoteButton.setIconSize(QtCore.QSize(20, 20))
        self.newNoteButton.setFlat(True)
        self.newNoteButton.setObjectName("newNoteButton")
        self.horizontalLayout.addWidget(self.newNoteButton)
        self.pinButton = QtWidgets.QPushButton(self.frame)
        self.pinButton.setMaximumSize(QtCore.QSize(35, 35))
        self.pinButton.setStyleSheet("QPushButton:hover:!pressed{\n"
"    border: 1px solid #000000;\n"
"}")
        self.pinButton.setText("")
        self.pinButton.setIconSize(QtCore.QSize(20, 20))
        self.pinButton.setFlat(True)
        self.pinButton.setObjectName("pinButton")
        self.horizontalLayout.addWidget(self.pinButton)
        self.editButton = QtWidgets.QPushButton(self.frame)
        self.editButton.setStyleSheet("QPushButton:hover:!pressed{\n"
"    border: 1px solid #000000;\n"
"}")
        self.editButton.setText("")
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setFlat(True)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(self.frame)
        self.closeButton.setMaximumSize(QtCore.QSize(35, 35))
        self.closeButton.setStyleSheet("QPushButton:hover:!pressed{\n"
"    border: 1px solid #000000;\n"
"}")
        self.closeButton.setText("")
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(True)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.minimizeButton = QtWidgets.QPushButton(self.frame)
        self.minimizeButton.setMaximumSize(QtCore.QSize(35, 35))
        self.minimizeButton.setStyleSheet("QPushButton:hover:!pressed{\n"
"    border: 1px solid #000000;\n"
"}")
        self.minimizeButton.setText("")
        self.minimizeButton.setIconSize(QtCore.QSize(20, 20))
        self.minimizeButton.setCheckable(False)
        self.minimizeButton.setFlat(True)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(4, -1, 2, 4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.editLabel = QtWidgets.QLabel(Note)
        font = QtGui.QFont()
        font.setFamily("Cascadia Mono")
        font.setPointSize(12)
        self.editLabel.setFont(font)
        self.editLabel.setObjectName("editLabel")
        self.verticalLayout_3.addWidget(self.editLabel)
        self.editor = MarkdownEditor(Note)
        self.editor.setStyleSheet("QTextEdit, QTextBrowser{\n"
"\n"
"border:1px solid #000000;\n"
"}")
        self.editor.setObjectName("editor")
        self.verticalLayout_3.addWidget(self.editor)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(2, 0, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.previewLabel = QtWidgets.QLabel(Note)
        font = QtGui.QFont()
        font.setFamily("Cascadia Mono")
        font.setPointSize(12)
        self.previewLabel.setFont(font)
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
from markdownEditor import MarkdownEditor


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Note = QtWidgets.QWidget()
    ui = Ui_Note()
    ui.setupUi(Note)
    Note.show()
    sys.exit(app.exec_())
