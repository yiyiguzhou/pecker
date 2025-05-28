# -*- coding: UTF-8 -*-

"""
File Name:      DialogWarnningWidget
Author:         zhangwei04
Create Date:    2018/10/25
"""
from PyQt5.QtWidgets import *


class DialogWarnningWidget():
    """警告提示对话框"""
    def __init__(self, comment):
        super().__init__()
        if isinstance(comment, list):
            comment = "\n".join(comment)
        self.comment = comment

