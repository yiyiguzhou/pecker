# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseView
Author:         zhangwei04
Create Date:    2018/10/11
"""
import os
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMouseEvent

from framework.ui.widgets.ConfigWidget import ConfigWidget
from framework.ui.widgets.ProjectConfigWidget import ProjectConfigWidget
from framework.ui.widgets.OthersConfigWidget import OthersConfigWidget
from framework.core.resource import g_resource


class ConfigView():
    def __init__(self, parent_laoyout):
        super().__init__()
        self.parent_laoyout = parent_laoyout
        self.layout = QVBoxLayout()
        self.parent_laoyout.addLayout(self.layout)
        self.conf_widget = OthersConfigWidget(os.path.join(g_resource['project_path'], 'conf'), "配置文件")
        # self.conf_widget.setObjectName()
        # self.conf_moust_event = QMouseEvent.MouseButtonPress()
        self.project_widget = ProjectConfigWidget(os.path.join(g_resource['project_path'], 'project'), "工程配置文件")

    def init_UI(self):
        self.layout.addWidget(self.project_widget)
        self.layout.addWidget(self.conf_widget)

    def _add_conf(self):
        for i in range(10):
            item = QListWidgetItem()
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setText("conf_{}".format(i))

            self.conf_widget.addItem(item)

    def _add_xml(self):
        for i in range(10):
            item = QListWidgetItem()
            item.setText("xml_{}".format(i))
            self.xml_widget.addItem(item)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

    def double_clicked(self):
        print("doublet click")

