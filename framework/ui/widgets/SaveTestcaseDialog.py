# -*- coding: UTF-8 -*-

"""
File Name:      SaveTestcaseDialog
Author:         zhangwei04
Create Date:    2018/11/5
"""

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QMouseEvent

from framework.ui.signal.Signal import g_signal


class SaveTestcaseDialog:
    def __init__(self, testcase_list):
        self.testcase_list = testcase_list
        self.dialog = QDialog()
        self.dialog.setWindowTitle("保存用例对话框")
        self.layout = QVBoxLayout()
        self.dialog.setLayout(self.layout)

        self.testcase_table = QTableWidget()
        self.testcase_file_name_widget = QLineEdit()

        self._init_testcase_list_layout()
        self.__init_testcae_name_layout()
        self._init_ensure_layout()

    def _init_testcase_list_layout(self):
        """初始化用例名、填入用例名的布局"""
        testcase_layout = QHBoxLayout()
        self.layout.addLayout(testcase_layout)
        self._update_testcase_table()
        testcase_layout.addWidget(self.testcase_table)

    def _update_testcase_table(self):
        """
        更新测试用例表格Widget
        """
        self.testcase_table.setRowCount(len(self.testcase_list))
        self.testcase_table.setColumnCount(1)
        for row, testcase_name in enumerate(self.testcase_list):
            item = QTableWidgetItem()
            item.setText(testcase_name)
            self.testcase_table.setItem(row, 0, item)

    def __init_testcae_name_layout(self):
        testcase_layout = QHBoxLayout()
        self.layout.addLayout(testcase_layout)
        testcase_layout.addWidget(QLabel("测试用例名"))
        testcase_layout.addWidget(self.testcase_file_name_widget)

    def _init_ensure_layout(self):
        """初始化确认窗口布局"""
        save_layout = QHBoxLayout()
        self.layout.addLayout(save_layout)
        ensure_button = QPushButton("保存")
        ensure_button.clicked.connect(self.save)
        ensure_button.clicked.connect(self.dialog.close)
        save_layout.addWidget(ensure_button)

    def save(self):
        """点击确认后，调用此函数发送确认添加信号"""
        from framework.core.resource import g_resource
        testcase_name = self.testcase_file_name_widget.text()

        testcase_path = os.path.join(g_resource['project_path'], 'project', testcase_name if testcase_name.endswith(".xml") else "{}.xml".format(testcase_name))

        # 写测试用例文件
        from xml.dom.minidom import Document
        doc = Document()
        root = doc.createElement("project")
        root.setAttribute("sort", 'normal')
        root.setAttribute("loop", "1")
        doc.appendChild(root)

        for testcase in self.testcase_list:
            ele = doc.createElement("testcase")
            testcase = str(testcase).rstrip('\\/')
            testcase = testcase.rsplit('.', 1)[0] if testcase.endswith(".py") else testcase
            ele.appendChild(doc.createTextNode(testcase))
            root.appendChild(ele)

        with open(testcase_path, 'w', encoding='utf-8') as fp:
            doc.writexml(fp, indent='\t', newl='\n', addindent='\t', encoding='utf-8')

    def exec_(self):
        """调用对话框方法，用于对话框显示"""
        self.dialog.exec_()
