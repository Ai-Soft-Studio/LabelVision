import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import traceback

from copy import deepcopy
from enum import Enum

if __name__ == "__main__":
    from ImgQLabel import ImgQLabel,ZoomType
    from Shape import Shape,ShapeType,make_rect_points,point_is_near,LABEL_COLORMAP,get_color,get_name_group_index,get_name_group,draw_line,shape_list_build,shape_type_dict
    from utils import Utils
else:
    from .ImgQLabel import ImgQLabel,ZoomType
    from .Shape import Shape,ShapeType,make_rect_points,point_is_near,LABEL_COLORMAP,get_color,get_name_group_index,get_name_group,draw_line,shape_list_build,shape_type_dict
    from .utils import Utils



class MouseState(Enum):
    normal = 0              # 未有状态
    drag = 1                # 拖动图片
    pointed = 2             # 指向对象
    selected = 3            # 选中对象
    has_rotate=4            # 选中对象中有旋转框 
    line_link=5            # 选中对象可以连线
    line_unlink=6          # 选中对象可以断连

class ImgCanvas(ImgQLabel):
    signal_shape_created    = Signal(dict)
    signal_shape_checked    = Signal(dict)
    signal_shape_updated    = Signal(dict)
    shape_supported = [
                        ShapeType.rectangle,    # 矩形
                        ShapeType.polygon,      # 多边形
                        ShapeType.point,        # 关键点
                        ShapeType.rotation,     # 旋转框
                        ShapeType.line,         # 线条
                      ]
    def __init__(self,image_path,parent=None):
        super(ImgCanvas, self).__init__(image_path,parent)
        self.shape_type = ShapeType.line            # 当前创建的形状类型
        self.is_show_name:bool=True                 # 是否显示标签
        self.is_show_group:bool=True                # 是否显示分组
        self.is_show_info:bool =True                # 是否显示信息
        
        self.line_rule:list[list[int]]=[]           # 规则_线条连接
        self.name_info:list[dict]=[]                # 存储标记名称
        self.group_info:list[dict]=[]               # 存储标记分组
        self.key_points:list[int]=[]                # 存储关键点
        self.init_canvas()
        super().signal_imgZoom.connect(self.signal_imgZoom_changed)
    #初始化程序,初始化画布流程的数据
    def init_canvas(self):
        '''初始化程序,初始化画布流程的数据'''
        self.shape_list:list[Shape] = []            # 存储绘制的形状
        self.shape_current:Shape = None             # 正在绘制的形状
        self.point_list:list[QPointF] = []          # 当前绘制的形状的顶点
        self.shape_checked:list[Shape] = []         # 存储选中的形状
        self.is_creating = False                    # 是否正在绘制形状
        self.is_moving = False                      # 是否正在移动
        self.mouse_state:MouseState=MouseState.normal  # 当前鼠标状态
        self.index_selected:int = None              # 被选中的形状索引
        self.index_vertexed:int = None              # 最近顶点的形状索引
        self.index_edge    :int = None              # 最近边的形状索引
        
        self.pos_move:QPointF = QPointF()           # 移动的坐标位置
        self.pos_last:QPointF = QPointF()           # 记录鼠标的最后位置
        
        self.shape_list_ctrl_z:list[dict]=[]        # 保存撤销时用
        self.shape_list_ctrl_y:list[dict]=[]        # 恢复撤销时用
        self.shape_is_store=True                    # 是否保存了形状数据(用来判断是否第一次恢复/撤销)
        self.backup_num = 10000                     # 保存的最大上限

        self.shape_copy_paste:list[Shape] = []      # 用来保存复制粘贴的形状
        self.pos_copy_paste:QPointF=QPointF()       # 记录复制时的位置

        self.line_list:list[list[int]]=[]           # 用来存储基于画线规则的关键点线条列表的列表(保存的是关键点在shape_list中的索引)
        self.shapes_store()
    

    #加载形状数据
    def load_shapes(self,shape_list:list[dict],name_info:list[dict],group_info:list[dict],key_points:list[int]):
        '''加载形状数据'''
        #shape_list:[{shape_type:shape_type,points:[[0,1],[],...]},{},...]
        self.set_shape_type(self.shape_type)
        self.shape_list.clear()
        self.name_info  = name_info
        self.group_info = group_info
        self.key_points = key_points
        rect  = super().get_rect()
        scale = super().get_scale()
        
        self.shape_list = shape_list_build(shape_list,name_info,group_info,rect,scale)

        self.update_normal()
        self.shape_list_ctrl_z:list[dict]=[]        # 保存撤销时用
        self.shape_list_ctrl_y:list[dict]=[]        # 恢复撤销时用
        self.shape_is_store = False                    # 是否保存了形状数据(用来判断是否第一次恢复/撤销)
        if len(self.line_rule):
            self.line_link_apply()
        self.shapes_store()
        # self.signal_shape_updated.emit({}) 
    
    #设置创建的形状类型
    def set_shape_type(self,shape_type:ShapeType):
        '''设置创建的形状类型'''
        if shape_type not in self.shape_supported :
            return
        self.shape_type = shape_type
        self.is_creating = False                    # 是否正在绘制多边形
        self.is_moving = False                      # 是否正在移动
        self.shape_current = None                   # 正在绘制的多边形
        self.point_list.clear()                     # 当前绘制的多边形的顶点
        self.index_selected = None                  # 被选中的形状索引
        self.index_vertexed = None                  # 最近顶点的形状索引
        self.index_edge     = None                  # 最近边的形状索引
        self.shape_checked.clear()                  # 点击选中的形状索引
        self.shape_copy_paste.clear()               # 用来保存复制粘贴的形状
    
              
   
    def paintEvent(self, event):
        '''重载绘制事件'''
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing,True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform,True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing,True)
        try:
            if self.is_creating :
                self.shape_checked.clear()
                
            length = len(self.shape_list)
            for i in range(length):
                if len(self.shape_checked) > 0 and self.shape_list[i] in self.shape_checked:
                    self.shape_list[i].isChecked = True
                else:
                    self.shape_list[i].isChecked = False
                self.shape_list[i].is_show_group = self.is_show_group 
                self.shape_list[i].is_show_name = self.is_show_name 
                self.shape_list[i].is_show_info  = self.is_show_info 
                self.shape_list[i].paint(painter)
                
            if self.is_creating and self.shape_current is not None:
                self.shape_current.is_show_group=True
                self.shape_current.is_show_name=True
                self.shape_current.is_show_info=True
                self.shape_current.paint(painter)
            
            #绘制基于规则的线条(关键点连线)    
            self.draw_rulu_line(painter)
        except Exception as e:
            print(e)
            traceback.print_exc()
        
        painter.end()
     
    #形状创建完成
    def shape_created(self, shape:Shape,is_emit:bool=True):
        '''形状创建完成'''
        if not self.is_valid:
            return
        if shape not in self.shape_list:
            self.shape_list.append(shape)
        data = {
            "shape":self.shape_list[-1],
            "index":len(self.shape_list)-1
            }

        self.update()
        self.shapes_store()
        if is_emit:
            self.signal_shape_created.emit(data)
    
    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if not self.is_valid :
            return
        
        pos_event = event.position()
        if self.is_pos_out_img(pos_event):
            return
        
        
        #按住CTRL/ALT键进入强制编辑模式,可以新建形状
        is_edit = self.is_editing(event)
        is_select = self.is_selecting(event)
        if event.button() == Qt.LeftButton:
            pos = self.pos_to_pix_pos(pos_event)
            if not is_select:
                self.shape_checked.clear()
            if (self.index_selected is None and self.index_vertexed is None and self.index_edge is None) or is_edit:
                if self.shape_type   in [ShapeType.rectangle,ShapeType.rotation]:
                    # 创建矩形和旋转框
                    self.is_creating = True
                    self.point_list = []
                    self.point_list.append(pos)
                    return  
                return

            if self.index_edge is not None and self.index_vertexed is None and not is_select:
                
                # 点击最近边线条
                if self.vertex_add(pos):
                    # 如果是多边形并且新增一个顶点成功
                    self.update_normal()
                    self.update()
                    self.shapes_store()
                    # return
            
            if self.index_selected is not None or self.index_vertexed is not None:
                # 是否选择了形状或者顶点,记录全局鼠标用来判断移动位置
                globalPos = event.globalPosition()
                self.pos_move = globalPos
                # 开始移动形状或顶点
                if not is_edit:
                    self.is_moving = True
                    self.set_cursor(Qt.CursorShape.ClosedHandCursor)
                    shape = self.get_shape_by_index(self.index_selected)
                    self.shape_checked_add(shape,is_select,is_remove_existing=(self.index_vertexed is None or shape.shape_type in [ShapeType.point,ShapeType.line]))
                    
                else:
                    self.is_moving = False
                return
             
    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        
        if not self.is_valid :
            return
        
        self.mouse_state_update()
        is_edit = self.is_editing(event)
        is_select = self.is_selecting(event)
        pos_event = event.position()
        if event.button() == Qt.LeftButton:
            pos = self.pos_to_pix_pos(pos_event)
            if (self.index_selected is None and self.index_vertexed is None and self.index_edge is None) or is_edit:
                if self.shape_type   in [ShapeType.rectangle,ShapeType.rotation]:
                    # 创建矩形和旋转框
                    if self.is_creating:
                        #如果正在创建,这里只有矩形和旋转框需要用释放鼠标方式进行创建
                        
                        #创建结束
                        self.is_creating = False
                        diff=self.point_list[0]-pos
                        if abs(diff.x())<10 and abs(diff.y())<10:
                            self.shape_current=None
                            self.point_list.clear()
                            return
                            
                        if abs(diff.x())<10:
                            pos.setX(pos.x()+10)
                        if abs(diff.y())<10:
                            pos.setY(pos.y()+10)
                            
                        points = make_rect_points([self.point_list[0],pos])
                        group_color = LABEL_COLORMAP[len(self.shape_list) % len(LABEL_COLORMAP)]
                        color = QColor(*group_color)
                        shape = Shape(self.shape_type,points,color,super().get_rect(),super().get_scale())
                        
                        self.shape_created(shape)
                        self.shape_current=None
                    return
                elif self.shape_type in [ShapeType.point]:
                    # 创建点point
                    self.point_list = []
                    self.is_creating = False
                    group_color = LABEL_COLORMAP[len(self.shape_list) % len(LABEL_COLORMAP)]
                    color = QColor(*group_color)
                    shape = Shape(self.shape_type,[pos],color,super().get_rect(),super().get_scale())
                    shape.line_width *= 2
                    self.shape_created(shape)
                    
                    return
                else:
                    # 创建多边形/线条
                    shape = self.get_shape_by_index(-1)
                    if (self.is_creating and self.shape_type == shape.shape_type and not shape.created and
                         point_is_near(shape.points[0],pos,10/ super().get_scale())
                        ):
                        if (len(shape.points)>2 or #多边形 或线条
                        (len(shape.points)>1 and shape.shape_type in [ShapeType.line])):
                            # 多边形创建结束,闭口,并且修改颜色
                            group_color = LABEL_COLORMAP[len(self.shape_list) % len(LABEL_COLORMAP)]
                            shape.color  = QColor(*group_color)
                            shape.created = True
                            shape.update_points_widget()
                            self.update()
                            
                            self.is_creating = False
                            self.point_list = []
                            self.shape_created(shape)
                            return
                    
                    if not  self.is_creating:
                        # 开始创建
                        self.is_creating = True
                        self.point_list = []
                        color = QColor(0,255,0,255)
                        shape = Shape(self.shape_type,[pos],color,super().get_rect(),super().get_scale())
                        shape.created=False
                        self.shape_created(shape,False)
                        return
                    if self.shape_type == shape.shape_type and not shape.created:
                        # 新增一个顶点
                        shape.points.append(pos)
                        shape.update_points_widget()
                        self.update()
                        self.shapes_store()
                        return
                        
                    print("创建多边形/线条时发生错误,无法新增point")    
                return        
                
            
            if self.index_selected is not None or self.index_vertexed is not None:
                # 拖动事件结束后进行更新处理,将移动后的窗口顶点转换为基于图片的顶点
                self.set_cursor_default()
                self.is_moving = False
                for shape in self.shape_checked:
                    shape.update_points_pix()
                
                if self.index_selected is not None:
                    shape = self.get_shape_by_index(self.index_selected)
                    if shape is not None:
                        shape.update_points_pix() 

                if self.index_vertexed is not None:
                    shape = self.get_shape_by_index(self.index_vertexed)
                    if shape is not None:
                        shape.update_points_pix() 
                self.update_normal()    
                self.update()
                self.shapes_store()
                return
    
    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if not self.is_valid :
            return
        
        pos_event = event.position()
        globalPos = event.globalPosition()
        self.pos_last = pos_event # 记录鼠标最后一个位置
 
        is_edit = self.is_editing(event)
        is_select = self.is_selecting(event)
        
        if (self.index_selected is None and self.index_vertexed is None and self.index_edge is None) or is_edit:
            if self.is_creating:
                # 正在创建形状
                pos = self.pos_to_pix_pos(pos_event)
                if self.shape_type   in [ShapeType.rectangle,ShapeType.rotation]:
                    # 矩形或者旋转框
                    points = make_rect_points([self.point_list[0],pos])
                    color = QColor(0,255,0,255)
                    shape = Shape(self.shape_type,points,color,super().get_rect(),super().get_scale())
                    self.shape_current = shape
                    self.update()
                else:
                    #多边形/线条
                    # 默认的多边形正在创建,需要处理是否高亮显示起始顶点
                    shape = self.get_shape_by_index(-1)
                    if self.shape_type == shape.shape_type and not shape.created:
                        shape.pos_current = pos # 跟随鼠标,用来临时充当多边形最后一个顶点
                        if point_is_near(shape.points[0],pos,10/ super().get_scale()) and (len(shape.points)>2 or #多边形 或线条
                        (len(shape.points)>1 and shape.shape_type in [ShapeType.line])):
                            shape.set_vertex_pointed(0)
                        else:
                            shape.set_vertex_pointed(None)
                return
        
        if is_edit:#按住CTRL/ALT键进入强制编辑模式,可以新建形状
            return
        
        if self.is_moving:
            # 正在拖动中...
            # 拖动结束后并且进入mouseReleaseEvent中会调用update_points_pix()更新坐标组
            drag_distance:QPointF = globalPos - self.pos_move
            self.pos_move = globalPos
            offset = QPoint(int(drag_distance.x()),int(drag_distance.y()))
            if self.index_vertexed is not None :
                # 拖动顶点
                shape = self.get_shape_by_index(self.index_vertexed)
                if shape is None: 
                    return
                if shape.shape_type not in [ShapeType.point]:#非关键点
                    index = shape.vertex_pointed
                    shape.move_offset_vertex(index,offset)
                    if shape.shape_type   in [ShapeType.rectangle]:
                        # 如果顶点是矩形的成员,需要根据拖动顶点的距离重新调整矩形大小
                        points = shape.points_widget
                        points = make_rect_points([points[index],points[(index+2)%4]])
                        shape.points_widget = points
                    self.update()
                    return

            if self.index_selected is not None :
                # 拖动形状
                shape = self.get_shape_by_index(self.index_selected)
                self.shape_checked_add(shape,is_select,is_remove_existing=False,is_signal=False)
                if is_select:
                    for shape in self.shape_checked:
                        shape.move_offset_widget(deepcopy(offset))
                else:
                    shape.move_offset_widget(offset)
                
                self.update()    
                return

        # 最后尝试设置距离鼠标位置最近的 形状/线条/顶点
        self.set_point_nearest(pos_event)

    #重载鼠标滚轮事件
    def wheelEvent(self, event:QWheelEvent):
        if not self.is_valid :
            return
        
        mods = event.modifiers()
        if not mods & Qt.KeyboardModifier.ControlModifier and not mods & Qt.KeyboardModifier.ShiftModifier:
            #未按下CTRL键+滚轮,调用父类事件
            super().wheelEvent(event)
            return
         
        
        # 根据滚轮值,设置逆时针还是顺时针旋转,每次默认1°,如果同时按住SHIFT键,则为10°
        delta = event.angleDelta()
        angle = 1 if delta.y() > 0 else -1
        if mods & Qt.KeyboardModifier.ShiftModifier:
            angle*=10
        self.rect_rotate_as(angle)

    def leaveEvent(self, event: QMouseEvent):
        QApplication.restoreOverrideCursor()    
   
    def keyPressEvent(self, event:QKeyEvent):
        super().keyPressEvent(event)
        
        if not self.is_valid :
            return
        
        key = event.key()
        mods = event.modifiers()
        # if  mods & Qt.KeyboardModifier.AltModifier:
        #     self.set_editing_state()
        
        if  mods & Qt.KeyboardModifier.ControlModifier:
            # print("ctrl+",key)
            if key==Qt.Key.Key_Z:
                self.shapes_ctrl_z()
            elif key==Qt.Key.Key_Y:
                self.shapes_ctrl_y()
            elif key==Qt.Key.Key_C:
                self.shape_copy()
            elif key==Qt.Key.Key_V:
                self.shape_paste()
        
        if key==Qt.Key.Key_Delete:
            # 删除指向的形状/顶点等
            self.delete_obj()    

    def keyReleaseEvent(self, event:QKeyEvent): 
        super().keyReleaseEvent(event)

    # 判断被选中形状中是否有旋转框
    def is_rotate_checked(self):
        '''判断被选中形状中是否有旋转框'''
        is_checked = False
        for shape in self.shape_checked:
            if not shape.is_visible or shape.shape_type not in [ShapeType.rotation]:
                continue
            is_checked=True
            break
        return is_checked
    

    #旋转矩形(被选中的旋转框)
    def rect_rotate_as(self,angle:float):
        '''旋转矩形(被选中的旋转框)'''
        for shape in self.shape_checked:
            if not shape.is_visible:
                continue
            shape.rotate_rect(angle)
        
        self.update()
        self.shapes_store()

    # 增加被选中的形状
    def shape_checked_add(self,shape:Shape,is_select:bool,is_remove_existing=True,is_signal=True) :
        '''增加被选中的形状'''
        if shape is None:
            return
        if is_select:
            if shape not in self.shape_checked:
                self.shape_checked.append(shape) 
            else:
                if is_remove_existing:
                    self.shape_checked.remove(shape)
        else:
            self.shape_checked = [shape]
        
        #发送选中的信号给界面程序
        if is_signal:
            self.signal_shape_checked.emit({})
    
    # 存储形状以供以后恢复（撤消功能）
    def shapes_store(self,is_clear_y=True):
        """存储形状以供以后恢复（撤消功能）"""
        shape_list:list[Shape] = deepcopy(self.shape_list)
        shape_checked:list[Shape] = []#deepcopy(self.shape_checked)
       
        #从当前深拷贝的shape_list中匹配shape_checked
        if len(self.shape_checked)>0:
            for i in range(len(self.shape_list)):
                if self.shape_list[i] not in self.shape_checked:
                    continue
                shape_checked.append(shape_list[i])
        
        # if len(self.line_list)>0 :
        #     for line in self.line_list:
        #         points=[]
        #         for i in range(len(self.shape_list)):
        #             if self.shape_list[i] not in line:
        #                 continue
        #             points.append(shape_list[i])
        
        
        
        if len(self.shape_list_ctrl_z) > self.backup_num:
            self.shape_list_ctrl_y.clear()
            self.shape_list_ctrl_z = self.shape_list_ctrl_z[-self.backup_num - 1 :]
        data={}
        data["shape_list"]=shape_list
        data["shape_checked"]=shape_checked
        data["is_creating"]=self.is_creating
        data["is_moving"]=self.is_moving
        
        # self.line_rule:list[list[int]]=[]           # 规则_线条连接
        # self.line_list:list[list[Shape]]=[]         # 用来存储基于画线规则的关键点线条列表的列表
        data["line_rule"]=self.line_rule
        data["line_list"]=self.line_list
        
        self.shape_list_ctrl_z.append(data)
        self.shape_is_store=True
        if is_clear_y:
            self.shape_list_ctrl_y.clear()
    
    # 撤销/恢复交换数据
    def shapes_backed_swap(self,data_from:list,data_to:list):
        '''撤销/恢复交换数据'''
        length = len(data_from)
        if length < 1:
            return False
        
        # # 弹出最后保存的数据,转储到另一个列表中
        if self.shape_is_store and length>1:
            self.shape_is_store = False
            data = data_from.pop()  
            data_to.append(data)

        # 弹出第二个数据,此为上步操作数据,可以用来撤销/恢复
        data:dict = data_from.pop()
        
        # 数据应用
        self.shape_list = data.get("shape_list")
        self.shape_checked = data.get("shape_checked")
        self.is_creating = data.get("is_creating")
        self.is_moving = data.get("is_moving")
        
        self.line_rule = data.get("line_rule")
        self.line_list = data.get("line_list")
        if len(self.shape_list)>0:
            data_to.append(data)
  
        #更新一下
        self.update_normal()
        self.update()
        self.signal_shape_updated.emit({}) 
        if length == 1:
            return False
        return True
    
    # 撤消形状
    def shapes_ctrl_z(self):
        """撤消形状"""
        if not  self.shapes_backed_swap(self.shape_list_ctrl_z,self.shape_list_ctrl_y):
            self.shapes_store(False)

    # 恢复撤消形状
    def shapes_ctrl_y(self):
        """恢复撤消形状"""
        self.shape_is_store=False
        self.shapes_backed_swap(self.shape_list_ctrl_y,self.shape_list_ctrl_z)
        self.shape_is_store=True

    # 缩放图片信号处理
    def signal_imgZoom_changed(self,data:dict):
        '''缩放图片信号处理'''
        if "scale" not in data: 
            return
        self.update_normal()
        self.update()
        
    # 更新归一化形状数据
    def update_normal(self):
        '''更新归一化形状数据'''
        rect  = super().get_rect()
        scale = super().get_scale()
        length = len(self.shape_list)
        for i in range(length):
            self.shape_list[i].rect(rect)
            self.shape_list[i].scale(scale)
            self.shape_list[i].update_points_widget()
        
        if self.is_creating and self.shape_current is not None:
            self.shape_current.rect(rect)
            self.shape_current.scale(scale)
            self.shape_current.update_points_widget()

    # ALT键进入强制编辑模式,可以新建形状
    def is_editing(self,event: QMouseEvent):
        '''ALT键进入强制编辑模式,可以新建形状'''
        is_edit = False
        mods = event.modifiers()
        if  mods & Qt.KeyboardModifier.AltModifier:
            is_edit = True
            self.set_cursor(Qt.CursorShape.CrossCursor)
            self.set_editing_state()
        return is_edit
    # 设置编辑状态,将会清除所有选中对象
    def set_editing_state(self):
        '''设置编辑状态,将会清除所有选中对象'''
        if self.index_selected is None and self.index_vertexed is None and self.index_edge is None and len(self.shape_checked)==0:
            return
        self.index_selected = None 
        self.index_vertexed = None
        self.index_edge = None
        self.shape_checked.clear()
        for i in range(len(self.shape_list)):
            shape = self.get_shape_by_index(i)
            if shape is not None:
                shape.shape_pointed=False
                shape.isChecked=False
                shape.vertex_pointed=None
        QApplication.restoreOverrideCursor()
        self.update()
    # 按住CTRL键进入多选模式
    def is_selecting(self,event: QMouseEvent):
        '''按住CTRL键进入多选模式'''
        is_selectingt = False
        mods = event.modifiers()
        if  mods & Qt.KeyboardModifier.ControlModifier :
            is_selectingt = True
            # self.set_cursor(Qt.CursorShape.ArrowCursor)
        return is_selectingt
     
    # 删除形状,一般为创建失败时触发,所以无需保存撤销用的数据以及发送更新信号到界面         
    def delete_shape(self,shape:Shape):
        '''删除形状,一般为创建失败时触发,所以无需保存撤销用的数据以及发送更新信号到界面'''
        if shape is None:
            return
        self.shape_list.remove(shape)
        self.update_normal()
        self.update()
   
    # 删除鼠标正在指向的形状顶点等
    def delete_obj(self):
        '''删除鼠标正在指向的形状顶点等'''
        self.delete_point_at()
        self.update_normal()
        self.update()
        self.shapes_store()
        self.signal_shape_updated.emit({})             
    
    #删除鼠标正在指向的形状/顶点等
    def delete_point_at(self):
        '''删除鼠标正在指向的形状/顶点等'''
        pos = self.pos_to_pix_pos(self.pos_last)
 
        if self.index_vertexed is not None:
            # 指向顶点
            shape = self.get_shape_by_index(self.index_vertexed)
            if shape is not None :
                self.index_vertexed = None
                if shape.shape_type not in [ShapeType.rectangle,ShapeType.rotation,ShapeType.point]:
                    # 排除矩形/旋转框/point点,然后根据最后鼠标指向的最后的顶点,进行删除
                    distance = 10/ super().get_scale()
                    vertex = shape.nearest_vertex(pos,distance)
                    if vertex is not None and len(shape.points)>(3 if shape.shape_type not in [ShapeType.line] else 2 )and shape in self.shape_checked:#被选中的形状的顶点才可以删除
                        #删除顶点
                        shape.remove_point(vertex)
                        return
        
        is_line_update=False
        # 删除选中列表中的所有元素
        count=len(self.shape_checked)
        for _ in range(count):
            self.index_selected=None
            for i in range(len(self.shape_list)):   
                shape = self.shape_list[i]
                if shape in self.shape_checked:
                    is_line_update = self.delete_line_by_point(shape)
                    self.shape_list.remove(shape)
                    break
                
        self.shape_checked.clear() 
        if is_line_update:  
            self.line_link_apply()     
    
    # 删除关键点形状时,删除其载荷的线条
    def delete_line_by_point(self,shape:Shape):
        '''删除关键点形状时,删除其载荷的线条'''
        if not len(self.line_list) or shape.shape_type not in [ShapeType.point]:
            return False
        is_ok=False
        index = self.shape_list.index(shape)
        while True:
            is_remove=False
            for line in self.line_list:
                if index not in line:
                    continue
                self.line_list.remove(line)
                is_remove=True
                is_ok=True
                break
            
            if  is_remove==False:
                break  
        return  is_ok
    
    # 设置指向的最近单位(形状/线条/顶点)        
    def set_point_nearest(self,pos:QPoint):
        '''设置指向的最近单位(形状/线条/顶点)'''
        pos_pix = self.pos_to_pix_pos(pos)
        distance = 10/ super().get_scale()
        length = len(self.shape_list)
        is_in = False       #是否指向形状
        vertex = None       #指向的顶点在形状中的索引
        edge=None           #指向的线条在形状中的索引
        for i in range(length):
            shape = self.get_shape_by_index(i)
            
            if shape is None or not shape.is_visible :
                continue
            
            if not is_in:
                # 只取一个包含当前鼠标的形状索引
                is_in = shape.is_point_in_shape(pos)
                shape.set_shape_pointed(is_in)
                if is_in:
                    self.index_selected = i
            else:
                shape.set_shape_pointed(False)

            if  vertex is None :
                #只取一个顶点
                vertex = shape.nearest_vertex(pos_pix,distance) 
                shape.set_vertex_pointed(vertex)
                if vertex is not None:
                    #指向顶点了,同时设置此形状为选中状态
                    shape.set_shape_pointed(True)
                    self.index_vertexed = i
                    self.index_selected = i
                    is_in=True
                
            else :    
                shape.set_vertex_pointed(None) 
                
                
            if edge is None:
                #只取一个边
                edge = shape.nearest_edge(pos_pix,distance)
                if edge is not None:
                    #指向边了,同时设置此形状为选中状态
                    shape.set_shape_pointed(True)
                    self.index_selected = i
                    self.index_edge = i
                    is_in=True
              
            
        if not is_in:  
            self.index_selected = None   
        if vertex is None:  
            self.index_vertexed = None
        if edge is None:
            self.index_edge = None  
        
        self.set_cursor_default()

    # 根据鼠标指向设置光标
    def set_cursor_default(self):
        '''根据鼠标指向设置光标'''
        
        if self.index_vertexed is not None :
            #顶点
            self.set_cursor(Qt.CursorShape.PointingHandCursor)
            shape = self.get_shape_by_index(self.index_vertexed)
            if shape.shape_type in [ShapeType.rectangle]:
                self.setToolTip(f"单击并拖动可以缩放 ['{shape.name}']" )
            else:
                self.setToolTip(f"单击并拖动可以移动顶点 ['{shape.name}']" )
        elif self.index_edge is not None:
            #边线
            self.set_cursor(Qt.CursorShape.ArrowCursor)
            shape = self.get_shape_by_index(self.index_edge)
            if shape.shape_type in [ShapeType.polygon,ShapeType.line]:
                self.setToolTip(f"单击可以创建新顶点 ['{shape.name}']" )
            else:
                self.setToolTip(f"单击并拖动可以移动对象 ['{shape.name}']" )
        elif self.index_selected is not None :
            #对象
            self.set_cursor(Qt.CursorShape.OpenHandCursor)
            shape = self.get_shape_by_index(self.index_selected)
            self.setToolTip(f"单击并拖动可以移动对象 ['{shape.name}']" )
        else:
            self.set_cursor(Qt.CursorShape.CrossCursor)
            # QApplication.restoreOverrideCursor()
            
            self.setToolTip(f"图像" )        
    
    # 设置光标
    def set_cursor(self, cursor):
        """设置光标"""
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(cursor)
    
    # 更新当前鼠标状态
    def mouse_state_update(self):
        '''更新当前鼠标状态'''
        if self.is_draged:
            self.mouse_state=MouseState.drag
            self.shape_checked.clear()
            self.update()
        elif len(self.shape_checked):
            if self.is_rotate_checked():
                self.mouse_state=MouseState.has_rotate
            else:
                self.mouse_state = self.line_rule_get_state()
                if self.mouse_state is None:
                    self.mouse_state=MouseState.selected
        elif not (self.index_selected is None and self.index_vertexed is None and self.index_edge is None): 
            self.mouse_state=MouseState.pointed
        else:
            self.mouse_state=MouseState.normal  

    # 基于索引获取形状
    def get_shape_by_index(self,index:int):
        '''基于索引获取形状'''
        if index is None:
            return None
        if index >= len(self.shape_list) :
            return None
        if index <0 and abs(index)>len(self.shape_list) :
            return None
        return self.shape_list[index]

    # 新增一个顶点
    def vertex_add(self,pos_pix:QPoint):
        '''新增一个顶点'''
        shape = self.get_shape_by_index(self.index_edge)
        if shape is None:
            return 
        # 获取最近边,在此边的顶点位置插入一个顶点
        distance = 10/ super().get_scale()
        edge = shape.nearest_edge(pos_pix,distance)
        if edge is not None:
            isok = shape.insert_point(edge,pos_pix)
            if isok:
                # 插入成功后需要更新高亮顶点和被点击顶点,以及选中本形状
                shape.set_vertex_pointed(edge)
                shape.set_shape_pointed(True)
                self.index_vertexed = self.index_edge
            return isok 
        return False

    # 复制形状
    def shape_copy(self):
        '''复制形状'''
        self.pos_copy_paste = self.pos_last
        self.shape_copy_paste.clear()
        for shape in self.shape_checked:
            self.shape_copy_paste.append(deepcopy(shape))

    # 粘贴形状
    def shape_paste(self):
        '''粘贴形状'''
        drag_distance:QPointF = self.pos_last - self.pos_copy_paste
        offset = QPoint(int(drag_distance.x()),int(drag_distance.y()))
        shape_news :list[Shape]=[]
        for shape in self.shape_copy_paste:
            shape = deepcopy(shape)
            if shape.shape_type in [ShapeType.point] :
                # 移动顶点
                shape.move_offset_vertex(0,offset)
            else:
                # 移动形状
                shape.move_offset_widget(offset)
            
            #通过移动的窗口坐标更新图片坐标
            shape.update_points_pix()
            self.shape_list.append(shape)
            shape_news.append(shape)
        if len(shape_news):
            self.shape_checked = shape_news
        self.update()
        self.shapes_store()
        self.signal_shape_updated.emit({}) 

    # 隐藏选中的形状
    def shape_checked_hide(self):
        '''隐藏选中的形状'''
        for shape in self.shape_list:
            if shape in self.shape_checked:
                shape.is_visible=False
        self.shape_checked.clear()
        self.update()
        self.signal_shape_updated.emit({})
    
    # 显示所有隐藏的形状
    def shape_checked_show(self):
        '''显示所有隐藏的形状'''
        for shape in self.shape_list:
            shape.is_visible=True
        self.shape_checked.clear()
        self.update()
        self.signal_shape_updated.emit({})
    
    # 判断坐标是否在图片范围外      
    def is_pos_out_img(self,pos:QPoint):
        '''判断坐标是否在图片范围外'''
        pos = super().get_pos_mouse(pos)
        size = self.pixmap().size()
        return pos.x() < 0 or pos.y() < 0 or pos.x() > size.width() or pos.y() > size.height()
    
    # 计算鼠标位置在图片的坐标(图片位置)
    def pos_to_pix_pos(self,pos:QPoint) -> QPoint:
        """计算鼠标位置在图片的坐标(图片位置)"""
        pos = super().posWidget_to_posPix(pos)
        return pos
    
    # 在分组列表中增加内容
    def group_list_add(self,group:str):
        '''在分组列表中增加内容'''
        index = Utils.list_info_add(self.group_info,group,color=None,text_exclude="None")      
        return index
    #获取group_id
    def group_list_get_id(self,group:str):
        _,group_id = get_name_group_index(None,group,None,self.group_info)
        return group_id
    # 获取group文本
    def group_list_get_str(self,group_id:int):
        _,group=get_name_group(None,group_id,None,self.group_info)
        return group    
    # 在名字列表中增加内容
    def name_list_add(self,name:str):
        '''在名字列表中增加内容'''
        index = Utils.list_info_add(self.name_info,name,color=None,text_exclude="未命名")      
        return index
    # 通过name获取name_id
    def name_list_get_id(self,name:str):
        '''通过name获取name_id'''
        name_id,_ = get_name_group_index(name,None,self.name_info,None)
        return name_id
    # 通过name_id获取name文本
    def name_list_get_str(self,name_id:int):
        '''通过name_id获取name文本'''
        name,_=get_name_group(name_id,None,self.name_info,None)
        return name
    # 增加关键点
    def key_points_add(self,name:str):
        '''增加关键点'''
        #关键点依赖于标注名称,所以直接从标注名称中取关键点id
        self.name_list_add(name)
        name_id = self.name_list_get_id(name)
        if name_id is None:
            return
        Utils.list_add(self.key_points,name_id)
        
    
    # 关键点连线
    def line_link(self):
        '''关键点连线'''
        if len(self.shape_checked) !=2 :
            return False
        #line_rule:list[list[int]]=[]
        line:list[int] = self.line_get_checked_line()
        if len(line) != 2 :
            return False
        
        index = self.line_get_rule_index(line)
        if index is not None:
            return False
        self.line_rule.append(line)
        return True  
    
    # 解除关键点连线
    def line_unlink(self):
        '''解除关键点连线'''
        if len(self.shape_checked) !=2 :
            return False
        #line_rule:list[list[int]]=[]
        line:list[int]  = self.line_get_checked_line()
        if len(line) != 2 :
            return False
        index = self.line_get_rule_index(line)
        if index is None:
            return False
        self.line_rule.pop(index)
        return True
    
    # 画线规则应用(连接关键点)
    def line_link_apply(self):
        '''画线规则应用(连接关键点)'''
        if len(self.line_rule) <= 0:
            #没有画线规则
            self.line_list.clear()
            self.update()
            return
        # print(self.line_rule)
        #提取所有关键点形状
        shape_points:list[Shape]=[]
        for shape in self.shape_list:
            if shape.shape_type not in  [ShapeType.point]:
                continue
            shape_points.append(shape)

        #获取提取形状的所有分组
        group_list:list[str]=[]
        for shape in shape_points:
            if shape.group.lower() in group_list:
                continue
            group_list.append(shape.group.lower())
        
        #将关键点分组存放
        group_point_list:list[list[Shape]]=[]
        for group in group_list:
            point_list:list[Shape]=[]
            for shape in shape_points:
                if shape.group.lower() != group or shape in point_list:
                    #分组名称不同或者已经在列表中
                    continue
                point_list.append(shape)
            
            if len(point_list)<2:
                #当前分组关键点数量不足2个
                continue
            group_point_list.append(point_list)
        
        #提取符合画线规则的分组关键点,并且组合成线条列表
        line_list:list[list[int]]=[]
        for point_list in group_point_list:
            #point_list为当前分组的关键点列表
            length = len(point_list)
            for i in range(length):
                for j in range(i + 1, length):
                    #从列表中两两提取关键点数据,并获取它们的名称id
                    id_i = self.name_list_get_id(point_list[i].name)
                    id_j = self.name_list_get_id(point_list[j].name)
                    if id_i is None or id_j is None:
                        continue
                    #通过名称id在画线规则中进行匹配
                    index = self.line_get_rule_index([id_i,id_j])
                    if index is  None:
                        #连线规则中不存在则两个点相连
                        continue
                    #将这两个关键点组成一个line    
                    index_i = self.shape_list.index(point_list[i])
                    index_j = self.shape_list.index(point_list[j])
                    line:list[int] = [index_i, index_j]
                    # line:list[Shape] = [point_list[i], point_list[j]]
                    #判断line是否已经存在于line列表
                    index = line_list_get_index(line,line_list)
                    if index is not  None:
                        #在连线列表中已经存在了
                        continue
                    line_list.append(line)
        
        self.line_list = line_list
        self.update()
        # self.signal_shape_updated.emit({})

    # 获取已选中的点线列表
    def line_get_checked_line(self):
        '''获取已选中的点线列表'''
        line:list[int] = []
        for shape in self.shape_checked:
            if shape.shape_type  not in [ShapeType.point]:
                continue
            name_id = self.name_list_get_id(shape.name)
            if name_id is None:
                continue
            line.append(name_id)
        return   line        
    
    # 检查线条索引是否在线条规则列表中        
    def line_get_rule_index(self,line:list[int]) :
        '''检查线条索引是否在线条规则列表中'''
        if len(line) !=2:
            return None #线条错误
        index = None
        for i in range(len(self.line_rule)):
            rule = self.line_rule[i]
            
            is_at= True
            find_list=[]
            for id in line :
                if id not in rule:
                    is_at = False
                    break
                if id in find_list:
                    continue
                find_list.append(id)
            if is_at and len(find_list)==len(line):
                index = i
                break
            
        return index     
    
    # 判断被选中形状是否可以进行连线
    def line_rule_get_state(self):
        '''判断被选中形状是否可以进行连线'''
        #line_rule:list[list[int]]=[]
        line:list[int] = self.line_get_checked_line()
        if len(line)!=2 or line[0]==line[1]:
            #选中的不是两个关键点形状
            return None
        index = self.line_get_rule_index(line)
        if index is not None:
            #已经存在索引,说明连接过了
            return MouseState.line_unlink
        return MouseState.line_link
            
    # 绘制基于规则的线条
    def draw_rulu_line(self,painter: QPainter):
        '''绘制基于规则的线条'''
        if len(self.line_list)<=0:
            return
        
        def get_mean_color(line:list[int]):
            colors:list[QColor]=[]
            for index in line:
                shape = self.get_shape_by_index(index)
                if shape is None:
                    continue
                colors.append(shape.color)
            return Utils.QColor_mean(colors)
        for line in self.line_list:
            points=[]
            color=None
            line_width=0
            scale=0
            for index in line:
                shape = self.get_shape_by_index(index)
                if shape is None:
                    continue
                if not len(shape.points_widget):
                    continue
                points.append(shape.points_widget[0])
                if color is not None:
                    continue
                line_width = shape.line_width
                scale = shape._scale
                if not shape.group:
                    color=get_mean_color(line)
                else:
                    color=shape.color
                
                
            if  not len(points) or color is None:
                continue
            draw_line(painter,points,color,line_width,scale)


def line_list_get_index(line:list[Shape],line_list:list[list[Shape]]):
    index = None
    for i in range(len(line_list)):
        points = line_list[i]
        is_at  = True
        find_list=[]
        for point in line :
            if point not in points:
                is_at = False
                break
            if point in find_list:
                continue
            find_list.append(point)
        if is_at and len(find_list)==len(line):
            index=i
            break
    return index


class ImgWidget(QWidget):
    def __init__(self,widget:QWidget,image_path:str,parent=None):
        super(ImgWidget, self).__init__(parent)
        #生成图像显示控件
        self.label = ImgCanvas(image_path)
        
        self.label.setContentsMargins(0, 0, 0, 0)
        
        #设置当前QWidget层为图像控件
        self.setLayout(self.label.lay)
        #替换控件
        self.replace_widget_in_parent(widget)

        self.label.img_zoom(ZoomType.zoom_auto)
    
    def resizeEvent(self, event:QResizeEvent): 
        super().resizeEvent(event)   
        self.label.resizeEvent(event)
        self.label.img_zoom(ZoomType.zoom_auto)
        self.label.update_normal()
        self.label.update()
        
    #图片控件添加到窗口    
    def replace_widget_in_parent(self, widget: QWidget):
        #获取目标QWidget层
        lay = widget.layout()
        if lay and lay.count() > 0:
            #删除此层第一个QWidget
            item = lay.itemAt(0)
            if item.widget() is not None:
                w = item.widget()
                lay.removeWidget(w)
                w.deleteLater()
        #重新添加
        lay = QVBoxLayout()
        # 设置边距为0
        lay.setContentsMargins(0, 0, 0, 0)
        # 设置控件之间的间距为0
        lay.setSpacing(0)
        #设置目标层
        widget.setLayout(lay)
        #设置目标层QWidget为当前窗口
        widget.layout().addWidget(self)
       
    #图片缩放 
    def img_zoom(self,mode:ZoomType):
        if self.label is None: 
            return
        self.label.img_zoom(mode)
        



if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QWidget()
    
    image_widget = ImgWidget(main_window,"./imgs/000000000110.jpg")
    main_window.resize(800,600)
    main_window.show()

    sys.exit(app.exec_())