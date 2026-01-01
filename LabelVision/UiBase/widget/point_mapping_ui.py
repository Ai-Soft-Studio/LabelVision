# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'point_mapping.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(447, 626)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMaximumSize(QSize(16777215, 200))
        self.frame_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_top)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_info = QLabel(self.frame_top)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setMaximumSize(QSize(16777215, 30))
        self.label_info.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_info)

        self.label_info_text = QLabel(self.frame_top)
        self.label_info_text.setObjectName(u"label_info_text")
        self.label_info_text.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.label_info_text.setAutoFillBackground(True)
        self.label_info_text.setTextFormat(Qt.TextFormat.AutoText)
        self.label_info_text.setScaledContents(False)
        self.label_info_text.setWordWrap(True)
        self.label_info_text.setMargin(5)

        self.verticalLayout_3.addWidget(self.label_info_text)


        self.verticalLayout_2.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame)
        self.frame_center.setObjectName(u"frame_center")
        self.frame_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_center)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_c_left = QFrame(self.frame_center)
        self.frame_c_left.setObjectName(u"frame_c_left")
        self.frame_c_left.setMinimumSize(QSize(200, 0))
        self.frame_c_left.setMaximumSize(QSize(16777215, 16777215))
        self.frame_c_left.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_c_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_left.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_c_left)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_point_original = QLabel(self.frame_c_left)
        self.label_point_original.setObjectName(u"label_point_original")
        self.label_point_original.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.label_point_original.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_point_original)

        self.listWidget_point_original = QListWidget(self.frame_c_left)
        self.listWidget_point_original.setObjectName(u"listWidget_point_original")
        self.listWidget_point_original.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.listWidget_point_original)


        self.horizontalLayout.addWidget(self.frame_c_left)

        self.frame_c_right = QFrame(self.frame_center)
        self.frame_c_right.setObjectName(u"frame_c_right")
        self.frame_c_right.setMinimumSize(QSize(200, 0))
        self.frame_c_right.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_c_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_right.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_c_right)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_point_mapping = QLabel(self.frame_c_right)
        self.label_point_mapping.setObjectName(u"label_point_mapping")
        self.label_point_mapping.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_point_mapping.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_point_mapping)

        self.listWidget_point_mapping = QListWidget(self.frame_c_right)
        self.listWidget_point_mapping.setObjectName(u"listWidget_point_mapping")
        self.listWidget_point_mapping.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.listWidget_point_mapping.setDragEnabled(False)
        self.listWidget_point_mapping.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)

        self.verticalLayout_4.addWidget(self.listWidget_point_mapping)


        self.horizontalLayout.addWidget(self.frame_c_right)


        self.verticalLayout_2.addWidget(self.frame_center)

        self.frame_bottom = QFrame(self.frame)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMinimumSize(QSize(0, 40))
        self.frame_bottom.setMaximumSize(QSize(16777215, 40))
        self.frame_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ok = QPushButton(self.frame_bottom)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(0, 38))

        self.horizontalLayout_2.addWidget(self.pushButton_ok)


        self.verticalLayout_2.addWidget(self.frame_bottom)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u5173\u952e\u70b9  - \u955c\u50cf\u6620\u5c04", None))
        self.label_info.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">\u5173\u952e\u70b9\u955c\u50cf\u7ffb\u8f6c</span></p></body></html>", None))
        self.label_info_text.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>\u5f53\u56fe\u50cf\u88ab\u6c34\u5e73\u7ffb\u8f6c\u65f6,\u5173\u952e\u70b9\u7684\u987a\u5e8f\u5e94\u8fdb\u884c\u76f8\u5e94\u8c03\u6574,\u5c24\u5176\u5bf9\u4e8e\u4eba\u4f53\u59ff\u6001\u8bc6\u522b\u7684\u6a21\u578b\u6765\u8bf4,\u5728\u8bad\u7ec3\u9636\u6bb5\u53ef\u80fd\u9700\u8981\u6784\u5efa\u5bf9\u5e94\u7684\u5173\u952e\u70b9\u955c\u50cf\u6620\u5c04\u5173\u7cfb.</p><p>\u4f8b\u5982:</p><p>[\u9f3b\u5b50,<span style=\" color:#aa0000;\">\u5de6\u773c</span>,<span style=\" color:#00aa00;\">\u53f3\u773c</span>,\u8116\u5b50,<span style=\" color:#aa0000;\">\u5de6\u80a9</span>,<span style=\" color:#00aa00;\">\u53f3\u80a9</span>,<span style=\" color:#aa0000;\">\u5de6\u624b</span>,<span style=\" color:#00aa00;\">\u53f3\u624b</span>,...]</p><p>\u5bf9\u5e94\u7684\u7ffb\u8f6c\u6620\u5c04\u5e94\u4e3a:</p><p>[\u9f3b\u5b50,<span style=\" color:#00aa00;\">\u53f3\u773c</span>,<span style=\" color:#aa0000;\">\u5de6\u773c</span>,\u8116\u5b50,<span style=\" color:#00aa00;\">\u53f3\u80a9</span>,<span style=\" co"
                        "lor:#aa0000;\">\u5de6\u80a9</span>,<span style=\" color:#00aa00;\">\u53f3\u624b</span>,<span style=\" color:#aa0000;\">\u5de6\u624b</span>,...]</p></body></html>", None))
        self.label_point_original.setText(QCoreApplication.translate("Dialog", u"\u6e90\u5173\u952e\u70b9\u5217\u8868", None))
        self.label_point_mapping.setText(QCoreApplication.translate("Dialog", u"\u6620\u5c04\u5217\u8868(\u8bf7\u9f20\u6807\u62d6\u62fd\u8c03\u6574)", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a\u6620\u5c04", None))
    # retranslateUi

