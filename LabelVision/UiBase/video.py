import os
import os.path as osp
import cv2
import shutil

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


def get_output_directory(source_video_path):
    video_dir = os.path.dirname(source_video_path)
    folder_name = os.path.splitext(os.path.basename(source_video_path))[0]
    output_dir = os.path.join(video_dir, folder_name)
    return output_dir


def ask_overwrite_directory(parent, output_dir):
    if not os.path.exists(output_dir):
        return True
    reply = QMessageBox.question( parent,"目录存在",f"目录 '{os.path.basename(output_dir)}' 已经存在. 您想覆盖它吗?", QMessageBox.Yes | QMessageBox.No,)
    if reply == QMessageBox.No:
        return False
    else:
        shutil.rmtree(output_dir)
    return True


def get_frame_interval(parent, fps, total_frames):
    interval, ok = QInputDialog.getInt(
        parent,
        "帧间隔",
        f"输入帧间隔 (FPS: {fps}):",
        1,  # 默认值
        1,  # 最小值
        total_frames,  # 最大值
        1,  # 步数
    )
    if not ok:
        QMessageBox.warning(parent, "取消", "帧提取已取消.")
    return interval if ok else None


def extract_frames_from_video(parent, source_video_path):
    output_dir:str = get_output_directory(source_video_path)

    if not ask_overwrite_directory(parent, output_dir):
        return None

    video_capture = cv2.VideoCapture(source_video_path)
    if not video_capture.isOpened():
        QMessageBox.critical(parent, "错误", "打开视频文件失败.")
        return None

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    interval = get_frame_interval(parent, fps, total_frames)
    if interval is None:
        return None

    os.makedirs(output_dir)

    progress_dialog = QProgressDialog(
        "提取帧。请稍候...",
        "取消",
        0,
        total_frames // interval,
        parent,
    )
    progress_dialog.setWindowModality(Qt.WindowModal)
    progress_dialog.setWindowTitle("进度")
    progress_dialog.setStyleSheet(
        """
        QProgressDialog QProgressBar {
            border: 1px solid grey;
            border-radius: 5px;
            text-align: center;
        }
        QProgressDialog QProgressBar::chunk {
            background-color: orange;
        }
        """
    )
    output_dir=output_dir.replace("\\", "/")
    frame_count = 0
    saved_frame_count = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if frame_count % interval == 0:
            frame_filename = os.path.join(output_dir, f"{saved_frame_count:05}.jpg")
            # cv2.imwrite(frame_filename, frame)
            from PIL import Image
            import numpy as np
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image.save(frame_filename)
            saved_frame_count += 1
            progress_dialog.setValue(saved_frame_count)
            if progress_dialog.wasCanceled():
                break

        frame_count += 1
    print("提取结束")
    video_capture.release()
    progress_dialog.close()

    return output_dir
