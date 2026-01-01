# LabelVision - YOLO标注工具

LabelVision是一款功能强大的YOLO标注工具，支持多种标注类型，包括目标检测、旋转框、关键点和实例分割。

## 功能特性

- **多种标注类型支持**
  - 目标检测（矩形框）
  - 旋转框标注（OBB）
  - 关键点标注（Pose）
  - 实例分割（Segmentation）

- **直观的用户界面**
  - 基于PySide6的现代化GUI
  - 支持图片和视频标注
  - 实时预览和编辑
  - 拖拽式操作

- **高效的标注工具**
  - 快捷键支持
  - 标注复制粘贴
  - 撤销/重做功能
  - 批量处理支持

- **灵活的导出格式**
  - 支持YOLOv8、YOLOv9、YOLOv11格式
  - 自动生成数据集配置文件
  - 支持多种标注类型混合导出

## 技术栈

- **开发语言**: Python 3.11+
- **GUI框架**: PySide6
- **计算机视觉**: OpenCV, NumPy, Pillow
- **深度学习**: ONNX Runtime (用于模型推理)
- **其他**: YAML (配置文件), JSON (项目配置)

## 依赖项

主要依赖项列在 `requirements.txt` 文件中，包括：

- PySide6==6.8.0.2
- opencv-python==4.10.0.84
- numpy==1.26.4
- onnxruntime==1.17.1
- Pillow==11.0.0
- PyYAML==6.0.2

## 安装和运行

### 1. 克隆项目

```bash
git clone https://github.com/Ai-Soft-Studio/LabelVision.git
cd LabelVision
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行应用

```bash
python LabelVision/main.py
```

## 快速开始

1. **打开图片文件夹**
   - 点击菜单栏的"文件" → "打开文件夹"
   - 选择包含图片的文件夹

2. **添加标注类别**
   - 在左侧类别列表中点击"添加类别"
   - 输入类别名称并保存

3. **开始标注**
   - 选择标注类型（矩形框、旋转框、关键点或分割）
   - 在图片上绘制标注
   - 调整标注位置和大小

4. **导出标注**
   - 点击"导出"按钮
   - 选择导出格式
   - 生成YOLO格式的标注文件

## 使用方法

### 标注类型

#### 1. 矩形框标注
- 选择"矩形"工具
- 点击并拖拽绘制矩形
- 调整矩形大小和位置

#### 2. 旋转框标注
- 选择"旋转"工具
- 绘制旋转矩形
- 调整旋转角度

#### 3. 关键点标注
- 选择"关键点"工具
- 点击添加关键点
- 支持关键点分组和连线

#### 4. 实例分割
- 选择"多边形"工具
- 点击添加多边形顶点
- 双击闭合多边形

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl + N | 新建项目 |
| Ctrl + O | 打开文件夹 |
| Ctrl + S | 保存标注 |
| Ctrl + E | 导出标注 |
| Ctrl + Z | 撤销 |
| Ctrl + Y | 重做 |
| Ctrl + C | 复制标注 |
| Ctrl + V | 粘贴标注 |
| Delete | 删除选中标注 |
| A | 上一张图片 |
| D | 下一张图片 |
| W | 放大图片 |
| S | 缩小图片 |
| R | 重置视图 |
| 1 | 矩形框工具 |
| 2 | 旋转框工具 |
| 3 | 关键点工具 |
| 4 | 多边形工具 |

### 标注管理

- **选择标注**: 点击标注对象进行选择
- **移动标注**: 拖拽标注对象
- **调整大小**: 拖拽标注边框上的控制点
- **复制标注**: 选中标注后使用Ctrl+C，切换图片后Ctrl+V
- **删除标注**: 选中标注后按Delete键

## 项目结构

```
LabelVision/
├── LabelVision/              # 主应用目录
│   ├── UiBase/              # UI基础组件
│   │   ├── YOLO/            # YOLO相关功能
│   │   ├── widget/          # 自定义部件
│   │   ├── ImgCanvas.py     # 图片画布
│   │   ├── ImgList.py       # 图片列表
│   │   ├── Shape.py         # 标注形状定义
│   │   └── ui_event.py      # UI事件处理
│   ├── resources/           # 资源文件
│   ├── main.py              # 应用入口
│   └── main_ui.py           # UI定义
├── dataset/                 # 示例数据集
├── imgs/                    # 示例图片和视频
├── model/                   # 预训练模型
├── config.json              # 应用配置
└── requirements.txt         # 依赖列表
```

## 导出格式

### YOLO目标检测格式

```
class_id x_center y_center width height
```

### YOLO旋转框格式（OBB）

```
class_id x_center y_center width height angle
```

### YOLO关键点格式（Pose）

```
class_id x_center y_center width height x1 y1 v1 x2 y2 v2 ...
```

### YOLO实例分割格式

```
class_id x_center y_center width height [segmentation_points]
```

## 数据集配置

导出时会自动生成数据集配置文件（如 `det.yaml`、`obb.yaml`、`pose.yaml`、`seg.yaml`），包含以下内容：

```yaml
train: ../train/images
val: ../val/images

nc: 10  # 类别数量
names: ['person', 'dog', 'cat', ...]  # 类别名称列表
```

## 支持的模型

- YOLOv8系列
- YOLOv9系列
- YOLOv11系列
- 支持目标检测、旋转框、关键点、实例分割等任务

## 常见问题

### Q: 如何添加新的标注类别？
A: 在左侧类别列表中点击"添加类别"按钮，输入类别名称即可。

### Q: 如何切换标注类型？
A: 在工具栏中选择相应的标注工具按钮即可切换。

### Q: 如何导出标注文件？
A: 点击工具栏的"导出"按钮，选择导出格式和路径即可。

### Q: 支持视频标注吗？
A: 支持，点击"文件"→"打开视频"选择视频文件即可。

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置

1. 克隆项目
2. 安装依赖
3. 运行应用进行测试

### 提交代码

1. Fork项目
2. 创建特性分支
3. 提交代码
4. 创建Pull Request

## 许可证

本项目采用Apache-2.0许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: https://github.com/Ai-Soft-Studio/LabelVision/issues
- Email: voouer@qq.com

## 更新日志

### v1.0.0 (2026-01-01)
- 初始版本发布
- 支持矩形框、旋转框、关键点、实例分割标注
- 支持YOLOv8-v11格式导出
- 完整的GUI界面
- 快捷键支持

## 致谢

感谢以下项目和库的支持：

- [PySide6](https://doc.qt.io/qtforpython/)
- [OpenCV](https://opencv.org/)
- [YOLO](https://ultralytics.com/)
- [NumPy](https://numpy.org/)

---

**LabelVision** - 让YOLO标注更简单、更高效！