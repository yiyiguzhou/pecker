# -*- coding: UTF-8 -*-

"""
File Name:      StartButtonsWidget
Author:         zhangwei04
Create Date:    2018/10/16
"""
from PyQt5.QtWidgets import *


class StartButtonWidget(QPushButton):
    """用例状态栏-按钮组组件-开始执行按钮组件"""
    def __init__(self):
        super().__init__()
        self.setText("开始")