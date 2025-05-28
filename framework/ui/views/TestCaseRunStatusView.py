# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseRunStatus
Author:         zhangwei04
Create Date:    2018/10/16
"""

from framework.ui.layout.RunStatusLayout import RunStatusLayout
from framework.ui.views.TestCaseRunningView import TestCaseRunningView
from framework.ui.views.TestCaseStatusBarView import TestCaseStatusBarView
from framework.ui.views.TestCaseRunButtonsView import TestCaseRunButtonsView


class TestCaseRunStatusView:
    """用例执行状态总布局，包含用例执行队列，用例进度条，执行按钮布局等"""
    def __init__(self, parent_layout):
        self.parent_layout = parent_layout
        self.layout = RunStatusLayout()
        self.parent_layout.addLayout(self.layout)

        self.testcase_running_view = TestCaseRunningView(self.layout)
        self.testcase_status_bar_view = TestCaseStatusBarView(self.layout)
        self.testcase_run_buttons_biew = TestCaseRunButtonsView(self.layout)

    def init_UI(self):
        self.testcase_running_view.init_UI()
        self.testcase_status_bar_view.init_UI()
        self.testcase_run_buttons_biew.init_UI()