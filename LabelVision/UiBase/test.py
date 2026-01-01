from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import sys


import numpy as np
import yaml
from pathlib import Path
import re




def yaml_load(file="data.yaml", append_filename=False):
        """
        Load YAML data from a file.

        Args:
            file (str, optional): File name. Default is 'data.yaml'.
            append_filename (bool): Add the YAML filename to the YAML dictionary. Default is False.

        Returns:
            (dict): YAML data and file name.
        """
        assert Path(file).suffix in {".yaml", ".yml"}, f"Attempting to load non-YAML file {file} with yaml_load()"
        with open(file, errors="ignore", encoding="utf-8") as f:
            s = f.read()  # string

            # Remove special characters
            if not s.isprintable():
                s = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+", "", s)

            # Add YAML filename to dict and return
            data = yaml.safe_load(s) or {}  # always return a dict (yaml.safe_load() may return None for empty files)
            if append_filename:
                data["yaml_file"] = str(file)
            return data
def yaml_save(file="data.yaml", data=None, header=""):

        # if data is None:
        #     data = {}
        # file = Path(file)
        # if not file.parent.exists():
        #     # Create parent directories if they don't exist
        #     file.parent.mkdir(parents=True, exist_ok=True)

        # # Convert Path objects to strings
        # valid_types = int, float, str, bool, list, tuple, dict, type(None)
        # for k, v in data.items():
        #     if not isinstance(v, valid_types):
        #         data[k] = str(v)

        # Dump data to file in YAML format
        with open(file, "w", errors="ignore", encoding="utf-8") as f:
            if header:
                f.write(header)
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,default_flow_style=None)
data = yaml_load("D:\\Code\\Yolo\\ultralytics-code\\ultralytics\\cfg\\datasets\\coco8-pose.yaml")
print(data)

yaml_save("testpose.yaml",data)



