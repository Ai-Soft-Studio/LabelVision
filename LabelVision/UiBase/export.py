import shutil
import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from copy import deepcopy
import json
from PIL import Image
import yaml
from pathlib import Path
import re
from .utils import Utils
from .Shape import Shape,ShapeType,shape_list_build,get_min_max_point,distance_to_edge
from .UiPointMapping import PointDialog
from .UiBaseWindow import messageBox



class Export():
    def __init__(self):
        pass
    def pose_make_group_date(group:str,rect:Shape,point_list:list[Shape]):
        group_date = {}
        group_date["group"]=group
        group_date["rect"] =rect
        group_date["group_point_list"]=point_list
        return group_date
    def pose_unpack_group_date(group_date:dict):
        group:str=""
        rect:Shape = None
        group_point_list:list[Shape] = []
        if group_date is None or not len(group_date) or not isinstance(group_date,dict):
            return group,rect,group_point_list
        group=group_date.get("group","")
        rect=group_date.get("rect",None)
        group_point_list=group_date.get("group_point_list",[])
        return group,rect,group_point_list
    def pose(parent,data:dict,img_list:list[str],img_dir:str,save_dir:str,split_ratio=0.7):
        if not (isinstance(data,dict) and len(data)>0):
            return False
        if not os.path.exists(img_dir): 
            return False
        if not os.path.exists(save_dir): 
            return False
        if img_list is None or not len(img_list):
            return False
        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])
        key_points:list[int] = data.get("key_points",[])
        
        #重新构建关键点名字列表
        point_names:list[str] = Export.pose_get_point_names(name_info,key_points)
        if len(point_names) != len(key_points):
            print("关键点数量不一致")
        if not len(point_names):
            return False
        
        #打开关键点镜像翻转映射窗口
        dialog_point = PointDialog(parent)
        dialog_point.set_point_names(name_info,key_points,point_names)
        key_points_mapping = dialog_point.show()
        if key_points_mapping is None:
            messageBox(parent,"提示","关键点映射关系未设置,将会忽略镜像翻转的关键点!\n无需构建映射关系的请忽略本条信息!!")
        
        data_list:list[dict]=[]
        for img_name in img_list:
            #提取单张图片的姿态识别(POSE)数据
            data_once = Export.pose_once(data,img_name,img_dir,name_info,group_info,point_names)
            if data_once is None or len(data_once) <=0: 
                continue
            data_list.append(data_once)
        
        length = len(data_list)
        if length<=0:
            return False
        
        #将训练集和验证集进行分割
        length_train = int(split_ratio * length)
        if length_train<1:
            length_train=1
        data_list_train = data_list[:length_train]
        data_list_val = data_list[length_train:]
        
        #保存训练集和验证集
        name_train="train"
        name_val="val"
        path_images=os.path.join(save_dir,"images")
        path_labels=os.path.join(save_dir,"labels")
        Export.dir_remake(path_images)
        Export.dir_remake(path_labels)
        index = Export.save_date_set(data_list_train,path_images,path_labels,name_train) 
        Export.save_date_set(data_list_val,path_images,path_labels,name_val)
        
        #构建yaml文件
        path_yaml = os.path.join(save_dir,"pose.yaml")
        data_yaml = Export.pose_build_yaml(name_info,key_points,key_points_mapping)
        save_yaml={}
        save_yaml['path']=save_dir
        save_yaml.update(data_yaml)
        Export.yaml_save(path_yaml,save_yaml)
        return index>0  
    def pose_build_yaml(name_info:list[dict],key_points:list[int],key_points_mapping:list[int]):
        '''构建姿态识别(POSE)的yaml文件'''
        data={}
        data["train"]="images/train"
        data["val"]="images/val"
        data["test"]=None
        data["kpt_shape"]=[len(key_points),3]
        if key_points_mapping is not  None and  len(key_points_mapping):
            # data["flip_idx"]=f"[{', '.join([str(i) for i in key_points_mapping])}]"
            data["flip_idx"]=key_points_mapping#[0, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15]
        
        name_list,_ = Utils.list_info_unpack(name_info)
        
        names={}
        for i in range(len(name_list)):
            names[i]=name_list[i]
        
        data["names"]=names
        
        return data     
    # 提取单张图片的姿态识别(POSE)数据
    def pose_once(data:dict,img_name:str,img_dir:str,name_info:list[dict],group_info:list[dict],point_names:list[str]):
        '''提取单张图片的姿态识别(POSE)数据'''
        if not (isinstance(data,dict) and len(data)>0):
            return None
        img_path = os.path.join(img_dir,img_name)
        if not  os.path.exists(img_path):
            return None
        
        # 获取图像的宽高
        width=None
        height=None
        with Image.open(img_path) as image:
            width, height = image.size
        
        if width is None or height is None or width<=0 or height<=0:
            return None
        
        #读取形状数据列表
        img_data:dict = data.get(img_name,{})
        if not (isinstance(img_data,dict) and len(img_data)>0):
            return None
        shape_list = img_data.get("shape_list",[])
        #对数据进行处理,并获得归一化数据文本
        group_date_list:list[dict] = Export.pose_once_get_datas(shape_list,name_info,group_info,point_names)
        text_normale_list:list[str] = Export.pose_once_normalization(group_date_list,name_info,width,height)
        if text_normale_list is None or len(text_normale_list) <=0:
            return None
        text=""
        for text_normale in text_normale_list:
            text+=text_normale+"\n"
        
        data={}
        data["img_path"]    =img_path
        data["img_name"]    =img_name
        data["text"]        =text
        return data  

    # 获取关键点和关联的矩形框数据
    def pose_once_get_datas(shape_list:list[dict],name_info:list[dict],group_info:list[dict],point_names:list[str]):
        """获取关键点和关联的矩形框数据"""
       
        shapes = shape_list_build(shape_list,name_info,group_info)
        
        #提取出所有矩形框和关键点,分别存放到列表中
        rect_list:list[Shape]=[]
        point_list:list[Shape]=[]
        for shape in shapes:
            if shape.shape_type in [ShapeType.rectangle]:
                Utils.list_add(rect_list,shape)
                continue
            if shape.shape_type in [ShapeType.point]:
                Utils.list_add(point_list,shape)
                continue
        
        #根据矩形框的分组,将数据划分
        group_date_list:list[dict] = Export.pose_make_group_date_list(rect_list,point_list)
        
        #按矩形框需要包含关键点的规则,再次划分数据
        group_date_list:list[dict] = Export.pose_make_group_date_list_as_contains(group_date_list)
        
        #获取未被包含的关键点
        point_list_no_contains:list[Shape] = Export.pose_get_points_as_no_contains(group_date_list,point_list)
        
        #未包含的关键点匹配哪个矩形的边离它最近
        group_date_list_nearest = Export.pose_make_group_date_list_as_nearest(rect_list,point_list_no_contains)
        
        #将包含的和距离最近的数据进行合并
        group_date_list:list[dict] = Export.pose_make_group_date_list_merge(group_date_list_nearest,group_date_list)
        
        #筛选和丢弃重复名字的关键点
        group_date_list:list[dict] = Export.pose_make_group_date_list_as_unique(group_date_list)
        
        #按名字列表对数据进行排序处理
        group_date_list = Export.pose_make_group_date_list_sort(group_date_list,point_names)
        
        #最后返回数据
        return group_date_list
    
    # 对数据进行归一化处理,并返回结果文本数组
    def pose_once_normalization(group_date_list:list[dict],name_info:list[dict],width:int, height:int):
        '''对数据进行归一化处理,并返回结果文本数组'''
        # pose 数据集 归一化规则
        # 图片 w h
        # 标注 x/w  y/h  boxw/w  boxh/h   px/w  py/h
        # 2维数据集 <class-index> <x> <y> <width> <height> <px1> <py1> <px2> <py2> ... <pxn> <pyn>
        # 3维数据集 <class-index> <x> <y> <width> <height> <px1> <py1> <p1-visibility> <px2> <py2> <p2-visibility> <pxn> <pyn> <p2-visibility>
        text_normale_list:list[str] =[]
        if group_date_list is None or len(group_date_list) <=0:
            return text_normale_list
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            
            name_id:(int|None) = Utils.list_info_get_index(name_info,rect.name)
            if name_id is None:
                name_id=0
            
            min_point,max_point = get_min_max_point(rect.points)
            rect_value:QRectF = QRectF(min_point, max_point)
            rect_value = Export.data_rect_normalization(rect_value,width,height)
            if rect_value is None:
                #矩形框归一化失败,代表标注无效
                continue
            point_value_list = []
            for point in group_point_list:
                lst=[]
                point_value:QPointF = None
                if point is not None:
                    point_value = Utils.list_get_data(point.points,0)
                    point_value = Export.data_point_normalization(point_value,width,height)
                if point_value is  None:
                    lst=[0,0,0]
                else:
                    lst=[point_value.x(),point_value.y(),2]
                point_value_list.append(lst)
            
            #将数据转为字符串
            # 3维数据集 <class-index> <x> <y> <width> <height> <px1> <py1> <p1-visibility> <px2> <py2> <p2-visibility> <pxn> <pyn> <p2-visibility>
            text_normale = f"{name_id} {rect_value.x():.6f} {rect_value.y():.6f} {rect_value.width():.6f} {rect_value.height():.6f} "   
            for i in range(len(point_value_list)) :
                point_value = point_value_list[i]   
                text_normale += f"{point_value[0]:.6f} {point_value[1]:.6f} {point_value[2]:.6f}"  
                text_normale=text_normale + (" " if i != len(point_value_list)-1 else "")
                    
            text_normale_list.append(text_normale)  
        return text_normale_list          
    
    # 将关键点分配给具有相同分组的矩形框数据列表
    def pose_make_group_date_list(rect_list:list[Shape],point_list:list[Shape]):
        '''将关键点分配给具有相同分组的矩形框数据列表'''
        group_date_list:list[dict]=[]
        for rect in rect_list:
            group = rect.group.lower()
            group_point_list:list[Shape]=[]
            for point in point_list:
                if point.group.lower() != group:
                    continue
                Utils.list_add(group_point_list,point)
            group_date = Export.pose_make_group_date(group,rect,group_point_list)
            Utils.list_add(group_date_list,group_date)
        return group_date_list 
    
    # 将关键点分配给包含它的矩形框数据列表             
    def pose_make_group_date_list_as_contains(group_date_list:list[dict]):
        '''将关键点分配给包含它的矩形框数据列表'''
        group_date_list_new:list[dict]=[]
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            
            topleft,bottomRight = get_min_max_point(rect.points)
            group_point_list_new:list[Shape]=[]
            for point in group_point_list:
                #关键点是否被包含在矩形框中
                is_in = Utils.point_is_in_rect(point.points[0],topleft,bottomRight)
                if not is_in:
                    continue
                Utils.list_add(group_point_list_new,point)
            group_date_new = Export.pose_make_group_date(group,rect,group_point_list_new)
            Utils.list_add(group_date_list_new,group_date_new)
        return group_date_list_new
    
    # 获取未被提取的关键点           
    def pose_get_points_as_no_contains(group_date_list:list[dict],point_list:list[Shape]):
        '''获取未被提取的关键点'''
        point_list_contained:list[Shape]=[]
        # 将已经提取的所有关键点放入列表
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            for point in group_point_list:
                Utils.list_add(point_list_contained,point)
        
        point_list_no_contains:list[Shape]=[]
        for point in point_list:
            #检查未被包含的所有关键点,并且提取到列表
            index = Utils.list_get_index(point_list_contained,point)
            if index is not None and index >=0 and index < len(point_list_contained):
                continue
            Utils.list_add(point_list_no_contains,point)
        return point_list_no_contains
    
    # 将关键点分配给距离它最近的矩形框数据列表
    def pose_make_group_date_list_as_nearest(rect_list:list[Shape],point_list_no_contains:list[Shape]):
        '''将关键点分配给距离它最近的矩形框数据列表'''
        group_date_list:list[dict]=[]
        for point in point_list_no_contains:
            group = point.group.lower()
            min_distance = float("inf")
            index = None
            for i in range(len(rect_list)):
                rect = rect_list[i]
                if rect.group.lower() != group:
                    #排除不同分组的矩形框
                    continue
                #取最近的矩形框
                distance = distance_to_edge(point.points[0],rect.points)
                if  distance > min_distance:
                    continue
                min_distance = distance
                index = i
            if index is  None:
                continue
            #提取到相同分组下,距离此关键点最近的矩形框
            rect = Utils.list_get_data(rect_list,index)
            group_date = Export.pose_make_group_date(group,rect,[point])
            Utils.list_add(group_date_list,group_date)
        return group_date_list
    
    # 将两个矩形框数据列表进行合并
    def pose_make_group_date_list_merge(group_date_list_nearest:list[dict],group_date_list:list[dict]):
        '''将两个矩形框数据列表进行合并'''
        group_date_list_new:list[dict]=[]
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            for group_date_nearest in group_date_list_nearest:
                group_nearest:str=""
                rect_nearest:Shape = None
                group_point_list_nearest:list[Shape] = []
                group_nearest,rect_nearest,group_point_list_nearest = Export.pose_unpack_group_date(group_date_nearest)
                if group_nearest != group:
                    continue
                if rect_nearest != rect: 
                    continue
                for point in group_point_list_nearest:
                    Utils.list_add(group_point_list,point)
            group_date_new = Export.pose_make_group_date(group,rect,group_point_list)
            Utils.list_add(group_date_list_new,group_date_new)                 
        return group_date_list_new
    
    #在矩形框数据列表中筛选和丢弃重复name的关键点
    def pose_make_group_date_list_as_unique(group_date_list:list[dict]):
        group_date_list_new:list[dict]=[]
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            group_point_list_new:list[Shape]=[]
            name_list:list[str]=[]
            for point in group_point_list:
                if point.group.lower() != group.lower():
                    continue
                name = point.name.lower()
                index = Utils.list_get_index(name_list,name)
                if not (index is not None and index >=0 and index < len(name_list)):
                    # 关键点并不存在于列表中,则拷贝过去
                    Utils.list_add(group_point_list_new,point)
                    Utils.list_add(name_list,name)
                    continue
                # 找到同样包含这个点的其他框列表
                group_date_list_others= Export.pose_get_group_date_list_as_contains(group_date_list,point,rect)
                if len(group_date_list_others):
                    continue
                #没有其他框包含这个点,则查询之前同名的点是否被包含
                #获取另外一个同名的点
                point_other:Shape=Utils.list_get_data(group_point_list_new,index)
                if point_other is  None or point_other.name.lower() != name:
                    continue
                #查询是否被包含
                group_date_list_others= Export.pose_get_group_date_list_as_contains(group_date_list,point_other,rect)
                if len(group_date_list_others):
                    #如果被包含则将当前点替换上个同名的点
                    Utils.list_set_data(group_point_list_new,index,point)
            group_date_new = Export.pose_make_group_date(group,rect,group_point_list_new)
            Utils.list_add(group_date_list_new,group_date_new)
        return group_date_list_new   
         
    # 获取包含某个关键点的所有矩形框数据列表
    def pose_get_group_date_list_as_contains(group_date_list:list[dict],point:Shape,rect_exclude:Shape):
        group_date_list_new:list[dict]=[]
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            if point.group.lower() != group.lower():
                continue
            if rect == rect_exclude:
                continue
            if point not in group_point_list :
                #未包含指定关键点
                continue
            Utils.list_add(group_date_list_new,group_date)
        return group_date_list_new        

    #按point_names对矩形框数据列表进行排序
    def pose_make_group_date_list_sort(group_date_list:list[dict],point_names:list[str]):
        group_date_list_new:list[dict]=[]
        
        for group_date in group_date_list:
            group:str=""
            rect:Shape = None
            group_point_list:list[Shape] = []
            group,rect,group_point_list = Export.pose_unpack_group_date(group_date)
            group_point_list_new:list[Shape]=[]
            for name in point_names:
                point_sort=None
                for point in group_point_list:
                    if point.name.lower() != name.lower():
                        continue
                    point_sort=point
                    break
                Utils.list_add(group_point_list_new,point_sort)

            group_date_new = Export.pose_make_group_date(group,rect,group_point_list_new)
            Utils.list_add(group_date_list_new,group_date_new)
        return group_date_list_new

    # 获取关键点名字列表    
    def pose_get_point_names(name_info:list[dict],key_points:list[int]):
        '''获取关键点名字列表'''
        point_names:list[str]=[]
        for index in key_points:
            # name = Utils.list_get_data(name_list,index)
            name,_ = Utils.list_info_get_data(name_info,index)
            if name is None:
                continue
            Utils.list_add(point_names,name)
        return   point_names

    # 获取关键点id列表
    def pose_get_point_ids(name_list:list[str],point_names:list[str]):
        '''获取关键点id列表'''
        point_ids:list[int]=[]
        for name in point_names:
            index = Utils.list_get_index(name_list,name)
            Utils.list_add(point_ids,index)
        return point_ids
    
    
    def segment(parent,data:dict,img_list:list[str],img_dir:str,save_dir:str,split_ratio=0.7):
        if not (isinstance(data,dict) and len(data)>0):
            return False
        if not os.path.exists(img_dir): 
            return False
        if not os.path.exists(save_dir): 
            return False
        if img_list is None or not len(img_list):
            return False
        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])

        
        data_list:list[dict]=[]
        for img_name in img_list:
            #提取单张图片的实例分割(SEGMENT)数据
            data_once = Export.segment_once(data,img_name,img_dir,name_info,group_info)
            if data_once is None or len(data_once) <=0: 
                continue
            data_list.append(data_once)
        
        length = len(data_list)
        if length<=0:
            return False
        
        #将训练集和验证集进行分割
        length_train = int(split_ratio * length)
        if length_train<1:
            length_train=1
        data_list_train = data_list[:length_train]
        data_list_val = data_list[length_train:]
        
        #保存训练集和验证集
        name_train="train"
        name_val="val"
        path_images=os.path.join(save_dir,"images")
        path_labels=os.path.join(save_dir,"labels")
        Export.dir_remake(path_images)
        Export.dir_remake(path_labels)
        index = Export.save_date_set(data_list_train,path_images,path_labels,name_train) 
        Export.save_date_set(data_list_val,path_images,path_labels,name_val)
        
        #构建yaml文件
        path_yaml = os.path.join(save_dir,"seg.yaml")
        data_yaml = Export.segment_build_yaml(name_info)
        save_yaml={}
        save_yaml['path']=save_dir
        save_yaml.update(data_yaml)
        Export.yaml_save(path_yaml,save_yaml)
        return index>0 
    
    def segment_build_yaml(name_info:list[dict]):
        data={}
        data["train"]   ="images/train"
        data["val"]     ="images/val"
        data["test"]    =None
        name_list,_ = Utils.list_info_unpack(name_info)
        names={}
        for i in range(len(name_list)):
            names[i]=name_list[i]
        data["names"]=names
        return data     
   
    def segment_once(data:dict,img_name:str,img_dir:str,name_info:list[dict],group_info:list[dict]):
        
        if not (isinstance(data,dict) and len(data)>0):
            return None
        img_path = os.path.join(img_dir,img_name)
        if not  os.path.exists(img_path):
            return None
        
        # 获取图像的宽高
        width=None
        height=None
        with Image.open(img_path) as image:
            width, height = image.size
        
        if width is None or height is None or width<=0 or height<=0:
            return None
        
        #读取形状数据列表
        img_data:dict = data.get(img_name,{})
        if not (isinstance(img_data,dict) and len(img_data)>0):
            return None
        shape_list = img_data.get("shape_list",[])
        #对数据进行处理,并获得归一化数据文本
        shape_list_find:list[Shape] = Export.shape_list_get_datas(shape_list,name_info,group_info,ShapeType.polygon)
        text_normale_list:list[str] = Export.polygon_normalization(shape_list_find,name_info,width,height,3)
        if text_normale_list is None or len(text_normale_list) <=0:
            return None
        text=""
        for text_normale in text_normale_list:
            text+=text_normale+"\n"
        
        data={}
        data["img_path"]    =img_path
        data["img_name"]    =img_name
        data["text"]        =text
        return data  

    
    def obb(parent,data:dict,img_list:list[str],img_dir:str,save_dir:str,split_ratio=0.7):
        if not (isinstance(data,dict) and len(data)>0):
            return False
        if not os.path.exists(img_dir): 
            return False
        if not os.path.exists(save_dir): 
            return False
        if img_list is None or not len(img_list):
            return False
        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])

        
        data_list:list[dict]=[]
        for img_name in img_list:
            #提取单张图片的定向边界框(OBB)数据
            data_once = Export.obb_once(data,img_name,img_dir,name_info,group_info)
            if data_once is None or len(data_once) <=0: 
                continue
            data_list.append(data_once)
        
        length = len(data_list)
        if length<=0:
            return False
        
        #将训练集和验证集进行分割
        length_train = int(split_ratio * length)
        if length_train<1:
            length_train=1
        data_list_train = data_list[:length_train]
        data_list_val = data_list[length_train:]
        
        #保存训练集和验证集
        name_train="train"
        name_val="val"
        path_images=os.path.join(save_dir,"images")
        path_labels=os.path.join(save_dir,"labels")
        Export.dir_remake(path_images)
        Export.dir_remake(path_labels)
        index = Export.save_date_set(data_list_train,path_images,path_labels,name_train) 
        Export.save_date_set(data_list_val,path_images,path_labels,name_val)
        
        #构建yaml文件
        path_yaml = os.path.join(save_dir,"obb.yaml")
        data_yaml = Export.obb_build_yaml(name_info)
        save_yaml={}
        save_yaml['path']=save_dir
        save_yaml.update(data_yaml)
        Export.yaml_save(path_yaml,save_yaml)
        return index>0 
    
    def obb_build_yaml(name_info:list[dict]):
        data={}
        data["train"]   ="images/train"
        data["val"]     ="images/val"
        data["test"]    =None
        name_list,_ = Utils.list_info_unpack(name_info)
        names={}
        for i in range(len(name_list)):
            names[i]=name_list[i]
        data["names"]=names
        return data
    
    def obb_once(data:dict,img_name:str,img_dir:str,name_info:list[dict],group_info:list[dict]):
        
        if not (isinstance(data,dict) and len(data)>0):
            return None
        img_path = os.path.join(img_dir,img_name)
        if not  os.path.exists(img_path):
            return None
        
        # 获取图像的宽高
        width=None
        height=None
        with Image.open(img_path) as image:
            width, height = image.size
        
        if width is None or height is None or width<=0 or height<=0:
            return None
        
        #读取形状数据列表
        img_data:dict = data.get(img_name,{})
        if not (isinstance(img_data,dict) and len(img_data)>0):
            return None
        shape_list = img_data.get("shape_list",[])
        #对数据进行处理,并获得归一化数据文本
        shape_list_find:list[Shape] = Export.shape_list_get_datas(shape_list,name_info,group_info,ShapeType.rotation)
        text_normale_list:list[str] = Export.polygon_normalization(shape_list_find,name_info,width,height,4)
        if text_normale_list is None or len(text_normale_list) <=0:
            return None
        text=""
        for text_normale in text_normale_list:
            text+=text_normale+"\n"
        
        data={}
        data["img_path"]    =img_path
        data["img_name"]    =img_name
        data["text"]        =text
        return data  
    
    
    def detect(parent,data:dict,img_list:list[str],img_dir:str,save_dir:str,split_ratio=0.7):
        if not (isinstance(data,dict) and len(data)>0):
            return False
        if not os.path.exists(img_dir): 
            return False
        if not os.path.exists(save_dir): 
            return False
        if img_list is None or not len(img_list):
            return False
        name_info:list[dict]  = data.get("name_info",[])
        group_info:list[dict] = data.get("group_info",[])

        
        data_list:list[dict]=[]
        for img_name in img_list:
            #提取单张图片的定向边界框(OBB)数据
            data_once = Export.detect_once(data,img_name,img_dir,name_info,group_info)
            if data_once is None or len(data_once) <=0: 
                continue
            data_list.append(data_once)
        
        length = len(data_list)
        if length<=0:
            return False
        
        #将训练集和验证集进行分割
        length_train = int(split_ratio * length)
        if length_train<1:
            length_train=1
        data_list_train = data_list[:length_train]
        data_list_val = data_list[length_train:]
        
        #保存训练集和验证集
        name_train="train"
        name_val="val"
        path_images=os.path.join(save_dir,"images")
        path_labels=os.path.join(save_dir,"labels")
        Export.dir_remake(path_images)
        Export.dir_remake(path_labels)
        index = Export.save_date_set(data_list_train,path_images,path_labels,name_train) 
        Export.save_date_set(data_list_val,path_images,path_labels,name_val)
        
        #构建yaml文件
        path_yaml = os.path.join(save_dir,"det.yaml")
        data_yaml = Export.obb_build_yaml(name_info)#矩形的配置和旋转框的通用
        save_yaml={}
        save_yaml['path']=save_dir
        save_yaml.update(data_yaml)
        Export.yaml_save(path_yaml,save_yaml)
        return index>0 
    
    
    def detect_once(data:dict,img_name:str,img_dir:str,name_info:list[dict],group_info:list[dict]):
        if not (isinstance(data,dict) and len(data)>0):
            return None
        img_path = os.path.join(img_dir,img_name)
        if not  os.path.exists(img_path):
            return None
        
        # 获取图像的宽高
        width=None
        height=None
        with Image.open(img_path) as image:
            width, height = image.size
        
        if width is None or height is None or width<=0 or height<=0:
            return None
        
        #读取形状数据列表
        img_data:dict = data.get(img_name,{})
        if not (isinstance(img_data,dict) and len(img_data)>0):
            return None
        shape_list = img_data.get("shape_list",[])
        #对数据进行处理,并获得归一化数据文本
        shape_list_find:list[Shape] = Export.shape_list_get_datas(shape_list,name_info,group_info,ShapeType.rectangle)
        text_normale_list:list[str] = Export.rect_normalization(shape_list_find,name_info,width,height)
        if text_normale_list is None or len(text_normale_list) <=0:
            return None
        text=""
        for text_normale in text_normale_list:
            text+=text_normale+"\n"
        
        data={}
        data["img_path"]    =img_path
        data["img_name"]    =img_name
        data["text"]        =text
        return data  
    
    
    
    
    
    def shape_list_get_datas(shape_list:list[dict],name_info:list[dict],group_info:list[dict],shape_type:ShapeType):
        shapes = shape_list_build(shape_list,name_info,group_info)
        #提取出所有多边形的数据
        shape_list_find:list[Shape]=[]
        for shape in shapes:
            if shape.shape_type not in [shape_type]:
                continue
            Utils.list_add(shape_list_find,shape)
        #最后返回数据
        return shape_list_find
    
    def polygon_normalization(shape_list_find:list[Shape],name_info:list[dict],width:int, height:int,check_num:int):
        '''对数据进行归一化处理,并返回结果文本数组'''
        # 多边形 数据集 归一化规则
        # 图片 w h
        # 标注 px/w  py/h
        # <class-index> <x1> <y1> <x2> <y2> ... <xn> <yn>
       
        text_normale_list:list[str] =[]
        if shape_list_find is None or len(shape_list_find) <=0:
            return text_normale_list
        for shape in shape_list_find:
            if shape is None:
                continue
            name_id:(int|None) = Utils.list_info_get_index(name_info,shape.name)
            if name_id is None:
                name_id = 0

            point_value_list = []
            for point in shape.points:
                lst=[]
                point_value:QPointF = Export.data_point_normalization(point,width,height)
                if point_value is  None:
                    continue
                lst=[point_value.x(),point_value.y()]
                point_value_list.append(lst)
            
            if len(point_value_list) <check_num:#四个点以上(起始正常应该==4)
                continue
            
            
            #将数据转为字符串
            text_normale = f"{name_id} "   
            for i in range(len(point_value_list)) :
                point_value = point_value_list[i]   
                text_normale += f"{point_value[0]:.6f} {point_value[1]:.6f}"  
                text_normale = text_normale + (" " if i != len(point_value_list)-1 else "")
                    
            text_normale_list.append(text_normale)  
        return text_normale_list 
    
    def rect_normalization(shape_list_find:list[Shape],name_info:list[dict],width:int, height:int):
        '''对数据进行归一化处理,并返回结果文本数组'''
        # 矩形 数据集 归一化规则
        # 图片 w h
        # 标注 px/w  py/h
        # class x_center y_center width height
       
        text_normale_list:list[str] =[]
        if shape_list_find is None or len(shape_list_find) <=0:
            return text_normale_list
        for shape in shape_list_find:
            if shape is None :
                continue
            name_id:(int|None) = Utils.list_info_get_index(name_info,shape.name)
            if name_id is None:
                name_id = 0

            min_point,max_point = get_min_max_point(shape.points)
            rect_value:QRectF = QRectF(min_point, max_point)
            rect_value = Export.data_rect_normalization(rect_value,width,height)
            if rect_value is None:
                #矩形框归一化失败,代表标注无效
                continue

            #将数据转为字符串
            text_normale = f"{name_id} {rect_value.x():.6f} {rect_value.y():.6f} {rect_value.width():.6f} {rect_value.height():.6f}"   
            text_normale_list.append(text_normale)  
        return text_normale_list
    
    # 矩形数据归一化        
    def data_rect_normalization(rect:QRectF,width:int, height:int):
        '''矩形数据归一化'''
        if rect is None or width<=0 or height<=0:
            return None
        topleft = rect.topLeft() 
        bottomRight = rect.bottomRight()
        if topleft.x()<0 :topleft.setX(0)
        if topleft.y()<0 :topleft.setY(0)
        if bottomRight.x()>width :bottomRight.setX(width)
        if bottomRight.y()>height :bottomRight.setY(height)
        if topleft.x() >= bottomRight.x() or topleft.y() >= bottomRight.y():
            return None
        w=bottomRight.x()-topleft.x()
        h=bottomRight.y()-topleft.y()
        x = topleft.x() + w/2
        y = topleft.y() + h/2
        
        rect_normal = QRectF(x/width,y/height,w/width,h/height)
        return rect_normal

    # Point点归一化
    def data_point_normalization(point:QPointF,width:int, height:int):
        '''Point点归一化'''
        if point is None or width<=0 or height<=0:
            return None
        x=point.x()
        y=point.y()
        if x<0 :x=0
        if y<0 :y=0
        if x>width :x=width
        if y>height :y=height
        point_normal = QPointF(x/width,y/height)
        return point_normal

    # 重新构建目录
    def dir_remake(path):
        '''重新构建目录'''
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        
    # 保存数据集
    def save_date_set(data_list:list[dict],path_images:str,path_labels:str,name:str):
        '''保存数据集'''
        cout=0
        for data in data_list:
            #data对应一张图片的标注数据
            if data is None or not len(data):
                continue
            img_path = data.get("img_path","")
            if not os.path.exists(img_path):
                continue
            file_name = os.path.basename(img_path)
            text_name = os.path.splitext(file_name)[0]
            # img_name=data.get("img_name","")
            text    =data.get("text","")
            save_path_images = os.path.join(path_images,name,file_name)
            save_path_labels = os.path.join(path_labels,name,text_name+".txt")
            os.makedirs(os.path.join(path_images,name),exist_ok=True)
            os.makedirs(os.path.join(path_labels,name),exist_ok=True)
            shutil.copy(img_path, save_path_images)
            with open(save_path_labels, 'w', encoding='utf-8') as file:
                # 将文本写入文件
                file.write(text)
                cout+=1
        return cout

    def yaml_save(file="data.yaml", data:dict=None, header:str=""):

        if data is None:
            data = {}
        file = Path(file)
        if not file.parent.exists():
            # 如果父路径不存在,则创建
            file.parent.mkdir(parents=True, exist_ok=True)

        # 将Path对象转换为字符串
        valid_types = int, float, str, bool, list, tuple, dict, type(None)
        for k, v in data.items():
            if not isinstance(v, valid_types):
                data[k] = str(v)

        # 将数据转储为YAML格式的文件
        with open(file, "w", errors="ignore", encoding="utf-8") as f:
            if header:
                f.write(header)
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,default_flow_style=None)


    def yaml_load(file="data.yaml"):
        assert Path(file).suffix in {".yaml", ".yml"}, f"无法载入 {file}"
        with open(file, errors="ignore", encoding="utf-8") as f:
            s = f.read()  
            # 删除不可打印字符
            if not s.isprintable():
                s = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+", "", s)

            data = yaml.safe_load(s) or {}  
            return data

       









#name_info=[
#       "人",
#       "狗",
#     "鼻子",
#     "左眼",
#     "右眼",
#     "嘴巴",
#     "脖子",
#     "左肩",
#     "右肩",
#     "左手",
#     "右手"
# ]

#point_list=[2,3,4,5,6,7,8,9,10]
#shape_list=[{name:2,point:[[100,100]]},{name:3,point:[[200,200]]}]   
    

#导出时生成一个临时的 name_list
# point_name=["鼻子","左眼","右眼","嘴巴","脖子","左肩","右肩","左手","右手"]
# (可以不用,直接在name_info匹配name_id也行)将shape_list.name_id 转name  例如 {name:2,point:[[100,100]]} -> {name:"鼻子",point:[[100,100]]}
# 之后开始处理数据
#1.找所有矩形框
#2.每找到1个框,判断是否有分组,遍历所有关键点,将(1.在此框范围内的点 或者2.相同分组的点)加入列表
#3.对于没有入框的点,在当前所有框中 找到最接近的框(按边线距离),并加入此框
#4.将框中的点按名字进行排序,如果有相同名字的点,则排查其他框,比如 框1有["鼻子","左眼","左眼","右眼"],框2有["鼻子","左眼","右眼"],并且框1的左眼1和框2的左眼是同一个点,则去掉框1的左眼1,
# (保证框2的左眼是唯一的,并且框1另外一个左眼不在框2中)否则只取第一个左眼
# 将排序后的框和框内点 进行归一化 导出txt和图片
# 导出时算法应该如下
# rect_points=[]
# for i in range(len(point_list)):
#   temp_point=None
#   for point in 框点_list:
#       if point.name_id  == point_list[i]:
#           temp_point=point
#           break
#   rect_points.append(temp_point)
#  最后rect_points 归一化,如果rect_points[n]==None  则 x=0,y=0,visible=0
    
    


















