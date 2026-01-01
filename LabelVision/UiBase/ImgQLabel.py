# -*- coding: utf-8 -*-
import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from enum import Enum

class ZoomType(Enum):
    zoom_in = 0     # 放大
    zoom_out = 1    # 缩小
    zoom_norm = 2   # 原始
    zoom_auto = 3   # 自动(自适应)




class ImgQLabel(QLabel):
    signal_mouseMove = Signal(dict)
    signal_imgZoom = Signal(dict)
    def __init__(self, img_path:str, parent:QWidget=None):
        super(ImgQLabel, self).__init__(parent)
        
        self.cross_pos = QPoint(0, 0)  # 交叉线的中心位置
       
        #添加自动滚动条控件(作为父frame)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)# 设置边距为0
        
        #添加布局控件
        self.lay = QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)# 设置边距为0
        self.lay.setSpacing(0)# 设置控件之间的间距为0
        self.lay.addWidget(self.scroll_area)#滚动条添加到布局控件

        
        
        
        # 加载图片,并且初始化各种类成员
        self.img_load(img_path)
        
        self.setMouseTracking(True)
        self._keyPressEvent = self.scroll_area.keyPressEvent
        self.scroll_area.keyPressEvent = self.keyPressEvent
        self._keyReleaseEvent = self.scroll_area.keyReleaseEvent
        self.scroll_area.keyReleaseEvent = self.keyReleaseEvent

        

     #加载图片,并且初始化各种成员   
    def img_load(self,img_path:str):
        '''加载图片,并且初始化各种成员'''
        self.is_valid = os.path.exists(img_path)  # 如果无效则不可操作
        self.img_path:str = img_path
        self.img_name:str = os.path.basename(img_path) if self.is_valid else ""
        self.img_dir:str  = os.path.dirname(img_path) if self.is_valid else ""
        self.pix = QPixmap(img_path) if self.is_valid else QPixmap(":/img/resources/imgs/app.png")
        self.scale_factor = 1.0
        self.setPixmap(self.pix)
        
        
        self.is_dragging = False        # 用于记录鼠标是否按下
        self.is_draged = False          # 用来判断是否有拖动图片行为
        self.pos_drag = QPoint()        # 用于记录鼠标按下的位置随着按下移动会更新
        self.pos_pressed = QPoint()     # 不更新,判断是否拖动了图片
        self.img_zoom(ZoomType.zoom_auto)
        self.update()
        
    #缩放图片
    def img_zoom(self, mode:ZoomType):
        if mode==ZoomType.zoom_in:
            # 放大
            self.scale_factor *= 1.1
        elif mode==ZoomType.zoom_out:
            # 缩小
            self.scale_factor /= 1.1
        elif mode==ZoomType.zoom_norm:
            self.scale_factor = 1.0
        elif mode==ZoomType.zoom_auto:
            self.scale_factor = self.get_auto_zoom_factor()
        
        self.scale_factor = max(0.1, min(self.scale_factor, 10))  # 限制缩放范围
        scaled_pixmap = self.pix.scaled(self.pix.size() * self.scale_factor,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        # 设置 QLabel 的对齐方式为居中
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPixmap(scaled_pixmap) 
        self.resize(scaled_pixmap.width(), scaled_pixmap.height())
        self.signal_imgZoom.emit({"scale":self.scale_factor})
    
    #获取自动缩放比例
    def get_auto_zoom_factor(self):
        # 获取 QLabel 的当前尺寸
        widget_size = self.scroll_area.size()
        # 计算 QPixmap 应该缩放到的尺寸，同时保持宽高比
        pix_size = self.pix.size()
        scale_factor_width = (widget_size.width()-8) / pix_size.width()
        scale_factor_height = (widget_size.height()-8)  / pix_size.height()
        scale_factor = min(scale_factor_width, scale_factor_height)  # 使用较小的比例因子来缩放
        return scale_factor
    
    #获取缩放因子
    def get_scale(self):
        '''获取缩放因子'''
        scale= self.scale_factor
        # print("scale",self.img_name,scale)
        return scale
    
    #获取图片矩形信息rect
    def get_rect(self) -> QRect:
        '''获取图片矩形信息rect'''
        size = self.pixmap().size()
        dif_size = super().size()  - size
        x = max(0,dif_size.width()/2)
        y = max(0,dif_size.height()/2)
        rect = QRect(int(x),int(y),size.width(),size.height())
        # print("rect",self.img_name,rect)
        return rect 
    
    #图片坐标转窗口坐标
    def posPix_to_posWidget(self,pos:QPoint) -> QPoint:
        '''图片坐标转窗口坐标'''
        rect = self.get_rect()
        x = max(0,pos.x()* self.scale_factor) 
        y = max(0,pos.y()* self.scale_factor) 
        x = rect.x() + x
        y = rect.y() + y
        if x>rect.right():x=rect.right()
        if y>rect.bottom():y=rect.bottom()
        pos = QPoint(int(x),int(y))
        return pos
    
    #窗口坐标转图片坐标
    def posWidget_to_posPix(self,pos:QPoint) -> QPoint:
        '''窗口坐标转图片坐标'''
        rect = self.get_rect()
        x=max(0,pos.x() - rect.x()) 
        y=max(0,pos.y() - rect.y()) 
        x=min(x/self.scale_factor,self.pix.width())
        y=min(y/self.scale_factor,self.pix.height())
        pos = QPoint(int(x),int(y))
        return pos
   
    #获取鼠标相对于图片的位置(窗口位置)
    def get_pos_mouse(self,pos:QPoint):
        '''获取鼠标相对于图片的位置(窗口位置)'''
        rect = self.get_rect()
        x = pos.x() - rect.x()
        y = pos.y() - rect.y()
        pos = QPoint(int(x),int(y))
        return pos
    
    #获取鼠标在图片上的坐标(图片位置)
    def get_pos_mouse_to_pix(self,pos:QPoint):
        """获取鼠标在图片上的坐标(图片位置)"""
        x=max(0,pos.x()) 
        y=max(0,pos.y()) 
        x=min(x/self.scale_factor,self.pix.width())
        y=min(y/self.scale_factor,self.pix.height())
        pos = QPoint(int(x),int(y))
        return pos
    
    #重载绘制事件
    def paintEvent(self, event):
        '''绘制重载'''
        super().paintEvent(event)
        if not self.is_valid:
            return
        
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 1, Qt.SolidLine)
        painter.setPen(pen)
 
        # 绘制水平线和垂直线
        painter.drawLine(0, self.cross_pos.y(), self.width(), self.cross_pos.y())
        painter.drawLine(self.cross_pos.x(), 0, self.cross_pos.x(), self.height())
        painter.end()
        
    #重载改变尺寸时间
    def resizeEvent(self, event:QResizeEvent):
        super().resizeEvent(event)
        # 重新设置图片大小以适应窗口大小
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        # print(event,self.get_pix_rect())    

    #重载鼠标滚轮事件
    def wheelEvent(self, event:QWheelEvent):
        mods = event.modifiers()
        # 检查 Ctrl 键是否被按下,按下不缩放(因为在子类中有用ctrl+滚轮调整倾斜角度)
        if mods & Qt.KeyboardModifier.ControlModifier or mods & Qt.KeyboardModifier.ShiftModifier:
            return
            
        delta = event.angleDelta()
        # 处理鼠标滚轮事件
        if delta.y() > 0:
            # 放大
            self.img_zoom(ZoomType.zoom_in)
        else:
            # 缩小
            self.img_zoom(ZoomType.zoom_out)
       
    #重载鼠标按钮按下事件
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            globalPos = event.globalPosition()
            self.pos_pressed = globalPos
            self.pos_drag = globalPos
            self.is_draged = False
            self.is_dragging = True
    
    #重载鼠标按钮释放事件
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            globalPos = event.globalPosition()
            pos_diff = self.pos_pressed - globalPos
            self.is_draged = abs(pos_diff.x())>10 or abs(pos_diff.y())>10
            self.is_dragging = False 
            
    #重载鼠标移动事件
    def mouseMoveEvent(self, event:QMouseEvent):
        pos:QPointF = event.position()
        # 更新交叉线的中心位置
        self.cross_pos = pos  
        # 触发重绘
        self.update()  
        
        #计算鼠标位置在图片的坐标(图片位置))
        pos = self.posWidget_to_posPix(pos)
        #发送信号给signal_mouseMove以便在状态栏显示
        self.signal_mouseMove.emit({"pos":pos})

        if not self.is_dragging:
            self.is_draged = False
            
        
        # 拖动图片处理
        if self.is_dragging:
            globalPos = event.globalPosition()
            
            # 计算拖动的距离
            drag_distance = globalPos - self.pos_drag
            
            # 获取滚动条的当前值
            h_bar_value = self.scroll_area.horizontalScrollBar().value()
            v_bar_value = self.scroll_area.verticalScrollBar().value()
            
            # 根据拖动距离更新滚动条位置
            new_h_value = h_bar_value - drag_distance.x()
            new_v_value = v_bar_value - drag_distance.y()
            
            # 设置新的滚动条位置
            self.scroll_area.horizontalScrollBar().setValue(new_h_value)
            self.scroll_area.verticalScrollBar().setValue(new_v_value)
            
            # 更新拖动开始位置为当前位置
            self.pos_drag = globalPos
    
    def keyPressEvent(self, event: QKeyEvent):
        self._keyPressEvent(event) 
        
    def keyReleaseEvent(self, event: QKeyEvent):
        self._keyReleaseEvent(event) 
        
        
            
        





















    