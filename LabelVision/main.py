import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from typing import Iterator, Tuple
import math
from main_ui import Ui_MainWindow

from UiBase.UiBaseWindow import UiBaseWindow
from UiBase.ui_event import UiEvents

from UiBase.utils import __appname__,__version__


def gradient_text(
    text: str,
    start_color: Tuple[int, int, int] = (0, 0, 255),
    end_color: Tuple[int, int, int] = (255, 0, 255),
    frequency: float = 1.0,
) -> str:
    def color_function(t: float) -> Tuple[int, int, int]:
        def interpolate(start: float, end: float, t: float) -> float:
            # 使用正弦波进行平滑、周期性插值
            return (
                start
                + (end - start) * (math.sin(math.pi * t * frequency) + 1) / 2
            )

        return tuple(
            round(interpolate(s, e, t)) for s, e in zip(start_color, end_color)
        )

    def gradient_gen(length: int) -> Iterator[Tuple[int, int, int]]:
        return (color_function(i / (length - 1)) for i in range(length))

    gradient = gradient_gen(len(text))
    return "".join(
        f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        for char, (r, g, b) in zip(text, gradient)
    )  


def run():
    text=gradient_text("软件启动")
    print(text)
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    
    win = UiBaseWindow(ui)
    win.setWindowTitle(__appname__+"    v"+__version__)
    events = UiEvents(win)
    win.show()
    sys.exit(app.exec())
    

    
if __name__ == '__main__':
    run()
    

#增加修改分组和删除分组
#增加切换目录后,保留原始类名分组信息,以及导入类名信息,连线规则等功能  
    
    
    
    
# 关键点连线规则
# 必须在同一个组

#遍历获取所有点形状
#按分组进行列表划分

#按名称进行连线,比如连线规则中有[[眼睛,鼻子],[鼻子,嘴巴]]
#连线时,眼睛和鼻子画线,鼻子和嘴巴划线

#如果未分组,所有关键点眼睛都会连向鼻子

#规则设置为全局性的

#例如:line_rule=[[眼睛,鼻子],[鼻子,嘴巴],[嘴巴,脖子],[脖子,肩膀]]

#画布中进行处理连线:
#1.遍历所有关键点形状
#2.按分组再次组成列表
#3.在列表中进行规则匹配,方法为 shape.name in line_rule[i]  lst[n].append(shape.name)
#4.如果匹配后生成的列表中关键点数量大于1 如 len(lst[n])>1 则执行连线

#断开连线
#两种方式,一种不修改规则:
#直接删除某个关键点
#修改规则:
#提示确定断开[眼睛,鼻子]的连线?
#在规则中匹配 rule[0] in line_rule[i][] and rule[1] in line_rule[i][] 或者 del line_runle[i]


    
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
    
    
