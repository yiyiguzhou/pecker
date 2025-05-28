# -*- coding: UTF-8 -*-

"""
File Name:      RunStatusLayout
Author:         zhangwei04
Create Date:    2018/10/11
"""

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout


class RunStatusLayout(QVBoxLayout):
    """执行状态列布局，包含用例执行队列模块、进度条、以及启动运行等按钮"""
    def __init__(self):
        super().__init__()
        self.run_testcase_layout = QVBoxLayout()
        self.testcase_status_bar_layout = QVBoxLayout()
        self.start_and_save_layout = QHBoxLayout()

        self.addLayout(self.run_testcase_layout)
        self.addLayout(self.testcase_status_bar_layout)
        self.addLayout(self.start_and_save_layout)

