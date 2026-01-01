import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from enum import Enum
from math import sqrt
import math
from copy import deepcopy
import numpy as np



if __name__ == "__main__":
    from utils import Utils
else:
    from .utils import Utils


import imgviz 
LABEL_COLORMAP = imgviz.label_colormap()[2:]



class ShapeType(Enum):
    rectangle   = 0     # 矩形
    polygon     = 1     # 多边形
    point       = 2     # 关键点
    rotation    = 3     # 旋转矩形
    line        = 4     # 线条
    

class Shape():
    line_width = 2.0
    def __init__(self,shape_type:ShapeType,points:list[QPointF],color:QColor,rect:QRectF,scale:float,name:str="未命名",group:str="None",info:str=""):
        super().__init__()
        self.shape_type:ShapeType = shape_type          # 形状类型
        self.name:str = name                            # 标注名称
        self.group:str = group                          # 标注分组
        self.info:str = info                            # 标注描述信息
        self.angle:float=0.0                            # 旋转角度
        self.points:list[QPointF] = points              # 坐标(基于图像)
        
        
        self.color:QColor = color                       # 颜色
        self._rect:QRectF = rect                        # 基于图片的矩形信息
        self._scale:float = scale                       # 基于图片的缩放银子
        self.points_widget:list[QPointF] = self.points_to_widget()      #坐标(基于窗口)
        
        self.shape_pointed:bool = False                 # 鼠标指向形状
        self.vertex_pointed:int=None                    # 鼠标指向顶点
        self.created:bool = False                       # 是否创建完毕(多边形闭口)
        self.pos_current:QPointF=None                   # 当前鼠标位置(多边形创建时临时显示)
        self.is_visible:bool = True                     # 是否显示形状
        self.is_show_name:bool=True                     # 是否显示名称
        self.is_show_group:bool=True                    # 是否显示分组
        self.is_show_info:bool =True                    # 是否显示描述
        self.isChecked=False                            # 是否被选中的
        self.key_point_visibility = 2                   # 关键点专用,是否显示
        self.set_info(info)

    
  
        
    #获取形状数据,转为字典,方便转换成josn进行存储
    def get_data(self,name_info:list[dict]=None,group_info:list[dict]=None):
        '''获取形状数据,转为字典,方便转换成josn进行存储'''
        
        name_id,group_id=get_name_group_index(self.name,self.group,name_info,group_info)
        
        data={}
        data["shape_type"]= self.shape_type.value
        data["name_id"]= name_id 
        data["group_id"]= group_id 
        data["info"]= self.info 
        data["angle"]= self.angle 
        data["points"]= [(round(p.x()), round(p.y())) for p in self.points]
        return data
    
    #加载形状数据,自动解析标注名称和分组,设置颜色,转换窗口坐标等
    def load_data(self, data: dict, rect:QRectF,scale:float,name_info:list[dict]=None,group_info:list[dict]=None,created=True):
        '''加载形状数据,自动解析标注名称和分组,设置颜色,转换窗口坐标等'''

        self.shape_type = ShapeType(data.get("shape_type", 0))
        self.name ,self.group= get_name_group_str(data,name_info,group_info)
        self.info = data.get("info")
        self.angle = data.get("angle", 0.0)
        self.points = [QPointF(p[0], p[1]) for p in data["points"]]
                      
        self._rect = rect                        
        self._scale = scale                       
        self.points_widget = self.points_to_widget() 
        self.created = created
        
        name_id,group_id = get_name_group_index(self.name,self.group,name_info,group_info)
        
        color=QColor()
        _,color=Utils.list_info_get_data(group_info,group_id)
        if color is None or color == QColor():
            _,color=Utils.list_info_get_data(name_info,name_id)
        if color is None or color == QColor():
            color=get_color(name_id)  
        
        self.color = color  #QColor(color.red(),color.green(),color.blue())
        
        return self
 
    #进行绘制(线框/填充背景/文本)
    def paint(self, painter: QPainter): 
        if not self.is_visible and not self.isChecked:
            return
        
        points_len=len(self.points_widget)
        if points_len<=0:
            painter.end()
            return
        alpha=self.color.alpha()
        #设置颜色和画笔
        color = self.color
        pen = QPen(color)
        pen.setWidth(max(1, int(round(self.line_width * self._scale))))
        painter.setPen(pen)
        
        
        
        #设置线框和顶点路径
        line_path = QPainterPath()
        vrtx_path = QPainterPath()
        
        
        if self.shape_type in [ShapeType.rectangle,ShapeType.rotation]:
            #矩形或者旋转框
            if  points_len == 4:
                line_path.moveTo(self.points_widget[0])
                for i, p in enumerate(self.points_widget):
                    line_path.lineTo(p)
                    if self.shape_pointed or self.isChecked:
                        self.draw_vertex(vrtx_path, i)
                line_path.lineTo(self.points_widget[0])
        elif self.shape_type in [ShapeType.point]:
            #关键点
            if points_len == 1:
                self.draw_vertex(vrtx_path, 0)
        else:
            #其余默认以多边形进行绘制
            line_path.moveTo(self.points_widget[0])
            for i, p in enumerate(self.points_widget):
                line_path.lineTo(p)
                if self.shape_pointed  or not self.created or self.isChecked or self.shape_type in [ShapeType.line]:
                    self.draw_vertex(vrtx_path, i)
            #是否闭口
            if self.created:
                self.pos_current=None
                self.draw_vertex(vrtx_path, 0)
                if self.shape_type not in [ShapeType.line]:
                    line_path.lineTo(self.points_widget[0])
            else:
                #没有闭口跟随当前鼠标进行画线
                if self.pos_current is not None:
                    line_path.lineTo(self.posPix_to_posWidget(self.pos_current,self._rect, self._scale))
                #填充颜色,透明度90    
                color_edit=QColor(color.red(),color.green(),color.blue(),90)
                painter.fillPath(line_path, color_edit)
            
        #将鼠标指向的顶点进行高亮显示    
        self.draw_vertex_pointed(painter,color,self.vertex_pointed)         
        
        if self.isChecked:
            #被选中则描白色边
            pen_ = QPen(QColor(255,255,255,255))
            pen_.setWidth(pen.width()*2)
            painter.setPen(pen_)
            
            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.setPen(pen)

        #绘制线框和顶点
        painter.drawPath(line_path)
        painter.drawPath(vrtx_path)

        painter.fillPath(vrtx_path, color)
        
        if self.shape_pointed or self.isChecked:
            #填充蒙版
            color.setAlpha(90)
            painter.fillPath(line_path, color)
            color.setAlpha(alpha)
            

        #文本处理
        text =   f"{self.name}  " if self.name and self.is_show_name else ""
        text +=  f"[{self.group}]" if self.group and self.is_show_group else ""
        #绘制文本
        self.draw_text(painter,text,row=0,is_rect=True)
        
        #信息处理,可以绘制带换行符的文本
        text =  f"{self.info}" if self.info and self.is_show_info else ""
        lines = text.split('\n')
        for i in range(len(lines)):
            self.draw_text(painter,lines[i],row=i+1,is_rect=False)
        
        #旋转框则在中心区域显示旋转度数
        if self.shape_type  in [ShapeType.rotation]:
            text =  f" {int(self.angle)}° " 
            self.draw_text(painter,text,row=None,is_rect=True)

    #绘制文本
    def draw_text(self,painter:QPainter,text:str,is_rect:bool=True,row:int=None):
        '''绘制文本内容'''
        if not text:
            return
        alpha=self.color.alpha()
        color = self.color

        #根据行号进行文本位置处理
        if row is not None:
            center = self.get_min_point(self.points_widget)
        else:
            #如果row为None,显示在中心位置
            center = self.get_center(False)
        
        #设置画笔字体
        font = QFont("Arial", int(max(10, int(round(8.0 * self._scale)))),8)
        font.setBold(True)
        painter.setFont(font)
        
        #根据字体和中心位置计算文本位置和背景框矩形
        pos,rect = get_font_pos_and_rect(font,center,text)
        
        #根据row处理背景框和文本位置
        if row is not None:
            height = rect.height()* row
            pos.setY(pos.y()+height)
            rect.setTop(rect.top()+height)
        else:
            diff = pos - rect.topLeft()
            rect = QRectF(center.x()-rect.width()/2,center.y()-rect.height()/2,rect.width(),rect.height())
            pos = rect.topLeft()+diff
        
        if is_rect:
            # 绘制背景
            color.setAlpha(120)
            painter.fillRect(rect, color)
            color.setAlpha(alpha)
        
        
        if not is_rect:
            #如果没有背景框,则绘制描边文字
            pen = QPen(QColor(0,0,0), 8, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawText(pos, text)
            pos += QPointF(2, 2)
            painter.drawText(pos, text)
        
        pen = QPen(QColor(255,255,255), 8, Qt.SolidLine)
        painter.setPen(pen)
        pos += QPointF(-1, -1)
        painter.drawText(pos, text) 

    #绘制鼠标指向的顶点
    def draw_vertex_pointed(self, painter:QPainter, color:QColor,index:int) -> QPointF: 
        '''绘制鼠标指向的顶点'''
        if index is  None or index >= len(self.points_widget): 
            return  
        if self.shape_type in [ShapeType.rectangle,ShapeType.rotation,ShapeType.point]:
            length=4
        else:
            length=8 if not self.created else 4
        
        path = QPainterPath()
        color_back = color
        self.draw_vertex(path, index,length=length,v_shape=1)
        painter.fillPath(path, color_back)
        color_front = QColor(255,255,255,188)
        self.draw_vertex(path, index,length=6,v_shape=1)
        painter.fillPath(path, color_front)
    
    #绘制普通顶点  
    def draw_vertex(self, path:QPainterPath, i:int,v_shape=None,length=4):
        """绘制普通顶点"""
        if i == self.vertex_pointed:
            v_shape = 1
            
        d = length * self._scale
        point = self.points_widget[i]
        if v_shape is None:
            path.addEllipse(point, d , d )
        else:
            path.addRect(point.x() - d*1.5 , point.y() - d *1.5, d*3, d*3)

    #获取中心位置
    def get_center(self,is_pix=True)->QPointF:
        '''获取中心位置'''
        x = 0
        y = 0
        if is_pix:
            points=self.points
        else:
            points=self.points_widget
        if len(points)==4:
            point_min , point_max = (points[0],points[2])
        else:
            point_min , point_max = get_min_max_point(points)
            
        x=(point_min.x() + point_max.x()) /2 
        y=(point_min.y() + point_max.y()) /2
        center=QPointF(x,y)
        return center
    
    #获取最小坐标
    def get_min_point(self,points:list[QPointF]):
        '''获取最小坐标'''
        point_min , point_max = get_min_max_point(points)
        return point_min
    
    #获取或者设置图片rect
    def rect(self,rect:QRectF=None):
        '''获取或者设置图片rect'''
        if rect==None: 
            return self._rect
        self._rect = rect
        
        return self._rect
    
    #获取或者设置缩放因子
    def scale(self,scale:float=None):
        '''获取或者设置缩放因子'''
        if scale==None: 
            return self._scale
        self._scale = scale
        return self._scale
    
    #更新图片坐标为窗口坐标
    def update_points_widget(self):
        '''更新图片坐标为窗口坐标'''
        self.points_widget = self.points_to_widget()
    
    #图片坐标转窗口坐标'
    def points_to_widget(self)->list[QPointF]:
        '''图片坐标转窗口坐标'''
        lst= [self.posPix_to_posWidget(p, self._rect, self._scale) for p in self.points]
        return lst
    
    #根据图片rect和缩放因子,图片坐标转窗口坐标
    def posPix_to_posWidget(self,pos:QPointF,rect:QRect,scale:float) -> QPointF:
        '''根据图片rect和缩放因子,图片坐标转窗口坐标'''
        x = max(0,pos.x()* scale) 
        y = max(0,pos.y()* scale) 
        x = rect.x() + x
        y = rect.y() + y
        if x>rect.right():x=rect.right()
        if y>rect.bottom():y=rect.bottom()
        pos = QPointF(x,y)
        return pos   
    
    #更新图片坐标
    def update_points_pix(self):
        '''更新图片坐标'''
        self.points = self.points_to_pix()
    
    #窗口坐标转图片坐标
    def points_to_pix(self)->list[QPointF]:
        '''窗口坐标转图片坐标'''
        lst = [self.posWidget_to_posPix(p,self._rect,self._scale) for p in self.points_widget]
        return lst
    
    #根据图片rect和缩放因子,窗口坐标转图片坐标
    def posWidget_to_posPix(self,pos:QPointF,rect:QRectF,scale:float) -> QPointF:
        '''根据图片rect和缩放因子,窗口坐标转图片坐标'''
        size:QSize = rect.size()/self._scale
        x=max(0,pos.x() - rect.x()) 
        y=max(0,pos.y() - rect.y()) 
        x=min(x/scale,size.width())
        y=min(y/scale,size.height())
        pos = QPointF(x,y)
        return pos 

    #旋转矩形
    def rotate_rect(self,angle:float):
        '''旋转矩形'''
        if self.shape_type not in [ShapeType.rotation]: 
            return
        
        length = len(self.points)
        
        if length != 4: 
            return
        
        #取中心点位置
        center = self.get_center()
        # center = self.posPix_to_posWidget(center,self._rect, self._scale)
        lst = []
        for i in range(length):
            pos = self.points[i]
            #根据图片坐标和中心点,计算旋转后的坐标位置
            pos = rotate_point(pos, center, angle%360)
            # self.points[i]=pos
            #转为窗口坐标
            pos = self.posPix_to_posWidget(pos,self._rect, self._scale)
            lst.append(pos)
        if len(lst):
            #更新窗口坐标,以及更新图片坐标
            self.points_widget = lst
            self.update_points_pix()
        self.angle += angle
        self.angle %= 360
        # print("rotate",self.angle)
    
    #检查点是否在多边形内
    def is_point_in_shape(self, point:QPointF):
        """检查点是否在多边形内"""
        path = QPainterPath(self.points_widget[0])
        for p in self.points_widget[1:]:
            path.lineTo(p)
        is_in = path.contains(point)
        return is_in
    
    #设置形状是否被指向
    def set_shape_pointed(self,shape_pointed:bool):
        self.shape_pointed = shape_pointed

    #按偏移量移动所有点
    def move_offset_widget(self, offset:QPointF):
        """按偏移量移动所有点"""
        # length = len(self.points_widget)  
        # for i in range(length):
        #     pos:QPoint = self.points_widget[i] + offset
        #     if pos.x()<self._rect.left() or pos.y()<self._rect.top():
        #         return
        #     if pos.x()>self._rect.right() or pos.y()>self._rect.bottom():
        #         return
        offset = self.fix_offset_widget(offset)
        self.points_widget = [p + offset for p in self.points_widget] 

    #修复窗口坐标偏移量
    def fix_offset_widget(self, offset:QPointF):
        '''修复窗口坐标偏移量'''
        length = len(self.points_widget)
        for i in range(length):
            offset = self.fix_offset_vertex(i,offset)
        return offset

    # 按偏移量移动特定顶点
    def move_offset_vertex(self, i, offset:QPointF):
        """按偏移量移动特定顶点"""
        offset=self.fix_offset_vertex(i,offset)
        self.points_widget[i] += offset   
    
    # 修复顶点坐标偏移量
    def fix_offset_vertex(self,i,offset:QPointF):
        '''修复顶点坐标偏移量'''
        pos:QPointF= self.points_widget[i] + offset
        fix_x = pos.x() - self._rect.left()
        fix_y = pos.y() - self._rect.top()
        if fix_x<0:
            offset.setX(offset.x()-fix_x)
        if fix_y<0:
            offset.setY(offset.y()-fix_y)
        pos:QPointF= self.points_widget[i] + offset
        fix_x = pos.x() - self._rect.right()
        fix_y = pos.y() - self._rect.bottom()
        if fix_x>0:
            offset.setX(offset.x()-fix_x)
        if fix_y>0:
            offset.setY(offset.y()-fix_y)
        return offset

    #找到离点最近的顶点的索引
    def nearest_vertex(self, point:QPointF, distance:float):
        """找到离点最近的顶点的索引
        仅考虑距离是否小于distance
        """
        min_distance = float("inf")
        index = None
        for i, p in enumerate(self.points):
            offset:QPointF = p - point
            dist = sqrt(offset.x() * offset.x() + offset.y() * offset.y())
            if  dist < min_distance:
                min_distance = dist
                if dist <= distance:
                    # print(f"nearest_vertex:{i}->{dist}->{distance}")
                    index = i
        return index
    
    #获取最近边索引
    def nearest_edge(self, point:QPointF, distance:float):
        """获取最近边索引"""
        length = len(self.points)
        if length < 2:
            return None
        min_distance = float("inf")
        post_i = None
        for i in range(len(self.points)):
            line = [self.points[i - 1], self.points[i]]
            dist = distance_to_line(point, line)
            if dist <= distance and dist < min_distance:
                min_distance = dist
                post_i = i
        return post_i
    
    #设置被鼠标指向的顶点索引(高亮显示顶点)
    def set_vertex_pointed(self, index:int, action=None):
        """设置被鼠标指向的顶点索引(高亮显示顶点)

        参数:
            i (int): 顶点索引
        """
        self.vertex_pointed = index
    
    #在特定索引中插入一个点
    def insert_point(self, i:int, point:QPointF):
        """在特定索引中插入一个点"""
        if self.shape_type  in [ShapeType.rectangle,ShapeType.rotation,ShapeType.point]:
            return False
        self.points.insert(i, point)
        return True

    #从特定索引中删除点"
    def remove_point(self, index:int):
        """从特定索引中删除点"""
        if self.shape_type in [ShapeType.rectangle,ShapeType.rotation,ShapeType.point]:
            return False
        if len(self.points)<=3 and self.shape_type not in [ShapeType.line]:
            return False
        if  index>=len(self.points): 
            return False
        
        self.points.pop(index)
        return True

    # 设置标注描述信息,默认为形状类型
    def set_info(self,info:str=""):
        '''设置标注描述信息,默认为形状类型'''
        if not info:
            if self.shape_type in [ShapeType.rectangle]:
                self.info="矩形"
            elif self.shape_type in [ShapeType.rotation]:
                self.info="旋转框"
            elif self.shape_type in [ShapeType.point]:
                self.info="关键点"
            elif self.shape_type in [ShapeType.line]:
                self.info="线条"
            else:
                self.info="多边形"
            return  
        self.info=info
    
    def copy(self):
        """复制形状"""
        return deepcopy(self)


def shape_list_build(shape_list:list[dict],name_info:list[dict],group_info:list[dict],rect:QRectF=QRectF(),scale:float=1.0):
    shapes:list[Shape] = []
    if shape_list is None:
        return shapes
    for data in shape_list:
        if len(data)<=0 or not isinstance(data,dict):
            continue
        name_id  = data.get("name_id",None)
        if name_id is None:
            continue
        shape = Shape(ShapeType.point,[QPointF()],QColor(),rect,scale)
        shape = shape.load_data(data,rect=rect,scale=scale,name_info=name_info,group_info=group_info)
        shapes.append(shape)
    return shapes


def shape_type_dict():
    # rectangle   = 0     # 矩形
    # polygon     = 1     # 多边形
    # point       = 2     # 关键点
    # rotation    = 3     # 旋转矩形
    # line        = 4     # 线条
    type_dict={}
    type_dict["rectangle"]=ShapeType.rectangle
    type_dict["polygon"]=ShapeType.polygon
    type_dict["point"]=ShapeType.point
    type_dict["rotation"]=ShapeType.rotation
    type_dict["line"]=ShapeType.line
    return type_dict


    



#根据顶点列表计算最大和最小的坐标,取最小/大的x值和y值,例如:(0,100),(5,10) 结果最小为(0,10)最大为(5,100)
def get_min_max_point(points:list[QPointF]): 
    '''根据顶点列表计算最大和最小的坐标,取最小/大的x值和y值,例如:(0,100),(5,10) 结果最小为(0,10)最大为(5,100)'''   
    min_x=float('inf')
    min_y=float('inf')
    max_x=float("-inf")
    max_y=float("-inf")
    length = len(points)
    for i in range(length):
        pos = points[i]
        min_x = min(pos.x(),min_x)
        min_y = min(pos.y(),min_y)
        max_x = max(pos.x(),max_x)
        max_y = max(pos.y(),max_y)
        
    min_point=QPointF(min_x,min_y)
    max_point=QPointF(max_x,max_y)
    
    return min_point, max_point

#生成矩形坐标列表(图片坐标)
def make_rect_points(points:list[QPointF]) :
    """生成矩形坐标列表(图片坐标)"""
    min_point,max_point = get_min_max_point(points)
    rect = QRectF(min_point, max_point)
    top_left = rect.topLeft()
    top_right = rect.topRight()
    bottom_left = rect.bottomLeft()
    bottom_right = rect.bottomRight()
    return [top_left,top_right,bottom_right,bottom_left]

def make_line_list_from_points(points:list[QPointF]):
    """生成线条坐标列表"""
    line_list:list[list[QPointF]]=[]
    for i in range(len(points)):
        point1 = points[i]
        point2 = points[(i + 1) % len(points)]
        line:list[QPointF]=[point1,point2]
        line_list.append(line)
    return line_list

#两个坐标是否在一个距离内
def point_is_near( point1:QPointF, point2:QPointF,distance:float):
    """两个坐标是否在一个距离内"""
    offset:QPointF = point1 - point2
    dist = sqrt(offset.x() * offset.x() + offset.y() * offset.y())
    if dist <= distance:
        return True
    return False
# 计算点到线段的最短距离
def distance_to_line(point:QPointF, line:list[QPointF]):
    """
    计算点到线段的最短距离。
    """
    distance = float("inf")
    if len(line)!=2: 
        return distance
    p1, p2 = line
    
    # 将输入转换为 NumPy 数组
    point_np = np.array([point.x(), point.y()])
    start = np.array([p1.x(), p1.y()])
    end = np.array([p2.x(), p2.y()])
    
    # 计算线段向量
    line_vec = end - start
    
    # 计算点到线段起点的向量
    vec_to_point = point_np - start
    
    # 计算点积以确定投影比例
    proj_len = np.dot(vec_to_point, line_vec) / np.dot(line_vec, line_vec)
    
    # 确保投影点在线段上
    if proj_len < 0:
        proj_len = 0  # 投影点在起点
    elif proj_len > 1:
        proj_len = 1  # 投影点在终点
    
    # 计算投影点的坐标
    projection = start + proj_len * line_vec
    
    # 计算点到投影点的距离
    distance = np.linalg.norm(point_np - projection)
    
    return distance

# 计算点到多边形的最短距离
def distance_to_edge(point:QPointF, points:list[QPointF]):
    '''计算点到多边形的最短距离'''
    min_distance = float("inf")
    length = len(points)
    if length < 2:
        return min_distance
    for i in range(length):
        line = [points[i - 1], points[i]]
        dist = distance_to_line(point, line)
        if  dist < min_distance:
            min_distance = dist
    return min_distance

#一个点围绕中心点转多少度,取其旋转后的坐标位置
def rotate_point(point:QPointF, point_center:QPointF, angle_deg:float):
    '''一个点围绕中心点转多少度,取其旋转后的坐标位置'''
    angle_radians = math.radians(angle_deg)
    original_x = point.x()
    original_y = point.y()
    center_x = point_center.x()
    center_y = point_center.y()
    new_x = center_x + (original_x - center_x) * math.cos(angle_radians) - (original_y - center_y) * math.sin(angle_radians)
    new_y = center_y + (original_x - center_x) * math.sin(angle_radians) + (original_y - center_y) * math.cos(angle_radians)
    point=QPointF(new_x, new_y)
    return point

#获取字体的位置和矩形
def get_font_pos_and_rect(font:QFont,center:QPointF,text:str):
    '''获取字体的位置和矩形'''
    fm = QFontMetrics(font)
    bound_rect = fm.boundingRect(text)
    rect = QRectF(
                    center.x(),
                    center.y(),
                    bound_rect.width()  + font.pointSize(),
                    bound_rect.height() + bound_rect.height()//2,
                    )
    pos = QPointF(
        center.x() + font.pointSize()//2,
        center.y() + bound_rect.height(),
        )
    return pos,rect

#获取形状的颜色
def get_color(index:int,alpha:int=None):
    '''获取形状的颜色'''
    group_color = LABEL_COLORMAP[index % len(LABEL_COLORMAP)]
    color = QColor(*group_color)
    if alpha  is not None:
        color.setAlpha(alpha)
    return  color

def draw_line(painter: QPainter,points:list[QPointF],color:QColor,line_width:float,scale:float):
    if painter is None or len(points)<2:
        return
    line_path = QPainterPath()
    line_path.moveTo(points[0])
    for p in points:
        line_path.lineTo(p)
    
    pen = QPen(color)
    pen.setWidth(max(1, int(round(line_width * scale))))
    # pen_ = QPen(QColor(255,255,255,color.alpha()*1.2))
    # pen_.setWidth(pen.width()*1.5)
    
    # painter.setPen(pen_)
    # painter.drawPath(line_path)
    
    painter.setPen(pen)
    painter.drawPath(line_path)



#根据名称列表和分组列表,取出对应的名字和分组索引
def get_name_group_index(name:str,group:str,name_info:list[dict]=None,group_info:list[dict]=None):
    '''根据名称列表和分组列表,取出对应的名字和分组索引'''
    name_id:(int|None) = Utils.list_info_get_index(name_info,name)
    group_id:(int|None) = Utils.list_info_get_index(group_info,group)
 
    return name_id,group_id


#解析数据中提取出标注名称和分组
def get_name_group_str(data:dict,name_info:list[dict]=None,group_info:list[dict]=None):
    '''解析数据中提取出标注名称和分组'''
    name=""
    group=""
    name_id  = data.get("name_id",None)
    group_id = data.get("group_id",None)
    name,group =get_name_group(name_id,group_id,name_info,group_info)
    return name,group

def get_name_group(name_id,group_id,name_info:list[dict]=None,group_info:list[dict]=None):
    name=""
    group=""
    if name_id is not None and name_info is not None:
        name,_ = Utils.list_info_get_data(name_info,name_id)

    
    if group_id is not None and group_info is not None:
        group,_ = Utils.list_info_get_data(group_info,group_id)
    return name,group






















