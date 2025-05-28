# -*- coding: UTF-8 -*-

"""
File Name:      SaveTestCaseWidget
Author:         zhangwei04
Create Date:    2018/10/16
"""
from PyQt5.QtWidgets import *
from framework.ui.signal.Signal import g_signal
from framework.ui.widgets.SaveTestcaseDialog import SaveTestcaseDialog


class SaveTestCaseWidget(QPushButton):
    """用例状态栏-按钮组组件-保存用例组件"""
    def __init__(self):
        super().__init__()
        self.setText("保存用例")
        g_signal.send_testcase_from_running.connect(self._save_testcase_xml)

    def _save_testcase_xml(self, testcase_list):
        save_dialog = SaveTestcaseDialog(testcase_list)
        save_dialog.exec_()
