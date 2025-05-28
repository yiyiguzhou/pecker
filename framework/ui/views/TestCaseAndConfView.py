# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseAndConfLayout
Author:         zhangwei04
Create Date:    2018/10/12
"""

from framework.ui.layout.TestCaseAndConfLayout import TestCaseAndConfLayout
from framework.ui.views.TestCaseView import TestCaseView
from framework.ui.views.ConfigView import ConfigView


class TestCaseAndConfView:
    def __init__(self, parent_layout):
        super().__init__()
        self.parent_layout = parent_layout
        self.layout = TestCaseAndConfLayout()
        self.parent_layout.addLayout(self.layout)
        self.testcase_view = TestCaseView(self.layout)
        self.conf_view = ConfigView(self.layout)

    def init_UI(self):
        self.testcase_view.init_UI()
        self.conf_view.init_UI()