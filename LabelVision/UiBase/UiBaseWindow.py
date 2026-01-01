from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from copy import deepcopy
import json
import os

from .utils import Utils


def setGraph(ui:QWidget):
    ui.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)	#将界面属性设置为半透明
    ui.shadow = QGraphicsDropShadowEffect()		#设定一个阴影,半径为 4,颜色为 2, 10, 25,偏移为 0,0
    ui.shadow.setBlurRadius(20)
    ui.shadow.setColor(QColor(2, 10, 25))
    ui.shadow.setOffset(0, 0)
    ui.setGraphicsEffect(ui.shadow)	#为frame设定阴影效果

class UiBaseWindow(QMainWindow):
    # single_message = Signal(dict)   #用来显示消息的信号
    def __init__(self,ui,parent = None):
        QMainWindow.__init__(self,parent = parent)
        self.ui = ui
        self.ui.setupUi(self)
        self.data={}
        self.windowTitle()
        

 
    def closeEvent(self,event):
        reply = messageBox(self,'提示','确定要退出程序吗?',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
    


class WidgetHook():
    def __init__(self,widget:QWidget):
        self.w=widget
        self._mousePressEvent=widget.mousePressEvent
        self._mouseReleaseEvent=widget.mouseReleaseEvent
        self._mouseMoveEvent=widget.mouseMoveEvent
        
        widget.mousePressEvent=self.mousePressEvent
        widget.mouseReleaseEvent=self.mouseReleaseEvent
        widget.mouseMoveEvent=self.mouseMoveEvent
        
        widget.setMouseTracking(True)
        
        self._resizing = False
        self._start_size = widget.size()
        self._start_pos = QPoint()
        self._cursor_offset = QPoint()

    
    def mousePressEvent(self, event: QMouseEvent): 
        self._mousePressEvent(event) 
        # print("mousePressEvent",event)  
        if event.button() != Qt.LeftButton:
            return
        ret=self.is_in_resize_area(event.position())
        if ret ==0:
            return
        self._start_pos = event.globalPos()
        self._start_size = self.w.size()
        self._resizing = True
        QApplication.restoreOverrideCursor()
        self.w.setCursor(Qt.CursorShape.SizeHorCursor)  # 改变光标形状以指示可以调整大小
        pass
    def mouseReleaseEvent(self, event: QMouseEvent):
        self._mouseReleaseEvent(event) 
        # print("mouseReleaseEvent",event)  
        if event.button() == Qt.LeftButton and self._resizing:
            self._resizing = False
            QApplication.restoreOverrideCursor()
            self.w.setCursor(Qt.CursorShape.ArrowCursor)
        pass
    def mouseMoveEvent(self, event: QMouseEvent):
        self._mouseMoveEvent(event) 
        # print("mouseMoveEvent",event)  
        if self._resizing:
            # 根据鼠标移动更新窗口尺寸
            global_pos = event.globalPos()
            pos_diff=global_pos-self._start_pos
            self._start_pos=global_pos
            new_size = self._start_size
            new_size.setWidth(new_size.width()+pos_diff.x())
            # self.w.maximumWidth()=
            # self.w.setMaximumWidth(new_size.width()-pos_diff.x())
            
            self.w.resize(QSize(new_size.width()+pos_diff.x(),new_size.height()))
            self.w.move(0,0)
            # self.w.setGeometry(0,0,new_size.width()+pos_diff.x(),new_size.height())
        pass
    
    def is_in_resize_area(self, pos: QPoint) -> bool:
        if pos.x()<=10:
            return 1
        if pos.x()>=self.w.rect().width()-10:
            return 2 
        return 0
        if pos.x()<=10 or pos.x()>=self.rect().width()-10:
            return True
        return False

#消息框
def messageBox(parent,title,text,botton:QMessageBox.StandardButton=None,default_botton:QMessageBox.StandardButton=None):
    '''弹出消息框'''
    reply=None
    if botton is None and default_botton is None:
        reply=QMessageBox.about(parent,title,text)
    elif (botton & QMessageBox.StandardButton.Yes or
          botton & QMessageBox.StandardButton.No ):
        if default_botton is None:
            default_botton = QMessageBox.StandardButton.Yes
        reply = QMessageBox.question(parent,title,text,botton,default_botton)
    elif (botton & QMessageBox.StandardButton.Ok or
          botton & QMessageBox.StandardButton.Cancel):
        if default_botton is None:
            default_botton = QMessageBox.StandardButton.Ok
        reply = QMessageBox.warning(parent,title,text,botton,default_botton)
    else:
        reply=QMessageBox.information(parent,title,text,botton)
    return reply 

#组合框增加内容项
def ComboBox_add_item(comboBox:QComboBox,text:str,is_select=True,is_force_add:bool=False):
    '''组合框增加内容项'''
    index_found = None
    
    if not text:
        return  index_found
    
    if comboBox is None:
        return index_found
    
    if not is_force_add:
        for index in range(comboBox.count()):
            if comboBox.itemText(index).lower() == text.lower():
                index_found = index
                break
    
    if index_found is None:
        comboBox.addItem(text)
        index_found = comboBox.count() - 1
    
    if is_select and index_found is not None and index_found < comboBox.count() and index_found >= 0:
        comboBox.setCurrentIndex(index_found)
    return index_found

#组合框获取内容列表数据
def ComboBox_get_data(comboBox:QComboBox,discardText:str=""):
    '''组合框获取内容列表数据'''
    lst:list[str]=[]
    for index in range(comboBox.count()):
        if len(discardText) and comboBox.itemText(index).lower() == discardText.lower():
            continue
        lst.append(comboBox.itemText(index))
    return lst

def ComboBox_remove(comboBox:QComboBox,get:str|int):
    if isinstance(get, int):
        if get <0 and get >= comboBox.count():
            return None
        comboBox.removeItem(get)
        return get
    
    if isinstance(get, str):
       index= comboBox.findText(get)
       if index is None or index <0 or index>= comboBox.count():
           return None
       comboBox.removeItem(index)
       return index
    return None

def ComboBox_set_text(comboBox:QComboBox,old_value:str|int,new_value:str,):
    if isinstance(old_value, int):
        if old_value <0 and old_value >= comboBox.count():
            return False
        comboBox.setItemText(old_value,new_value)
        return True   
    if isinstance(old_value, str):
       index= comboBox.findText(old_value)
       if index is None or index <0 or index>= comboBox.count():
           return False
       comboBox.setItemText(index,new_value)
       return True
    return False 
        

#列表框增加内容项
def ListWidget_add_item(listWidget:QListWidget,text:str,is_select:bool=False,is_check_enble:bool=False,is_checked:bool=False,is_force_add:bool=False,is_show_index=False):
    '''列表框增加内容项'''
    index_found = None  
    
    if not text:
        return  index_found
    
    if listWidget  is None:
        return  index_found
    
    if not is_force_add:
        for i in range(listWidget.count()):
            temp = listWidget.item(i).text()
            if is_show_index:
                parts = temp.split(']\t')
                temp = parts[1] if len(parts) > 1 else temp
            if temp.lower() == text.lower():
                index_found = i
                break
    
    if index_found is None:
        temp=text
        if is_show_index:
            temp=f"[{listWidget.count()}]\t{text}"
        item = QListWidgetItem(temp)
        if is_check_enble:
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if is_checked else  Qt.CheckState.Unchecked)
        
        listWidget.addItem(item) 

        index_found = listWidget.count() - 1
    
    if is_select and index_found is not None and index_found < listWidget.count() and index_found >= 0:
        listWidget.setCurrentRow(index_found)
    # 滚动到底部以显示新添加的项
    listWidget.scrollToBottom()    
    return index_found    

#列表框获取指定项
def ListWidget_get_item(listWidget:QListWidget,get:str|int,is_show_index=False):
    '''列表框获取指定项'''
    item:QListWidgetItem = None
    if get is None or listWidget is None:
        return item
    
    if isinstance(get, int):
        if get >=0 and get < listWidget.count():
            item = listWidget.item(get)
        return item
    
    if isinstance(get, str):
        for i in range(listWidget.count()):
            temp = listWidget.item(i).text()
            if is_show_index:
                parts = temp.split(']\t')
                temp = parts[1] if len(parts) > 1 else temp
            if temp.lower() == get.lower():
                item = listWidget.item(i)
                break
    else:
        # 如果info既不是字符串也不是整数，可以抛出一个异常或返回None等
        raise ValueError("参数必须为字符串内容或者整数索引")

    return item

def ListWidget_get_index(listWidget:QListWidget,get:str|int,is_show_index=False):
    item = ListWidget_get_item(listWidget,get,is_show_index)
    if item is None:
        return None
    index = listWidget.row(item)
    return index

def ListWidget_remove(listWidget:QListWidget,get:str|int,is_show_index=False):
    index = ListWidget_get_index(listWidget,get,is_show_index)
    if index is None or index <0 or index>=listWidget.count():
        return None
    listWidget.takeItem(index)
    return index

def ListWidget_get_text(listWidget:QListWidget,index:int,is_show_index=False):
    if index <0 and index >= listWidget.count():
        return None
    text = listWidget.item(index).text()
    if is_show_index:
        parts = text.split(']\t')
        text = parts[1] if len(parts) > 1 else text
    return text    

def ListWidge_current_text(listWidget:QListWidget,is_show_index=False):
    index = listWidget.currentRow()
    if index is None:
        return ""
    text = ListWidget_get_text(listWidget,index,is_show_index)  
    if text is None or not text:
        return "" 
    return text

# 列表框修改指定文本内容
def ListWidget_set_text(listWidget:QListWidget,old_value:str|int,new_value:str,is_show_index=False):
    '''列表框修改指定文本内容'''
    item=ListWidget_get_item(listWidget,old_value,is_show_index)
    if item is None:
        return False
    temp = new_value
    
    if is_show_index:
        temp=f"[{listWidget.row(item)}]\t{new_value}"
    item.setText(temp)
    return True

# 获取列表项的颜色
def ListWidget_get_color(listWidget:QListWidget,text:str,is_show_index=False):
    '''获取列表项的颜色'''
    color=QColor()
    if text is None or not text:
        return color
    item = ListWidget_get_item(listWidget,text,is_show_index=is_show_index)
    color = ListWidget_get_color_by_item(item)
    return color

# 获取列表项的颜色
def ListWidget_get_color_by_item(item:QListWidgetItem):
    '''获取列表项的颜色'''
    color=QColor()
    if item is None :
        return color
    color = item.background().color()
    return color

# 列表框当前项选择颜色
def ListWidget_current_set_color(listWidget:QListWidget,is_show_index=False,parent=None):
    '''列表框当前项选择颜色'''
    text = ListWidge_current_text(listWidget,is_show_index=is_show_index)
    if text is None or not text:
        return None
    item = ListWidget_get_item(listWidget,text,is_show_index=is_show_index)
    if item is None :
        return None
    color = item.background().color()
    color=QColorDialog.getColor(color,parent=parent,title="选择颜色",options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
    if color==QColor():
        return None
    # color.setAlpha(188)
    color= ListWidget_item_set_color(item,color)
    return color

# 列表框设置颜色
def ListWidget_item_set_color(item:QListWidgetItem,color:QColor):
    '''列表框设置颜色'''
    if item is None or color==QColor():
        return None
    item.setBackground(color)
    # if (color.red()>120 and color.green()>120 and color.blue()>120) or ( color.alpha() <100) :
    #     item.setForeground(QColor(0,0,0,255))
    # else:
    #     item.setForeground(QColor(255,255,255,255))
    if ((color.red() + color.green() +  color.blue())/3>120) or ( color.alpha() <100) :
        item.setForeground(QColor(0,0,0,255))
    else:
        item.setForeground(QColor(255,255,255,255))
    return color


# 列表框获取数据,包含文本和颜色/
def ListWidget_get_list_info(listWidget:QListWidget,is_show_index=False):
    '''列表框获取数据,包含文本和颜色'''
    list_info:list[dict]=[]
    for i in range(listWidget.count()):
        text = ListWidget_get_text(listWidget,i,is_show_index=is_show_index)
        color = ListWidget_get_color_by_item(listWidget.item(i))
        if text is None or not text or color is None or color==QColor():
            continue
        data = Utils.list_info_make_data(text,color)
        list_info.append(data)
    return list_info

# 加载数据到列表框,并且设置每一项的文本和颜色
def ListWidget_load_list_info(listWidget:QListWidget,list_info:list[dict],is_show_index=False,is_check_enble:bool=False,is_checked:bool=False,is_force_add:bool=False,alpha:int=None):
    '''加载数据到列表框,并且设置每一项的文本和颜色'''
    length = len(list_info)
    for i in range(length):
        data = list_info[i]
        ListWidget_load_data(listWidget,data,is_show_index=is_show_index,is_check_enble=is_check_enble,is_checked=is_checked,is_force_add=is_force_add,alpha=alpha)

# 加载数据到列表框,解析文本和颜色分别进行设置/
def ListWidget_load_data(listWidget:QListWidget,data:dict,is_show_index=False,is_check_enble:bool=False,is_checked:bool=False,is_force_add:bool=False,alpha:int=None):
    '''加载数据到列表框,解析文本和颜色分别进行设置'''
    if len(data) <=0 or not isinstance(data,dict):
        return None
    text  = data.get("text",None)
    color:QColor = Utils.QColor_load_info(data.get("color",[]))
    if text is None or not text:
        return None
    index = ListWidget_add_item(listWidget,text,is_select=True,is_show_index=is_show_index,is_check_enble=is_check_enble,is_checked=is_checked,is_force_add=is_force_add)
    if index is None:
        return None
    #添加过文本内容后再判断是否需要更改颜色
    if color is None or color == QColor():
        return index
    if alpha is not None:
        color.setAlpha(alpha)
    item = ListWidget_get_item(listWidget,index,is_show_index)
    ListWidget_item_set_color(item,color)  
    return index 
         

def ListWidget_init_setStyleSheet(listWidget:QListWidget):
    listWidget.setStyleSheet("""
                                QListWidget::item:selected {
                                    background-color: #000000; /* 选中项的背景色 */
                                    color: white; /* 选中项的文本色（可选） */
                                }
                                QListWidget::item:hover {
                                    background-color: #585858; /* 鼠标悬停项的背景色 */
                                    color: white; /* 选中项的文本色（可选） */
                                }
                            """)





#新增菜单按钮
def Action_add(text:str,parent:QWidget,slot:object,icon:QIcon|QPixmap=None,
               shortcut:list|tuple|QKeySequence|QKeySequence.StandardKey|str|int=None,
               checkable:bool=False,enabled=True,checked=False,auto_trigger=False,
               ContextMenuPolicy:Qt.ContextMenuPolicy=Qt.ContextMenuPolicy.ActionsContextMenu):
    '''新增菜单按钮'''
    if not text or parent is None:
        return None
    #设置菜单策略
    parent.setContextMenuPolicy(ContextMenuPolicy)
    
    action  = QAction(text,parent)
    if icon is not None:
        #设置菜单图标
        action.setIconText(text.replace(" ", "\n"))
        action.setIcon(icon)
    if shortcut is not None:
        #设置菜单快捷键
        if isinstance(shortcut, (list, tuple)):
            action.setShortcuts(shortcut)
        else:
            action.setShortcut(shortcut)
    
    if slot is not None:
        #连接槽
        action.triggered.connect(slot)

    if checkable:
        #是否可勾选
        action.setCheckable(True)
    
    action.setEnabled(enabled)
    action.setChecked(checked)
    if auto_trigger:
        action.triggered.emit(checked)
    
    parent.addAction(action)  
    
    return action

#写配置项
def ini_write(path:str,key:str,value:dict):
    """写配置项"""
    cfg = QSettings(path,QSettings.Format.IniFormat)
    # 将字典转换为 JSON 字符串
    json_string = json.dumps(value)
    cfg.setValue(key,json_string)

#读配置项
def ini_read(path:str,key:str,defaultValue: dict):
    '''读配置项'''
    cfg = QSettings(path, QSettings.Format.IniFormat)
    # 读取字符串值
    raw_value = cfg.value(key, '', type=str)  # 注意：这里我们传递 str 作为类型参数
    # 尝试将字符串解析为字典，如果失败则使用默认值
    try:
        value = json.loads(raw_value)
        if not isinstance(value, dict):
            raise ValueError("解析值不是字典")
    except (json.JSONDecodeError, ValueError):
        value = defaultValue
    return value

#读取 JSON 配置文件
def read_json_config(file_path)->dict:
    """读取 JSON 配置文件"""
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            config = json.load(file)
        except json.JSONDecodeError:
            # 如果文件内容不是有效的 JSON 格式，返回空字典
            return {}
    
    return config
 
#使用 json.dumps() 写入 JSON 配置文件，并添加缩进格式化
def write_json(file_path, config):
    """使用 json.dumps() 写入 JSON 配置文件，并添加缩进格式化"""
    json_string = json.dumps(config, indent=4, ensure_ascii=False)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_string)

#更新 JSON 配置文件，键名一样则覆盖，键名不一样则新增
def write_json_config(file_path, updates:dict,remove_key:str=""):
    """更新 JSON 配置文件，键名一样则覆盖，键名不一样则新增"""
    # 读取现有的配置
    config = read_json_config(file_path)
    
    # 更新配置
    for key, value in updates.items():
        config[key] = value
    if remove_key is not None and remove_key:
        del config[remove_key]
    # 写回文件
    write_json(file_path, config)
    config_save_golbal(config)
    
def config_save_golbal(config:dict):
    """保存全局配置"""
    
    name_info:list[dict]  = config.get("name_info",[])
    group_info:list[dict] = config.get("group_info",[])
    key_points:list[int] = config.get("key_points",[])
    line_rule:list[list[int]] = config.get("line_rule",[])
    data={}
    data["name_info"] = name_info
    data["group_info"] = group_info
    data["key_points"] = key_points
    data["line_rule"] = line_rule
    write_json("./config.json", data)    
   
def config_read_golbal():
    """读取全局配置"""
    data = read_json_config("./config.json")
    return data
   
   
   
   
   