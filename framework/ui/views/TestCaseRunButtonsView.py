# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseRunStatus
Author:         zhangwei04
Create Date:    2018/10/16
"""

from framework.ui.layout.RunStatusLayout import RunStatusLayout
from framework.ui.widgets.StartButtonWidget import StartButtonWidget
from framework.ui.widgets.SaveTestCaseWidget import SaveTestCaseWidget
from framework.ui.views.TestCaseRunningView import TestCaseRunningView
from framework.ui.signal.Signal import g_signal


class TestCaseRunButtonsView:
    def __init__(self, parent_layout):
        self.parent_layout = parent_layout
        self.layout = parent_layout.start_and_save_layout
        self.run_widget = StartButtonWidget()
        self.save_testcase = SaveTestCaseWidget()

    def init_UI(self):
        """初始化布局及组件"""
        self.layout.addWidget(self.run_widget)
        self.layout.addWidget(self.save_testcase)
        self.run_widget.clicked.connect(self.clicked_start_run)
        self.save_testcase.clicked.connect(self._save_testcase_to_xml)

    def clicked_start_run(self):
        """点击开始执行按钮"""
        g_signal.update_testcase_running_table.emit()  # 更新用例执行队列
        self.start_ipecker()

    def start_ipecker(self):
        """执行ipecker信号"""
        g_signal.start_ipecker.emit()

    def _save_testcase_to_xml(self):
        g_signal.get_testcase_from_running.emit()