# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseRunStatus
Author:         zhangwei04
Create Date:    2018/10/16
"""
from PyQt5.QtWidgets import *
from framework.ui.layout.RunStatusLayout import RunStatusLayout
from framework.ui.views.TestCaseView import TestCaseView
from framework.ui.widgets.TestCaseStatusBarWidget import TestCaseStatusBarWidget


class TestCaseStatusBarView:
    def __init__(self, parent_layout):
        self.parent_layout = parent_layout
        self.layout = self.parent_layout.testcase_status_bar_layout

        self.label_widget = QLabel("用例队列执行进度")
        self.widget = TestCaseStatusBarWidget()

    def init_UI(self):
        self.layout.addWidget(self.label_widget)
        self.layout.addWidget(self.widget)


