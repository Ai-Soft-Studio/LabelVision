import os
import cv2
import math
import numpy as np
from typing import Union, Tuple, List
from argparse import Namespace
from cv2 import UMat,Mat



if __name__ == "__main__":
    from OnnxBaseModel import OnnxBaseModel
    from points_conversion import *
else:
    from .OnnxBaseModel import OnnxBaseModel
    from .points_conversion import *

class Yolos:
    def __init__(self, model_path, device_type="cpu") -> None:
        self.net = OnnxBaseModel(model_path, device_type)
        (
            _,
            _,
            self.input_height,
            self.input_width,
        ) = self.net.get_input_shape()
        
        self.replace = True
        self.stride:int = None
        self.task:str = None
        self.batch:int = None
        self.imgsz:list[int] = []
        self.names:list[str] = []
        self.kpt_shape = None
        
        metadata = self.net.ort_session.get_modelmeta().custom_metadata_map
        print("Model metadata:", metadata)
        if metadata and isinstance(metadata, dict):
            for k, v in metadata.items():
                if k in {"stride", "batch"}:
                    metadata[k] = int(v)
                elif k in {"imgsz", "names", "kpt_shape"} and isinstance(v, str):
                    metadata[k] = eval(v)
            self.stride = metadata["stride"]
            self.task = metadata["task"]
            self.batch = metadata["batch"]
            self.imgsz = metadata["imgsz"]
            self.names = metadata["names"]
            self.kpt_shape = metadata.get("kpt_shape")

        self.nc = len(self.names)
        self.input_shape = (self.input_height, self.input_width)

        


    def inference(self, blob):
        outputs = self.net.get_ort_inference(blob=blob, extract=False)
        return outputs

    def read_cv_img(img_path):
        if img_path is  None or not  os.path.exists(img_path):
            return None
        # 直接从路径加载图像
        # NOTE: 潜在问题-无法处理翻转的图像.
        # 临时解决方法: cv_image = cv2.imread(img_path)
        cv_image = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # 转 uint8
        if cv_image.dtype != np.uint8:
            cv2.normalize(cv_image, cv_image, 0, 255, cv2.NORM_MINMAX)
            cv_image = np.array(cv_image, dtype=np.uint8)
        # 转 RGB
        if len(cv_image.shape) == 2 or cv_image.shape[2] == 1:
            cv_image = cv2.merge([cv_image, cv_image, cv_image])
        return cv_image
    
    
    def preprocess(self, image:np.ndarray):
        self.img_height, self.img_width = image.shape[:2]
        input_img = letterbox(image, self.input_shape)[0]
       
        # Transpose
        input_img = input_img.transpose(2, 0, 1)
        # Expand
        input_img = input_img[np.newaxis, :, :, :].astype(np.float32)
        # Contiguous
        input_img = np.ascontiguousarray(input_img)
        # Norm
        blob = input_img / 255.0
        return blob

    def postprocess(self, preds,conf_thres=0.5,iou_thres=0.5):
        p = non_max_suppression_v8(
            preds[0],
            task=self.task,
            conf_thres=conf_thres,
            iou_thres=iou_thres,
            multi_label=False,
            nc=self.nc,
        )
       
        masks, keypoints = None, None
        img_shape = (self.img_height, self.img_width)
        if self.task == "segment":
            proto = preds[1][-1] if len(preds[1]) == 3 else preds[1]
            self.mask_height, self.mask_width = proto.shape[2:]
        
        for i, pred in enumerate(p):
            if self.task == "segment":
                if np.size(pred) == 0:
                    continue
                masks = process_mask(
                    proto[i],
                    pred[:, 6:],
                    pred[:, :4],
                    self.input_shape,
                    upsample=True,
                )  # HWC
            elif self.task == "obb":
                pred[:, :4] = scale_boxes(
                    self.input_shape, pred[:, :4], img_shape, xywh=True
                )
            else:
                pred[:, :4] = scale_boxes(
                    self.input_shape, pred[:, :4], img_shape
                )

        if self.task == "obb":
            pred = np.concatenate(
                [pred[:, :4], pred[:, -1:], pred[:, 4:6]], axis=-1
            )
            bbox = pred[:, :5]
            conf = pred[:, -2]
            clas = pred[:, -1]
        elif self.task == "pose":
            pred_kpts = pred[:, 6:]
            if pred.shape[0] != 0:
                pred_kpts = pred_kpts.reshape(
                    pred_kpts.shape[0], *self.kpt_shape
                )
            bbox = pred[:, :4]
            conf = pred[:, 4:5]
            clas = pred[:, 5:6]
            keypoints = scale_coords(
                self.input_shape, pred_kpts, self.image_shape
            )
        else:
            bbox = pred[:, :4]
            conf = pred[:, 4:5]
            clas = pred[:, 5:6]
        return (bbox, clas, conf, masks, keypoints)

    def predict_shapes(self, image_path,type_dict:dict,kpt_maps:list[int],conf_thres=0.5,iou_thres=0.5):
        image:np.ndarray = []
        try:
            image = Yolos.read_cv_img( image_path)
        except Exception as e:  
            return []
        self.image_shape = image.shape
        blob = self.preprocess(image)
        outputs = self.inference(blob)
        boxes, class_ids, scores, masks, keypoints = self.postprocess(outputs,conf_thres=conf_thres,iou_thres=iou_thres)

        points = [[] for _ in range(len(boxes))]
        if self.task == "segment" and masks is not None:
            points = [
                scale_coords(self.input_shape, x, image.shape, normalize=False)
                for x in masks2segments(masks, 0.001)
            ]
        if keypoints is None:
            keypoints = [[] for _ in range(len(boxes))]
        # detect,segment,pose,obb
        
        # data={}
        # data["shape_type"]= self.shape_type.value
        # data["name_id"]= name_id 
        # data["group_id"]= group_id 
        # data["info"]= self.info 
        # data["angle"]= self.angle 
        # data["points"]= [(round(p.x()), round(p.y())) for p in self.points]
        shape_list:list[dict]=[]
        for i, (class_id, score,box,  point, keypoint) in enumerate(zip(class_ids, scores, boxes,points, keypoints)):
            shape_data = None
            class_id = int(class_id)
            name = self.names[class_id]
            if self.task == "detect":
                shape_data = shape_data_rectangle(type_dict,name,score[0],box)
                shape_list_add(shape_list,shape_data)
            elif self.task == "segment":
                shape_data = shape_data_polygon(type_dict,name,score[0],point)
                shape_list_add(shape_list,shape_data)
            elif self.task == "pose":
                shape_data = shape_data_rectangle(type_dict,name,score[0],box,i)
                shape_list_add(shape_list,shape_data)
                shape_data_keypoints(type_dict,class_id,keypoint,shape_list,kpt_maps,i)
            elif self.task == "obb":
                shape_data = shape_data_rotation(type_dict,name,score,box)
                shape_list_add(shape_list,shape_data)
            
            pass
        
        return shape_list

def shape_data_rotation(type_dict:dict,name:str,score:float,box:np.ndarray):
    # [265.8409423828125, 754.474853515625, 83.97158813476562, 182.71507263183594, 0.06224644184112549]
    if len(box)!=5:
        return None
    # rectangle,polygon,point,rotation,line
    poly:np.ndarray = xywhr2xyxyxyxy(box)
    if len(poly)!=4:
        return None
    data={}
    data["shape_type"] = get_shape_type_from_dict(type_name="rotation",type_dict=type_dict)
    data["name"]=name
    data["group_id"]=None
    data["info"]=f"旋转框 (自动标注 置信度:{score:0.2f})"
    data["angle"]=xyxyxyxy2rotation(poly)
    data["points"]=[(round(p[0]), round(p[1])) for p in poly]
    return data


def shape_data_keypoints(type_dict:dict,class_id:int,keypoints:np.ndarray,shape_list:list[dict],kpt_maps:list[int],group_id:int=None):
    kpt_len = len(keypoints)
    if kpt_len == 0: 
        return None
    
    is_name=True
    if kpt_len> len(kpt_maps) : #or kpt_len> len(names) or max(kpt_maps) >= len(names)
        is_name=False
    for i in range(kpt_len):
        kpt = keypoints[i]
        id = kpt_maps[i] if is_name else -1-i #if is_name else class_id
        name=str(id)
        # name = names[id] if is_name else f"关键点-未命名({i})"
        shape_data = shape_data_point(type_dict,name,kpt,group_id)
        shape_list_add(shape_list,shape_data)

def shape_data_point(type_dict:dict,name:str,keypoint:np.ndarray,group_id:int=None):
    # [array([111.375, 398.25 ]), array([104.625 , 399.9375])]
    if len(keypoint)<2  :
        return None
    if keypoint[1]==0 and keypoint[2]==0 : 
        return None
    # rectangle,polygon,point,rotation,line
    data={}
    data["shape_type"] = get_shape_type_from_dict(type_name="point",type_dict=type_dict)
    data["name"]=name
    data["group_id"]=group_id
    data["info"]=f"关键点 (自动标注 置信度:{keypoint[2] if len(keypoint)>2 else 0.0:0.2f})"
    data["angle"]=0
    data["points"]=[(round(keypoint[0]), round(keypoint[1]))]
    return data


def shape_data_polygon(type_dict:dict,name:str,score:float,points:np.ndarray):
    # [array([111.375, 398.25 ]), array([104.625 , 399.9375])]
    if len(points)<3:
        return None
    # rectangle,polygon,point,rotation,line
    data={}
    data["shape_type"] = get_shape_type_from_dict(type_name="polygon",type_dict=type_dict)
    data["name"]=name
    data["group_id"]=None
    data["info"]=f"多边形 (自动标注 置信度:{score:0.2f})"
    data["angle"]=0
    data["points"]=[(round(p[0]), round(p[1])) for p in points]
    return data

def shape_data_rectangle(type_dict:dict,name:str,score:float,box:np.ndarray,group_id=None):
    # array([669.06207848, 391.50288391, 810.        , 876.39463806])
    if len(box)!=4:
        return None
    data={}
    data["shape_type"] = get_shape_type_from_dict(type_name="rectangle",type_dict=type_dict)
    data["name"]=name
    data["group_id"]=group_id
    data["info"]=f"矩形 (自动标注 置信度:{score:0.2f})"
    data["angle"]=0
    data["points"]=xyxy2xyxyxyxy(round(box[0]),round(box[1]),round(box[2]),round(box[3]))
    return data

def get_shape_type_from_dict(type_name:str,type_dict:dict):
    # rectangle,polygon,point,rotation,line
    if type_dict is None or not type_name or not  isinstance(type_dict,dict):
        return None
    return type_dict.get(type_name,None)


def shape_list_add(shape_list:list[dict],shape_data:dict):
    if shape_data is None:
        return
    shape_list.append(shape_data)


def show_boxex(image_path,boxes):
    from PIL import Image, ImageDraw
    # 打开图片
    image = Image.open(image_path)

    # 创建一个可绘制的对象
    draw = ImageDraw.Draw(image)

    # 遍历所有矩形框坐标并画出矩形
    for box in boxes:
        x1, y1, x2, y2 = box
        # 画出矩形，颜色为红色，宽度为3
        draw.rectangle([x1, y1, x2, y2], outline='red', width=3)

    # 保存或显示图片
    # 保存图片
    image.save('output_image_with_boxes.jpg')  

def shape_type_dict():
    # rectangle   = 0     # 矩形
    # polygon     = 1     # 多边形
    # point       = 2     # 关键点
    # rotation    = 3     # 旋转矩形
    # line        = 4     # 线条
    type_dict={}
    type_dict["rectangle"]=0
    type_dict["polygon"]=1
    type_dict["point"]=2
    type_dict["rotation"]=3
    type_dict["line"]=4
    return type_dict

if __name__ == "__main__":
    model_path="./model/yolo11n-obb.onnx"
    img_path="./imgs/001.jpg"
    # img_path="./imgs/bus.jpg"
    model_path="./model/yolo11n.onnx"
    img_path="./imgs/bus.jpg"
    model = Yolos(model_path)
    kpt_maps=[i+1 for i in range(17)]
    model.predict_shapes(img_path,shape_type_dict(),kpt_maps)

























