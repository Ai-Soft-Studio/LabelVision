# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)
import 资源_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1035, 789)
        icon = QIcon()
        icon.addFile(u":/img/resources/imgs/app.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.action_file_open_dir = QAction(MainWindow)
        self.action_file_open_dir.setObjectName(u"action_file_open_dir")
        icon1 = QIcon()
        icon1.addFile(u":/img/resources/imgs/\u6587\u4ef6\u5939_\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_file_open_dir.setIcon(icon1)
        self.action_file_img_next = QAction(MainWindow)
        self.action_file_img_next.setObjectName(u"action_file_img_next")
        icon2 = QIcon()
        icon2.addFile(u":/img/resources/imgs/\u4e0b\u4e00\u5f20.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_file_img_next.setIcon(icon2)
        self.action_file_img_prev = QAction(MainWindow)
        self.action_file_img_prev.setObjectName(u"action_file_img_prev")
        icon3 = QIcon()
        icon3.addFile(u":/img/resources/imgs/\u4e0a\u4e00\u5f20.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_file_img_prev.setIcon(icon3)
        self.action_file_img_next_nolabel = QAction(MainWindow)
        self.action_file_img_next_nolabel.setObjectName(u"action_file_img_next_nolabel")
        self.action_file_img_next_nolabel.setIcon(icon2)
        self.action_file_img_prev_nolabel = QAction(MainWindow)
        self.action_file_img_prev_nolabel.setObjectName(u"action_file_img_prev_nolabel")
        self.action_file_img_prev_nolabel.setIcon(icon3)
        self.action_file_open_video = QAction(MainWindow)
        self.action_file_open_video.setObjectName(u"action_file_open_video")
        icon4 = QIcon()
        icon4.addFile(u":/img/resources/imgs/\u89c6\u9891.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_file_open_video.setIcon(icon4)
        self.action_file_delete_img = QAction(MainWindow)
        self.action_file_delete_img.setObjectName(u"action_file_delete_img")
        icon5 = QIcon()
        icon5.addFile(u":/img/resources/imgs/\u5220\u9664.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_file_delete_img.setIcon(icon5)
        self.action_file_exit = QAction(MainWindow)
        self.action_file_exit.setObjectName(u"action_file_exit")
        icon6 = QIcon()
        icon6.addFile(u":/img/resources/imgs/\u9000\u51fa.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_file_exit.setIcon(icon6)
        self.action_edit_create_rect = QAction(MainWindow)
        self.action_edit_create_rect.setObjectName(u"action_edit_create_rect")
        icon7 = QIcon()
        icon7.addFile(u":/img/resources/imgs/\u77e9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_create_rect.setIcon(icon7)
        self.action_edit_create_polygon = QAction(MainWindow)
        self.action_edit_create_polygon.setObjectName(u"action_edit_create_polygon")
        icon8 = QIcon()
        icon8.addFile(u":/img/resources/imgs/\u591a\u8fb9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_create_polygon.setIcon(icon8)
        self.action_edit_create_point = QAction(MainWindow)
        self.action_edit_create_point.setObjectName(u"action_edit_create_point")
        icon9 = QIcon()
        icon9.addFile(u":/img/resources/imgs/\u5173\u952e\u70b9.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_create_point.setIcon(icon9)
        self.action_edit_create_rotate = QAction(MainWindow)
        self.action_edit_create_rotate.setObjectName(u"action_edit_create_rotate")
        icon10 = QIcon()
        icon10.addFile(u":/img/resources/imgs/\u65cb\u8f6c.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_create_rotate.setIcon(icon10)
        self.action_edit_obj_copy = QAction(MainWindow)
        self.action_edit_obj_copy.setObjectName(u"action_edit_obj_copy")
        icon11 = QIcon()
        icon11.addFile(u":/img/resources/imgs/\u590d\u5236.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_obj_copy.setIcon(icon11)
        self.action_edit_obj_paste = QAction(MainWindow)
        self.action_edit_obj_paste.setObjectName(u"action_edit_obj_paste")
        icon12 = QIcon()
        icon12.addFile(u":/img/resources/imgs/\u7c98\u8d34.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_obj_paste.setIcon(icon12)
        self.action_edit_obj_revoke = QAction(MainWindow)
        self.action_edit_obj_revoke.setObjectName(u"action_edit_obj_revoke")
        icon13 = QIcon()
        icon13.addFile(u":/img/resources/imgs/\u64a4\u9500.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_obj_revoke.setIcon(icon13)
        self.action_edit_obj_delete = QAction(MainWindow)
        self.action_edit_obj_delete.setObjectName(u"action_edit_obj_delete")
        icon14 = QIcon()
        icon14.addFile(u":/img/resources/imgs/\u5220\u9664_\u64cd\u4f5c.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_obj_delete.setIcon(icon14)
        self.action_view_zoom_in = QAction(MainWindow)
        self.action_view_zoom_in.setObjectName(u"action_view_zoom_in")
        icon15 = QIcon()
        icon15.addFile(u":/img/resources/imgs/\u653e\u5927.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_view_zoom_in.setIcon(icon15)
        self.action_view_zoom_out = QAction(MainWindow)
        self.action_view_zoom_out.setObjectName(u"action_view_zoom_out")
        icon16 = QIcon()
        icon16.addFile(u":/img/resources/imgs/\u7f29\u5c0f.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_view_zoom_out.setIcon(icon16)
        self.action_view_zoom_restore = QAction(MainWindow)
        self.action_view_zoom_restore.setObjectName(u"action_view_zoom_restore")
        icon17 = QIcon()
        icon17.addFile(u":/img/resources/imgs/\u8fd8\u539f.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_view_zoom_restore.setIcon(icon17)
        self.action_view_zoom_auto = QAction(MainWindow)
        self.action_view_zoom_auto.setObjectName(u"action_view_zoom_auto")
        icon18 = QIcon()
        icon18.addFile(u":/img/resources/imgs/\u9002\u5e94\u7a97\u53e3.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_view_zoom_auto.setIcon(icon18)
        self.action_view_obj_hide = QAction(MainWindow)
        self.action_view_obj_hide.setObjectName(u"action_view_obj_hide")
        icon19 = QIcon()
        icon19.addFile(u":/img/resources/imgs/\u9690\u85cf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_view_obj_hide.setIcon(icon19)
        self.action_view_obj_show = QAction(MainWindow)
        self.action_view_obj_show.setObjectName(u"action_view_obj_show")
        icon20 = QIcon()
        icon20.addFile(u":/img/resources/imgs/\u663e\u793a.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_view_obj_show.setIcon(icon20)
        self.action_view_show_name = QAction(MainWindow)
        self.action_view_show_name.setObjectName(u"action_view_show_name")
        self.action_view_show_name.setCheckable(True)
        self.action_view_show_name.setChecked(True)
        self.action_view_show_info = QAction(MainWindow)
        self.action_view_show_info.setObjectName(u"action_view_show_info")
        self.action_view_show_info.setCheckable(True)
        self.action_view_show_info.setChecked(True)
        self.action_view_show_group = QAction(MainWindow)
        self.action_view_show_group.setObjectName(u"action_view_show_group")
        self.action_view_show_group.setCheckable(True)
        self.action_view_show_group.setChecked(True)
        self.action_help_about = QAction(MainWindow)
        self.action_help_about.setObjectName(u"action_help_about")
        icon21 = QIcon()
        icon21.addFile(u":/img/resources/imgs/\u5173\u4e8e.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_help_about.setIcon(icon21)
        self.action_help_Usage = QAction(MainWindow)
        self.action_help_Usage.setObjectName(u"action_help_Usage")
        icon22 = QIcon()
        icon22.addFile(u":/img/resources/imgs/\u4f7f\u7528\u65b9\u6cd5.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_help_Usage.setIcon(icon22)
        self.action_edit_obj_restore = QAction(MainWindow)
        self.action_edit_obj_restore.setObjectName(u"action_edit_obj_restore")
        icon23 = QIcon()
        icon23.addFile(u":/img/resources/imgs/\u6062\u590d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_obj_restore.setIcon(icon23)
        self.action_line_link = QAction(MainWindow)
        self.action_line_link.setObjectName(u"action_line_link")
        icon24 = QIcon()
        icon24.addFile(u":/img/resources/imgs/\u7ebf\u6761\u8fde\u63a5.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_line_link.setIcon(icon24)
        self.action_line_unlink = QAction(MainWindow)
        self.action_line_unlink.setObjectName(u"action_line_unlink")
        icon25 = QIcon()
        icon25.addFile(u":/img/resources/imgs/\u7ebf\u6761\u65ad\u5f00.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_line_unlink.setIcon(icon25)
        self.action_edit_create_line = QAction(MainWindow)
        self.action_edit_create_line.setObjectName(u"action_edit_create_line")
        icon26 = QIcon()
        icon26.addFile(u":/img/resources/imgs/\u52a0\u7ebf\u6761.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_edit_create_line.setIcon(icon26)
        self.action_export_labels_rect = QAction(MainWindow)
        self.action_export_labels_rect.setObjectName(u"action_export_labels_rect")
        self.action_export_labels_rect.setIcon(icon7)
        self.action_export_labels_polygon = QAction(MainWindow)
        self.action_export_labels_polygon.setObjectName(u"action_export_labels_polygon")
        self.action_export_labels_polygon.setIcon(icon8)
        self.action_export_labels_point = QAction(MainWindow)
        self.action_export_labels_point.setObjectName(u"action_export_labels_point")
        self.action_export_labels_point.setIcon(icon9)
        self.action_export_labels_rotation = QAction(MainWindow)
        self.action_export_labels_rotation.setObjectName(u"action_export_labels_rotation")
        self.action_export_labels_rotation.setIcon(icon10)
        self.action_export_labels_line = QAction(MainWindow)
        self.action_export_labels_line.setObjectName(u"action_export_labels_line")
        self.action_export_labels_line.setIcon(icon26)
        self.action_keys_info = QAction(MainWindow)
        self.action_keys_info.setObjectName(u"action_keys_info")
        icon27 = QIcon()
        icon27.addFile(u":/img/resources/imgs/\u5feb\u6377\u952e.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_keys_info.setIcon(icon27)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.centralwidget)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 110))
        self.frame_top.setMaximumSize(QSize(16777215, 110))
        self.frame_top.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_top)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_t_top = QFrame(self.frame_top)
        self.frame_t_top.setObjectName(u"frame_t_top")
        self.frame_t_top.setMaximumSize(QSize(16777215, 36))
        self.frame_t_top.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"border-radius: 5px;\n"
"")
        self.frame_t_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_t_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 0, 6, 0)
        self.frame_t_t_left = QFrame(self.frame_t_top)
        self.frame_t_t_left.setObjectName(u"frame_t_t_left")
        self.frame_t_t_left.setMaximumSize(QSize(120, 32))
        self.frame_t_t_left.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"border-radius: 5px;\n"
"")
        self.frame_t_t_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_t_left.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_t_t_left)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_file_open_dir = QPushButton(self.frame_t_t_left)
        self.pushButton_file_open_dir.setObjectName(u"pushButton_file_open_dir")
        self.pushButton_file_open_dir.setMaximumSize(QSize(30, 30))
        self.pushButton_file_open_dir.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_file_open_dir.setIcon(icon1)
        self.pushButton_file_open_dir.setIconSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.pushButton_file_open_dir)

        self.pushButton_file_open_video = QPushButton(self.frame_t_t_left)
        self.pushButton_file_open_video.setObjectName(u"pushButton_file_open_video")
        self.pushButton_file_open_video.setMaximumSize(QSize(30, 30))
        self.pushButton_file_open_video.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_file_open_video.setIcon(icon4)
        self.pushButton_file_open_video.setIconSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.pushButton_file_open_video)

        self.pushButton_file_img_delete = QPushButton(self.frame_t_t_left)
        self.pushButton_file_img_delete.setObjectName(u"pushButton_file_img_delete")
        self.pushButton_file_img_delete.setMaximumSize(QSize(30, 30))
        self.pushButton_file_img_delete.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_file_img_delete.setIcon(icon5)
        self.pushButton_file_img_delete.setIconSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.pushButton_file_img_delete)


        self.horizontalLayout.addWidget(self.frame_t_t_left)

        self.frame_t_t_center = QFrame(self.frame_t_top)
        self.frame_t_t_center.setObjectName(u"frame_t_t_center")
        self.frame_t_t_center.setMaximumSize(QSize(200, 32))
        self.frame_t_t_center.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"border-radius: 0px ;\n"
"border-left: 2px solid rgb(255, 255, 255);\n"
"border-right: 2px solid rgb(255, 255, 255);\n"
"")
        self.frame_t_t_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_t_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_t_t_center)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_edit_create_rect = QPushButton(self.frame_t_t_center)
        self.pushButton_edit_create_rect.setObjectName(u"pushButton_edit_create_rect")
        self.pushButton_edit_create_rect.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_create_rect.setStyleSheet(u"QPushButton:!checked {  \n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"}  \n"
"QPushButton:checked {  \n"
"	background-color: rgb(50,50, 50);\n"
"	color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"} \n"
"\n"
"")
        icon28 = QIcon()
        icon28.addFile(u":/img/resources/imgs/\u77e9\u5f62_\u672a\u9009\u4e2d.png", QSize(), QIcon.Mode.Selected, QIcon.State.Off)
        icon28.addFile(u":/img/resources/imgs/\u77e9\u5f62.png", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.pushButton_edit_create_rect.setIcon(icon28)
        self.pushButton_edit_create_rect.setIconSize(QSize(28, 28))
        self.pushButton_edit_create_rect.setCheckable(True)
        self.pushButton_edit_create_rect.setChecked(True)

        self.horizontalLayout_3.addWidget(self.pushButton_edit_create_rect)

        self.pushButton_edit_create_polygon = QPushButton(self.frame_t_t_center)
        self.pushButton_edit_create_polygon.setObjectName(u"pushButton_edit_create_polygon")
        self.pushButton_edit_create_polygon.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_create_polygon.setStyleSheet(u"QPushButton:!checked {  \n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"}  \n"
"QPushButton:checked {  \n"
"	background-color: rgb(50,50, 50);\n"
"	color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"} \n"
"")
        icon29 = QIcon()
        icon29.addFile(u":/img/resources/imgs/\u591a\u8fb9\u5f62_\u672a\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon29.addFile(u":/img/resources/imgs/\u591a\u8fb9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        icon29.addFile(u":/img/resources/imgs/\u591a\u8fb9\u5f62_\u672a\u9009\u4e2d.png", QSize(), QIcon.Mode.Selected, QIcon.State.Off)
        icon29.addFile(u":/img/resources/imgs/\u591a\u8fb9\u5f62.png", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.pushButton_edit_create_polygon.setIcon(icon29)
        self.pushButton_edit_create_polygon.setIconSize(QSize(28, 28))
        self.pushButton_edit_create_polygon.setCheckable(True)
        self.pushButton_edit_create_polygon.setChecked(False)

        self.horizontalLayout_3.addWidget(self.pushButton_edit_create_polygon)

        self.pushButton_edit_create_point = QPushButton(self.frame_t_t_center)
        self.pushButton_edit_create_point.setObjectName(u"pushButton_edit_create_point")
        self.pushButton_edit_create_point.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_create_point.setStyleSheet(u"QPushButton:!checked {  \n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"}  \n"
"QPushButton:checked {  \n"
"	background-color: rgb(50,50, 50);\n"
"	color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"} \n"
"\n"
"")
        icon30 = QIcon()
        icon30.addFile(u":/img/resources/imgs/\u5173\u952e\u70b9_\u672a\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon30.addFile(u":/img/resources/imgs/\u5173\u952e\u70b9.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_edit_create_point.setIcon(icon30)
        self.pushButton_edit_create_point.setIconSize(QSize(28, 28))
        self.pushButton_edit_create_point.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButton_edit_create_point)

        self.pushButton_edit_create_rotate = QPushButton(self.frame_t_t_center)
        self.pushButton_edit_create_rotate.setObjectName(u"pushButton_edit_create_rotate")
        self.pushButton_edit_create_rotate.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_create_rotate.setStyleSheet(u"QPushButton:!checked {  \n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"}  \n"
"QPushButton:checked {  \n"
"	background-color: rgb(50,50, 50);\n"
"	color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"} \n"
"")
        icon31 = QIcon()
        icon31.addFile(u":/img/resources/imgs/\u65cb\u8f6c_\u672a\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon31.addFile(u":/img/resources/imgs/\u65cb\u8f6c.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_edit_create_rotate.setIcon(icon31)
        self.pushButton_edit_create_rotate.setIconSize(QSize(28, 28))
        self.pushButton_edit_create_rotate.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButton_edit_create_rotate)

        self.pushButton_edit_create_line = QPushButton(self.frame_t_t_center)
        self.pushButton_edit_create_line.setObjectName(u"pushButton_edit_create_line")
        self.pushButton_edit_create_line.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_create_line.setStyleSheet(u"QPushButton:!checked {  \n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"}  \n"
"QPushButton:checked {  \n"
"	background-color: rgb(50,50, 50);\n"
"	color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;\n"
"} ")
        icon32 = QIcon()
        icon32.addFile(u":/img/resources/imgs/\u52a0\u7ebf\u6761_\u672a\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon32.addFile(u":/img/resources/imgs/\u52a0\u7ebf\u6761.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_edit_create_line.setIcon(icon32)
        self.pushButton_edit_create_line.setIconSize(QSize(32, 32))
        self.pushButton_edit_create_line.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButton_edit_create_line)


        self.horizontalLayout.addWidget(self.frame_t_t_center)

        self.frame_t_t_right = QFrame(self.frame_t_top)
        self.frame_t_t_right.setObjectName(u"frame_t_t_right")
        self.frame_t_t_right.setMaximumSize(QSize(240, 32))
        self.frame_t_t_right.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"border-radius: 5px;\n"
"")
        self.frame_t_t_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_t_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_t_t_right)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_edit_obj_revoke = QPushButton(self.frame_t_t_right)
        self.pushButton_edit_obj_revoke.setObjectName(u"pushButton_edit_obj_revoke")
        self.pushButton_edit_obj_revoke.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_obj_revoke.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_edit_obj_revoke.setIcon(icon13)
        self.pushButton_edit_obj_revoke.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_edit_obj_revoke)

        self.pushButton_edit_obj_restore = QPushButton(self.frame_t_t_right)
        self.pushButton_edit_obj_restore.setObjectName(u"pushButton_edit_obj_restore")
        self.pushButton_edit_obj_restore.setMaximumSize(QSize(30, 30))
        self.pushButton_edit_obj_restore.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_edit_obj_restore.setIcon(icon23)
        self.pushButton_edit_obj_restore.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_edit_obj_restore)

        self.pushButton_view_zoom_in = QPushButton(self.frame_t_t_right)
        self.pushButton_view_zoom_in.setObjectName(u"pushButton_view_zoom_in")
        self.pushButton_view_zoom_in.setMaximumSize(QSize(30, 30))
        self.pushButton_view_zoom_in.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_view_zoom_in.setIcon(icon15)
        self.pushButton_view_zoom_in.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_view_zoom_in)

        self.pushButton_view_zoom_out = QPushButton(self.frame_t_t_right)
        self.pushButton_view_zoom_out.setObjectName(u"pushButton_view_zoom_out")
        self.pushButton_view_zoom_out.setMaximumSize(QSize(30, 30))
        self.pushButton_view_zoom_out.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_view_zoom_out.setIcon(icon16)
        self.pushButton_view_zoom_out.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_view_zoom_out)

        self.pushButton_view_zoom_restore = QPushButton(self.frame_t_t_right)
        self.pushButton_view_zoom_restore.setObjectName(u"pushButton_view_zoom_restore")
        self.pushButton_view_zoom_restore.setMaximumSize(QSize(30, 30))
        self.pushButton_view_zoom_restore.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_view_zoom_restore.setIcon(icon17)
        self.pushButton_view_zoom_restore.setIconSize(QSize(26, 26))

        self.horizontalLayout_4.addWidget(self.pushButton_view_zoom_restore)

        self.pushButton_view_zoom_auto = QPushButton(self.frame_t_t_right)
        self.pushButton_view_zoom_auto.setObjectName(u"pushButton_view_zoom_auto")
        self.pushButton_view_zoom_auto.setMaximumSize(QSize(30, 30))
        self.pushButton_view_zoom_auto.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        icon33 = QIcon()
        icon33.addFile(u":/img/resources/imgs/\u9002\u5e94\u7a97\u53e3.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_view_zoom_auto.setIcon(icon33)
        self.pushButton_view_zoom_auto.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_view_zoom_auto)

        self.pushButton_view_obj_hide = QPushButton(self.frame_t_t_right)
        self.pushButton_view_obj_hide.setObjectName(u"pushButton_view_obj_hide")
        self.pushButton_view_obj_hide.setMaximumSize(QSize(30, 30))
        self.pushButton_view_obj_hide.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        icon34 = QIcon()
        icon34.addFile(u":/img/resources/imgs/\u9690\u85cf.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_view_obj_hide.setIcon(icon34)
        self.pushButton_view_obj_hide.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_view_obj_hide)

        self.pushButton_view_obj_show = QPushButton(self.frame_t_t_right)
        self.pushButton_view_obj_show.setObjectName(u"pushButton_view_obj_show")
        self.pushButton_view_obj_show.setMaximumSize(QSize(30, 30))
        self.pushButton_view_obj_show.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        icon35 = QIcon()
        icon35.addFile(u":/img/resources/imgs/\u663e\u793a.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_view_obj_show.setIcon(icon35)
        self.pushButton_view_obj_show.setIconSize(QSize(28, 28))

        self.horizontalLayout_4.addWidget(self.pushButton_view_obj_show)


        self.horizontalLayout.addWidget(self.frame_t_t_right)

        self.frame_t_t_other = QFrame(self.frame_t_top)
        self.frame_t_t_other.setObjectName(u"frame_t_t_other")
        self.frame_t_t_other.setMaximumSize(QSize(16777215, 32))
        self.frame_t_t_other.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"border-radius: 5px;\n"
"")
        self.frame_t_t_other.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_t_other.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame_t_t_other)


        self.verticalLayout_2.addWidget(self.frame_t_top)

        self.frame_t_center = QFrame(self.frame_top)
        self.frame_t_center.setObjectName(u"frame_t_center")
        self.frame_t_center.setMinimumSize(QSize(0, 0))
        self.frame_t_center.setMaximumSize(QSize(16777215, 0))
        self.frame_t_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_center.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_t_center.setLineWidth(0)

        self.verticalLayout_2.addWidget(self.frame_t_center)

        self.frame_t_bottom = QFrame(self.frame_top)
        self.frame_t_bottom.setObjectName(u"frame_t_bottom")
        self.frame_t_bottom.setMaximumSize(QSize(16777215, 60))
        self.frame_t_bottom.setFrameShape(QFrame.Shape.Box)
        self.frame_t_bottom.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_t_bottom)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_t_b_left = QFrame(self.frame_t_bottom)
        self.frame_t_b_left.setObjectName(u"frame_t_b_left")
        self.frame_t_b_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_b_left.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_t_b_left)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_t_b_l_top = QFrame(self.frame_t_b_left)
        self.frame_t_b_l_top.setObjectName(u"frame_t_b_l_top")
        self.frame_t_b_l_top.setMaximumSize(QSize(16777215, 30))
        self.frame_t_b_l_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_b_l_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_t_b_l_top)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(6, 0, 6, 0)
        self.label_model_path = QLabel(self.frame_t_b_l_top)
        self.label_model_path.setObjectName(u"label_model_path")
        self.label_model_path.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_7.addWidget(self.label_model_path)

        self.lineEdit_model_path = QLineEdit(self.frame_t_b_l_top)
        self.lineEdit_model_path.setObjectName(u"lineEdit_model_path")
        self.lineEdit_model_path.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_7.addWidget(self.lineEdit_model_path)

        self.pushButton_model_path = QPushButton(self.frame_t_b_l_top)
        self.pushButton_model_path.setObjectName(u"pushButton_model_path")
        self.pushButton_model_path.setMaximumSize(QSize(16777215, 20))
        self.pushButton_model_path.setStyleSheet(u"QPushButton {\n"
"	border: 1px solid rgb(0, 0, 0);\n"
"	border-radius: 2px;	\n"
"	background-color: rgb(200, 200, 200);\n"
"	color: rgb(255, 255, 255);\n"
"	padding-top: 0px;    /* \u4e0a\u5185\u8fb9\u8ddd */\n"
"    padding-right: 15px;  /* \u53f3\u5185\u8fb9\u8ddd */\n"
"    padding-bottom: 0px; /* \u4e0b\u5185\u8fb9\u8ddd */\n"
"    padding-left: 15px;   /* \u5de6\u5185\u8fb9\u8ddd */\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")

        self.horizontalLayout_7.addWidget(self.pushButton_model_path)


        self.verticalLayout_3.addWidget(self.frame_t_b_l_top)

        self.frame_t_b_l_center = QFrame(self.frame_t_b_left)
        self.frame_t_b_l_center.setObjectName(u"frame_t_b_l_center")
        self.frame_t_b_l_center.setMaximumSize(QSize(16777215, 0))
        self.frame_t_b_l_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_b_l_center.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.frame_t_b_l_center)

        self.frame_t_b_l_bottom = QFrame(self.frame_t_b_left)
        self.frame_t_b_l_bottom.setObjectName(u"frame_t_b_l_bottom")
        self.frame_t_b_l_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_b_l_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.label_model_score = QLabel(self.frame_t_b_l_bottom)
        self.label_model_score.setObjectName(u"label_model_score")
        self.label_model_score.setGeometry(QRect(10, 0, 52, 14))
        self.doubleSpinBox_model_score = QDoubleSpinBox(self.frame_t_b_l_bottom)
        self.doubleSpinBox_model_score.setObjectName(u"doubleSpinBox_model_score")
        self.doubleSpinBox_model_score.setGeometry(QRect(60, 0, 88, 22))
        self.doubleSpinBox_model_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_model_score.setDecimals(5)
        self.doubleSpinBox_model_score.setMaximum(1.000000000000000)
        self.doubleSpinBox_model_score.setSingleStep(0.010000000000000)
        self.doubleSpinBox_model_score.setValue(0.500000000000000)

        self.verticalLayout_3.addWidget(self.frame_t_b_l_bottom)


        self.horizontalLayout_5.addWidget(self.frame_t_b_left)

        self.frame_t_b_center = QFrame(self.frame_t_bottom)
        self.frame_t_b_center.setObjectName(u"frame_t_b_center")
        self.frame_t_b_center.setMaximumSize(QSize(0, 16777215))
        self.frame_t_b_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_b_center.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_t_b_center)

        self.frame_t_b_right = QFrame(self.frame_t_bottom)
        self.frame_t_b_right.setObjectName(u"frame_t_b_right")
        self.frame_t_b_right.setMinimumSize(QSize(70, 50))
        self.frame_t_b_right.setMaximumSize(QSize(70, 50))
        self.frame_t_b_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_t_b_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_t_b_right)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton_model_run = QPushButton(self.frame_t_b_right)
        self.pushButton_model_run.setObjectName(u"pushButton_model_run")
        self.pushButton_model_run.setMinimumSize(QSize(60, 40))
        self.pushButton_model_run.setMaximumSize(QSize(60, 40))
        font = QFont()
        font.setBold(True)
        self.pushButton_model_run.setFont(font)
        self.pushButton_model_run.setStyleSheet(u"\n"
"QPushButton {\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(200, 200, 200);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"	\n"
"}")
        icon36 = QIcon()
        icon36.addFile(u":/img/resources/imgs/\u6d4b\u8bd5\u6d4b\u8bd5_\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon36.addFile(u":/img/resources/imgs/\u6d4b\u8bd5\u6d4b\u8bd5_\u9009\u4e2d.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_model_run.setIcon(icon36)
        self.pushButton_model_run.setIconSize(QSize(28, 28))

        self.horizontalLayout_6.addWidget(self.pushButton_model_run)


        self.horizontalLayout_5.addWidget(self.frame_t_b_right)


        self.verticalLayout_2.addWidget(self.frame_t_bottom)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(self.centralwidget)
        self.frame_center.setObjectName(u"frame_center")
        self.frame_center.setMaximumSize(QSize(16777215, 16777215))
        self.frame_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_c_left = QFrame(self.frame_center)
        self.frame_c_left.setObjectName(u"frame_c_left")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_c_left.sizePolicy().hasHeightForWidth())
        self.frame_c_left.setSizePolicy(sizePolicy)
        self.frame_c_left.setMinimumSize(QSize(120, 0))
        self.frame_c_left.setMaximumSize(QSize(200, 16777215))
        self.frame_c_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_left.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_c_left)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 6, 0)
        self.lineEdit_img_search = QLineEdit(self.frame_c_left)
        self.lineEdit_img_search.setObjectName(u"lineEdit_img_search")

        self.verticalLayout_4.addWidget(self.lineEdit_img_search)

        self.listWidget_img_list = QListWidget(self.frame_c_left)
        self.listWidget_img_list.setObjectName(u"listWidget_img_list")

        self.verticalLayout_4.addWidget(self.listWidget_img_list)


        self.horizontalLayout_8.addWidget(self.frame_c_left)

        self.frame_c_center = QFrame(self.frame_center)
        self.frame_c_center.setObjectName(u"frame_c_center")
        sizePolicy.setHeightForWidth(self.frame_c_center.sizePolicy().hasHeightForWidth())
        self.frame_c_center.setSizePolicy(sizePolicy)
        self.frame_c_center.setMinimumSize(QSize(0, 0))
        self.frame_c_center.setMaximumSize(QSize(16777215, 16777215))
        self.frame_c_center.setStyleSheet(u"border: 1px solid rgb(0, 0, 0);")
        self.frame_c_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_c_center)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_c_c_left = QFrame(self.frame_c_center)
        self.frame_c_c_left.setObjectName(u"frame_c_c_left")
        self.frame_c_c_left.setMaximumSize(QSize(20, 16777215))
        self.frame_c_c_left.setStyleSheet(u"border: 0px solid rgb(0, 0, 0);")
        self.frame_c_c_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_c_left.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_c_c_left)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_file_img_prev = QPushButton(self.frame_c_c_left)
        self.pushButton_file_img_prev.setObjectName(u"pushButton_file_img_prev")
        self.pushButton_file_img_prev.setMaximumSize(QSize(18, 18))
        self.pushButton_file_img_prev.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_file_img_prev.setIcon(icon3)
        self.pushButton_file_img_prev.setIconSize(QSize(16, 16))

        self.horizontalLayout_11.addWidget(self.pushButton_file_img_prev)


        self.horizontalLayout_9.addWidget(self.frame_c_c_left)

        self.widget_img = QWidget(self.frame_c_center)
        self.widget_img.setObjectName(u"widget_img")
        self.widget_img.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.widget_img.setStyleSheet(u"border: 0px solid rgb(0, 0, 0);")

        self.horizontalLayout_9.addWidget(self.widget_img)

        self.frame_c_c_right = QFrame(self.frame_c_center)
        self.frame_c_c_right.setObjectName(u"frame_c_c_right")
        self.frame_c_c_right.setMaximumSize(QSize(20, 16777215))
        self.frame_c_c_right.setStyleSheet(u"border: 0px solid rgb(0, 0, 0);")
        self.frame_c_c_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_c_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_c_c_right)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.pushButton_file_img_next = QPushButton(self.frame_c_c_right)
        self.pushButton_file_img_next.setObjectName(u"pushButton_file_img_next")
        self.pushButton_file_img_next.setMaximumSize(QSize(18, 18))
        self.pushButton_file_img_next.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(200, 200, 200);\n"
"	border-radius: 5px;	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 150, 150);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(100, 100, 100);\n"
"	color: rgb(150, 150, 150);\n"
"}")
        self.pushButton_file_img_next.setIcon(icon2)
        self.pushButton_file_img_next.setIconSize(QSize(16, 16))

        self.horizontalLayout_10.addWidget(self.pushButton_file_img_next)


        self.horizontalLayout_9.addWidget(self.frame_c_c_right)


        self.horizontalLayout_8.addWidget(self.frame_c_center)

        self.frame_c_right = QFrame(self.frame_center)
        self.frame_c_right.setObjectName(u"frame_c_right")
        sizePolicy.setHeightForWidth(self.frame_c_right.sizePolicy().hasHeightForWidth())
        self.frame_c_right.setSizePolicy(sizePolicy)
        self.frame_c_right.setMinimumSize(QSize(120, 0))
        self.frame_c_right.setMaximumSize(QSize(200, 16777215))
        self.frame_c_right.setStyleSheet(u"")
        self.frame_c_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_right.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_c_right)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 0, 0, 0)
        self.frame_c_r_top = QFrame(self.frame_c_right)
        self.frame_c_r_top.setObjectName(u"frame_c_r_top")
        self.frame_c_r_top.setMinimumSize(QSize(0, 60))
        self.frame_c_r_top.setMaximumSize(QSize(16777215, 140))
        self.frame_c_r_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_r_top.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_c_r_top)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_obj_info = QLabel(self.frame_c_r_top)
        self.label_obj_info.setObjectName(u"label_obj_info")

        self.verticalLayout_7.addWidget(self.label_obj_info)

        self.textEdit_obj_info = QTextEdit(self.frame_c_r_top)
        self.textEdit_obj_info.setObjectName(u"textEdit_obj_info")

        self.verticalLayout_7.addWidget(self.textEdit_obj_info)


        self.verticalLayout_5.addWidget(self.frame_c_r_top)

        self.frame_c_r_center = QFrame(self.frame_c_right)
        self.frame_c_r_center.setObjectName(u"frame_c_r_center")
        self.frame_c_r_center.setMinimumSize(QSize(0, 100))
        self.frame_c_r_center.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_r_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_c_r_center)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_label = QTabWidget(self.frame_c_r_center)
        self.tabWidget_label.setObjectName(u"tabWidget_label")
        self.tab_label_name = QWidget()
        self.tab_label_name.setObjectName(u"tab_label_name")
        self.verticalLayout_10 = QVBoxLayout(self.tab_label_name)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.listWidget_name_list = QListWidget(self.tab_label_name)
        self.listWidget_name_list.setObjectName(u"listWidget_name_list")

        self.verticalLayout_10.addWidget(self.listWidget_name_list)

        self.tabWidget_label.addTab(self.tab_label_name, "")
        self.tab_label_group = QWidget()
        self.tab_label_group.setObjectName(u"tab_label_group")
        self.verticalLayout_6 = QVBoxLayout(self.tab_label_group)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.listWidget_group_list = QListWidget(self.tab_label_group)
        self.listWidget_group_list.setObjectName(u"listWidget_group_list")

        self.verticalLayout_6.addWidget(self.listWidget_group_list)

        self.tabWidget_label.addTab(self.tab_label_group, "")

        self.horizontalLayout_14.addWidget(self.tabWidget_label)


        self.verticalLayout_5.addWidget(self.frame_c_r_center)

        self.frame_c_r_bottom = QFrame(self.frame_c_right)
        self.frame_c_r_bottom.setObjectName(u"frame_c_r_bottom")
        self.frame_c_r_bottom.setMinimumSize(QSize(0, 300))
        self.frame_c_r_bottom.setMaximumSize(QSize(16777215, 16777215))
        self.frame_c_r_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_r_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_c_r_bottom)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_label_name = QLabel(self.frame_c_r_bottom)
        self.label_label_name.setObjectName(u"label_label_name")

        self.verticalLayout_8.addWidget(self.label_label_name)

        self.frame_c_r_b_show = QFrame(self.frame_c_r_bottom)
        self.frame_c_r_b_show.setObjectName(u"frame_c_r_b_show")
        self.frame_c_r_b_show.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_r_b_show.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_c_r_b_show)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_c_r_b_name = QFrame(self.frame_c_r_b_show)
        self.frame_c_r_b_name.setObjectName(u"frame_c_r_b_name")
        self.frame_c_r_b_name.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_r_b_name.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_c_r_b_name)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_name = QLabel(self.frame_c_r_b_name)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_12.addWidget(self.label_name)

        self.comboBox_label_name = QComboBox(self.frame_c_r_b_name)
        self.comboBox_label_name.setObjectName(u"comboBox_label_name")

        self.horizontalLayout_12.addWidget(self.comboBox_label_name)


        self.verticalLayout_9.addWidget(self.frame_c_r_b_name)

        self.frame_c_r_b_group = QFrame(self.frame_c_r_b_show)
        self.frame_c_r_b_group.setObjectName(u"frame_c_r_b_group")
        self.frame_c_r_b_group.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_c_r_b_group.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_c_r_b_group)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_group = QLabel(self.frame_c_r_b_group)
        self.label_group.setObjectName(u"label_group")
        self.label_group.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_13.addWidget(self.label_group)

        self.comboBox_label_group = QComboBox(self.frame_c_r_b_group)
        self.comboBox_label_group.setObjectName(u"comboBox_label_group")

        self.horizontalLayout_13.addWidget(self.comboBox_label_group)


        self.verticalLayout_9.addWidget(self.frame_c_r_b_group)


        self.verticalLayout_8.addWidget(self.frame_c_r_b_show)

        self.listWidget_shape_list = QListWidget(self.frame_c_r_bottom)
        self.listWidget_shape_list.setObjectName(u"listWidget_shape_list")
        self.listWidget_shape_list.setDragEnabled(False)
        self.listWidget_shape_list.setAlternatingRowColors(False)
        self.listWidget_shape_list.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)

        self.verticalLayout_8.addWidget(self.listWidget_shape_list)


        self.verticalLayout_5.addWidget(self.frame_c_r_bottom)


        self.horizontalLayout_8.addWidget(self.frame_c_right)


        self.verticalLayout.addWidget(self.frame_center)

        self.frame_bottom = QFrame(self.centralwidget)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMaximumSize(QSize(16777215, 1))
        self.frame_bottom.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_bottom)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1035, 33))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu = QMenu(self.menu_file)
        self.menu.setObjectName(u"menu")
        icon37 = QIcon()
        icon37.addFile(u":/img/resources/imgs/\u5bfc\u51fa.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu.setIcon(icon37)
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_file_open_dir)
        self.menu_file.addAction(self.action_file_open_video)
        self.menu_file.addAction(self.action_file_img_next)
        self.menu_file.addAction(self.action_file_img_prev)
        self.menu_file.addAction(self.action_file_img_next_nolabel)
        self.menu_file.addAction(self.action_file_img_prev_nolabel)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_file_delete_img)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu.menuAction())
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_file_exit)
        self.menu.addAction(self.action_export_labels_rect)
        self.menu.addAction(self.action_export_labels_polygon)
        self.menu.addAction(self.action_export_labels_point)
        self.menu.addAction(self.action_export_labels_rotation)
        self.menu.addAction(self.action_export_labels_line)
        self.menu_edit.addAction(self.action_edit_create_rect)
        self.menu_edit.addAction(self.action_edit_create_polygon)
        self.menu_edit.addAction(self.action_edit_create_point)
        self.menu_edit.addAction(self.action_edit_create_rotate)
        self.menu_edit.addAction(self.action_edit_create_line)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_line_link)
        self.menu_edit.addAction(self.action_line_unlink)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_edit_obj_copy)
        self.menu_edit.addAction(self.action_edit_obj_paste)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_edit_obj_revoke)
        self.menu_edit.addAction(self.action_edit_obj_restore)
        self.menu_edit.addAction(self.action_edit_obj_delete)
        self.menu_view.addAction(self.action_view_zoom_in)
        self.menu_view.addAction(self.action_view_zoom_out)
        self.menu_view.addAction(self.action_view_zoom_restore)
        self.menu_view.addAction(self.action_view_zoom_auto)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.action_view_obj_hide)
        self.menu_view.addAction(self.action_view_obj_show)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.action_view_show_info)
        self.menu_view.addAction(self.action_view_show_name)
        self.menu_view.addAction(self.action_view_show_group)
        self.menu_help.addAction(self.action_keys_info)
        self.menu_help.addAction(self.action_help_Usage)
        self.menu_help.addAction(self.action_help_about)

        self.retranslateUi(MainWindow)

        self.tabWidget_label.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LabelVision \u534a\u81ea\u52a8\u6807\u6ce8\u5de5\u5177", None))
        self.action_file_open_dir.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u76ee\u5f55", None))
        self.action_file_img_next.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u5f20", None))
#if QT_CONFIG(shortcut)
        self.action_file_img_next.setShortcut(QCoreApplication.translate("MainWindow", u"Down", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_img_prev.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e00\u5f20", None))
#if QT_CONFIG(shortcut)
        self.action_file_img_prev.setShortcut(QCoreApplication.translate("MainWindow", u"Up", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_img_next_nolabel.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u5f20 \u672a\u6807\u6ce8", None))
#if QT_CONFIG(shortcut)
        self.action_file_img_next_nolabel.setShortcut(QCoreApplication.translate("MainWindow", u"Right", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_img_prev_nolabel.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e00\u5f20 \u672a\u6807\u6ce8", None))
#if QT_CONFIG(shortcut)
        self.action_file_img_prev_nolabel.setShortcut(QCoreApplication.translate("MainWindow", u"Left", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_open_video.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u89c6\u9891", None))
        self.action_file_delete_img.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u56fe\u7247", None))
#if QT_CONFIG(shortcut)
        self.action_file_delete_img.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Del", None))
#endif // QT_CONFIG(shortcut)
        self.action_file_exit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
#if QT_CONFIG(shortcut)
        self.action_file_exit.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_create_rect.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u77e9\u5f62", None))
        self.action_edit_create_polygon.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u591a\u8fb9\u5f62", None))
        self.action_edit_create_point.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u5173\u952e\u70b9", None))
        self.action_edit_create_rotate.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u65cb\u8f6c\u6846", None))
        self.action_edit_obj_copy.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u5bf9\u8c61", None))
#if QT_CONFIG(shortcut)
        self.action_edit_obj_copy.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_obj_paste.setText(QCoreApplication.translate("MainWindow", u"\u7c98\u8d34\u5bf9\u8c61", None))
#if QT_CONFIG(shortcut)
        self.action_edit_obj_paste.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_obj_revoke.setText(QCoreApplication.translate("MainWindow", u"\u64a4\u9500", None))
#if QT_CONFIG(shortcut)
        self.action_edit_obj_revoke.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_obj_delete.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
#if QT_CONFIG(shortcut)
        self.action_edit_obj_delete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_zoom_in.setText(QCoreApplication.translate("MainWindow", u"\u653e\u5927", None))
#if QT_CONFIG(shortcut)
        self.action_view_zoom_in.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl++", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_zoom_out.setText(QCoreApplication.translate("MainWindow", u"\u7f29\u5c0f", None))
#if QT_CONFIG(shortcut)
        self.action_view_zoom_out.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_zoom_restore.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u5927\u5c0f", None))
#if QT_CONFIG(shortcut)
        self.action_view_zoom_restore.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_zoom_auto.setText(QCoreApplication.translate("MainWindow", u"\u9002\u5e94\u7a97\u53e3", None))
#if QT_CONFIG(shortcut)
        self.action_view_zoom_auto.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_obj_hide.setText(QCoreApplication.translate("MainWindow", u"\u9690\u85cf\u9009\u4e2d", None))
        self.action_view_obj_hide.setIconText(QCoreApplication.translate("MainWindow", u"\u9690\u85cf\u9009\u4e2d", None))
#if QT_CONFIG(tooltip)
        self.action_view_obj_hide.setToolTip(QCoreApplication.translate("MainWindow", u"\u9690\u85cf\u9009\u4e2d", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_view_obj_hide.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+H", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_obj_show.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u9690\u85cf\u5bf9\u8c61", None))
#if QT_CONFIG(shortcut)
        self.action_view_obj_show.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_view_show_name.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u540d\u79f0", None))
        self.action_view_show_info.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u63cf\u8ff0", None))
        self.action_view_show_group.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5206\u7ec4", None))
        self.action_help_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.action_help_Usage.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u65b9\u6cd5", None))
        self.action_edit_obj_restore.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d", None))
#if QT_CONFIG(shortcut)
        self.action_edit_obj_restore.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.action_line_link.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u7ebf\u6761", None))
        self.action_line_unlink.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00\u7ebf\u6761", None))
        self.action_edit_create_line.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u7ebf\u6761", None))
        self.action_export_labels_rect.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u77e9\u5f62\u6807\u6ce8", None))
        self.action_export_labels_polygon.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u591a\u8fb9\u5f62\u6807\u6ce8", None))
        self.action_export_labels_point.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u5173\u952e\u70b9\u6807\u6ce8", None))
        self.action_export_labels_rotation.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u65cb\u8f6c\u6846\u6807\u6ce8", None))
        self.action_export_labels_line.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u7ebf\u6761\u6807\u6ce8", None))
        self.action_keys_info.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u6377\u952e", None))
#if QT_CONFIG(tooltip)
        self.pushButton_file_open_dir.setToolTip(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_file_open_dir.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_file_open_video.setToolTip(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u89c6\u9891", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_file_open_video.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_file_img_delete.setToolTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u56fe\u7247", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_file_img_delete.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_create_rect.setToolTip(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u77e9\u5f62", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_create_rect.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_create_polygon.setToolTip(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u591a\u8fb9\u5f62", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_create_polygon.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_create_point.setToolTip(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u5173\u952e\u70b9", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_create_point.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_create_rotate.setToolTip(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u65cb\u8f6c\u6846", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_create_rotate.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_create_line.setToolTip(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u7ebf\u6761", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_create_line.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_obj_revoke.setToolTip(QCoreApplication.translate("MainWindow", u"\u64a4\u9500", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_obj_revoke.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_edit_obj_restore.setToolTip(QCoreApplication.translate("MainWindow", u"\u6062\u590d", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_edit_obj_restore.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_view_zoom_in.setToolTip(QCoreApplication.translate("MainWindow", u"\u653e\u5927", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_view_zoom_in.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_view_zoom_out.setToolTip(QCoreApplication.translate("MainWindow", u"\u7f29\u5c0f", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_view_zoom_out.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_view_zoom_restore.setToolTip(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u5927\u5c0f", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_view_zoom_restore.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_view_zoom_auto.setToolTip(QCoreApplication.translate("MainWindow", u"\u9002\u5e94\u7a97\u53e3", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_view_zoom_auto.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_view_zoom_auto.setShortcut("")
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_view_obj_hide.setToolTip(QCoreApplication.translate("MainWindow", u"\u9690\u85cf\u5f53\u524d\u9009\u4e2d\u5bf9\u8c61", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_view_obj_hide.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_view_obj_show.setToolTip(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u6240\u6709\u9690\u85cf\u5bf9\u8c61", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_view_obj_show.setText("")
        self.label_model_path.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u8def\u5f84 : ", None))
        self.lineEdit_model_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u6a21\u578b\u6587\u4ef6(.onnx)\u6240\u5728\u8def\u5f84", None))
        self.pushButton_model_path.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9", None))
        self.label_model_score.setText(QCoreApplication.translate("MainWindow", u"\u7f6e\u4fe1\u5ea6 : ", None))
        self.pushButton_model_run.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.lineEdit_img_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6587\u4ef6\u540d", None))
        self.pushButton_file_img_prev.setText("")
        self.pushButton_file_img_next.setText("")
        self.label_obj_info.setText(QCoreApplication.translate("MainWindow", u"\u5bf9\u8c61\u63cf\u8ff0", None))
        self.tabWidget_label.setTabText(self.tabWidget_label.indexOf(self.tab_label_name), QCoreApplication.translate("MainWindow", u"\u540d\u79f0", None))
        self.tabWidget_label.setTabText(self.tabWidget_label.indexOf(self.tab_label_group), QCoreApplication.translate("MainWindow", u"\u5206\u7ec4", None))
        self.label_label_name.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u6807\u6ce8", None))
        self.label_name.setText(QCoreApplication.translate("MainWindow", u"\u540d\u79f0", None))
        self.label_group.setText(QCoreApplication.translate("MainWindow", u"\u5206\u7ec4", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u6807\u6ce8(YOLO\u683c\u5f0f)", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

