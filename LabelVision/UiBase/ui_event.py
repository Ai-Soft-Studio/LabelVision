from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import os
from copy import deepcopy
import sys





# if __name__ == "__main__":
#     __dir__ = os.path.dirname(os.path.abspath(__file__))
#     sys.path.append(__dir__)
#     sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "..")))
#     from main_ui import Ui_MainWindow
#     from ImgList import ImgList
#     from ImgCanvas import ImgWidget,ZoomType,ShapeType,Shape,get_color,MouseState,get_name_group_index
#     from UiNameDialog import NameDialog,InputDialog
#     from UiBaseWindow import *       
#     from utils import Utils
# else:
from main_ui import Ui_MainWindow
from .ImgList import ImgList
from .ImgCanvas import ImgWidget,ZoomType,ShapeType,Shape,get_color,MouseState,get_name_group_index,shape_type_dict
from .UiNameDialog import NameDialog,InputDialog
from .UiBaseWindow import *       
from .utils import Utils
from .video import extract_frames_from_video
from .export import Export
from .YOLO.Yolos import Yolos 

class UiEvents():
    
    def __init__(self, win :UiBaseWindow):
        pass
        self.win:UiBaseWindow = win
        self.ui : Ui_MainWindow = win.ui
        self.ImgList:ImgList=None
        self.ImgWidget:ImgWidget=None
        self.message_data={}
        self.shape_info:Shape=None
        self.path_export=""#导出标注的路径
        self.model_yolo:Yolos=None
        self.model_path_yolo=""
        # self.hook_w=WidgetHook(self.ui.frame_c_left)
        
        self.img_Widget_init()
        # 设置标注名称对话框
        self.nameDialog = NameDialog(self.win)
        self.nameDialog.setWindowIcon(self.win.windowIcon())
        self.nameDialog.setWindowTitle(self.win.windowTitle()+" 标注名称")
        # self.nameDialog.signal_labelName.connect(self.single_labelName)
        
        self.init_comboBox_listWidget()
        self.ui.tabWidget_label.setCurrentIndex(0)
        
        #设置形状列表可以多选
        self.ui.listWidget_shape_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        ListWidget_init_setStyleSheet(self.ui.listWidget_shape_list)
        
        #对象列表(显示标注)成员被点击
        self.ui.listWidget_shape_list.itemClicked.connect(lambda:self.shape_list_select_changed())

        #设置列表选中和悬停样式
        ListWidget_init_setStyleSheet(self.ui.listWidget_group_list)
        ListWidget_init_setStyleSheet(self.ui.listWidget_name_list)

        
        
        #对象描述
        self.ui.textEdit_obj_info.textChanged.connect(lambda: self.shape_info_edit())
        #组合框显示标注名或者分组发生改变
        self.ui.comboBox_label_name.currentIndexChanged.connect(lambda:self.list_name_or_group_comboBox_changed(self.ui.comboBox_label_name))
        self.ui.comboBox_label_group.currentIndexChanged.connect(lambda:self.list_name_or_group_comboBox_changed(self.ui.comboBox_label_group))
        
        
        #图片搜索
        self.ui.lineEdit_img_search.textChanged.connect(lambda x: self.img_search(x))
        
        #图片列表 某项被点击
        self.ui.listWidget_img_list.itemClicked.connect(lambda x: self.img_list_click(x.text()))
        
        #工具栏按钮 互斥按钮设置
        self.leftBtns= self.ui.frame_t_t_center.findChildren(QPushButton)
        for i in range(len(self.leftBtns)):
            btn:QPushButton = self.leftBtns[i]
            btn.clicked.connect(lambda isChecked,item=btn: self.check_button_state(item,isChecked))
        
        
        #打开目录
        self.ui.action_file_open_dir.triggered.connect(lambda: self.open_dir_img())
        self.ui.pushButton_file_open_dir.clicked.connect(lambda: self.open_dir_img())
        
        #打开视频
        self.ui.action_file_open_video.triggered.connect(lambda: self.open_video_img())
        self.ui.pushButton_file_open_video.clicked.connect(lambda: self.open_video_img())
        
        #导出标注
        self.ui.action_export_labels_rect.triggered.connect(lambda: self.export_lables(ShapeType.rectangle))
        self.ui.action_export_labels_polygon.triggered.connect(lambda: self.export_lables(ShapeType.polygon))
        self.ui.action_export_labels_point.triggered.connect(lambda: self.export_lables(ShapeType.point))
        self.ui.action_export_labels_rotation.triggered.connect(lambda: self.export_lables(ShapeType.rotation))
        self.ui.action_export_labels_line.triggered.connect(lambda: self.export_lables(ShapeType.rotation))
        
        
        #下一张
        self.ui.action_file_img_next.triggered.connect(lambda: self.img_list_click_cased("next"))
        self.ui.pushButton_file_img_next.clicked.connect(lambda: self.img_list_click_cased("next"))
        #上一张
        self.ui.action_file_img_prev.triggered.connect(lambda: self.img_list_click_cased("prev"))
        self.ui.pushButton_file_img_prev.clicked.connect(lambda: self.img_list_click_cased("prev"))
        #下一张未标注
        self.ui.action_file_img_next_nolabel.triggered.connect(lambda: self.img_list_click_cased("next_nolabel"))
        #上一张未标注
        self.ui.action_file_img_prev_nolabel.triggered.connect(lambda: self.img_list_click_cased("prev_nolabel"))
        
        
        
        #删除图片
        self.ui.action_file_delete_img.triggered.connect(lambda: self.img_list_delete_item())
        self.ui.pushButton_file_img_delete.clicked.connect(lambda: self.img_list_delete_item())
        
        #创建矩形
        self.ui.action_edit_create_rect.triggered.connect(lambda: self.img_create_rect())
        self.ui.pushButton_edit_create_rect.clicked.connect(lambda: self.img_create_rect())
        
        #创建多边形
        self.ui.action_edit_create_polygon.triggered.connect(lambda: self.img_create_polygon())
        self.ui.pushButton_edit_create_polygon.clicked.connect(lambda: self.img_create_polygon())
        
        #创建关键点
        self.ui.action_edit_create_point.triggered.connect(lambda: self.img_create_point())
        self.ui.pushButton_edit_create_point.clicked.connect(lambda: self.img_create_point())
        
        #创建旋转框
        self.ui.action_edit_create_rotate.triggered.connect(lambda: self.img_create_rotate())
        self.ui.pushButton_edit_create_rotate.clicked.connect(lambda: self.img_create_rotate())
        
        #创建线条
        self.ui.action_edit_create_line.triggered.connect(lambda: self.img_create_line())
        self.ui.pushButton_edit_create_line.clicked.connect(lambda: self.img_create_line())
        
        #线条连接与断开
        self.ui.action_line_link.triggered.connect(lambda: self.img_obj_line_set(True))
        self.ui.action_line_unlink.triggered.connect(lambda: self.img_obj_line_set(False))
        
        #复制粘贴
        self.ui.action_edit_obj_copy.triggered.connect(lambda: self.img_obj_copy())
        self.ui.action_edit_obj_paste.triggered.connect(lambda: self.img_obj_paste())
        
        #撤销/恢复
        self.ui.action_edit_obj_revoke.triggered.connect(lambda: self.img_obj_revoke())
        self.ui.action_edit_obj_restore.triggered.connect(lambda: self.img_obj_restore())
        self.ui.pushButton_edit_obj_revoke.clicked.connect(lambda: self.img_obj_revoke())
        self.ui.pushButton_edit_obj_restore.clicked.connect(lambda: self.img_obj_restore())
        
        #删除
        self.ui.action_edit_obj_delete.triggered.connect(lambda: self.img_obj_delete())
        
        
        #放大图片
        self.ui.action_view_zoom_in.triggered.connect(lambda: self.img_zoom(ZoomType.zoom_in))
        self.ui.pushButton_view_zoom_in.clicked.connect(lambda: self.img_zoom(ZoomType.zoom_in))
        #缩小图片
        self.ui.action_view_zoom_out.triggered.connect(lambda: self.img_zoom(ZoomType.zoom_out))
        self.ui.pushButton_view_zoom_out.clicked.connect(lambda: self.img_zoom(ZoomType.zoom_out))
        #图片原始尺寸
        self.ui.action_view_zoom_restore.triggered.connect(lambda: self.img_zoom(ZoomType.zoom_norm))
        self.ui.pushButton_view_zoom_restore.clicked.connect(lambda: self.img_zoom(ZoomType.zoom_norm))
        #图片自适应
        self.ui.action_view_zoom_auto.triggered.connect(lambda: self.img_zoom(ZoomType.zoom_auto))
        self.ui.pushButton_view_zoom_auto.clicked.connect(lambda: self.img_zoom(ZoomType.zoom_auto))
        
        #隐藏对象
        self.ui.action_view_obj_hide.triggered.connect(lambda: self.img_obj_hide(True))
        self.ui.pushButton_view_obj_hide.clicked.connect(lambda: self.img_obj_hide(True))
        
        #隐藏对象
        self.ui.action_view_obj_show.triggered.connect(lambda: self.img_obj_hide(False))
        self.ui.pushButton_view_obj_show.clicked.connect(lambda: self.img_obj_hide(False))
        
        #显示对象名字/分组/描述
        self.ui.action_view_show_name.triggered.connect(lambda: self.shape_show_hide_label())
        self.ui.action_view_show_group.triggered.connect(lambda: self.shape_show_hide_label())
        self.ui.action_view_show_info.triggered.connect(lambda: self.shape_show_hide_label())
        
        
        
        #关闭按钮
        self.ui.action_file_exit.triggered.connect(lambda: self.win.close())
        
        #绑定状态栏显示内容信号
        # self.win.single_message.connect(lambda x: self.statusbar_showMessage(x))
        
        self.action_init()
        self.ui.pushButton_model_path.clicked.connect(lambda: self.open_model_onnx())
        self.ui.pushButton_model_run.clicked.connect(lambda: self.img_label_auto())
        
        self.ui.action_keys_info.triggered.connect(lambda: messageBox(self.win,"快捷键说明",Utils.keysinfo()))
        self.ui.action_help_Usage.triggered.connect(lambda: messageBox(self.win,"使用说明",Utils.useinfo()))
        self.ui.action_help_about.triggered.connect(lambda: messageBox(self.win,"关于",Utils.aboutinfo()))
        
    #菜单按钮初始化
    def action_init(self):
        '''菜单按钮初始化'''
        #文件列表
        Action_add("打开目录",self.ui.listWidget_img_list,lambda: self.open_dir_img())
        Action_add("删除图片",self.ui.listWidget_img_list,lambda: self.img_list_delete_item())
       
        #标注形状列表
        Action_add("编辑",self.ui.listWidget_shape_list,lambda: self.shape_list_edit())
        Action_add("隐藏",self.ui.listWidget_shape_list,lambda: self.img_obj_hide(True))
        Action_add("显示",self.ui.listWidget_shape_list,lambda: self.img_obj_hide(False))
        Action_add("删除",self.ui.listWidget_shape_list,lambda: self.img_obj_delete())
        Action_add("清空",self.ui.listWidget_shape_list,lambda: self.shape_list_clear())
        
        Action_add("颜色调整",self.ui.listWidget_name_list,lambda: self.name_list_color())
        Action_add("修改名称",self.ui.listWidget_name_list,lambda: self.list_name_or_group_edit(self.ui.listWidget_name_list,self.ui.comboBox_label_name,"名称"))
        Action_add("删除名称",self.ui.listWidget_name_list,lambda: self.list_name_or_group_delete(self.ui.listWidget_name_list,self.ui.comboBox_label_name,"名称"))
        
        Action_add("颜色调整",self.ui.listWidget_group_list,lambda: self.group_list_color())
        Action_add("修改分组",self.ui.listWidget_group_list,lambda: self.list_name_or_group_edit(self.ui.listWidget_group_list,self.ui.comboBox_label_group,"分组"))
        Action_add("删除分组",self.ui.listWidget_group_list,lambda: self.list_name_or_group_delete(self.ui.listWidget_group_list,self.ui.comboBox_label_group,"分组"))

        # 设置画布菜单右键事件以生成菜单
        self.ui.widget_img.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.widget_img.customContextMenuRequested.connect(self.action_canvas_menu)
        
    #生成画布右键菜单
    def action_canvas_menu(self,position: QPoint):
        """生成画布右键菜单"""
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return
        
        mouse_state = self.ImgWidget.label.mouse_state
        if  mouse_state == MouseState.drag:
            #拖动图片
            return
        
        # 创建上下文菜单
        menu = QMenu(self.ui.widget_img)
        # action = Action_add("测试",self.ui.widget_img,lambda: self.shape_get_data(),ContextMenuPolicy=Qt.ContextMenuPolicy.CustomContextMenu)
        action={}
        action["create_rect"]=self.ui.action_edit_create_rect
        action["create_polygon"]=self.ui.action_edit_create_polygon
        action["create_point"]=self.ui.action_edit_create_point
        action["create_rotate"]=self.ui.action_edit_create_rotate
        action["create_line"]=self.ui.action_edit_create_line
        
        action["line_link"]=self.ui.action_line_link
        action["line_unlink"]=self.ui.action_line_unlink
        
        action["obj_copy"]=self.ui.action_edit_obj_copy
        action["obj_paste"]=self.ui.action_edit_obj_paste
        action["obj_revoke"]=self.ui.action_edit_obj_revoke
        action["obj_restore"]=self.ui.action_edit_obj_restore
        action["obj_delete"]=self.ui.action_edit_obj_delete
        action["obj_hide"]=self.ui.action_view_obj_hide
        action["obj_show"]=self.ui.action_view_obj_show
        action["show_name"]=self.ui.action_view_show_name
        action["show_group"]=self.ui.action_view_show_group
        action["show_info"]=self.ui.action_view_show_info
        action_list=[]
        if (mouse_state == MouseState.selected or mouse_state == MouseState.has_rotate or
            mouse_state == MouseState.line_link or mouse_state == MouseState.line_unlink):
            if mouse_state == MouseState.has_rotate:
                temp = Action_add("旋转需要使用CTRL键+鼠标滚轮",self.ui.widget_img,slot=None,ContextMenuPolicy=Qt.ContextMenuPolicy.CustomContextMenu)
                action_list.append(temp)
            
            if mouse_state == MouseState.line_link:
                action_list.append(action["line_link"])
            if mouse_state == MouseState.line_unlink:
                action_list.append(action["line_unlink"])
            
            action_list.append(action["obj_hide"])
            action_list.append(action["obj_show"])
            action_list.append(action["obj_delete"])
            action_list.append(action["obj_copy"])
        elif mouse_state==MouseState.normal:
            #鼠标状态正常,未指向任何对象
            action_list.append(action["create_rect"])
            action_list.append(action["create_polygon"])
            action_list.append(action["create_point"])
            action_list.append(action["create_rotate"])
            action_list.append(action["create_line"])
            # action_list.append(QAction())
            action_list.append(action["obj_show"])
            action_list.append(action["show_name"])
            action_list.append(action["show_group"])
            action_list.append(action["show_info"])
        elif mouse_state == MouseState.pointed:
            #鼠标指向对象,未选中
            pass
            
        if len(self.ImgWidget.label.shape_copy_paste):
            action_list.append(action["obj_paste"])
        action_list.append(action["obj_revoke"])
        action_list.append(action["obj_restore"])
            
        
        # 将 QAction 添加到菜单中
        menu.addActions(action_list)
        menu.exec(self.ui.widget_img.mapToGlobal(position))    
    
    #初始化组合框(名称/分组)
    def init_comboBox_listWidget(self):
        '''初始化组合框(名称/分组)'''
        self.ui.comboBox_label_name.clear()
        ComboBox_add_item(self.ui.comboBox_label_name,"👀",False)
        self.ui.comboBox_label_group.clear()
        ComboBox_add_item(self.ui.comboBox_label_group,"👀",False)

    # 互斥按钮   
    def check_button_state(self,item,isChecked): 
        sender :QPushButton = item  # 获取发送信号的按钮对象
        sender.setChecked(True)
        if sender.isChecked():  
            for i in range(len(self.leftBtns)):
                btn:QPushButton=self.leftBtns[i]
                if btn == sender:
                    continue
                btn.setChecked(not sender.isChecked())
     
    def open_model_onnx(self):
        file_path=self.win.data.get("model_path","")
        fileFormats = "*.onnx"
        file_path, _ = QFileDialog.getOpenFileName(self.win,"选择模型文件",file_path,fileFormats,)
        if not file_path or not os.path.isfile(file_path):
            return
        self.win.data["model_path"]=file_path
        
        self.ui.lineEdit_model_path.setText(file_path)
        
          
    #获取图片目录
    def get_img_dir(self):
        img_dir = ""
        if "img_dir" in self.win.data:
            img_dir = self.win.data["img_dir"]
            if not os.path.isdir(img_dir): 
                img_dir=""
        return img_dir
    
    #打开图片目录    
    def open_dir_img(self):
        img_dir = self.get_img_dir()
        img_dir = QFileDialog.getExistingDirectory(self.win, "请选择图片所在目录", img_dir,QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if not img_dir or not  os.path.isdir(img_dir):
            return
        self.win.data["img_dir"]=img_dir
        self.ImgList=ImgList(self.ui.listWidget_img_list,img_dir)
        self.widget_config_load()
        self.config_read_model()

        # print("图片目录:" + img_dir)

    def open_video_img(self):
        img_dir = self.get_img_dir()
        supportedVideoFormats = ( "*.asf *.avi *.m4v *.mkv *.mov *.mp4 *.mpeg *.mpg *.ts *.wmv")
        source_video_path, _ = QFileDialog.getOpenFileName(self.win,"打开视频文件",img_dir,supportedVideoFormats,)

        if not  os.path.exists(source_video_path):
            return
        target_dir_path = extract_frames_from_video(self.win, source_video_path)
        if target_dir_path is None or not os.path.isdir(target_dir_path):
            return
        self.win.data["img_dir"]=target_dir_path
        self.ImgList=ImgList(self.ui.listWidget_img_list,target_dir_path)
        self.widget_config_load()    

    
    def export_lables(self,type:ShapeType):
        img_dir = self.get_img_dir()
        img_list = self.ImgList.get_img_list()
        if not img_dir or len(img_list)<=0: 
            return
        data = read_json_config(img_dir+'/config.json')
        if len(data)<=0 or not isinstance(data,dict):
            messageBox(self.win,"错误","当前所选图片目录暂无标注数据,请标注后再执行导出操作")
            return 
        if not self.path_export:
            self.path_export = "./"
        save_dir = QFileDialog.getExistingDirectory(self.win, "请选择数据集存放目录", self.path_export,QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if not (save_dir and os.path.isdir(save_dir)):
            return
        self.path_export=save_dir
        ret=False
        if type == ShapeType.rectangle:
           ret= Export.detect(self.win,data,img_list,img_dir,save_dir)
        if type == ShapeType.polygon:
           ret= Export.segment(self.win,data,img_list,img_dir,save_dir)   
        if type == ShapeType.point:
           ret= Export.pose(self.win,data,img_list,img_dir,save_dir)
        if type == ShapeType.rotation:
           ret= Export.obb(self.win,data,img_list,img_dir,save_dir)
        if type == ShapeType.line:
           messageBox(self.win,"错误","此类型的标注数据暂不支持导出")
           return
        
        
        if ret:
            messageBox(self.win,"提示",f"导出标注数据成功,数据集已生成,请您到以下目录查看:\n{save_dir}")
        else:
            messageBox(self.win,"错误","导出标注数据失败,请检查所选图片目录是否正确")
    
    def widget_config_load_golbal(self):
        data = config_read_golbal()
        if len(data)<=0 :
            return
        
        #更新标注名字和分组

        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])
        key_points:list[int] = data.get("key_points",[])
        line_rule:list[list[int]] = data.get("line_rule",[])
        
        
        
        #将标注名称和分组加入对应的组合框中
        for info in name_info:
            self.list_name_or_group_add(self.ui.listWidget_name_list,self.ui.comboBox_label_name,info,is_set_color=False)
            ListWidget_load_data(self.ui.listWidget_name_list,info,is_show_index=True)
        for info in group_info:
            self.list_name_or_group_add(self.ui.listWidget_group_list,self.ui.comboBox_label_group,info,is_set_color=False)
            ListWidget_load_data(self.ui.listWidget_group_list,info,is_show_index=True)
        
        self.ImgWidget.label.key_points = key_points
        self.ImgWidget.label.line_rule = line_rule
        
        
    #更新界面标注配置信息
    def widget_config_load(self):
        '''更新图片列表中所有图片名是否已被标注,选择框选中或取消选中'''
        if self.ImgList is None:
            return
        img_dir = self.ImgList.get_img_dir()
        if img_dir is None or not img_dir:
            return 
        data = read_json_config(img_dir+'/config.json')
        if len(data)<=0 :
            return
        
        #读取全局配置进行更新
        self.widget_config_load_golbal()
        
        #更新图片列表中图片是否已经被标注
        img_list = self.ImgList.get_img_list()
        for name in img_list:
            if not name:
                continue
            self.img_list_set_labeled(name,data)
         
    #在列表中搜索图片
    def img_search(self,img_name:str):
        if self.ImgList is None:
            return
        self.ImgList.show_search_img_list(img_name)
            
    #点击列表中图片
    def img_list_click(self,img_name:str):
        # print("点击图片:" + img_name)
        img_dir = self.get_img_dir()
        img_path = os.path.join(img_dir,img_name)
        if not  os.path.exists(img_path):
            return
        # self.ui.widget_img.setStyleSheet("QLabel { border: 2px solid  rgb(0, 0, 0); }")
        
        if self.ImgWidget is None or self.ImgWidget.label is  None: 
            return
        self.ImgWidget.label.set_shape_type(self.img_create_get_shape())
        if self.ImgWidget.label.is_valid:
            self.img_save_label()
        
        self.ImgWidget.label.img_load(img_path)
        self.ImgWidget.label.init_canvas()    
        
        self.img_label_load()
        self.update_shape_list()
    
    #初始化画布窗口
    def img_Widget_init(self):
        '''初始化图片画布窗口'''
        self.ImgWidget = ImgWidget(self.ui.widget_img,"",self.win)
        self.ImgWidget.label.signal_mouseMove.connect(self.single_mouse_move)
        self.ImgWidget.label.signal_shape_created.connect(self.single_shape_created)
        self.ImgWidget.label.signal_shape_checked.connect(lambda:self.update_shape_list())
        self.ImgWidget.label.signal_shape_updated.connect(lambda:self.update_shape_list())
    
    #图片的标注数据加载
    def img_label_load(self):
        '''图片的标注数据加载'''
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return
        img_dir = self.ImgWidget.label.img_dir
        img_name = self.ImgWidget.label.img_name
        shape_list:list[dict]=[]

        shape_list,data = self.label_data_load(img_dir,img_name)
        
        if data is not None:
            line_rule = data.get("line_rule",[])
            self.ImgWidget.label.line_rule = line_rule
        
        # if len(shape_list)<=0:
        #     return
        
         
        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])
        key_points:list[int] = data.get("key_points",[])
        
        #将标注名称和分组加入对应的组合框中
        for info in name_info:
            self.list_name_or_group_add(self.ui.listWidget_name_list,self.ui.comboBox_label_name,info,is_set_color=False)
            ListWidget_load_data(self.ui.listWidget_name_list,info,is_show_index=True)
        for info in group_info:
            self.list_name_or_group_add(self.ui.listWidget_group_list,self.ui.comboBox_label_group,info,is_set_color=False)
            ListWidget_load_data(self.ui.listWidget_group_list,info,is_show_index=True)
        
        #加载形状数据
        self.ImgWidget.label.load_shapes(shape_list,name_info,group_info,key_points)
    
    #获取当前需要创建的形状类型
    def img_create_get_shape(self):
        if self.ui.pushButton_edit_create_rect.isChecked():
            return ShapeType.rectangle
        if self.ui.pushButton_edit_create_polygon.isChecked():
            return ShapeType.polygon
        if self.ui.pushButton_edit_create_point.isChecked():
            return ShapeType.point
        if self.ui.pushButton_edit_create_rotate.isChecked():
            return ShapeType.rotation
        if self.ui.pushButton_edit_create_line.isChecked():
            return ShapeType.line
        return ShapeType.polygon
    
    #设置形状类型
    def img_create_set_shape(self):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        shape_type = self.img_create_get_shape()
        self.ImgWidget.label.set_shape_type(shape_type)

    #创建矩形
    def img_create_rect(self):
        self.check_button_state(self.ui.pushButton_edit_create_rect,True)
        self.img_create_set_shape()

    #创建多边形
    def img_create_polygon(self):
        self.check_button_state(self.ui.pushButton_edit_create_polygon,True)
        self.img_create_set_shape()

    #创建关键点
    def img_create_point(self):
        self.check_button_state(self.ui.pushButton_edit_create_point,True)
        self.img_create_set_shape()

    #创建旋转框
    def img_create_rotate(self): 
        self.check_button_state(self.ui.pushButton_edit_create_rotate,True)
        self.img_create_set_shape()  

    #创建线条
    def img_create_line(self): 
        self.check_button_state(self.ui.pushButton_edit_create_line,True)
        self.img_create_set_shape() 
    
    
    def img_obj_line_set(self,is_link):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        name0 = self.ImgWidget.label.shape_checked[0].name
        name1 = self.ImgWidget.label.shape_checked[1].name
        text="连接线条" if is_link else "断开线条"
        ret = messageBox(self.win,"提示",f"此操作将会使得所有名称为{name0}和{ name1}的关键点{text}!\n您确定吗?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,QMessageBox.StandardButton.Yes)
        if ret != QMessageBox.StandardButton.Yes:
            return
        if is_link:
            self.ImgWidget.label.line_link()
        else:
            self.ImgWidget.label.line_unlink()
        self.ImgWidget.label.line_link_apply()
        #保留一次记录
        self.ImgWidget.label.shapes_store()
        self.update_shape_list()
        
    #复制形状
    def img_obj_copy(self):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        self.ImgWidget.label.shape_copy()
    
    #粘贴形状
    def img_obj_paste(self):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        self.ImgWidget.label.shape_paste()

    #撤销
    def img_obj_revoke(self):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        self.ImgWidget.label.shapes_ctrl_z()

    #恢复
    def img_obj_restore(self):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        self.ImgWidget.label.shapes_ctrl_y()

    #删除
    def img_obj_delete(self):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        self.ImgWidget.label.delete_obj()

    #选择上/下张图片
    def img_list_click_cased(self,mode):
        if not self.ImgList: 
            return
        name = ""
        swich = {
            "next":self.ImgList.get_img_list_next,
            "prev":self.ImgList.get_img_list_prev,
            "next_nolabel":self.ImgList.get_img_list_next_nolabel,
            "prev_nolabel":self.ImgList.get_img_list_prev_nolabel
        }
        if mode not in swich:
            return
        fun = swich[mode]
        name = fun()
        if name:
            self.ImgList.set_item_select(name)
            self.img_list_click(name)
    
    #删除图片文件和数据
    def img_list_delete_item(self):
        if self.ImgList is None:
            return
        img_name = self.ImgList.get_img_list_current_name()
        print("删除图片:" + img_name)
        img_dir = self.get_img_dir()
        img_path = os.path.join(img_dir,img_name)
        if not  os.path.exists(img_path):
            return
        response = QMessageBox.warning(
                                self.win,
                                "警告",
                                f"您将会删除此图片文件{img_name}. \n是否继续?",
                                QMessageBox.Cancel | QMessageBox.Ok,)

        if response != QMessageBox.Ok:
            return
        Utils.file_move(img_path,"./_backups/imgs/")
        # os.remove(img_path)
        index = self.ImgList.delete_img(img_name)
        img_name = self.ImgList.get_img_list_name_by_index(index)
        self.img_list_click(img_name)
        
    #图片缩放
    def img_zoom(self,mode:ZoomType):
        if self.ImgWidget is not None and self.ImgWidget.label.isVisible():
            self.ImgWidget.img_zoom(mode)
   
    #隐藏对象
    def img_obj_hide(self,is_hide:bool):
        if self.ImgWidget is None:
            return 
        if self.ImgWidget.label is None:
            return
        if is_hide:
            self.ImgWidget.label.shape_checked_hide()
        else:
            self.ImgWidget.label.shape_checked_show()
    
    #处理图片控件鼠标移动信号
    def single_mouse_move(self,data:dict):
        if "pos" not in data:
            return
        self.message_data["pos"] = data["pos"]
        #将信号转发给self.win.single_message
        # self.win.single_message.emit(self.message_data)
        self.statusbar_showMessage(self.message_data)
    
    #绑定在single_message用来处理状态栏显示内容
    def statusbar_showMessage(self,data:dict):
        pass
        pos_str=""
        if "pos" in self.message_data:
            pos:QPoint=self.message_data["pos"]
            pos_str = f"坐标:{pos.x()},{pos.y()}\t"
            
        msg_str = f"{pos_str}"
        self.ui.statusbar.showMessage(msg_str)
    
    #信号,形状被创建后发送信号,此槽函数进行处理
    def single_shape_created(self,data:dict,is_edit=False):
        '''信号,形状被创建后发送信号,此槽函数进行处理'''
        # "shape":self.shape_list[-1],
        # "index":len(self.shape_list)-1 
        check=["shape","index"]
        for string in check:
            if string not in data:
                return False  
        shape:Shape = data["shape"]
        index:int   = data["index"]
        if shape is None :
            return False
        
        name_info = ListWidget_get_list_info(self.ui.listWidget_name_list,is_show_index=True)
        group_info = ListWidget_get_list_info(self.ui.listWidget_group_list,is_show_index=True)
        
        name_list,_ = Utils.list_info_unpack(name_info)
        group_list,_ = Utils.list_info_unpack(group_info)

        key_points = self.shape_get_key_points()
        
        #传递要创建的形状的信息给模态窗口
        self.nameDialog.set_shape(shape,index)
        self.nameDialog.set_name_list(name_list)
        self.nameDialog.set_group_list(group_list)
        self.nameDialog.set_key_points(key_points)
        
        data = self.nameDialog.show()
        data["is_edit"] = is_edit

        #处理
        self.single_labelName(data)

    #'''创建成功形状后会进入此信号'''
    def single_labelName(self,data:dict):
        '''创建成功形状后会进入此信号,用来处理更新形状的功能'''
        check =["name","info","group","isok","shape","index"]
        for string in check:
            if string not in data:
                return False
        
        name:str    =   data["name"]
        info:str    =   data["info"]
        group:str   =   data["group"]
        isok:bool   =   data["isok"]
        shape:Shape =   data["shape"]
        index:int   =   data["index"]
        is_edit     =   data.get("is_edit",False)
        if shape is None:
            return False
        
        #将未命名形状从撤销恢复的队列中删除
        self.ImgWidget.label.shape_list_ctrl_z.pop()
        
        if not isok or not name:
            #未命名且非编辑状态的形状统一删除
            if not is_edit:
                self.ImgWidget.label.delete_shape(shape)
            return False
        
        #更新形状对象的名称/分组/描述等信息
        shape.name = name
        shape.group = group
        if info:
            shape.info = info
        
        
        color = None
        #分组框和列表框的数据更新和填充        
        index = self.list_name_or_group_add(self.ui.listWidget_name_list,self.ui.comboBox_label_name,Utils.list_info_make_data(name,None))
        self.list_name_or_group_add(self.ui.listWidget_group_list,self.ui.comboBox_label_group,Utils.list_info_make_data(group,None))
        if color is None or color ==QColor():
            color = ListWidget_get_color(self.ui.listWidget_group_list,group,is_show_index=True)
        if color is None or color ==QColor():
            color = ListWidget_get_color(self.ui.listWidget_name_list,name,is_show_index=True)
        if color is None or color ==QColor():    
            color = get_color(index)
        
        if color is not None:
            shape.color = color
        
        #新增标注名称和分组信息到数据中
        self.ImgWidget.label.name_list_add(name)
        self.ImgWidget.label.group_list_add(group)
        
        #新增关键点到数据中
        if shape.shape_type in [ShapeType.point]:
            self.ImgWidget.label.key_points_add(name)
        
        #如果新建的形状是关键点时,判断是否规则画线
        if shape.shape_type in [ShapeType.point] and len(self.ImgWidget.label.line_rule):
            self.ImgWidget.label.line_link_apply()
        
        #保留一次记录
        self.ImgWidget.label.shapes_store()
        self.update_shape_list()

    def list_name_or_group_add(self,listWidget:QListWidget,comboBox:QComboBox,data:dict,is_set_color=True):
        index = ListWidget_load_data(listWidget,data,is_show_index=True)
        text  = data.get("text",None)
        ComboBox_add_item(comboBox,text,False)
        if index is not None and index == listWidget.count()-1 and is_set_color:
            color = get_color(index)
            item = ListWidget_get_item(listWidget,index,is_show_index=True)
            ListWidget_item_set_color(item,color) 
        return index
    
    #更新形状列表中所有内容
    def update_shape_list(self):
        """更新形状列表中所有内容"""
        self.ui.listWidget_shape_list.clear()
        shape_list:list[Shape] = self.ImgWidget.label.shape_list
        list_selected_item :list[QListWidgetItem]=[]
        for shape in shape_list:
            text = shape.name+("\t"+f"({shape.group})" if shape.group else "") 
            #添加控件
            index = ListWidget_add_item(
                                self.ui.listWidget_shape_list,
                                text,
                                is_select=False,
                                is_check_enble=True,
                                is_checked=shape.is_visible,
                                is_force_add=True)
            #添加后再去获取控件
            item = ListWidget_get_item(self.ui.listWidget_shape_list,index)
            if item is not None :
                color = QColor(shape.color.red(),shape.color.green(),shape.color.blue(),50)
                ListWidget_item_set_color(item,color)
                is_selected = shape in self.ImgWidget.label.shape_checked
                if is_selected:
                    list_selected_item.append(item)
        
        for item in  list_selected_item:
            item.setSelected(True)
            self.ui.listWidget_shape_list.setCurrentItem(item)
        #显示形状描述信息
        self.shape_info_show()
        #保存标注数据到配置文件中
        self.img_save_label()
    
    #形状对象列表控件被单击             
    def shape_list_select_changed(self):
        '''形状对象列表控件被单击 '''
        self.shape_list_update_action()
        #获取当前被选中的所有项的索引
        list_selected:list[int]=[]
        for index in range(self.ui.listWidget_shape_list.count()):
            item = ListWidget_get_item(self.ui.listWidget_shape_list,index)
            if item is None:
                continue
            
            #是否被选中(非勾选)
            if item.isSelected():
                list_selected.append(index)
            shape = self.ImgWidget.label.get_shape_by_index(index)
            if shape is None:
                continue
            
            #是否被勾选
            if item.checkState() == Qt.CheckState.Unchecked:
                shape.is_visible=False
            else:
                shape.is_visible=True
                
        #获取形状,并且更新形状列表
        list_checkde:list[Shape]=[]
        for index in list_selected:
            shape = self.ImgWidget.label.get_shape_by_index(index)
            if shape is None:
                continue
            list_checkde.append(shape)
        #更换选中形状数据
        self.ImgWidget.label.shape_checked = list_checkde
        self.ImgWidget.label.update()
        self.ImgWidget.label.shapes_store()
        self.shape_info_show()
    
    #编辑框中展示当前形状的描述信息info
    def shape_info_show(self):
        '''编辑框中展示当前形状的描述信息info'''
        if  self.ImgWidget is None or  self.ImgWidget.label is None:
            self.shape_info = None
            self.ui.textEdit_obj_info.setText("")
            return  
        
        if len(self.ImgWidget.label.shape_checked)!=1:
            self.shape_info = None
            self.ui.textEdit_obj_info.setText("")
            return        
        shape = self.ImgWidget.label.shape_checked[0] 
        info  = shape.info
        self.shape_info = shape
        self.ui.textEdit_obj_info.setText(info)
    
    #编辑形状描述信息
    def shape_info_edit(self):
        '''编辑形状描述信息'''
        if  self.ImgWidget is None or  self.ImgWidget.label is None:
            self.shape_info = None
            return  
        if self.shape_info is None:
            return
        text = self.ui.textEdit_obj_info.toPlainText()
        if self.shape_info.info == text :
            return
        # if not text:
        #     return
        self.shape_info.set_info(text) 
        self.ImgWidget.label.update()
        self.ImgWidget.label.shapes_store()
    
    #名字/分组的组合框当前项发生改变
    def list_name_or_group_comboBox_changed(self,comboBox:QComboBox):
        '''名字/分组的组合框当前项发生改变'''
        if comboBox is None:
            return
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return
        
        text_cur=""
        
        is_name = None
        if comboBox == self.ui.comboBox_label_name:
            is_name=True
            text_cur  = comboBox.currentText()
        elif comboBox==self.ui.comboBox_label_group:
            is_name=False
            text_cur = comboBox.currentText()
        
        if not text_cur  or is_name is None:
            return

        #显示当前选择的标注信息,隐藏未在组合框中选择的形状
        shape_list = self.ImgWidget.label.shape_list
        for shape in shape_list:
            text_shape= shape.name.lower() if is_name else shape.group.lower()
            if text_cur == "👀" :
                shape.is_visible=True
            elif text_shape == text_cur.lower():
                shape.is_visible=True
            else:
                shape.is_visible=False
            
            continue
            
            
        self.ImgWidget.label.shape_checked.clear()
        self.ImgWidget.label.update()
        self.ImgWidget.label.shapes_store()
        self.update_shape_list()       
    
    #更新标注形状列表控件的编辑菜单状态
    def shape_list_update_action(self):
        '''更新标注形状列表控件的编辑菜单状态'''
        #获取'编辑'菜单按钮
        action=None
        actions = self.ui.listWidget_shape_list.actions()
        for i in range(len(actions)):
            if actions[i].text()=="编辑":
                action=actions[i]
                break
        if action is None:
            return        

        #获取当前被选中的形状数量
        list_selected:list[int]=[]
        for index in range(self.ui.listWidget_shape_list.count()):
            item = ListWidget_get_item(self.ui.listWidget_shape_list,index)
            if item is None:
                continue
            if item.isSelected():
                list_selected.append(index)
        #数量不等于1禁用按钮
        if len(list_selected)!=1:
            action.setEnabled(False)
            return
        action.setEnabled(True)
    
    #形状列表菜单按钮'编辑'槽事件
    def shape_list_edit(self):
        '''形状列表菜单按钮'编辑'槽事件'''
        list_selected:list[int]=[]
        for index in range(self.ui.listWidget_shape_list.count()):
            item = ListWidget_get_item(self.ui.listWidget_shape_list,index)
            if item is None:
                continue
            if item.isSelected():
                list_selected.append(index)
        
        if len(list_selected)!=1:
            return
        
        #取出形状
        shape = self.ImgWidget.label.get_shape_by_index(list_selected[0])  
        if shape is None:
            return
        #和创建形状一样,通过形状来修改其名字和分组等信息          
        data={}
        data["shape"] = shape
        data["index"] = list_selected[0]
        self.single_shape_created(data,is_edit=True)
    
    #清空当前图像所有标注内容 
    def shape_list_clear(self):
        '''清空当前图像所有标注内容'''
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return 
        self.ImgWidget.label.shape_list.clear()
        self.ImgWidget.label.set_shape_type(self.ImgWidget.label.shape_type)
        self.ImgWidget.label.update()
        self.ImgWidget.label.shapes_store()
        self.update_shape_list()
    
    #显示或者隐藏标注名称/分组/描述信息
    def shape_show_hide_label(self):
        '''显示或者隐藏标注名称/分组/描述信息'''
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return
        
        is_show_name = self.ui.action_view_show_name.isChecked()
        is_show_group = self.ui.action_view_show_group.isChecked()
        is_show_info  = self.ui.action_view_show_info.isChecked()
        
        self.ImgWidget.label.is_show_name = is_show_name
        self.ImgWidget.label.is_show_group = is_show_group
        self.ImgWidget.label.is_show_info  = is_show_info
        
        self.ImgWidget.label.update()

    # 获取关键点连线规则
    def shape_get_line_rule(self):
        '''获取关键点连线规则'''
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return []
        line_rule = self.ImgWidget.label.line_rule
        return line_rule
    
    # 获取关键点列表
    def shape_get_key_points(self):
        '''获取关键点列表'''
        if self.ImgWidget is None or not self.ImgWidget.label.is_valid :
            return []
        key_points = deepcopy(self.ImgWidget.label.key_points)
        return key_points
    
    #获取当前图像文件标注的形状数据
    def shape_get_data(self):
        '''获取当前图像文件标注的形状数据'''
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return None
        img_name = self.ImgWidget.label.img_name
        img_path = self.ImgWidget.label.img_path
        img_dir=self.ImgWidget.label.img_dir
        if not img_name:
            return None
        name_info = ListWidget_get_list_info(self.ui.listWidget_name_list,is_show_index=True)
        group_info = ListWidget_get_list_info(self.ui.listWidget_group_list,is_show_index=True)


        line_rule = self.shape_get_line_rule()
        key_points = self.shape_get_key_points()
        
        shape_list:list[dict]=[]
        for shape in self.ImgWidget.label.shape_list:
            temp:dict = shape.get_data(name_info,group_info)
            shape_list.append(temp)
        temp:dict = {}
        temp["img_path"] = img_path
        temp["shape_list"] = shape_list
        data = {}
        data["img_dir"]     = img_dir
        data["name_info"]  = name_info
        data["group_info"] = group_info
        data["line_rule"]   = line_rule 
        
        data["key_points"] = key_points
        data[img_name]  = temp
        
        #data[img_name]  = data{img_path:img_path,shape_list:[{shape_type:shape_type,points:[[0,1],[],...]},{},...]}
        return data
    
    #保存当前标注数据  
    def img_save_label(self):
        '''保存当前标注数据'''
        if self.ImgList is None:
            return
        img_dir = self.ImgList.get_img_dir()
        if img_dir is None or not img_dir:
            return 
        data = self.shape_get_data()
        if data is None or len(data)<=0:
            return
        remove_key=""
        img_name = self.ImgWidget.label.img_name
        if img_name is not None and  img_name:
            is_labeled = self.img_list_set_labeled(img_name,data)
            if not is_labeled:
                remove_key=img_name

        write_json_config(img_dir+'/config.json',data,remove_key=remove_key)
    
    #加载指定图像文件的标注数据
    def label_data_load(self,img_dir,img_name,data_has_read:dict=None):
        '''加载指定图像文件的标注数据'''
        shape_list:list[dict]=[]

        data={}
        if data_has_read is not None and  isinstance(data_has_read,dict):
            data = deepcopy(data_has_read)
        else:
            data = read_json_config(img_dir+'/config.json')
        if len(data)<=0 or not isinstance(data,dict):
            return shape_list,data

        img_data:dict = data.get(img_name,{})
        #data={shape_list:[{shape_type:shape_type,points:[[0,1],[],...]},{},...]}
        if len(img_data)<=0:
            return shape_list,data
        
        shape_list = img_data.get("shape_list",[])
        return shape_list,data
    
    #图像文件是否已被标注
    def img_is_labeled(self,img_name:str,data_has_read:dict=None):
        '''图像文件是否已被标注'''
        if self.ImgList is None or not img_name:
            return False
        img_dir = self.ImgList.get_img_dir()
        if img_dir is None or not img_dir:
            return False
        shape_list:list[dict]=[]
        shape_list , _  =self.label_data_load(img_dir,img_name,data_has_read)
        if len(shape_list)<=0:
            return False
        return True

    #设置文件列表中对应图像文件是否被标注(打勾)
    def img_list_set_labeled(self,img_name:str,data_has_read:dict=None):
        '''设置文件列表中对应图像文件是否被标注(打勾)'''
        if self.ImgList is None or not img_name:
            return False
        is_labeled = self.img_is_labeled(img_name,data_has_read)
        self.ImgList.set_labeled(img_name,is_labeled)
        return is_labeled
    
    def list_name_or_group_delete(self,listWidget:QListWidget,comboBox:QComboBox,mode=""):
        if self.ImgWidget is None or self.ImgWidget.label is None:
            return
        text = ListWidge_current_text(listWidget,is_show_index=True)
        if text is None or not text:
            return
        ret=None
        name=None
        group=None
        if mode=="name" or mode=="名称":
            name=text
            ret = messageBox(self.win,"提示",f"删除标注名称['{text}']将会清除此类别的所有标注数据!\n\t确定删除?",QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        if mode=="group" or mode=="分组":
            group=text
            ret = messageBox(self.win,"提示",f"删除标注分组['{text}']将会打散此组合的所有标注数据!\n\t确定删除?",QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        if ret!=QMessageBox.StandardButton.Ok:
            return
        
        self.delete_name_or_group(name,group)
        
        ListWidget_remove(listWidget,text,is_show_index=True)
        ComboBox_remove(comboBox,text)
        listWidget.clear()
        self.ImgWidget.label.init_canvas()    
        self.img_label_load()
        self.update_shape_list()    
    
    def delete_name_or_group(self,name:str,group:str):
        self.img_save_label()#先保存一次,方便后续直接对json文件修改
        img_list = self.ImgList.get_img_list()
        img_dir  = self.ImgList.get_img_dir()
        if not len(img_list) or not len(img_dir):
            return

        data = read_json_config(img_dir+'/config.json')
        if len(data)<=0 or not isinstance(data,dict):
            return 

        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])
        key_points:list[int] = data.get("key_points",[])

        line_rule:list[list[int]]=data.get("line_rule",[])
        name_id,group_id = get_name_group_index(name,group,name_info,group_info)
        
        if name_id is not None:
            line_rule_new:list[list[int]]=[]
            for line in line_rule:
                if name_id in line:
                    continue
                line_new:list[int]=[]
                for id in line:
                    if id> name_id:
                        id-=1
                    line_new.append(id)
                line_rule_new.append(line_new) 
            data["line_rule"]=line_rule_new  
            
            key_points = Utils.list_remove_id(key_points,name_id) 
            data["key_points"]=key_points


        
        if name_id is not None and name:
            data["name_info"] = Utils.list_info_remove(name_info,name)
            
            
        if group_id is not None and group:
            data["group_info"] = Utils.list_info_remove(group_info,group)
       
        for img_name in img_list:
            img_data:dict = data.get(img_name,{})
            #data={shape_list:[{shape_type:shape_type,points:[[0,1],[],...]},{},...]}
            if len(img_data)<=0:
                continue
            shape_list_new:list[dict]=[]
            shape_list:list[dict] = img_data.get("shape_list",[])
            for shape in shape_list:
                '''
                data={}
                data["shape_type"]= self.shape_type.value
                data["name_id"]= name_id 
                data["group_id"]= group_id 
                data["info"]= self.info 
                data["angle"]= self.angle 
                data["points"]= [(round(p.x()), round(p.y())) for p in self.points]
                '''
                
                if name_id is not None:
                    name_ = shape.get("name_id",None)
                    if name_ is None or name_ == name_id:
                        continue
                    if name_ > name_id:
                        name_-=1
                    shape["name_id"]=name_
                
                if group_id is not None:
                    group_ = shape.get("group_id",None)
                    if group_ is  None or group_==group_id:
                        group_=None
                    else:
                        if group_ > group_id:
                            group_-=1
                    shape["group_id"]=group_   
                     
                shape_list_new.append(shape)
            img_data["shape_list"]= shape_list_new   
            data[img_name]=img_data
            self.img_list_set_labeled(img_name,data)
        
        write_json_config(img_dir+'/config.json',data,remove_key="")    
                
    def edit_name_or_group(self,mode="",old_value=""):
        dialog = InputDialog(self.win,mode,old_value)
        text=""
        if dialog.exec() == QDialog.Accepted:
            text = dialog.get_text()
        return text        
    
    def edit_name_or_group_run(self,mode="",old_value="",new_value="")  :
        self.img_save_label()#先保存一次,方便后续直接对json文件修改
        img_list = self.ImgList.get_img_list()
        img_dir  = self.ImgList.get_img_dir()
        if not len(img_list) or not len(img_dir):
            return

        data = read_json_config(img_dir+'/config.json')
        if len(data)<=0 or not isinstance(data,dict):
            return 
        name_info  = data.get("name_info",[])
        group_info = data.get("group_info",[])

        if mode=="name" or mode=="名称":
            name_info = Utils.list_info_update_text(name_info,old_value,new_value)
        if mode=="group" or mode=="分组":
            group_info = Utils.list_info_update_text(group_info,old_value,new_value)       
        data["name_info"]  = name_info
        data["group_info"] = group_info
        write_json_config(img_dir+'/config.json',data,remove_key="")

    def list_name_or_group_edit(self,listWidget:QListWidget,comboBox:QComboBox,mode="") : 
        text = ListWidge_current_text(listWidget,is_show_index=True)
        text_new = self.edit_name_or_group(mode,text) 
        if text_new is None or not text_new:
            return
        index = ListWidget_get_index(listWidget,text_new,is_show_index=True)
        if index is not None:
            messageBox(self.win,"提示",f"['{text_new}'] 在{mode}列表中已经存在,请勿使用重复的{mode}!")
            return
        self.edit_name_or_group_run(mode,text,text_new)     
        ListWidget_set_text(listWidget,text,text_new,True)  
        ComboBox_set_text(comboBox,text,text_new)   

        self.ImgWidget.label.init_canvas()    
        self.img_label_load()
        self.update_shape_list()            
    
    def name_list_color(self):
        if not  self.ImgWidget.label.is_valid:
            return
        ListWidget_current_set_color(self.ui.listWidget_name_list,is_show_index=True,parent=self.win)
        self.img_save_label()#先保存一次,方便后续直接对json文件修改
        self.ImgWidget.label.init_canvas()    
        self.img_label_load()
        self.update_shape_list() 
        
    def group_list_color(self):
        if not  self.ImgWidget.label.is_valid:
            return
        ListWidget_current_set_color(self.ui.listWidget_group_list,is_show_index=True,parent=self.win) 
        self.img_save_label()#先保存一次,方便后续直接对json文件修改 
        self.ImgWidget.label.init_canvas()    
        self.img_label_load()
        self.update_shape_list()           
                
    def img_label_auto(self):
        img_path = self.ImgWidget.label.img_path
        if not  os.path.exists(img_path):
            return
        
        model_path = self.ui.lineEdit_model_path.text()
        if not model_path or not  os.path.exists(model_path):
            messageBox(self.win,"提示","模型路径无效,选择有效模型!")
            return
        
        suffix = os.path.splitext(model_path)[1]
        if suffix.lower() not in [".onnx"]:
            messageBox(self.win,"提示","模型文件无效,请选择.onnx后缀的模型文件!")  
            return
        self.config_save_model()
        if self.model_yolo is None or self.model_path_yolo != model_path:
            self.model_path_yolo = model_path 
            self.model_yolo = Yolos(model_path)  
        
        conf_thres = self.ui.doubleSpinBox_model_score.value()
        
        shape_list = self.model_yolo.predict_shapes(img_path,shape_type_dict(),self.ImgWidget.label.key_points,conf_thres=conf_thres)  
        if len(shape_list)>0:
            self.ImgWidget.label.set_shape_type(self.ImgWidget.label.shape_type)
            self.ImgWidget.label.shape_list.clear()
        for shape_data in shape_list:
            name = shape_data.get("name","")
            shape_type = shape_data.get("shape_type",None)
            points = shape_data.get("points")
            info =shape_data.get("info","")
            angle=shape_data.get("angle",0)
            group_id=shape_data.get("group_id",0)
            point_list = [QPointF(point[0],point[1]) for point in points ]
            color = get_color(self.ui.listWidget_name_list.count())  
            rect=self.ImgWidget.label.get_rect()
            scale=self.ImgWidget.label.get_scale()
            
            shape = Shape(shape_type,point_list,color,rect,scale)
            shape.angle = angle
            shape.created=True
            self.ImgWidget.label.shape_created(shape,False)
            
            if shape_type in [ShapeType.point]:
                name_id = int(name)
                if name_id >=0:
                    name = self.ImgWidget.label.name_list_get_str(name_id)
                else:
                    name=""
                if not name:
                    name=f"关键点-未命名({name_id})"
            group = self.ImgWidget.label.group_list_get_str(group_id)
            if group_id is None:
                group=""
            else:
                group = group if group else f"未知分组({group_id})"
                
            
            data={}
            data["name"]=name
            data["info"]=info
            data["group"]=group
            data["isok"] = True
            data["shape"] = shape
            data["index"] = self.ui.listWidget_name_list.count()
            self.single_labelName(data)
        
        
    def config_save_model(self):
        img_dir = self.ImgList.get_img_dir()
        if img_dir is None or not img_dir:
            return 
        model_path = self.ui.lineEdit_model_path.text()
        conf_thres = self.ui.doubleSpinBox_model_score.value()
        data = {}
        data["model_path"]     = model_path
        data["conf_thres"]     = conf_thres
        write_json_config(img_dir+'/config.json',data)
    
    def config_read_model(self):
        img_dir = self.ImgList.get_img_dir()
        if img_dir is None or not img_dir:
            return 
        data = read_json_config(img_dir+'/config.json')
        model_path = data.get("model_path","")
        conf_thres = data.get("conf_thres",0.5)
        self.ui.lineEdit_model_path.setText(model_path)
        self.ui.doubleSpinBox_model_score.setValue(conf_thres)
        
def run():
    
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()

    win = UiBaseWindow(ui)
    events = UiEvents(win)
    win.show()
    sys.exit(app.exec())
    

    
if __name__ == '__main__':
    run()               