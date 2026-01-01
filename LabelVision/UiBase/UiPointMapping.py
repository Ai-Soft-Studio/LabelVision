from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import os
from copy import deepcopy

from .widget.point_mapping_ui import Ui_Dialog
from .UiBaseWindow import ListWidget_get_text,ListWidget_add_item,messageBox,ListWidget_load_list_info
from .ImgCanvas import ImgWidget,ZoomType,ShapeType,Shape,get_color,MouseState,get_name_group_index
from .utils import Utils






class PointDialog(QDialog, Ui_Dialog):
    signal_labelName = Signal(dict)
    def __init__(self,parent=None):
        super(PointDialog, self).__init__(parent)
        self.setupUi(self)
        self.listWidget_point_mapping.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.point_names:list[str]=[]
        self.is_ok = False
        self.pushButton_ok.clicked.connect(self.ok)
        
    def set_point_names(self,name_info:list[dict],key_points:list[int],point_names:list[str]):
        is_in = Utils.list_is_all_in(point_names,self.point_names)
        if not is_in:
            self.listWidget_point_original.clear()
            self.listWidget_point_mapping.clear()
        self.point_names = deepcopy(point_names)
        data_list = deepcopy(Utils.list_get_data_list(name_info,key_points))
        ListWidget_load_list_info(self.listWidget_point_original,data_list,True,alpha=100)
        ListWidget_load_list_info(self.listWidget_point_mapping,data_list,True,alpha=100)

    def get_mapping_names(self):
        listWidget = self.listWidget_point_mapping
        list_text:list[str]=[]
        for i in range(listWidget.count()):
            text = ListWidget_get_text(listWidget,i,is_show_index=True)
            if text is None or not text :
                continue
            Utils.list_add(list_text,text)

        return list_text
        
        
    
    
    def show(self):
        self.exec_()
        if not self.is_ok:
            return None
        self.is_ok=False
        mapping_names = self.get_mapping_names()
        key_points_mapping = Utils.list_get_index_list(self.point_names,mapping_names)
        if len(key_points_mapping) != len(self.point_names):
            return None
        
        return key_points_mapping

    def ok(self):
        self.is_ok = True
        self.close()



# 使用示例
if __name__ == "__main__":
    app = QApplication([])
 
    # dialog = InputDialog()
    # if dialog.exec() == QDialog.Accepted:
    #     text = dialog.get_text()
    #     print(f"User entered: {text}")
 
    # app.exec()


