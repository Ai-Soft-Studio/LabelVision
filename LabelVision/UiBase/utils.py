import shutil
import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from copy import deepcopy
import json


__appname__ = "LabelVision半自动标注工具"
__version__ = "1.0.0"


class Utils():
    def __init__(self):
        pass
     
    def file_move(source_file:str,destination_dir:str):
        # 确保目标目录存在，如果不存在则创建
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # 目标文件路径（包括文件名）
        destination_file = os.path.join(destination_dir, os.path.basename(source_file))
        
        # 移动文件
        shutil.move(source_file, destination_file)
        
    def QColor_get_info(color:QColor):
        if color is None:
            return []
        color_info:list[int] = [color.red(),color.green(),color.blue(),color.alpha()]
        return color_info

    def QColor_load_info(color_info:list[int]):
        if color_info is None or len(color_info) !=4:
            return None
        color=QColor(color_info[0],color_info[1],color_info[2],color_info[3])
        return color    
    
    def QColor_mean(colors:list[QColor])  :
        if colors is None or len(colors) <=0:
            return None
        num=0
        r,g,b,a=0,0,0,0
        for color in colors:
            if color is None: continue
            r += color.red()
            g += color.green()
            b += color.blue()
            a += color.alpha()
            num+=1
        
        return QColor(r//num,g//num,b//num,a//num)
        
    def list_info_make_data(text:str,color:QColor):
        data = {}
        data["text"] = text
        data["color"]= Utils.QColor_get_info(color)
        return data  
    
    def list_info_unpack(list_info:list[dict]):
        list_text:list[str]=[]
        list_color:list[QColor]=[]
        for data in list_info:
            if len(data) <=0:
                continue
            text  = data.get("text",None)
            color = Utils.QColor_load_info(data.get("color",[]))
            list_text.append(text)
            list_color.append(color)
        return list_text,list_color    
    
    def list_info_add(list_info:list[dict],text:str,color:QColor=None,text_exclude:str=None):
        index=None
        if not text:
            return index
        if text_exclude is not None and  text_exclude and text_exclude==text:
            return index
        index = Utils.list_info_get_index(list_info,text)
        if index is not None:
            return index
        data=Utils.list_info_make_data(text,color)
        list_info.append(data)
        index = len(list_info) -1    
        return index 
    
    def list_info_remove(list_info:list[dict],text:str):
        list_info_new:list[dict]=[]
        for data in list_info:
            if len(data) <=0:
                continue
            text_data:str  = data.get("text","")
            if not text_data or text_data.lower()==text.lower():
                continue
            list_info_new.append(data)
        return list_info_new    
        
    def list_info_update_text(list_info:list[dict],text:str,text_new:str):
        if text is None or not text or text_new is None or not text_new:
            return list_info
        list_info_new:list[dict]=[]
        for data in list_info:
            if len(data) <=0:
                continue
            text_data:str  = data.get("text","")
            if not text_data :
                continue
            if text_data.lower()==text.lower():
                data["text"]=text_new
            list_info_new.append(data)
        return list_info_new    
        
    def list_info_get_index(list_info:list[dict],text:str):
        index = None
        if text is None or not text  or list_info is None:
            return index
        length = len(list_info)
        for i in range(length):
            data:dict= list_info[i]
            text_data:str  = data.get("text","")
            if not text_data :
                continue
            if text_data.lower()==text.lower():
                index=i
                break
        return index    
    
    def list_info_get_data(list_info:list[dict],index:int):
        text=None
        color=None
        # if not Utils.index_in(list_info,index):
        #     return text,color
        # data = list_info[index]
        data = Utils.list_get_data(list_info,index)
        if data is None or not isinstance(data,dict):
            return text,color
        text:str=data.get("text","")
        color:QColor = Utils.QColor_load_info(data.get("color",[]))
        return text,color
    
    def index_in(lst:list,index:int):
        if index is None or not isinstance(index,int):
            return False
        if index >= len(lst) :
            return False
        if index <0 and abs(index)>len(lst) :
            return False  
        return True  
    def list_get_index(lst:list,data:any):
        index = None
        if lst is None or not isinstance(lst,list): 
            return index
        if data in lst:
            index = lst.index(data)
        return index
    
    def list_get_index_list(lst:list,data_list:list):
        index_list:list[int]=[]
        if lst is None or not isinstance(lst,list): 
            return index_list
        if data_list is None or not isinstance(data_list,list): 
            return index_list
        for data in data_list:
            index = Utils.list_get_index(lst,data)
            if index is  None: 
                continue
            index_list.append(index)
        return index_list
            
    def list_get_data(lst:list,index:int):
        if not Utils.index_in(lst,index):
            return None   
        data=lst[index]
        return data
    
    def list_get_data_list(lst:list,index_list:list[int]):
        data_list:list=[]
        for index in index_list:
            data = Utils.list_get_data(lst,index)
            data_list.append(data)
        return data_list
    
    def list_is_all_in(lst:list,data_list:list):
        is_all_in = False
        if lst is None or not isinstance(lst,list): 
            return False
        if data_list is None or not isinstance(data_list,list): 
            return False
        if len(data_list) <=0 or len(lst) <=0:
            return False
        for data in data_list:
            if data not in lst:
                return False
            is_all_in=True
        return is_all_in 
    
    def list_set_data(lst:list,index:int,data:any):
        if not Utils.index_in(lst,index):
            return None   
        lst[index]=data
        return data
    
    def list_add(lst:list,data:any,is_force_add=False):
        index = Utils.list_get_index(lst,data)
        if index is not None and not is_force_add:
            return index
        lst.append(data)
        index = len(lst) -1
        return index    
        
    def point_is_in_rect(point:QPointF,topleft: QPointF, bottomRight: QPointF) -> bool:
        rect = QRectF(topleft,bottomRight)    
        return rect.contains(point)
        
    def list_remove_id(id_list:list[int],remove_id:int):
        id_list_new:list[int]=[]
        for id in id_list:
            if remove_id ==id:
                continue
            if id> remove_id:
                id-=1
            id_list_new.append(id) 
        return id_list_new    
        
    def keysinfo():
        msg = (
            "快捷键\t\t\t说明\n"
            "———————————————————————\n"
            "鼠标滚轮-向上\t\t放大图片\n"
            "鼠标滚轮-向下\t\t缩小图片\n"
            "鼠标左键\t\t创建或单选标记框\n"
            "鼠标右键\t\t弹出菜单\n"
            "鼠标右键-按下拖动\t拖拽图像\n"
            
            "Ctrl  + 鼠标滚轮\t\t旋转 1°(可旋转的)标记框\n"
            "Shift+ 鼠标滚轮\t\t旋转10°(可旋转的)标记框\n"
            "Ctrl  + 鼠标左键\t\t多选标记框\n"
            "Alt   + 鼠标左键\t\t强制创建标记\n"
            
            "Ctrl  + H\t\t\t隐藏选中标记\n"
            "Ctrl  + S\t\t\t显示所有标记\n"
            "Ctrl  + C\t\t\t复制标记\n"
            "Ctrl  + V\t\t\t粘贴标记\n"
            "Ctrl  + Z\t\t\t撤销操作\n"
            "Ctrl  + Y\t\t\t恢复操作\n"
            
            "Delete\t\t\t删除选中标记\n"
            "Ctrl  + Delete\t\t删除整张图片\n"
            "↑→↓←\t\t\t切换标记图片\n"
            "———————————————————————\n"
            "注:Mac用户Command键替换上述Ctrl键"
        )
        return msg    
    
    def useinfo():  
        msg = (
            "\t\t\t使用方法\n"
            "———————————————————————\n"
            "1.加载图片:\n"
            "    点击左上角按钮选择图片文件夹或者打开视频文件。\n"
            "    加载成功之后在左侧文件列表中选择要标注的图片。\n"
            "\n"
            "2.手动标注:\n"
            "    在顶部菜单栏选择要创建的标注形状。\n"
            "    在画布中通过鼠标左键创建标记框。\n"
            "    多边形和线条需要鼠标指向第一个点,再次点击可完成创建。\n"
            "    形状创建完成后会弹出命名窗口,填写标注名称再点击确定按钮可完成标注命名。\n"
            "    新增并选择分组可以给标注分组,一般是关键点标注时有用,可以将同一个对象的各个关键点组合在一起。\n"
            "    描述信息是给标注一个描述性文本,一般用来帮助记忆或者说明标注附加的信息。\n"
            "\n"
            "3.自动标注(可选):\n"
            "    在顶部选择模型所在路径,模型文件必须为onnx格式,一般为YOLO训练工具训练并导出的模型。\n"
            "    置信度阈值和IOU阈值是模型自动标注的参数,一般不需要修改。\n"
            "    点击'运行'按钮,模型会自动识别出图片中所有目标并自动创建标记框。\n"
            "\n"
            "4.修改标注:\n"
            "    在右侧可以修改对象描述(需选中标注)。\n"
            "    在名称列表或分组列表中右键可以修改标签颜色,重新改名,以及删除。\n"
            "    在右下方标注列表中可以给标注修改命名,删除,隐藏,显示。\n"
            "\n"
            "5.导出标注:\n"
            "    在顶部菜单选择导出标注,选择要导出的类型。\n"
            "    在弹出的窗口中选择保存路径,点击保存按钮即可。\n"
            "    如果图片未标注,则不会导出。"
            "\n"
            "    关键点标注导出将会额外弹出映射表,用于将关键点顺序在图片进行镜像翻转时映射到正确的关键点顺序。"

            "———————————————————————\n"
            "感谢您的使用,如果有好的建议,欢迎您提出。\n"
        )
        return msg   
    
    def aboutinfo():    
        msg=(
            f"{__appname__}\n"
            f"版本:{__version__}\n"
            "作者:无忧开发组\n"
            "官网:http://www.voouer.com\n"
            "版权所有©2025\n"
            "本软件为个人开发,并提供免费使用。\n若您觉得本软件好用,还请给我点个赞👆♥\n"
            )
             
        return msg
        
    
        