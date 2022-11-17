# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'note.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QVBoxLayout, QWidget)

from markdownEditor import (MarkdownEditor, MarkdownPreview)

class Ui_Note(object):
    def setupUi(self, Note):
        if not Note.objectName():
            Note.setObjectName(u"Note")
        Note.resize(805, 710)
        Note.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Note)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Note)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"QFrame{\n"
"	background: #f0f000;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)
        self.newNoteButton = QPushButton(self.frame)
        self.newNoteButton.setObjectName(u"newNoteButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.newNoteButton.sizePolicy().hasHeightForWidth())
        self.newNoteButton.setSizePolicy(sizePolicy1)
        self.newNoteButton.setMaximumSize(QSize(35, 35))
        self.newNoteButton.setStyleSheet(u"QPushButton:hover:!pressed{\n"
"	border: 1px solid #000000;\n"
"}")
        self.newNoteButton.setIconSize(QSize(20, 20))
        self.newNoteButton.setFlat(True)

        self.horizontalLayout.addWidget(self.newNoteButton)

        self.pinButton = QPushButton(self.frame)
        self.pinButton.setObjectName(u"pinButton")
        self.pinButton.setMaximumSize(QSize(35, 35))
        self.pinButton.setStyleSheet(u"QPushButton:hover:!pressed{\n"
"	border: 1px solid #000000;\n"
"}")
        self.pinButton.setIconSize(QSize(20, 20))
        self.pinButton.setFlat(True)

        self.horizontalLayout.addWidget(self.pinButton)

        self.editButton = QPushButton(self.frame)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setStyleSheet(u"QPushButton:hover:!pressed{\n"
"	border: 1px solid #000000;\n"
"}")
        self.editButton.setIconSize(QSize(20, 20))
        self.editButton.setFlat(True)

        self.horizontalLayout.addWidget(self.editButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.minimizeButton = QPushButton(self.frame)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMaximumSize(QSize(35, 35))
        self.minimizeButton.setStyleSheet(u"QPushButton:hover:!pressed{\n"
"	border: 1px solid #000000;\n"
"}")
        self.minimizeButton.setIconSize(QSize(20, 20))
        self.minimizeButton.setCheckable(False)
        self.minimizeButton.setFlat(True)

        self.horizontalLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.frame)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(35, 35))
        self.closeButton.setStyleSheet(u"QPushButton:hover:!pressed{\n"
"	border: 1px solid #000000;\n"
"}")
        self.closeButton.setIconSize(QSize(20, 20))
        self.closeButton.setFlat(True)

        self.horizontalLayout.addWidget(self.closeButton)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Note)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 0, 5, 5)
        self.splitter = QSplitter(self.frame_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setStyleSheet(u"QSplitter::handle{\n"
"	border: 1px solid black;\n"
"}")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.editorLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.editorLayout.setSpacing(0)
        self.editorLayout.setObjectName(u"editorLayout")
        self.editorLayout.setContentsMargins(0, 0, 0, 0)
        self.editLabel = QLabel(self.verticalLayoutWidget_2)
        self.editLabel.setObjectName(u"editLabel")
        font = QFont()
        font.setFamilies([u"Cascadia Mono"])
        font.setPointSize(12)
        self.editLabel.setFont(font)

        self.editorLayout.addWidget(self.editLabel)

        self.editor = MarkdownEditor(self.verticalLayoutWidget_2)
        self.editor.setObjectName(u"editor")
        self.editor.setStyleSheet(u"QTextEdit, QTextBrowser{\n"
"\n"
"border:1px solid #000000;\n"
"}")

        self.editorLayout.addWidget(self.editor)

        self.splitter.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.previewLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.previewLayout.setSpacing(0)
        self.previewLayout.setObjectName(u"previewLayout")
        self.previewLayout.setContentsMargins(0, 0, 0, 0)
        self.previewLabel = QLabel(self.verticalLayoutWidget)
        self.previewLabel.setObjectName(u"previewLabel")
        self.previewLabel.setFont(font)

        self.previewLayout.addWidget(self.previewLabel)

        self.preview = MarkdownPreview(self.verticalLayoutWidget)
        self.preview.setObjectName(u"preview")
        self.preview.setStyleSheet(u"QTextEdit{\n"
"\n"
"border:1px solid #000000;\n"
"}")
        self.preview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.preview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.preview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.preview.setSearchPaths([])
        self.preview.setOpenExternalLinks(True)

        self.previewLayout.addWidget(self.preview)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.horizontalLayout_4.addWidget(self.splitter)


        self.verticalLayout.addWidget(self.frame_2)


        self.retranslateUi(Note)

        QMetaObject.connectSlotsByName(Note)
    # setupUi

    def retranslateUi(self, Note):
        Note.setWindowTitle(QCoreApplication.translate("Note", u"Form", None))
        self.newNoteButton.setText("")
        self.pinButton.setText("")
        self.editButton.setText("")
        self.minimizeButton.setText("")
        self.closeButton.setText("")
        self.editLabel.setText(QCoreApplication.translate("Note", u"Edit Markdown", None))
        self.previewLabel.setText(QCoreApplication.translate("Note", u"Preview", None))
    # retranslateUi

