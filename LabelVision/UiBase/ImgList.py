from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import os
import fnmatch


class ImgList():
    def __init__(self,list_widget:QListWidget,img_dir:str=""):
        self.list_widget = list_widget
        self.data = {}
        self.data["img_dir"]  = ""
        self.data["img_list"]= []
        if img_dir:
            self.build_data(img_dir)
        self.build_list_widget()

    # 构建数据
    def build_data(self,img_dir:str):
        '''构建数据'''
        if not os.path.isdir(img_dir): 
            return None

        extensions=["jpg", "jpeg", "png", "tiff", "bmp"]
        # 初始化一个空列表来存储文件名
        img_list:list[dict] = []
        filename:str=""
        # 遍历文件夹中的所有文件
        for filename in os.listdir(img_dir):
            # 检查文件名是否匹配指定的扩展名之一
            if any(fnmatch.fnmatch(filename.lower(), f'*.{ext}') for ext in extensions):
                # 如果是匹配的文件，将其添加到列表中
                # 注意：这里只添加了文件名，如果需要完整路径，可以使用 os.path.join(folder_path, filename)
                data={}
                data["name"] = filename
                data["is_labeled"]=False
                img_list.append(data)
        self.data["img_dir"]=img_dir
        self.data["img_list"]=img_list
        
    # 生成图像文件列表控件
    def build_list_widget(self,img_name:str=""):
        '''构建列表控件'''
        self.list_widget.clear()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)  # 设置单选模式
        img_list = self.data["img_list"]
        for data in img_list:
            if "name" not in data or not data["name"]:
                continue
            name:str = data["name"]
            if img_name and img_name.lower() not in name.lower():
                continue
            is_labeled=Qt.CheckState.Unchecked
            if "is_labeled" in data and data["is_labeled"]:
                is_labeled=Qt.CheckState.Checked
            item = QListWidgetItem(name)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(is_labeled)
            self.list_widget.addItem(item)
            
    #更新列表数据
    def img_list_update(self,img_name:str,**kwargs):
        '''更新图像列表数据'''
        if img_name is None or not img_name: 
            return
        arg = {}
        arg.update(kwargs)
        length = len(self.data["img_list"])
        for i in range(length):
            data=self.data["img_list"][i]
            if "name" not in data or not data["name"]:
                continue
            name:str = data["name"]
            if name.lower() != img_name.lower():
                continue
            arg["name"] = name
            self.data["img_list"][i] = arg
            break
        # if "is_labeled" in arg:
        #     self.set_item_labeled(img_name,is_labeled=arg["is_labeled"])
    
    #将图片数据从列表删除
    def delete_img_list_by_name(self,img_name:str):
        '''将图片数据从列表删除'''
        is_delete = False
        if img_name is None or not img_name: 
            return is_delete
        length = len(self.data["img_list"])
        for i in range(length):
            data = self.data["img_list"][i]
            if "name" not in data or not data["name"]:
                continue
            name:str = data["name"]
            if name.lower() != img_name.lower():
                continue
            del self.data["img_list"][i] 
            is_delete=True
            break
        return is_delete
    #通过索引查找图片名字
    def get_img_list_name_by_index(self,index:int) -> str:
        """通过索引查找图片名字"""
        length = len(self.data["img_list"])
        if index < 0 :
            return ""
        if index >= length :
            index=length-1
        data = self.data["img_list"][index]
        if "name" not in data or not data["name"]:
            return ""
        name:str = data["name"]
        return name
    # 获取当前选中列的图片名称
    def get_img_list_current_name(self):
        '''获取当前选中列的图片名字'''
        item = self.list_widget.currentItem()
        if item:
            return item.text()
        return ""
    #获取下一张图片名字
    def get_img_list_next(self):
        '''获取下一张图片名字'''
        # 检查QListWidget是否为空
        if self.list_widget.count() == 0:
            return ""  # 如果为空，直接返回空字符串
    
        # 计算下一个项的索引，使用取模运算确保索引在有效范围内内循环
        index = (self.list_widget.currentIndex().row() + 1) % self.list_widget.count()
        # 获取项
        item = self.list_widget.item(index)
        if item is not None:
            return item.text()
        return ""
    #获取上一张图片名字    
    def get_img_list_prev(self):
        '''获取上一张图片名字'''
        # 检查QListWidget是否为空
        if self.list_widget.count() == 0:
            return ""  # 如果为空，直接返回空字符串
        # 获取当前选中项的行索引
        current_row = self.list_widget.currentIndex().row()
        
        # 计算上一个项的行索引
        # 如果当前项是第一个项（索引为0），则上一个项为最后一个项
        prev_row = current_row - 1 if current_row > 0 else self.list_widget.count() - 1
        # 获取项
        item = self.list_widget.item(prev_row)
        if item is not None:
            return item.text()
        return ""
    #获取图片列表中 图片列表以及当前选中项的索引
    def get_img_list_ListAndCurrentIndex(self):
        '''获取图片列表数据以及当前选中项索引'''
        data_list = self.data["img_list"]
        index = -1
        length = len(data_list)
        current_name = self.get_img_list_current_name()
        if current_name == "" or length == 0:
            return data_list,index

        for i in range(length):
            data = data_list[i]
            if "name" not in data :
                continue
            name :str= data["name"]
            if name.lower()==current_name.lower():
                index=i
                break
        return data_list,index
    #获取下一张未标注图片名字    
    def get_img_list_next_nolabel(self):
        '''获取下一张未标注图片名字'''
        data_list,index = self.get_img_list_ListAndCurrentIndex()
        length = len(data_list)
        if length==0:
            return ""
        for i in range(length):
            n = (index + 1 + i) % length
            data = data_list[n]
            if "name" not in data or "is_labeled" not in data:
                continue
            name:str = data["name"]
            is_labeled = data["is_labeled"]
            if not is_labeled and name:
                return name
        return ""  
    #获取上一张未标注图片名字
    def get_img_list_prev_nolabel(self):
        '''获取上一张未标注图片名字'''
        data_list,index = self.get_img_list_ListAndCurrentIndex()
        length = len(data_list)
        if length == 0:
            return ""
        index = index if index >= 0 else 0
        for i in range(length):
            
            n = (index - 1 - i) 
            data = data_list[n]
            if "name" not in data or "is_labeled" not in data:
                continue
            name:str = data["name"]
            is_labeled = data["is_labeled"]
            if not is_labeled and name:
                return name
        return ""      
           
    #显示搜索文件列表
    def show_search_img_list(self,img_name:str):
        '''显示搜索文件列表'''
        self.build_list_widget(img_name)
     
    #获取指定图片的列表item
    def get_img_list_item(self,img_name:str):
        '''获取指定图片的列表item'''
        ret_item=None
        count=self.list_widget.count()
        for index in range(count):
            item = self.list_widget.item(index)
            name:str = item.text()
            if name.lower()==img_name.lower():
                ret_item=item
                break
        
        return ret_item    
    
    #设置列表项为选中        
    def set_item_select(self, img_name:str):
        '''设置指定名字的列表项为选中状态'''
        item = self.get_img_list_item(img_name)
        if item is None: 
            return
        self.list_widget.setCurrentItem(item)  # 选中该项
        self.list_widget.scrollToItem(item)  # 如果需要，可以滚动到该项
        
    #将指定图片从列表项中删除,返回索引
    def delete_img(self, img_name:str):
        '''将指定图片从列表项中删除,返回索引'''
        if not self.delete_img_list_by_name(img_name):
            return -1
        item = self.get_img_list_item(img_name)
        if item is  None: 
            return -1
        index = self.list_widget.row(item)
        if index<0 or index>=self.list_widget.count():
            return -1
        self.list_widget.takeItem(index)
        return index
        
    # 获取图片目录
    def get_img_dir(self):
        '''获取图片目录'''
        img_dir:str = self.data.get("img_dir","")  
        return  img_dir
    
    #获取图片名称列表
    def get_img_list(self):
        ''''获取图片名称列表'''
        # data["name"] = filename
        # data["is_labeled"]=False
        # img_list.append(data)
        img_list:list[dict] = self.data.get("img_list",[])
        if len(img_list) <=0 or not isinstance(img_list,list):
            return []
        lst:list[str] = []
        for data in img_list:
            if not isinstance(data,dict):
                return []
            name=data.get("name","")
            if not  name:
                continue
            lst.append(name)
        return lst
    
    def set_labeled(self,img_name:str,is_labeled:bool):
        item = self.get_img_list_item(img_name)
        if item is None: 
            return
        item.setCheckState(Qt.CheckState.Checked if is_labeled else Qt.CheckState.Unchecked)  # 勾选该项
        self.img_list_update(img_name,is_labeled=is_labeled)
    
    
    
    