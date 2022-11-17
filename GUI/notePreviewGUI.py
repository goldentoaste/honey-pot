# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'notePreview.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QHBoxLayout, QLabel,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_NotePreview(object):
    def setupUi(self, NotePreview):
        if not NotePreview.objectName():
            NotePreview.setObjectName(u"NotePreview")
        NotePreview.resize(340, 140)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NotePreview.sizePolicy().hasHeightForWidth())
        NotePreview.setSizePolicy(sizePolicy)
        NotePreview.setMinimumSize(QSize(340, 140))
        NotePreview.setAutoFillBackground(False)
        NotePreview.setStyleSheet(u"QWidget#NotePreview{\n"
"	background-color: 	#FAF0C8;\n"
"}")
        self.verticalLayout = QVBoxLayout(NotePreview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.timeLabel = QLabel(NotePreview)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.timeLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textBrowser = QTextBrowser(NotePreview)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.textBrowser.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(NotePreview)

        QMetaObject.connectSlotsByName(NotePreview)
    # setupUi

    def retranslateUi(self, NotePreview):
        NotePreview.setWindowTitle(QCoreApplication.translate("NotePreview", u"Form", None))
        self.timeLabel.setText(QCoreApplication.translate("NotePreview", u"Data/time", None))
    # retranslateUi

