# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'labelName.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)
import 资源_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(309, 271)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_main)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMaximumSize(QSize(16777215, 120))
        self.frame_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_top)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_t_top = QFrame(self.frame_top)
        self.frame_t_top.setObjectName(u"frame_t_top")
        self.frame_t_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_t_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_t_t_left = QFrame(self.frame_t_top)
        self.frame_t_t_left.setObjectName(u"frame_t_t_left")
        self.frame_t_t_left.setMinimumSize(QSize(165, 0))
        self.frame_t_t_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_t_left.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_t_t_left)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 6, 0)
        self.label_name = QLabel(self.frame_t_t_left)
        self.label_name.setObjectName(u"label_name")

        self.horizontalLayout_2.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit(self.frame_t_t_left)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.horizontalLayout_2.addWidget(self.lineEdit_name)


        self.horizontalLayout.addWidget(self.frame_t_t_left)

        self.frame_t_t_right = QFrame(self.frame_t_top)
        self.frame_t_t_right.setObjectName(u"frame_t_t_right")
        self.frame_t_t_right.setMinimumSize(QSize(120, 0))
        self.frame_t_t_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_t_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_t_t_right)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_group = QLabel(self.frame_t_t_right)
        self.label_group.setObjectName(u"label_group")
        self.label_group.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_3.addWidget(self.label_group)

        self.comboBox_group = QComboBox(self.frame_t_t_right)
        self.comboBox_group.setObjectName(u"comboBox_group")

        self.horizontalLayout_3.addWidget(self.comboBox_group)


        self.horizontalLayout.addWidget(self.frame_t_t_right)


        self.verticalLayout_3.addWidget(self.frame_t_top)

        self.frame_t_center = QFrame(self.frame_top)
        self.frame_t_center.setObjectName(u"frame_t_center")
        self.frame_t_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_t_center)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_group_add = QLabel(self.frame_t_center)
        self.label_group_add.setObjectName(u"label_group_add")

        self.horizontalLayout_4.addWidget(self.label_group_add)

        self.lineEdit_group_add = QLineEdit(self.frame_t_center)
        self.lineEdit_group_add.setObjectName(u"lineEdit_group_add")

        self.horizontalLayout_4.addWidget(self.lineEdit_group_add)

        self.pushButton_group_add = QPushButton(self.frame_t_center)
        self.pushButton_group_add.setObjectName(u"pushButton_group_add")

        self.horizontalLayout_4.addWidget(self.pushButton_group_add)


        self.verticalLayout_3.addWidget(self.frame_t_center)

        self.frame_t_bottom = QFrame(self.frame_top)
        self.frame_t_bottom.setObjectName(u"frame_t_bottom")
        self.frame_t_bottom.setMaximumSize(QSize(16777215, 70))
        self.frame_t_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_t_bottom)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.textEdit_info = QTextEdit(self.frame_t_bottom)
        self.textEdit_info.setObjectName(u"textEdit_info")
        self.textEdit_info.setMinimumSize(QSize(0, 60))
        self.textEdit_info.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout_5.addWidget(self.textEdit_info)


        self.verticalLayout_3.addWidget(self.frame_t_bottom)


        self.verticalLayout_2.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        self.frame_center.setMaximumSize(QSize(16777215, 30))
        self.frame_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_c_left = QFrame(self.frame_center)
        self.frame_c_left.setObjectName(u"frame_c_left")
        self.frame_c_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_left.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_c_left)

        self.frame_c_center = QFrame(self.frame_center)
        self.frame_c_center.setObjectName(u"frame_c_center")
        self.frame_c_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_center.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_c_center)

        self.frame_c_right = QFrame(self.frame_center)
        self.frame_c_right.setObjectName(u"frame_c_right")
        self.frame_c_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_c_right)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ok = QPushButton(self.frame_c_right)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        icon = QIcon()
        icon.addFile(u":/img/resources/imgs/mti-\u786e\u5b9a.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_ok.setIcon(icon)

        self.horizontalLayout_6.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.frame_c_right)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        icon1 = QIcon()
        icon1.addFile(u":/img/resources/imgs/\u53d6\u6d88.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_cancel.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.pushButton_cancel)


        self.horizontalLayout_5.addWidget(self.frame_c_right)


        self.verticalLayout_2.addWidget(self.frame_center)

        self.frame_bottom = QFrame(self.frame_main)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMinimumSize(QSize(0, 110))
        self.frame_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_bottom)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 10, 0, 0)
        self.label_name_list = QLabel(self.frame_bottom)
        self.label_name_list.setObjectName(u"label_name_list")

        self.verticalLayout_4.addWidget(self.label_name_list)

        self.listWidget_name_list = QListWidget(self.frame_bottom)
        self.listWidget_name_list.setObjectName(u"listWidget_name_list")

        self.verticalLayout_4.addWidget(self.listWidget_name_list)


        self.verticalLayout_2.addWidget(self.frame_bottom)


        self.verticalLayout.addWidget(self.frame_main)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u6807\u6ce8\u540d\u79f0", None))
        self.label_name.setText(QCoreApplication.translate("Dialog", u"\u6807\u6ce8\u540d\u79f0", None))
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8bf7\u586b\u5199\u6807\u6ce8\u540d\u79f0", None))
        self.label_group.setText(QCoreApplication.translate("Dialog", u"\u5206\u7ec4", None))
        self.label_group_add.setText(QCoreApplication.translate("Dialog", u"\u589e\u52a0\u5206\u7ec4", None))
        self.lineEdit_group_add.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8bf7\u586b\u5199\u9700\u8981\u65b0\u589e\u7684\u5206\u7ec4\u540d\u79f0", None))
        self.pushButton_group_add.setText(QCoreApplication.translate("Dialog", u"\u65b0\u589e", None))
        self.textEdit_info.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u9644\u52a0\u63cf\u8ff0\u4fe1\u606f", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
        self.label_name_list.setText(QCoreApplication.translate("Dialog", u"\u540d\u79f0\u5217\u8868", None))
    # retranslateUi

