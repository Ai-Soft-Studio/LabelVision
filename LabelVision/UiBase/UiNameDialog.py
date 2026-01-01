from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import os
from copy import deepcopy

from .widget.labelName_ui import Ui_Dialog
from .UiBaseWindow import ComboBox_add_item,ListWidget_add_item,messageBox
from .ImgCanvas import ImgWidget,ZoomType,ShapeType,Shape,get_color,MouseState,get_name_group_index

class NameDialog(QDialog, Ui_Dialog):
    signal_labelName = Signal(dict)
    def __init__(self,parent=None):
        super(NameDialog, self).__init__(parent)
        self.setupUi(self)
        self.isok = False #用来表示是否点击了确定
        self.shape:Shape =  None #用来保存形状
        self.index = None   #用来保存形状的索引
        
        self.label_name:str = ""
        self.label_info:str = ""
        self.label_group:str = ""
        
        self.group_list:list[str] = []
        self.name_list:list[str]  = []
        self.key_points:list[int] = []
        
        self.listWidget_name_list.itemClicked.connect(self.name_list_item_clicked)
        self.pushButton_group_add.clicked.connect(self.group_add)
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_ok.clicked.connect(self.ok)
        
    #设置形状
    def set_shape(self,shape,index):
        '''设置形状'''
        self.shape =  shape
        self.index =  index
    
    #设置名称列表
    def set_name_list(self,name_list:list[str]):
        self.name_list = deepcopy(name_list)
    
    #设置分组列表
    def set_group_list(self,group_list:list):
        self.group_list = deepcopy(group_list)
    
    def set_key_points(self,key_points:list):
        self.key_points = deepcopy(key_points)
    
    def get_name_list(self):
        name_list_normal:list[str]=[]
        name_list_points:list[str]=[]
        for i in range(len(self.name_list)):
            name = self.name_list[i]
            if i in self.key_points:
                name_list_points.append(name)
            else:
                name_list_normal.append(name)
        if self.shape.shape_type in [ShapeType.point]:
            return name_list_points
        return name_list_normal
        
        
    #获取标注数据
    def get_data(self):
        """#获取标注数据"""
        data={}
        data["name"]=self.label_name
        data["info"]=self.label_info
        data["group"]=self.label_group if self.label_group!="未分组" else ""
        data["isok"] = self.isok
        data["shape"] = self.shape
        data["index"] = self.index
        return data
    
    #弹出窗体
    def show(self):
        """#弹出窗体"""
        # super(NameDialog, self).show()
        
        name_list = self.get_name_list()
        #控件内容填充
        self.lineEdit_group_add.setText("")
        self.textEdit_info.setText(self.label_info)
        
        
        self.comboBox_group.clear()
        ComboBox_add_item(self.comboBox_group,"未分组",False)
        for group in self.group_list:
            ComboBox_add_item(self.comboBox_group,group,False)
        ComboBox_add_item(self.comboBox_group,self.label_group,True)
        
        self.listWidget_name_list.clear()
        
        for name in name_list:
            ListWidget_add_item(self.listWidget_name_list,name,False)
        
        self.lineEdit_name.setText("")
        if self.label_name in name_list:
            self.lineEdit_name.setText(self.label_name)
            ListWidget_add_item(self.listWidget_name_list,self.label_name,True)
        
        #模态窗口弹出
        self.exec_()
        
        #获取并返回数据
        data = self.get_data()
        self.clear()
        return data
    
    #清理留存数据
    def clear(self):
        """#清理留存数据"""
        self.isok = False #用来表示是否点击了确定
        self.shape = None #用来保存形状
        self.index = None #用来保存形状的索引
        self.group_list.clear()
        self.name_list.clear()
        self.key_points.clear()
    
    #点击ok按钮处理事件
    def ok(self):
        """#点击ok按钮处理事件"""
        self.label_name = self.lineEdit_name.text()
        self.label_info = self.textEdit_info.toPlainText()
        self.label_group= self.comboBox_group.currentText()
        
        
        if self.label_name == "":
            messageBox(self, "提示", "请输入标注名称", QMessageBox.Ok)
            return
        
        name_list = self.get_name_list()
        if self.label_name not in name_list and self.label_name  in self.name_list :
            #已经存在于全部名称列表中,但是不在当前列表中,说明和其他类别冲突,比如关键点和框名重复了
            text="该名称已存在,请重新输入"
            if self.shape.shape_type in [ShapeType.point] :
                text="该名称无法为关键点命名,原因为:名称列表中已存在!"
            else:
                text="该名称已被关键点名称占用,请重新输入!"
            messageBox(self, "提示", text, QMessageBox.Ok)
            return
        
        self.isok=True
        # data = self.get_data()
        # self.signal_labelName.emit(data)
        self.close()
    
    #点击取消按钮
    def cancel(self):
        """点击取消按钮"""
        self.isok=False
        super().close()
    
    #名称列表项被点击    
    def name_list_item_clicked(self,item:QListWidgetItem):
        '''名称列表项被点击'''
        if item is None:
            return
        text=item.text()
        self.lineEdit_name.setText(text) 
    
    #增加分组按钮被点击
    def group_add(self):
        '''增加分组按钮被点击'''
        text = self.lineEdit_group_add.text()
        if text=="":
            return
        ComboBox_add_item(self.comboBox_group,text)
        
    






class InputDialog(QDialog):
    def __init__(self, parent=None,mode="",old_value=""):
        super().__init__(parent)

        str_title=f"修改标注{mode}"
        self.setWindowTitle(str_title)
 
        # 创建布局和控件
        layout = QVBoxLayout(self)
 
        self.label = QLabel("请输入新文本:", self)
        layout.addWidget(self.label)
 
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(old_value)
        layout.addWidget(self.line_edit)
 
        self.submit_button = QPushButton("确定", self)
        self.submit_button.clicked.connect(self.accept)
        layout.addWidget(self.submit_button)
 
    def get_text(self):
        return self.line_edit.text()



# 使用示例
if __name__ == "__main__":
    app = QApplication([])
 
    dialog = InputDialog()
    if dialog.exec() == QDialog.Accepted:
        text = dialog.get_text()
        print(f"User entered: {text}")
 
    app.exec()


