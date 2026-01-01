import cv2
import numpy as np
import math

def refine_contours(contours, img_area, epsilon_factor=0.001):
    """
    Refine contours by approximating and filtering.

    Parameters:
    - contours (list): List of input contours.
    - img_area (int): Maximum factor for contour area.
    - epsilon_factor (float, optional): Factor used for epsilon calculation in contour approximation. Default is 0.001.

    Returns:
    - list: List of refined contours.
    """
    # Refine contours
    approx_contours = []
    for contour in contours:
        # Approximate contour
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        approx_contours.append(approx)

    # Remove too big contours ( >90% of image size)
    if len(approx_contours) > 1:
        areas = [cv2.contourArea(contour) for contour in approx_contours]
        filtered_approx_contours = [
            contour
            for contour, area in zip(approx_contours, areas)
            if area < img_area * 0.9
        ]

    # Remove small contours (area < 20% of average area)
    if len(approx_contours) > 1:
        areas = [cv2.contourArea(contour) for contour in approx_contours]
        avg_area = np.mean(areas)

        filtered_approx_contours = [
            contour
            for contour, area in zip(approx_contours, areas)
            if area > avg_area * 0.2
        ]
        approx_contours = filtered_approx_contours

    return approx_contours


def xyxy2xywh(x):
    """
    Convert bounding box coordinates from (x1, y1, x2, y2) format to (x, y, width, height) format.

    Args:
        x (np.ndarray): The input bounding box coordinates in (x1, y1, x2, y2) format.
    Returns:
       y (np.ndarray): The bounding box coordinates in (x, y, width, height) format.
    """
    y = np.copy(x)
    y[..., 0] = (x[..., 0] + x[..., 2]) / 2  # x center
    y[..., 1] = (x[..., 1] + x[..., 3]) / 2  # y center
    y[..., 2] = x[..., 2] - x[..., 0]  # width
    y[..., 3] = x[..., 3] - x[..., 1]  # height
    return y


def xywh2xyxy(x):
    """
    Convert bounding box coordinates from (x, y, width, height) format to (x1, y1, x2, y2) format where (x1, y1) is the
    top-left corner and (x2, y2) is the bottom-right corner.

    Args:
        x (np.ndarray): The input bounding box coordinates in (x, y, width, height) format.
    Returns:
        y (np.ndarray): The bounding box coordinates in (x1, y1, x2, y2) format.
    """
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2  # top left x
    y[..., 1] = x[..., 1] - x[..., 3] / 2  # top left y
    y[..., 2] = x[..., 0] + x[..., 2] / 2  # bottom right x
    y[..., 3] = x[..., 1] + x[..., 3] / 2  # bottom right y
    return y


def xywhn2xyxy(x, w=640, h=640, padw=0, padh=0):
    """
    Convert normalized bounding box coordinates to pixel coordinates.

    Args:
        x (np.ndarray): The bounding box coordinates.
        w (int): Width of the image. Defaults to 640
        h (int): Height of the image. Defaults to 640
        padw (int): Padding width. Defaults to 0
        padh (int): Padding height. Defaults to 0
    Returns:
        y (np.ndarray): The coordinates of the bounding box in the format [x1, y1, x2, y2] where
            x1,y1 is the top-left corner, x2,y2 is the bottom-right corner of the bounding box.
    """
    y = np.copy(x)
    y[..., 0] = w * (x[..., 0] - x[..., 2] / 2) + padw  # top left x
    y[..., 1] = h * (x[..., 1] - x[..., 3] / 2) + padh  # top left y
    y[..., 2] = w * (x[..., 0] + x[..., 2] / 2) + padw  # bottom right x
    y[..., 3] = h * (x[..., 1] + x[..., 3] / 2) + padh  # bottom right y
    return y


def xyxy2xywhn(x, w=640, h=640, clip=False, eps=0.0):
    """
    Convert bounding box coordinates from (x1, y1, x2, y2) format to (x, y, width, height, normalized) format.
    x, y, width and height are normalized to image dimensions

    Args:
        x (np.ndarray): The input bounding box coordinates in (x1, y1, x2, y2) format.
        w (int): The width of the image. Defaults to 640
        h (int): The height of the image. Defaults to 640
        clip (bool): If True, the boxes will be clipped to the image boundaries. Defaults to False
        eps (float): The minimum value of the box's width and height. Defaults to 0.0
    Returns:
        y (np.ndarray): The bounding box coordinates in (x, y, width, height, normalized) format
    """
    if clip:
        clip_boxes(x, (h - eps, w - eps))  # warning: inplace clip
    y = np.copy(x)
    y[..., 0] = ((x[..., 0] + x[..., 2]) / 2) / w  # x center
    y[..., 1] = ((x[..., 1] + x[..., 3]) / 2) / h  # y center
    y[..., 2] = (x[..., 2] - x[..., 0]) / w  # width
    y[..., 3] = (x[..., 3] - x[..., 1]) / h  # height
    return y


def xyn2xy(x, w=640, h=640, padw=0, padh=0):
    """
    Convert normalized coordinates to pixel coordinates of shape (n,2)

    Args:
        x (np.ndarray): The input tensor of normalized bounding box coordinates
        w (int): The width of the image. Defaults to 640
        h (int): The height of the image. Defaults to 640
        padw (int): The width of the padding. Defaults to 0
        padh (int): The height of the padding. Defaults to 0
    Returns:
        y (np.ndarray): The x and y coordinates of the top left corner of the bounding box
    """
    y = np.copy(x)
    y[..., 0] = w * x[..., 0] + padw  # top left x
    y[..., 1] = h * x[..., 1] + padh  # top left y
    return y


def xywh2ltwh(x):
    """
    Convert the bounding box format from [x, y, w, h] to [x1, y1, w, h], where x1, y1 are the top-left coordinates.

    Args:
        x (np.ndarray): The input tensor with the bounding box coordinates in the xywh format
    Returns:
        y (np.ndarray): The bounding box coordinates in the xyltwh format
    """
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    return y


def xyxy2ltwh(x):
    """
    Convert nx4 bounding boxes from [x1, y1, x2, y2] to [x1, y1, w, h], where xy1=top-left, xy2=bottom-right

    Args:
      x (np.ndarray): The input tensor with the bounding boxes coordinates in the xyxy format
    Returns:
      y (np.ndarray): The bounding box coordinates in the xyltwh format.
    """
    y = np.copy(x)
    y[:, 2] = x[:, 2] - x[:, 0]  # width
    y[:, 3] = x[:, 3] - x[:, 1]  # height
    return y


def ltwh2xywh(x):
    """
    Convert nx4 boxes from [x1, y1, w, h] to [x, y, w, h] where xy1=top-left, xy=center

    Args:
      x (np.ndarray): the input tensor
    """
    y = np.copy(x)
    y[:, 0] = x[:, 0] + x[:, 2] / 2  # center x
    y[:, 1] = x[:, 1] + x[:, 3] / 2  # center y
    return y


def ltwh2xyxy(x):
    """
    It converts the bounding box from [x1, y1, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right

    Args:
      x (np.ndarray): the input image

    Returns:
      y (np.ndarray): the xyxy coordinates of the bounding boxes.
    """
    y = np.copy(x)
    y[:, 2] = x[:, 2] + x[:, 0]  # width
    y[:, 3] = x[:, 3] + x[:, 1]  # height
    return y


def cxywh2xyxy(x):
    """
    Converts bounding box coordinates from [cx, cy, w, h] to [x1, y1, x2, y2] format.

    Args:
        x (np.ndarray): Input bounding box coordinates in the format [cx, cy, w, h].

    Returns:
        y (np.ndarray): Converted bounding box coordinates in the format [x1, y1, x2, y2].
    """
    y = np.copy(x)
    y[:, 0] = x[:, 0] - 0.5 * x[:, 2]  # x1
    y[:, 1] = x[:, 1] - 0.5 * x[:, 3]  # y1
    y[:, 2] = x[:, 0] + 0.5 * x[:, 2]  # x2
    y[:, 3] = x[:, 1] + 0.5 * x[:, 3]  # y2
    return y


def xywhr2xyxyxyxy(center):
    """
    Convert batched Oriented Bounding Boxes (OBB) from [xywh, rotation] to [xy1, xy2, xy3, xy4]. Rotation values should
    be in degrees from 0 to 90.

    Args:
        center (numpy.ndarray): Input data in [cx, cy, w, h, rotation] format of shape (n, 5) or (b, n, 5).

    Returns:
        (numpy.ndarray): Converted corner points of shape (n, 4, 2) or (b, n, 4, 2).
    """
    cos, sin = (np.cos, np.sin)

    ctr = center[..., :2]
    w, h, angle = (center[..., i : i + 1] for i in range(2, 5))
    cos_value, sin_value = cos(angle), sin(angle)
    vec1 = [w / 2 * cos_value, w / 2 * sin_value]
    vec2 = [-h / 2 * sin_value, h / 2 * cos_value]
    vec1 = np.concatenate(vec1, axis=-1)
    vec2 = np.concatenate(vec2, axis=-1)
    pt1 = ctr + vec1 + vec2
    pt2 = ctr + vec1 - vec2
    pt3 = ctr - vec1 - vec2
    pt4 = ctr - vec1 + vec2
    return np.stack([pt1, pt2, pt3, pt4], axis=-2)

def xyxy2xyxyxyxy(x1, y1, x2, y2):
    # 定义矩形的四个顶点
    vertices = [
        (x1, y1),  # 左上角
        (x2, y1),  # 右上角
        (x2, y2),  # 右下角
        (x1, y2)   # 左下角
    ]
    return vertices


def rbox2poly(obboxes):
    """
    Trans rbox format to poly format.
    Args:
        rboxes (array/tensor): (num_gts, [cx cy l s θ]) θ∈[-pi/2, pi/2)

    Returns:
        polys (array/tensor): (num_gts, [x1 y1 x2 y2 x3 y3 x4 y4])
    """
    center, w, h, theta = np.split(obboxes, (2, 3, 4), axis=-1)
    Cos, Sin = np.cos(theta), np.sin(theta)
    vector1 = np.concatenate([w / 2 * Cos, -w / 2 * Sin], axis=-1)
    vector2 = np.concatenate([-h / 2 * Sin, -h / 2 * Cos], axis=-1)

    point1 = center + vector1 + vector2
    point2 = center + vector1 - vector2
    point3 = center - vector1 - vector2
    point4 = center - vector1 + vector2
    order = obboxes.shape[:-1]
    return np.concatenate([point1, point2, point3, point4], axis=-1).reshape(
        *order, 8
    )


def denormalize_bbox(bbox, input_shape, image_shape):
    """
    Denormalizes bounding box coordinates from input_shape to image_shape.

    Parameters:
    - bbox: Normalized bounding box coordinates [xmin, ymin, xmax, ymax]
    - input_shape: The shape of the input image used during normalization (e.g., [640, 640])
    - image_shape: The shape of the original image (e.g., [height, width])

    Returns:
    - Denormalized bounding box coordinates [xmin, ymin, xmax, ymax]
    """
    xmin, ymin, xmax, ymax = bbox

    # Denormalize x-coordinates
    denorm_xmin = int(xmin * image_shape[1] / input_shape[1])
    denorm_xmax = int(xmax * image_shape[1] / input_shape[1])

    # Denormalize y-coordinates
    denorm_ymin = int(ymin * image_shape[0] / input_shape[0])
    denorm_ymax = int(ymax * image_shape[0] / input_shape[0])

    denormalized_bbox = [denorm_xmin, denorm_ymin, denorm_xmax, denorm_ymax]

    return denormalized_bbox


def rescale_box(input_shape, boxes, image_shape, kpts=False):
    """Rescale the output to the original image shape"""
    ratio = min(
        input_shape[0] / image_shape[0],
        input_shape[1] / image_shape[1],
    )
    padding = (
        (input_shape[1] - image_shape[1] * ratio) / 2,
        (input_shape[0] - image_shape[0] * ratio) / 2,
    )
    boxes[:, [0, 2]] -= padding[0]
    boxes[:, [1, 3]] -= padding[1]
    boxes[:, :4] /= ratio
    boxes[:, 0] = np.clip(boxes[:, 0], 0, image_shape[1])  # x1
    boxes[:, 1] = np.clip(boxes[:, 1], 0, image_shape[0])  # y1
    boxes[:, 2] = np.clip(boxes[:, 2], 0, image_shape[1])  # x2
    boxes[:, 3] = np.clip(boxes[:, 3], 0, image_shape[0])  # y2
    if kpts:
        num_kpts = boxes.shape[1] // 3
        for i in range(2, num_kpts + 1):
            boxes[:, i * 3 - 1] = (boxes[:, i * 3 - 1] - padding[0]) / ratio
            boxes[:, i * 3] = (boxes[:, i * 3] - padding[1]) / ratio
    return boxes


def rescale_box_and_landmark(input_shape, boxes, lmdks, image_shape):
    ratio = min(
        input_shape[0] / image_shape[0],
        input_shape[1] / image_shape[1],
    )
    padding = (
        (input_shape[1] - image_shape[1] * ratio) / 2,
        (input_shape[0] - image_shape[0] * ratio) / 2,
    )
    boxes[:, [0, 2]] -= padding[0]
    boxes[:, [1, 3]] -= padding[1]
    boxes[:, :4] /= ratio
    boxes[:, 0] = np.clip(boxes[:, 0], 0, image_shape[1])  # x1
    boxes[:, 1] = np.clip(boxes[:, 1], 0, image_shape[0])  # y1
    boxes[:, 2] = np.clip(boxes[:, 2], 0, image_shape[1])  # x2
    boxes[:, 3] = np.clip(boxes[:, 3], 0, image_shape[0])  # y2
    # lmdks
    lmdks[:, [0, 2, 4, 6, 8]] -= padding[0]
    lmdks[:, [1, 3, 5, 7, 9]] -= padding[1]
    lmdks[:, :10] /= ratio
    lmdks[:, 0] = np.clip(lmdks[:, 0], 0, image_shape[1])
    lmdks[:, 1] = np.clip(lmdks[:, 1], 0, image_shape[0])
    lmdks[:, 2] = np.clip(lmdks[:, 2], 0, image_shape[1])
    lmdks[:, 3] = np.clip(lmdks[:, 3], 0, image_shape[0])
    lmdks[:, 4] = np.clip(lmdks[:, 4], 0, image_shape[1])
    lmdks[:, 5] = np.clip(lmdks[:, 5], 0, image_shape[0])
    lmdks[:, 6] = np.clip(lmdks[:, 6], 0, image_shape[1])
    lmdks[:, 7] = np.clip(lmdks[:, 7], 0, image_shape[0])
    lmdks[:, 8] = np.clip(lmdks[:, 8], 0, image_shape[1])
    lmdks[:, 9] = np.clip(lmdks[:, 9], 0, image_shape[0])

    return np.round(boxes), np.round(lmdks)


def rescale_tlwh(
    input_shape,
    boxes,
    image_shape,
    kpts=False,
    has_visible=True,
    multi_label=False,
):
    """Rescale the output to the original image shape"""
    ratio = min(
        input_shape[0] / image_shape[0],
        input_shape[1] / image_shape[1],
    )
    padding = (
        (input_shape[1] - image_shape[1] * ratio) / 2,
        (input_shape[0] - image_shape[0] * ratio) / 2,
    )
    boxes[:, 0] -= padding[0]
    boxes[:, 1] -= padding[1]
    boxes[:, :4] /= ratio
    boxes[:, 0] = np.clip(boxes[:, 0], 0, image_shape[1])  # x1
    boxes[:, 1] = np.clip(boxes[:, 1], 0, image_shape[0])  # y1
    boxes[:, 2] = np.clip((boxes[:, 0] + boxes[:, 2]), 0, image_shape[1])  # x2
    boxes[:, 3] = np.clip((boxes[:, 1] + boxes[:, 3]), 0, image_shape[0])  # y2
    if kpts:
        start_index = 6 if multi_label else 5
        num_kpts = boxes.shape[1] - start_index
        interval = 3 if has_visible else 2
        for i in range(0, num_kpts, interval):
            boxes[:, start_index + i] = (
                boxes[:, start_index + i] - padding[0]
            ) / ratio
            boxes[:, start_index + i + 1] = (
                boxes[:, start_index + i + 1] - padding[1]
            ) / ratio
            # skip visible flag
            if has_visible and (i + 1) % interval == 0:
                continue
    return boxes


def scale_boxes(
    img1_shape, boxes, img0_shape, ratio_pad=None, padding=True, xywh=False
):
    """
    Rescales bounding boxes (in the format of xyxy) from the shape of the image they were originally specified in
    (img1_shape) to the shape of a different image (img0_shape).

    Args:
      img1_shape (tuple): The shape of the image that the bounding boxes are for, in the format of (height, width).
      boxes (np.ndarray): the bounding boxes of the objects in the image, in the format of (x1, y1, x2, y2)
      img0_shape (tuple): the shape of the target image, in the format of (height, width).
      ratio_pad (tuple): a tuple of (ratio, pad) for scaling the boxes. If not provided, the ratio and pad will be
                         calculated based on the size difference between the two images.
      padding (bool): If True, assuming the boxes is based on image augmented by yolo style. If False then do regular
        rescaling.
        xywh (bool): The box format is xywh or not, default=False.

    Returns:
      boxes (np.ndarray): The scaled bounding boxes, in the format of (x1, y1, x2, y2)
    """
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(
            img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1]
        )  # gain  = old / new
        pad = round((img1_shape[1] - img0_shape[1] * gain) / 2 - 0.1), round(
            (img1_shape[0] - img0_shape[0] * gain) / 2 - 0.1
        )  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    if padding:
        boxes[..., [0]] -= pad[0]  # x padding
        boxes[..., [1]] -= pad[1]  # y padding
        if not xywh:
            boxes[..., 2] -= pad[0]  # x padding
            boxes[..., 3] -= pad[1]  # y padding
    boxes[..., :4] /= gain
    clip_boxes(boxes, img0_shape)
    return boxes


def scale_masks(masks, shape, padding=True):
    """
    Rescale segment masks to shape.

    Args:
        masks (np.ndarray): (C, H, W).
        shape (tuple): Height and width with input shape.
        padding (bool): If True, assuming the boxes are based on an image augmented by YOLO style.
                        If False, then do regular rescaling.
    """
    _, mh, mw = masks.shape
    gain = min(mh / shape[0], mw / shape[1])  # gain = old / new
    pad = [mw - shape[1] * gain, mh - shape[0] * gain]  # wh padding
    if padding:
        pad[0] /= 2
        pad[1] /= 2
    top, left = (int(pad[1]), int(pad[0])) if padding else (0, 0)  # y, x
    bottom, right = (int(mh - pad[1]), int(mw - pad[0]))
    masks = masks[:, top:bottom, left:right]
    # Resizing without loop
    masks = cv2.resize(
        masks.transpose((1, 2, 0)),
        (shape[1], shape[0]),
        interpolation=cv2.INTER_LINEAR,
    )
    masks = masks.transpose((2, 0, 1))
    return masks


def scale_coords(
    img1_shape,
    coords,
    img0_shape,
    ratio_pad=None,
    normalize=False,
    padding=True,
):
    """
    Rescale segment coordinates (xyxy) from img1_shape to img0_shape

    Args:
      img1_shape (tuple): The shape of the image that the coords are from.
      coords (np.ndarray): the coords to be scaled
      img0_shape (tuple): the shape of the image that the segmentation is being applied to
      ratio_pad (tuple): the ratio of the image size to the padded image size.
      normalize (bool): If True, the coordinates will be normalized to the range [0, 1]. Defaults to False
      padding (bool): If True, assuming the boxes is based on image augmented by yolo style. If False then do regular
        rescaling.

    Returns:
      coords (np.ndarray): the segmented image.
    """
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(
            img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1]
        )  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (
            img1_shape[0] - img0_shape[0] * gain
        ) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    if padding:
        coords[..., 0] -= pad[0]  # x padding
        coords[..., 1] -= pad[1]  # y padding
    coords[..., 0] /= gain
    coords[..., 1] /= gain
    clip_coords(coords, img0_shape)
    if normalize:
        coords[..., 0] /= img0_shape[1]  # width
        coords[..., 1] /= img0_shape[0]  # height
    return coords


def clip_coords(coords, shape):
    """
    Clip line coordinates to the image boundaries.

    Args:
        coords (numpy.ndarray): A list of line coordinates.
        shape (tuple): A tuple of integers representing the size of the image in the format (height, width).

    Returns:
        (None): The function modifies the input `coordinates` in place, by clipping each coordinate to the image boundaries.
    """
    coords[..., 0] = coords[..., 0].clip(0, shape[1])  # x
    coords[..., 1] = coords[..., 1].clip(0, shape[0])  # y


def clip_boxes(boxes, shape):
    """
    It takes a list of bounding boxes and a shape (height, width) and clips the bounding boxes to the
    shape

    Args:
      boxes (np.ndarray): the bounding boxes to clip
      shape (tuple): the shape of the image
    """
    boxes[..., [0, 2]] = boxes[..., [0, 2]].clip(0, shape[1])  # x1, x2
    boxes[..., [1, 3]] = boxes[..., [1, 3]].clip(0, shape[0])  # y1, y2


def masks2segments(masks, epsilon_factor=0.001):
    """
    It takes a list of masks(n,h,w) and returns a list of segments(n,xy)

    Args:
      masks (np.ndarray):
        the output of the model, which is a tensor of shape (batch_size, 160, 160)
      epsilon_factor (float, optional):
        Factor used for epsilon calculation in contour approximation.
        A smaller value results in smoother contours but with more points.
        If the value is set to 0, the default result will be used.

    Returns:
      segments (List): list of segment masks
    """
    segments = []
    for x in masks.astype("uint8"):
        c = cv2.findContours(x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        img_area = masks.shape[1] * masks.shape[2]
        c = refine_contours(c, img_area, epsilon_factor)
        if c:
            c = np.array([c[0] for c in c[0]])
            c = np.concatenate([c, [c[0]]])  # Close the contour
        else:
            c = np.zeros((0, 2))  # no segments found
        segments.append(c.astype("float32"))
    return segments


def tlwh_to_xyxy(x):
    """ " Convert tlwh to xyxy"""
    x1 = x[0]
    y1 = x[1]
    x2 = x[2] + x1
    y2 = x[3] + y1
    return [x1, y1, x2, y2]


def xyxy_to_tlwh(x):
    x1, y1, x2, y2 = x
    w = x2 - x1
    h = y2 - y1
    return [x1, y1, w, h]



def xyxyxyxy2rotation(corners):
    """
    从旋转矩形的四个顶点反推出旋转角度（0-360度）。
    
    Args:
        corners (numpy.ndarray): 旋转矩形的四个顶点，形状为 (4, 2) 或 (b, 4, 2)。
    
    Returns:
        numpy.ndarray: 旋转角度（0-360度），形状为 (b,) 如果输入包含批次维度，否则为标量。
    """
    # 假设输入形状为 (b, 4, 2)，其中 b 是批次大小，4 是顶点数，2 是坐标 (x, y)。
    # 如果输入没有批次维度，则添加它（形状变为 (1, 4, 2)）。
    if corners.ndim == 2:
        corners = corners[np.newaxis, :, :]
    
    # 选择从顶点 1 到顶点 2 的边来计算角度。
    vec = corners[:, 2, :] - corners[:, 1, :]  # 第二个顶点到第三个顶点的向量（但这里用1到2因为通常1-2是长边的一部分）
    # 注意：这里实际上用了1到2的边，因为对于0-90度的旋转，这通常是长边的一部分。
    # 但是，为了通用性，应该检查哪个边更长，并使用那条边。
    # 不过，由于函数限制在0-90度，我们可以假设1-2边总是长的。
    
    # 计算与x轴的夹角（弧度）。
    angle_rad = np.arctan2(vec[:, 1], vec[:, 0])
    
    # 将角度转换为0-360度（顺时针方向，从x轴正方向开始）。
    angle_deg = (np.degrees(angle_rad) + 360) % 360  # 确保角度在0-360度之间
    
    # 由于使用了1-2边，并且假设它是长边，所以不需要额外调整角度。
    # 但是，如果矩形的短边与旋转角度的方向一致（这在你的函数中不太可能），
    # 可能需要将角度加上90度或相应的值来得到正确的旋转角度。
    
    # 如果输入没有批次维度，则移除它。
    if corners.shape[0] == 1:
        angle_deg = angle_deg[0]
    
    return angle_deg


def calculate_rotation_theta(poly):
        """
        Calculate the rotation angle of the polygon.

        Args:
            poly (np.ndarray): A numpy array of shape (4, 2) representing the polygon.

        Returns:
            (float): The rotation angle of the polygon in radians.
        """
        x1, y1 = poly[0]
        x2, y2 = poly[1]

        # Calculate one of the diagonal vectors (after rotation)
        diagonal_vector_x = x2 - x1
        diagonal_vector_y = y2 - y1

        # Calculate the rotation angle in radians
        rotation_angle = math.atan2(diagonal_vector_y, diagonal_vector_x)

        # Convert radians to degrees
        rotation_angle_degrees = math.degrees(rotation_angle)

        if rotation_angle_degrees < 0:
            rotation_angle_degrees += 360

        return rotation_angle_degrees / 360 * (2 * math.pi)




def box_area(boxes):
    return (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])


def box_iou(box1, box2):
    area1 = box_area(box1)  # N
    area2 = box_area(box2)  # M
    # broadcasting
    lt = np.maximum(box1[:, np.newaxis, :2], box2[:, :2])
    rb = np.minimum(box1[:, np.newaxis, 2:], box2[:, 2:])
    wh = rb - lt
    wh = np.maximum(0, wh)  # [N, M, 2]
    inter = wh[:, :, 0] * wh[:, :, 1]
    iou = inter / (area1[:, np.newaxis] + area2 - inter)
    return iou  # NxM


def numpy_nms(boxes, scores, iou_threshold):
    idxs = scores.argsort()
    keep = []
    while idxs.size > 0:
        max_score_index = idxs[-1]
        max_score_box = boxes[max_score_index][None, :]
        keep.append(max_score_index)
        if idxs.size == 1:
            break
        idxs = idxs[:-1]
        other_boxes = boxes[idxs]
        ious = box_iou(max_score_box, other_boxes)
        idxs = idxs[ious[0] <= iou_threshold]
    keep = np.array(keep)
    return keep


def numpy_nms_rotated(boxes, scores, iou_threshold):
    if len(boxes) == 0:
        return np.empty((0,), dtype=np.int8)

    sorted_idx = np.argsort(scores)[::-1]
    boxes = boxes[sorted_idx]
    ious = batch_probiou(boxes, boxes)
    ious = np.triu(ious, k=1)
    pick = np.nonzero(np.max(ious, axis=0) < iou_threshold)[0]
    return sorted_idx[pick]


def batch_probiou(obb1, obb2, eps=1e-7):
    x1, y1 = np.split(obb1[..., :2], 2, axis=-1)
    x2, y2 = (x.squeeze(-1)[None] for x in np.split(obb2[..., :2], 2, axis=-1))
    a1, b1, c1 = _get_covariance_matrix(obb1)
    a2, b2, c2 = (x.squeeze(-1)[None] for x in _get_covariance_matrix(obb2))
    t1 = (
        (
            (a1 + a2) * (np.power(y1 - y2, 2))
            + (b1 + b2) * (np.power(x1 - x2, 2))
        )
        / ((a1 + a2) * (b1 + b2) - (np.power(c1 + c2, 2)) + eps)
    ) * 0.25
    t2 = (
        ((c1 + c2) * (x2 - x1) * (y1 - y2))
        / ((a1 + a2) * (b1 + b2) - (np.power(c1 + c2, 2)) + eps)
    ) * 0.5

    t3 = (
        np.log(
            ((a1 + a2) * (b1 + b2) - (np.power(c1 + c2, 2)))
            / (
                4
                * np.sqrt(
                    (a1 * b1 - np.power(c1, 2)).clip(0)
                    * (a2 * b2 - np.power(c2, 2)).clip(0)
                )
                + eps
            )
            + eps
        )
        * 0.5
    )
    bd = t1 + t2 + t3
    bd = np.clip(bd, eps, 100.0)
    hd = np.sqrt(1.0 - np.exp(-bd) + eps)
    return 1 - hd


def _get_covariance_matrix(boxes):
    gbbs = np.concatenate(
        (np.power(boxes[:, 2:4], 2) / 12, boxes[:, 4:]), axis=-1
    )
    a, b, c = np.split(gbbs, [1, 2], axis=-1)
    return (
        a * np.cos(c) ** 2 + b * np.sin(c) ** 2,
        a * np.sin(c) ** 2 + b * np.cos(c) ** 2,
        a * np.cos(c) * np.sin(c) - b * np.sin(c) * np.cos(c),
    )





def letterbox(
    im:np.ndarray,
    new_shape,
    color=(114, 114, 114),
    auto=False,
    scaleFill=False,
    scaleup=True,
    stride=32,
):
    """
    Resize and pad image while meeting stride-multiple constraints
    Returns:
        im (array): (height, width, 3)
        ratio (array): [w_ratio, h_ratio]
        (dw, dh) (array): [w_padding h_padding]
    """
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):  # [h_rect, w_rect]
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # wh ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))  # w h
    dw, dh = (
        new_shape[1] - new_unpad[0],
        new_shape[0] - new_unpad[1],
    )  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])  # [w h]
        ratio = (
            new_shape[1] / shape[1],
            new_shape[0] / shape[0],
        )  # [w_ratio, h_ratio]

    dw /= 2  # divide padding into 2 sides
    dh /= 2
    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(
        im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
    )
    return im, ratio, (dw, dh)








def non_max_suppression_v8(
    prediction,
    task="detect",
    conf_thres=0.25,
    iou_thres=0.45,
    classes=None,
    agnostic=False,
    multi_label=False,
    labels=(),
    max_det=300,
    nc=0,  # number of classes (optional)
    max_nms=30000,
    max_wh=7680,
):
    assert (
        0 <= conf_thres <= 1
    ), f"Invalid Confidence threshold {conf_thres}, \
        valid values are between 0.0 and 1.0"
    assert (
        0 <= iou_thres <= 1
    ), f"Invalid IoU {iou_thres}, \
        valid values are between 0.0 and 1.0"
    if task == "seg" and nc == 0:
        raise ValueError("The value of nc must be set when the mode is 'seg'.")
    if isinstance(prediction, (list, tuple)):
        prediction = prediction[0]  # select only inference output
    bs = prediction.shape[0]  # batch size
    if task in ["detect", "track"]:
        nc = prediction.shape[1] - 4  # number of classes
    nm = prediction.shape[1] - nc - 4
    mi = 4 + nc  # mask start index
    xc = np.amax(prediction[:, 4:mi], axis=1) > conf_thres  # candidates

    multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)

    # shape(1,84,6300) to shape(1,6300,84)
    prediction = np.transpose(prediction, (0, 2, 1))
    if task != "obb":
        prediction[..., :4] = xywh2xyxy(prediction[..., :4])  # xywh to xyxy
    output = [np.zeros((0, 6 + nm))] * bs

    for xi, x in enumerate(prediction):  # image index, image inference
        # Apply constraints
        # x[((x[:, 2:4] < min_wh) |
        # (x[:, 2:4] > max_wh)).any(1), 4] = 0  # width-height
        x = x[xc[xi]]  # confidence

        if labels and len(labels[xi]) and task != "obb":
            lb = labels[xi]
            v = np.zeros((len(lb), nc + nm + 5))
            v[:, :4] = lb[:, 1:5]  # box
            v[np.arange(len(lb)), lb[:, 0].astype(int) + 4] = 1.0  # cls
            x = np.concatenate((x[xc], v), axis=0)

        if not x.shape[0]:
            continue

        box = x[:, :4]
        cls = x[:, 4 : 4 + nc]
        mask = x[:, 4 + nc : 4 + nc + nm]

        if multi_label:
            i, j = np.where(cls > conf_thres)
            x = np.concatenate(
                (box[i], x[i, 4 + j, None], j[:, None].astype(float), mask[i]),
                axis=1,
            )
        else:  # best class only
            conf = np.max(cls, axis=1, keepdims=True)
            j = np.argmax(cls, axis=1, keepdims=True)
            x = np.concatenate((box, conf, j.astype(float), mask), axis=1)[
                conf.flatten() > conf_thres
            ]
        if classes is not None:
            x = x[(x[:, 5:6] == np.array(classes)).any(1)]

        n = x.shape[0]
        if not n:
            continue
        if n > max_nms:
            x = x[np.argsort(x[:, 4])[::-1][:max_nms]]

        c = x[:, 5:6] * (0 if agnostic else max_wh)
        scores = x[:, 4]
        if task == "obb":
            boxes = np.concatenate(
                (x[:, :2] + c, x[:, 2:4], x[:, -1:]), axis=-1
            )  # xywhr
            i = numpy_nms_rotated(boxes, scores, iou_thres)
        else:
            boxes = x[:, :4] + c
            i = numpy_nms(boxes, scores, iou_thres)
        i = i[:max_det]
       

        output[xi] = x[i]

    return output







def process_mask( protos, masks_in, bboxes, shape, upsample=False):
        """
        Apply masks to bounding boxes using the output of the mask head.

        Args:
            protos (np.ndarray): A tensor of shape [mask_dim, mask_h, mask_w].
            masks_in (np.ndarray): A tensor of shape [n, mask_dim], where n is the number of masks after NMS.
            bboxes (np.ndarray): A tensor of shape [n, 4], where n is the number of masks after NMS.
            shape (tuple): A tuple of integers representing the size of the input image in the format (h, w).
            upsample (bool): A flag to indicate whether to upsample the mask to the original image size. Default is False.

        Returns:
            (np.ndarray): A binary mask tensor of shape [n, h, w],
            where n is the number of masks after NMS, and h and w
            are the height and width of the input image.
            The mask is applied to the bounding boxes.
        """
        c, mh, mw = protos.shape
        ih, iw = shape
        masks = 1 / (
            1
            + np.exp(
                -np.dot(masks_in, protos.reshape(c, -1).astype(float)).astype(
                    float
                )
            )
        )
        masks = masks.reshape(-1, mh, mw)

        downsampled_bboxes = bboxes.copy()
        downsampled_bboxes[:, 0] *= mw / iw
        downsampled_bboxes[:, 2] *= mw / iw
        downsampled_bboxes[:, 3] *= mh / ih
        downsampled_bboxes[:, 1] *= mh / ih
        masks = crop_mask_np(masks, downsampled_bboxes)  # CHW
        if upsample:
            if masks.shape[0] == 1:
                masks_np = np.squeeze(masks, axis=0)
                masks_resized = cv2.resize(
                    masks_np,
                    (shape[1], shape[0]),
                    interpolation=cv2.INTER_LINEAR,
                )
                masks = np.expand_dims(masks_resized, axis=0)
            else:
                masks_np = np.transpose(masks, (1, 2, 0))
                masks_resized = cv2.resize(
                    masks_np,
                    (shape[1], shape[0]),
                    interpolation=cv2.INTER_LINEAR,
                )
                masks = np.transpose(masks_resized, (2, 0, 1))
        masks[masks > 0.5] = 1
        masks[masks <= 0.5] = 0

        return masks


def crop_mask_np(masks, boxes):
        """
        It takes a mask and a bounding box, and returns a mask that is cropped to the bounding box.

        Args:
            masks (np.ndarray): [n, h, w] array of masks.
            boxes (np.ndarray): [n, 4] array of bbox coordinates in relative point form.

        Returns:
            (np.ndarray): The masks are being cropped to the bounding box.
        """
        n, h, w = masks.shape
        x1, y1, x2, y2 = np.hsplit(boxes[:, :, None], 4)
        r = np.arange(w, dtype=x1.dtype)[None, None, :]  # rows shape(1,1,w)
        c = np.arange(h, dtype=x1.dtype)[None, :, None]  # cols shape(1,h,1)

        return masks * ((r >= x1) & (r < x2) & (c >= y1) & (c < y2))



