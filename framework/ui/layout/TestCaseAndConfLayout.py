# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseAndConfLayout
Author:         zhangwei04
Create Date:    2018/10/11
"""

from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot


class TestCaseAndConfLayout(QVBoxLayout):
    """测试用例及配置列"""
    def __init__(self):
        super().__init__()
        self.testcase_layout = QVBoxLayout()
        self.conf_layout = QVBoxLayout()
        self.tree = QTreeWidget()
        self.testcase_layout.setObjectName("testcase")
        self.addChildLayout(self.testcase_layout)
        self.addChildLayout(self.conf_layout)