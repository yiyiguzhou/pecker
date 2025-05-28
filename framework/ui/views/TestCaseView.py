# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseView
Author:         zhangwei04
Create Date:    2018/10/11
"""
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from framework.ui.widgets.TestCaseWidget import TestCaseWidget



class TestCaseView():
    def __init__(self, parent_layout):
        super().__init__()
        self.parent_layout = parent_layout
        self.layout = QVBoxLayout()
        self.parent_layout.addLayout(self.layout)
        self.tree = TestCaseWidget()

    def init_UI(self):

        button = QPushButton()
        button.setText("确定")
        button.clicked.connect(self.choose)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(button)
        # self.show()

    # @pyqtSlot()
    def choose(self):
        from PyQt5.QtWidgets import QWidget
        # a = QWidget()
        # a.text()

        try:
            iterator = QTreeWidgetItemIterator(self.tree)
            lastParent = 'root'
            while iterator.value():
                item = iterator.value()
                # QTreeWidgetItem().checkState()'
                print(item.text(0), item.checkState(0), self._get_path(item))
                iterator += 1
        except Exception as e:
            print(e)

        print(self.tree.children())

    def save(self, file_name):
        testcase_list = self.tree.get_selected_testcase()

    def _write_xml(self):
        pass

    def _get_path(self, item):
        path = ""
        while True:
            path = "{}/{}".format(item.text(0), path)
            item = item.parent()
            if item is None:
                break
        return path