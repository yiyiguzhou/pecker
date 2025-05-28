# -*- coding: UTF-8 -*-

"""
File Name:      ConsoleWidget
Author:         zhangwei04
Create Date:    2018/10/23
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMouseEvent, QTextCursor
from PyQt5 import QtCore


class ConsoleWidget(QTextEdit):
    """控制台组件"""
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

