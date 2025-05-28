# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseStatusBarWidget
Author:         zhangwei04
Create Date:    2018/10/16
"""
from PyQt5.QtWidgets import *
from framework.ui.signal.Signal import g_signal


class TestCaseStatusBarWidget(QProgressBar):
    """用例状态栏-用例执行百分比状态栏组件"""
    def __init__(self):
        super().__init__()
        self.setToolTip("执行状态")
        g_signal.update_testcase_status_bar[int].connect(self._update_vlaue)

    def _update_vlaue(self, value:int):
        """更新进度条"""
        self.setValue(value)
