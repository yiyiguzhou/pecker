# -*- coding: UTF-8 -*-

"""
File Name:      AddTestCaseDialog
Author:         zhangwei04
Create Date:    2018/10/23
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QMouseEvent

from framework.ui.signal.Signal import g_signal


class AddTestCaseDialog:
    """添加用例对话窗口，用例树模块用例右键菜单栏点击添加时，弹出此对话框"""
    def __init__(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("用例添加")
        self.layout = QVBoxLayout()
        self.dialog.setLayout(self.layout)
        self._init_testcase_layout()
        self._init_ensure_layout()

    def _init_testcase_layout(self):
        """初始化用例名、填入用例名的布局"""
        testcase_layout = QHBoxLayout()
        self.layout.addLayout(testcase_layout)
        testcase_layout.addWidget(QLabel("用例名"))
        self.testcase_name_edit = QLineEdit()
        testcase_layout.addWidget(self.testcase_name_edit)

    def _init_ensure_layout(self):
        """初始化确认窗口布局"""
        ensure_layout = QHBoxLayout()
        self.layout.addLayout(ensure_layout)
        ensure_button = QPushButton("确定")
        ensure_button.clicked.connect(self.send_testcae_name)
        ensure_button.clicked.connect(self.dialog.close)
        ensure_layout.addWidget(ensure_button)

    def send_testcae_name(self):
        """点击确认后，调用此函数发送确认添加信号"""
        testcase_name = self.testcase_name_edit.text()
        g_signal.add_testcase.emit(testcase_name)
        g_signal.testcase_tree_reload.emit()

    def exec_(self):
        """调用对话框方法，用于对话框显示"""
        self.dialog.exec_()
