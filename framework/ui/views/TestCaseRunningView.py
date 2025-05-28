# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseRunStatus
Author:         zhangwei04
Create Date:    2018/10/16
"""

from framework.ui.layout.RunStatusLayout import RunStatusLayout
from framework.ui.views.TestCaseView import TestCaseView
from framework.ui.widgets.RunningTestCaseWidget import RunningTestCaseWidget


class TestCaseRunningView:
    def __init__(self, parent_layout):
        self.parent_layout = parent_layout
        self.layout = self.parent_layout.run_testcase_layout

    def init_UI(self):
        self.widget = RunningTestCaseWidget()
        # self.widget.add_select_testcase([i for i in range(10)])
        self.layout.addWidget(self.widget)


